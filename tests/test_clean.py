import pandas as pd
import pytest

from tennisage._clean import _add_opponent_age, _rows_to_frame
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