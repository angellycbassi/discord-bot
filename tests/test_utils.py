import os
import sys
import builtins

# Add path to bot-discord directory so we can import utils
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'bot-discord')))

import utils
import pytest


def _patch_randint(monkeypatch, values):
    it = iter(values)
    monkeypatch.setattr(utils.random, "randint", lambda a, b: next(it))


@pytest.mark.parametrize(
    "dice_str,vals,expected_total,expected_str",
    [
        ("2d6+3", [4, 2], 9, "2d6+3 = [4, 2] +3 = 9"),
        ("1d20", [7], 7, "1d20 = [7] = 7"),
        ("3d4-2", [1, 2, 3], 4, "3d4-2 = [1, 2, 3] -2 = 4"),
    ],
)
def test_roll_dice_valid(monkeypatch, dice_str, vals, expected_total, expected_str):
    _patch_randint(monkeypatch, vals)
    total, rolls, result_str = utils.roll_dice(dice_str)
    assert rolls == vals
    assert total == expected_total
    assert result_str == expected_str


@pytest.mark.parametrize(
    "dice_str",
    ["", "2d", "ad6", "2d6++3", "1d6+-2"],
)
def test_roll_dice_invalid(dice_str):
    with pytest.raises(ValueError):
        utils.roll_dice(dice_str)
