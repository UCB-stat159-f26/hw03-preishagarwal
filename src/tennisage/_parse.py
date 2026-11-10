"""Private helpers for turning Tennis Abstract career JS files into rows."""

import json
from tennisage._parse import _extract_matches, _format_player_name
from tests.mock_data import FEMALE_JS, MALE_JS

OPP_AGE_FIELD = 16  # opponent birthdate (women's files) or age (men's files)


def _format_player_name(name):
    """Convert 'serena williams' or 'SerenaWilliams' to 'SerenaWilliams'."""
    tokens = name.strip().split()
    if not tokens:
        raise ValueError("Player name cannot be empty.")
    return "".join(tok[0].upper() + tok[1:] for tok in tokens)


def _extract_matches(js_text):
    """Return the match rows from career JS text as a list of lists."""
    if "[" not in js_text:
        raise ValueError("No match data found in the JS content.")
    array_text = js_text[js_text.index("["): js_text.rindex("]") + 1]
    return json.loads(array_text)


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