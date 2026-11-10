import pandas as pd
import pytest

from tennisage._parse import (_extract_birthdate, _extract_matches,
                              _format_player_name, _is_male_file)
from tests.mock_data import FEMALE_JS, MALE_JS

@pytest.mark.parametrize("name", ["serena williams", "Serena Williams",
                                  "SerenaWilliams", "  serena   williams "])
def test_format_name_variants(name):
    assert _format_player_name(name) == "SerenaWilliams"


def test_format_name_rejects_empty():
    with pytest.raises(ValueError):
        _format_player_name("   ")


def test_extract_female_rows():
    rows = _extract_matches(FEMALE_JS)
    assert len(rows) == 3
    assert rows[0][11] == "Anne Miller"
    assert rows[0][16] == "19770119"


def test_extract_male_rows():
    rows = _extract_matches(MALE_JS)
    assert len(rows) == 3
    assert rows[1][11] == "Stefano Galvani"
    assert rows[1][16] == "24.2902121834"


def test_extract_rejects_text_without_array():
    with pytest.raises(ValueError):
        _extract_matches("var nothing = 0;")


def test_detects_female_file():
    assert not _is_male_file(_extract_matches(FEMALE_JS))


def test_detects_male_file():
    assert _is_male_file(_extract_matches(MALE_JS))


def test_female_row_with_stats_is_not_male():
    row = _extract_matches(FEMALE_JS)[0]
    long_row = row[:20] + ["10"] * 19 + [""] * 4 + [row[-1]]  # 44 fields
    assert not _is_male_file([long_row])

def test_extract_birthdate():
    page = "<script>\nvar dob = 19860603;\nfunction calculateAge(dobString) {"
    assert _extract_birthdate(page) == pd.Timestamp("1986-06-03")


def test_extract_birthdate_missing():
    with pytest.raises(ValueError):
        _extract_birthdate("<html>no birthday here</html>")