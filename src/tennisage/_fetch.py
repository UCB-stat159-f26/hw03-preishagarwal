"""Private helpers for downloading files from tennisabstract.com."""

BASE_URL = "https://www.tennisabstract.com"


def _career_url(player):
    """Return the URL of a player's career JS file."""
    return f"{BASE_URL}/jsmatches/{player}Career.js"


def _player_page_url(player, is_male):
    """Return the URL of a player's page (men and women use different scripts)."""
    script = "player.cgi" if is_male else "wplayer.cgi"
    return f"{BASE_URL}/cgi-bin/{script}?p={player}"