import pandas as pd
import pytest
from tennisage._clean import (_add_opponent_age, _add_player_age,
                              _rows_to_frame, _sort_matches)
from tennisage._parse import _extract_matches
from tests.mock_data import FEMALE_JS, MALE_JS


@pytest.fixture
def female_matches():
    return _rows_to_frame(_extract_matches(FEMALE_JS))


@pytest.fixture
def male_matches():
    return _rows_to_frame(_extract_matches(MALE_JS))


def test_rows_to_frame_columns(female_matches):
    assert list(female_matches.columns) == ["date", "result", "round",
                                            "opp_name", "opp_age_raw"]
    assert female_matches.loc[0, "date"] == pd.Timestamp("1995-10-30")


def test_female_opponent_age_from_birthdate(female_matches):
    ages = _add_opponent_age(female_matches, is_male=False)["opp_age"]
    assert ages[0] == pytest.approx(18.78, abs=0.01)  # Anne Miller


def test_male_opponent_age_read_directly(male_matches):
    ages = _add_opponent_age(male_matches, is_male=True)["opp_age"]
    assert ages[0] == pytest.approx(22.264, abs=0.001)  # Guillermo Platel

def test_player_age_and_gap(female_matches):
    matches = _add_opponent_age(female_matches, is_male=False)
    matches = _add_player_age(matches, pd.Timestamp("1981-09-26"))
    assert matches.loc[0, "player_age"] == pytest.approx(14.09, abs=0.01)
    assert matches.loc[0, "age_diff"] == pytest.approx(14.09 - 18.78, abs=0.02)


def test_sort_puts_earlier_round_first(male_matches):
    matches = _add_opponent_age(male_matches, is_male=True)
    matches = _add_player_age(matches, pd.Timestamp("1986-06-03"))
    rounds = _sort_matches(matches)["round"].tolist()
    assert rounds == ["R32", "R32", "R16"]  # Spain F10, then Seville R32, R16