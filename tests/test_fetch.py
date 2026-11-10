import pytest

from tennisage import _fetch
from tennisage._fetch import _career_url, _load_career_rows, _player_page_url

def test_career_url():
    assert _career_url("RafaelNadal") == (
        "https://www.tennisabstract.com/jsmatches/RafaelNadalCareer.js")


def test_player_page_url_men_and_women():
    assert _player_page_url("RafaelNadal", True).endswith("player.cgi?p=RafaelNadal")
    assert _player_page_url("SerenaWilliams", False).endswith("wplayer.cgi?p=SerenaWilliams")

def test_unknown_player_gives_clear_error(monkeypatch):
    def fake_download(url):
        raise ValueError(f"Page not found: {url}")

    monkeypatch.setattr(_fetch, "_download_text", fake_download)
    with pytest.raises(ValueError, match="Could not find career matches for 'GastonSanchez'"):
        _load_career_rows("GastonSanchez")


def test_page_without_matches_gives_clear_error(monkeypatch):
    monkeypatch.setattr(_fetch, "_download_text", lambda url: "<html>Not here</html>")
    with pytest.raises(ValueError, match="Could not find career matches"):
        _load_career_rows("Gaston Sanchez")