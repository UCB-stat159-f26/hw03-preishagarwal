"""Private helpers for downloading files from tennisabstract.com."""

BASE_URL = "https://www.tennisabstract.com"
USER_AGENT = "Mozilla/5.0 (stat159-hw03)"

from urllib.error import HTTPError
from urllib.request import Request, urlopen

from tennisage._parse import _extract_matches, _format_player_name

def _career_url(player):
    """Return the URL of a player's career JS file."""
    return f"{BASE_URL}/jsmatches/{player}Career.js"


def _player_page_url(player, is_male):
    """Return the URL of a player's page (men and women use different scripts)."""
    script = "player.cgi" if is_male else "wplayer.cgi"
    return f"{BASE_URL}/cgi-bin/{script}?p={player}"

def _download_text(url):
    """Download a page as text; a missing page raises ValueError."""
    request = Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(request, timeout=60) as response:
            return response.read().decode("utf-8", errors="replace")
    except HTTPError as err:
        if err.code == 404:
            raise ValueError(f"Page not found: {url}") from err
        raise


def _load_career_rows(name):
    """Return the formatted name and match rows, or a clear error for bad names."""
    player = _format_player_name(name)
    try:
        rows = _extract_matches(_download_text(_career_url(player)))
    except ValueError:
        rows = []
    if not rows:
        raise ValueError(f"Could not find career matches for '{name}' on "
                         f"tennisabstract.com (looked for {player}). Check the "
                         "spelling, e.g. 'Serena Williams' or 'Rafael Nadal'.")
    return player, rows