from tennisage import _fetch, get_player_matches
from tests.mock_data import FEMALE_JS, MALE_JS


def fake_site(career_js, dob):
    """Return a stand-in for _download_text that serves mock content."""
    def fake_download(url):
        return career_js if url.endswith("Career.js") else f"var dob = {dob};"
    return fake_download


def test_female_player_end_to_end(monkeypatch):
    monkeypatch.setattr(_fetch, "_download_text", fake_site(FEMALE_JS, "19810926"))
    matches = get_player_matches("serena williams")
    assert len(matches) == 3
    assert {"player_age", "opp_age", "age_diff", "result"} <= set(matches.columns)


def test_male_player_end_to_end(monkeypatch):
    monkeypatch.setattr(_fetch, "_download_text", fake_site(MALE_JS, "19860603"))
    matches = get_player_matches("Rafael Nadal")
    assert matches["age_diff"].notna().all()