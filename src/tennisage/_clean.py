"""Private helpers for turning match rows into a data frame with ages."""

import pandas as pd

KEEP_FIELDS = {0: "date", 4: "result", 8: "round", 11: "opp_name", 16: "opp_age_raw"}
DAYS_PER_YEAR = 365.25


def _rows_to_frame(rows):
    """Keep the fields needed for graphing and give them names."""
    records = [{col: row[i] for i, col in KEEP_FIELDS.items()} for row in rows]
    matches = pd.DataFrame(records)
    matches["date"] = pd.to_datetime(matches["date"], format="%Y%m%d")
    return matches


def _years_between(start, end):
    """Return the number of years from start to end."""
    return (end - start).dt.days / DAYS_PER_YEAR


def _add_opponent_age(matches, is_male):
    """Add opp_age: given directly for men, computed from birthdate for women."""
    matches = matches.copy()
    raw = matches["opp_age_raw"]
    if is_male:
        matches["opp_age"] = pd.to_numeric(raw, errors="coerce")
    else:
        birthdate = pd.to_datetime(raw, format="%Y%m%d", errors="coerce")
        matches["opp_age"] = _years_between(birthdate, matches["date"])
    return matches.drop(columns="opp_age_raw")