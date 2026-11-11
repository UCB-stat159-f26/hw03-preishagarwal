"""Public function for plotting a player's age against the age gap."""

import matplotlib.pyplot as plt

PLOT_COLUMNS = ["player_age", "age_diff", "result"]
RESULT_STYLES = [("W", "#2a6f97", "Win"), ("L", "#d1495b", "Loss")]


def _check_plot_columns(matches):
    """Raise a clear error if the data frame is missing a needed column."""
    missing = [col for col in PLOT_COLUMNS if col not in matches.columns]
    if missing:
        raise ValueError(f"Data frame is missing column(s) {missing}. "
                         "Pass the output of get_player_matches().")


def _style_axes(ax, title):
    """Add the zero line, labels, legend, and light styling."""
    ax.axhline(0, color="#222222", linewidth=1)
    ax.set_xlabel("Player's age")
    ax.set_ylabel("Player's age minus opponent's age")
    ax.set_title(title, loc="left", fontsize=13, fontweight="bold")
    ax.grid(linestyle=":", alpha=0.5)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(loc="best", frameon=False, markerscale=2)


def plot_age_gap(matches, title="Player's age vs. age gap with opponents"):
    """Scatter plot of a player's age against the age gap with each opponent.

    matches: data frame returned by get_player_matches().
    title:   optional plot title, e.g. "Serena Williams".

    Each point is one match. Points above zero are matches against younger
    opponents. Wins and losses are shown in different colors.
    Returns the matplotlib figure, so it can be saved with fig.savefig().
    """
    _check_plot_columns(matches)
    fig, ax = plt.subplots(figsize=(10, 6))
    for result, color, label in RESULT_STYLES:
        games = matches[matches["result"] == result]
        ax.scatter(games["player_age"], games["age_diff"], s=16, color=color,
                   alpha=0.6, edgecolors="none", label=label)
    _style_axes(ax, title)
    return fig