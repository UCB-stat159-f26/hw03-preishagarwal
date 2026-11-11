import matplotlib

matplotlib.use("Agg")  # draw without a screen, so tests run anywhere

import matplotlib.pyplot as plt
import pandas as pd
import pytest

from tennisage import plot_age_gap


@pytest.fixture
def matches():
    return pd.DataFrame({"player_age": [15.0, 20.0, 30.0],
                         "age_diff": [-3.0, 1.5, 6.0],
                         "result": ["L", "W", "W"]})


def test_returns_figure(matches):
    fig = plot_age_gap(matches)
    assert isinstance(fig, plt.Figure)
    plt.close(fig)


def test_one_point_per_match(matches):
    fig = plot_age_gap(matches)
    points = sum(len(c.get_offsets()) for c in fig.axes[0].collections)
    assert points == 3
    plt.close(fig)


def test_custom_title(matches):
    fig = plot_age_gap(matches, title="Serena Williams")
    assert fig.axes[0].get_title(loc="left") == "Serena Williams"
    plt.close(fig)


def test_missing_column_raises(matches):
    with pytest.raises(ValueError, match="missing column"):
        plot_age_gap(matches.drop(columns="result"))