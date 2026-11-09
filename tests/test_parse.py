import pytest

from tennisage._parse import _format_player_name


@pytest.mark.parametrize("name", ["serena williams", "Serena Williams",
                                  "SerenaWilliams", "  serena   williams "])
def test_format_name_variants(name):
    assert _format_player_name(name) == "SerenaWilliams"


def test_format_name_rejects_empty():
    with pytest.raises(ValueError):
        _format_player_name("   ")