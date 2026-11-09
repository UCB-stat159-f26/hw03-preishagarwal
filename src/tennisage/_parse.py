"""Private helpers for turning Tennis Abstract career JS files into rows."""

import json

OPP_AGE_FIELD = 16  # opponent birthdate (women's files) or age (men's files)


def _format_player_name(name):
    """Convert 'serena williams' or 'SerenaWilliams' to 'SerenaWilliams'."""
    tokens = name.strip().split()
    if not tokens:
        raise ValueError("Player name cannot be empty.")
    return "".join(tok[0].upper() + tok[1:] for tok in tokens)