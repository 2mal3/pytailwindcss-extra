from os import environ, rename
from tempfile import gettempdir
from stat import S_IXUSR
from sys import argv, stdout, stdin
from platform import system, machine
from subprocess import run, CompletedProcess
from pathlib import Path
from json import loads, dumps
from time import time
from typing import Generator
from datetime import datetime, timedelta

from platformdirs import user_cache_dir
import niquests
from tqdm import tqdm

from pytailwindcss_extra.logger import log

GITHUB_REPO = "dobicinaitis/tailwind-cli-extra"
MAJOR_TAILWIND_CLI_EXTRA_VERSION = 2
MEGABYTE = 1024 * 1024
CACHE_EXPIRATION_HOURS = 24


def main() -> int:
    bin_dir_path = Path(user_cache_dir("pytailwindcss-extra")) / "bin"

    cache_file_path = Path(user_cache_dir("pytailwindcss-extra")) / "versions.json"
    version = get_version(environ.get("PYTAILWINDCSS_EXTRA_VERSION", "major"), cache_file_path)

    bin_path = bin_dir_path / f"tailwindcss-extra-{version.replace('.', '-')}"
    if not bin_path.exists():
        bin_dir_path.mkdir(parents=True, exist_ok=True)
        install(bin_path, version)
        # TODO: remove old versions

    log.debug(f"Running '{bin_path}' ...")
    result = run_file_with_arguments(bin_path, argv[1:])
    return result.returncode


def get_version(specifier: str, cache_file_path: Path) -> str:
    if specifier not in ["latest", "major"]:
        return specifier

    cached_version = get_cached_version(specifier, cache_file_path)
    if cached_version:
        return cached_version

    if specifier == "latest":
        version = get_latest_version_tag()
    elif specifier == "major":
        version = get_latest_major_version_tag(MAJOR_TAILWIND_CLI_EXTRA_VERSION)
    else:
        raise RuntimeError(f"Unknown version specifier: {specifier}")

    set_cached_version(specifier, version, cache_file_path)
    return version


def get_cached_version(key: str, cache_file_path: Path) -> str | None:
    if not cache_file_path.exists():
        return None

    with cache_file_path.open("r") as file:
        cache = loads(file.read())

    cache_for_key = cache.get(key)
    if not cache_for_key:
        return None

    if datetime.fromtimestamp(int(cache_for_key["time"])) + timedelta(hours=CACHE_EXPIRATION_HOURS) < datetime.now():
        return None

    return cache_for_key["version"]


def set_cached_version(key: str, version: str, cache_file_path: Path) -> None:
    if not cache_file_path.exists():
        cache_file_path.parent.mkdir(parents=True, exist_ok=True)
        with cache_file_path.open("w") as file:
            file.write("{}")

    with cache_file_path.open("r") as file:
        cache = loads(file.read())

    new_cache = {
        "version": version,
        "time": int(time()),
    }

    cache[key] = new_cache

    with cache_file_path.open("w") as file:
        file.write(dumps(cache))


# TODO: remove partially downloaded file on error
def install(bin_path: Path, version: str) -> None:
    download_url = get_download_url(version)

    log.info(f"Downloading 'tailwindcss-extra-{get_os_name()}-{get_arch_name()}' {version} ...")

    download_path = Path(gettempdir()) / f"tailwindcss-extra-{int(time())}"
    if in_non_interactive_mode():
        all(download_url_to_path(download_url, download_path))
    else:
        download_url_to_path_with_progress(download_url, download_path)

    make_file_executable(download_path)

    rename(download_path, bin_path)


def in_non_interactive_mode() -> bool:
    return not stdin.isatty() or not stdout.isatty()


def download_url_to_path_with_progress(download_url: str, dest_path: Path) -> None:
    progress_bar = tqdm(unit="B", unit_scale=True, unit_divisor=1024)

    for chunk, total_size in download_url_to_path(download_url, dest_path):
        progress_bar.total = total_size
        progress_bar.update(chunk)

    progress_bar.close()


def download_url_to_path(download_url: str, dest_path: Path) -> Generator[tuple[int, int], None, None]:
    with niquests.get(download_url, stream=True, timeout=60) as request:
        request.raise_for_status()
        with open(dest_path, "wb") as file:
            for chunk in request.iter_content(chunk_size=MEGABYTE):
                file.write(chunk)
                yield MEGABYTE, int(request.headers["Content-Length"])


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
    response = niquests.get(f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest", timeout=60)
    response.raise_for_status()
    return response.json()["tag_name"]


def get_latest_major_version_tag(major_version: int) -> str:
    log.info(f"Getting latest tailwind-cli-extra version for v{major_version} ...")

    response = niquests.get(
        f"https://api.github.com/repos/{GITHUB_REPO}/git/matching-refs/tags/v{major_version}", timeout=60
    )
    response.raise_for_status()
    if not response.text:
        raise RuntimeError("No releases found")
    releases = loads(response.text)

    release_tag = releases[-1]["ref"].split("/")[-1]
    return release_tag


def run_file_with_arguments(file_path: Path, arguments: list[str]) -> CompletedProcess[bytes]:
    return run([file_path] + arguments, check=False)


def make_file_executable(path: Path) -> None:
    path.chmod(path.stat().st_mode | S_IXUSR)


if __name__ == "__main__":
    main()
