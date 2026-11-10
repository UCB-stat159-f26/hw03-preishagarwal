"""Private helpers for turning match rows into a data frame with ages."""

import pandas as pd

KEEP_FIELDS = {0: "date", 4: "result", 8: "round", 11: "opp_name", 16: "opp_age_raw"}
DAYS_PER_YEAR = 365.25
ROUND_ORDER = ["Q1", "Q2", "Q3", "RR", "R128", "R64", "R32", "R16", "QF", "SF", "F"]


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

def _add_player_age(matches, birthdate):
    """Add the player's age and the age gap (player minus opponent)."""
    matches = matches.copy()
    matches["player_age"] = (matches["date"] - birthdate).dt.days / DAYS_PER_YEAR
    matches["age_diff"] = matches["player_age"] - matches["opp_age"]
    return matches


def _sort_matches(matches):
    """Sort by date, then by round, and drop matches with no known age gap."""
    round_rank = matches["round"].map({rnd: i for i, rnd in enumerate(ROUND_ORDER)})
    return (matches.assign(_rank=round_rank)
                   .sort_values(["date", "_rank"])
                   .drop(columns="_rank")
                   .dropna(subset=["age_diff"])
                   .reset_index(drop=True))