from os import environ, path, mkdir, chmod
from stat import S_IXUSR, S_IRUSR, S_IWUSR
from sys import argv, exit
from platform import system, machine
from subprocess import run
from pathlib import Path

from get_project_root import root_path
import niquests

from pytailwindcss_extra.logger import log

GITHUB_REPO = "dobicinaitis/tailwind-cli-extra"


def main() -> None:
    bin_dir = environ.get("PYTAILWINDCSS_EXTRA_BIN_DIR")
    if not bin_dir:
        project_root_path = root_path(ignore_cwd=True)
        bin_dir = Path(__file__).parent.resolve() / "bin"

    # TODO: cache the latest version so it doesn't need to send a request each run
    version = environ.get("PYTAILWINDCSS_EXTRA_VERSION", "latest")
    if version == "latest":
        log.info("Getting latest tailwind-cli-extra version ...")
        response = niquests.get(
            f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
        )
        response.raise_for_status()
        version = response.json()["tag_name"]

    bin_path = path.join(bin_dir, f"tailwindcss-extra-{version.replace('.', '-')}")
    if not path.exists(bin_path):
        log.info(f"Installing tailwindcss-extra {version} ...")
        if not path.exists(bin_dir):
            mkdir(bin_dir)
        install(bin_path, version)
        # TODO: remove old versions

    log.debug(f"Running {bin_path}...")
    result = run([bin_path] + argv[1:], check=False)
    exit(result.returncode)


# TODO: remove partially downloaded file on error
def install(bin_path: str, version: str) -> None:
    os = system().lower()
    if not os:
        raise RuntimeError("Unknown OS")
    arch = machine().lower()
    if not arch:
        raise RuntimeError("Unknown system architecture")

    os_name = {"linux": "linux", "darwin": "macos", "win32": "windows"}[os]
    arch_name = {
        "x86_64": "x64",
        "amd64": "x64",
        "aarch64": "arm64",
        "arm64": "arm64",
        "armv8": "arm64",
        "armv7l": "armv7",
    }[arch]
    ending = {"linux": "", "macos": "", "windows": ".exe"}[os_name]
    download_url = f"https://github.com/{GITHUB_REPO}/releases/download/{version}/tailwindcss-extra-{os_name}-{arch_name}{ending}"

    log.debug(f"Downloading for {os_name}-{arch_name} ...")

    with niquests.get(download_url, stream=True) as request:
        request.raise_for_status()
        with open(bin_path, "wb") as bin_file:
            for chunk in request.iter_content(chunk_size=1024 * 1024):
                bin_file.write(chunk)

    chmod(bin_path, S_IXUSR | S_IRUSR | S_IWUSR)


if __name__ == "__main__":
    main()
