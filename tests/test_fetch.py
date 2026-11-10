import pytest

from tennisage import _fetch
from tennisage._fetch import _career_url, _player_page_url


def test_career_url():
    assert _career_url("RafaelNadal") == (
        "https://www.tennisabstract.com/jsmatches/RafaelNadalCareer.js")


def test_player_page_url_men_and_women():
    assert _player_page_url("RafaelNadal", True).endswith("player.cgi?p=RafaelNadal")
    assert _player_page_url("SerenaWilliams", False).endswith("wplayer.cgi?p=SerenaWilliams")