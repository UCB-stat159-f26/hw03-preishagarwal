"""Fetch Tennis Abstract career matches and plot player vs opponent age."""

from tennisage.matches import get_player_matches
from tennisage.plot import plot_age_gap

__all__ = ["get_player_matches", "plot_age_gap"]