from os import environ
from stat import S_IXUSR
from sys import argv, exit
from platform import system, machine
from subprocess import run, CompletedProcess
from pathlib import Path
from json import loads

import niquests

from pytailwindcss_extra.logger import log

GITHUB_REPO = "dobicinaitis/tailwind-cli-extra"
MAJOR_TAILWIND_CLI_EXTRA_VERSION = 2


def main() -> None:
    temp_bin_dir_path = environ.get("PYTAILWINDCSS_EXTRA_BIN_DIR")
    if not temp_bin_dir_path:
        bin_dir_path: Path = Path(__file__).parent.resolve() / "bin"
    else:
        bin_dir_path = Path(temp_bin_dir_path)

    # TODO: cache the latest version so it doesn't need to send a request each run
    version = environ.get("PYTAILWINDCSS_EXTRA_VERSION")
    if version == "latest":
        version = get_latest_version_tag()
    elif not version:
        version = get_latest_major_version_tag(MAJOR_TAILWIND_CLI_EXTRA_VERSION)

    bin_path = bin_dir_path / f"tailwindcss-extra-{version.replace('.', '-')}"
    if not bin_path.exists():
        if not bin_dir_path.exists():
            bin_dir_path.mkdir(parents=True)
        install(bin_path, version)
        # TODO: remove old versions

    log.debug(f"Running '{bin_path}' ...")
    result = run_file_with_arguments(bin_path, argv[1:])
    exit(result.returncode)


# TODO: remove partially downloaded file on error
def install(bin_path: Path, version: str) -> None:
    download_url = get_download_url(version)

    log.info(f"Downloading 'tailwindcss-extra-{get_os_name()}-{get_arch_name()}' {version} ...")

    download_url_to_path(download_url, bin_path)

    make_file_executable(bin_path)


def download_url_to_path(download_url: str, dest_path: Path) -> None:
    with niquests.get(download_url, stream=True) as request:
        request.raise_for_status()
        with open(dest_path, "wb") as file:
            for chunk in request.iter_content(chunk_size=1024 * 1024):
                file.write(chunk)


def get_download_url(version: str) -> str:
    os_name = get_os_name()
    arch_name = get_arch_name()
    ending = {"linux": "", "macos": "", "windows": ".exe"}[os_name]
    download_url = (
        f"https://github.com/{GITHUB_REPO}/releases/download/{version}/tailwindcss-extra-{os_name}-{arch_name}{ending}"
    )

    return download_url


def get_arch_name() -> str:
    arch = machine().lower()
    if not arch:
        raise RuntimeError("Unknown system architecture")

    return {
        "x86_64": "x64",
        "amd64": "x64",
        "aarch64": "arm64",
        "arm64": "arm64",
        "armv8": "arm64",
        "armv7l": "armv7",
    }[arch]


def get_os_name() -> str:
    os = system().lower()
    if not os:
        raise RuntimeError("Unknown OS")
    return {"linux": "linux", "darwin": "macos", "win32": "windows", "windows": "windows"}[os]


def get_latest_version_tag() -> str:
    log.info("Getting latest tailwind-cli-extra version ...")
    response = niquests.get(f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest")
    response.raise_for_status()
    return response.json()["tag_name"]


def get_latest_major_version_tag(major_version: int) -> str:
    log.info(f"Getting latest tailwind-cli-extra version for v{major_version} ...")
    response = niquests.get(f"https://api.github.com/repos/{GITHUB_REPO}/releases")
    response.raise_for_status()
    if not response.text:
        raise RuntimeError("No releases found")
    releases = loads(response.text)
    matching_releases = [release for release in releases if release["tag_name"].startswith(f"v{major_version}.")]
    return matching_releases[0]["tag_name"]


def run_file_with_arguments(file_path: Path, arguments: list[str]) -> CompletedProcess[bytes]:
    return run([file_path] + arguments, check=False)


def make_file_executable(path: Path) -> None:
    path.chmod(path.stat().st_mode | S_IXUSR)


if __name__ == "__main__":
    main()
