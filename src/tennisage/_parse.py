"""Private helpers for turning Tennis Abstract files into Python objects."""

import json
import re

import pandas as pd

OPP_AGE_FIELD = 16  # opponent birthdate (women's files) or age (men's files)
DOB_PATTERN = re.compile(r"var dob\s*=\s*(\d{8})")

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

def _is_male_file(rows):
    """Men's files store opponent age as a decimal; women's store a birthdate."""
    return any("." in row[OPP_AGE_FIELD] for row in rows)

def _extract_birthdate(page_html):
    """Return the player's birthdate from a Tennis Abstract player page."""
    found = DOB_PATTERN.search(page_html)
    if found is None:
        raise ValueError("No birthdate found on the player page.")
    return pd.to_datetime(found.group(1), format="%Y%m%d")