"""Public function for getting a player's career matches."""

from tennisage import _fetch
from tennisage._clean import (_add_opponent_age, _add_player_age,
                              _rows_to_frame, _sort_matches)
from tennisage._parse import _extract_birthdate, _is_male_file


def get_player_matches(name):
    """Return a player's career matches from tennisabstract.com, ready to plot.

    name: player's name, e.g. "Serena Williams", "serena williams",
          or "SerenaWilliams".

    Returns a data frame with one row per match and the columns date, result,
    round, opp_name, opp_age, player_age, and age_diff (player minus opponent).
    Raises ValueError if tennisabstract.com has no career file for the name.
    """
    player, rows = _fetch._load_career_rows(name)
    is_male = _is_male_file(rows)
    page = _fetch._download_text(_fetch._player_page_url(player, is_male))
    matches = _add_opponent_age(_rows_to_frame(rows), is_male)
    matches = _add_player_age(matches, _extract_birthdate(page))
    return _sort_matches(matches)