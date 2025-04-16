from pathlib import Path
from typing import Generator, Callable
from os import remove

import pytest

from pytailwindcss_extra.main import get_latest_major_version_tag, get_download_url, get_version


def test_get_latest_major_version_tag() -> None:
    assert get_latest_major_version_tag(1) == "v1.7.27"


def test_get_download_url() -> None:
    assert get_download_url("v1.7.27")


@pytest.fixture(scope="module")
def cleanup_cache() -> Generator:
    yield
    remove(Path("cache.json").absolute())


@pytest.mark.parametrize("specifier", ["latest", "major", "v1.7.27"])
def test_get_version(cleanup_cache: Callable, specifier: str) -> None:
    cache_file_path = Path("cache.json").absolute()

    assert get_version(specifier, cache_file_path).startswith("v")
