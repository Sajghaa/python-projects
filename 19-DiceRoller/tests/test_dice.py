import pytest
from dice import Dice
from statistics import StatisticsTracker


@pytest.fixture
def standard_d6():
    """Fixture for a standard D6 dice."""
    return Dice(sides=6)


@pytest.fixture
def custom_d20():
    """Fixture for a D20 dice."""
    return Dice(sides=20, name="Custom D20")


@pytest.fixture
def stats_tracker():
    """Fixture for a clean statistics tracker."""
    return StatisticsTracker()


@pytest.fixture
def dice_set():
    """Fixture for a set of dice."""
    from dice import DiceSet
    dice_set = DiceSet()
    dice_set.add_dice(Dice(6))
    dice_set.add_dice(Dice(20))
    return dice_set