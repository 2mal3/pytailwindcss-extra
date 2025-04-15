from pytailwindcss_extra.main import get_latest_major_version_tag


def test_get_latest_major_version_tag() -> None:
    assert get_latest_major_version_tag(1) == "v1.7.27"
