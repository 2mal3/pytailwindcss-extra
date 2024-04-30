from os import environ
from stat import S_IXUSR
from sys import argv, exit
from platform import system, machine
from subprocess import run
from pathlib import Path

import niquests

from pytailwindcss_extra.logger import log

GITHUB_REPO = "dobicinaitis/tailwind-cli-extra"


def main() -> None:
    bin_dir_path = environ.get("PYTAILWINDCSS_EXTRA_BIN_DIR")
    if not bin_dir_path:
        bin_dir_path = Path(__file__).parent.resolve() / "bin"

    # TODO: cache the latest version so it doesn't need to send a request each run
    version = environ.get("PYTAILWINDCSS_EXTRA_VERSION", "latest")
    if version == "latest":
        log.info("Getting latest tailwind-cli-extra version ...")
        response = niquests.get(
            f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
        )
        response.raise_for_status()
        version = response.json()["tag_name"]

    bin_path = bin_dir_path / f"tailwindcss-extra-{version.replace('.', '-')}"
    if not bin_path.exists():
        if not bin_dir_path.exists():
            bin_dir_path.mkdir(parents=True)
        install(bin_path, version)
        # TODO: remove old versions

    log.debug(f"Running '{bin_path}' ...")
    result = run([bin_path] + argv[1:], check=False)
    exit(result.returncode)


# TODO: remove partially downloaded file on error
def install(bin_path: Path, version: str) -> None:
    os = system().lower()
    if not os:
        raise RuntimeError("Unknown OS")
    arch = machine().lower()
    if not arch:
        raise RuntimeError("Unknown system architecture")

    os_name = {"linux": "linux", "darwin": "macos", "win32": "windows", "windows": "windows"}[os]
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

    log.info(f"Downloading for 'tailwindcss-extra-{os_name}-{arch_name}' {version}...")

    with niquests.get(download_url, stream=True) as request:
        request.raise_for_status()
        with open(bin_path, "wb") as bin_file:
            for chunk in request.iter_content(chunk_size=1024 * 1024):
                bin_file.write(chunk)

    bin_path.chmod(bin_path.stat().st_mode | S_IXUSR)


if __name__ == "__main__":
    main()
