import random
from typing import List, Tuple, Dict, Optional


class Dice:
    """A class representing a single die with configurable sides."""
    
    # Common dice types in tabletop gaming
    DICE_TYPES = {
        4: "D4",
        6: "D6",
        8: "D8",
        10: "D10",
        12: "D12",
        20: "D20",
        100: "D100"
    }
    
    def __init__(self, sides: int = 6, name: Optional[str] = None):
        """
        Initialize a dice with specified number of sides.
        
        Args:
            sides (int): Number of sides on the dice (default: 6)
            name (str, optional): Custom name for the dice
        """
        if sides < 2:
            raise ValueError("Dice must have at least 2 sides")
        
        self.sides = sides
        self.name = name or self.DICE_TYPES.get(sides, f"D{sides}")
        self._history = []
        
    def roll(self) -> int:
        """
        Roll the dice once.
        
        Returns:
            int: Random number between 1 and number of sides
        """
        result = random.randint(1, self.sides)
        self._history.append(result)
        return result
    
    def roll_multiple(self, times: int = 1) -> List[int]:
        """
        Roll the dice multiple times.
        
        Args:
            times (int): Number of rolls
            
        Returns:
            List[int]: List of roll results
        """
        if times < 1:
            raise ValueError("Number of rolls must be at least 1")
        
        return [self.roll() for _ in range(times)]
    
    def get_history(self) -> List[int]:
        """Get the history of all rolls for this dice."""
        return self._history.copy()
    
    def clear_history(self) -> None:
        """Clear the roll history."""
        self._history.clear()
    
    def get_average(self) -> float:
        """Calculate average of all rolls."""
        if not self._history:
            return 0.0
        return sum(self._history) / len(self._history)
    
    def __str__(self) -> str:
        return f"{self.name} (d{self.sides})"
    
    def __repr__(self) -> str:
        return f"Dice(sides={self.sides}, name='{self.name}')"


class DiceSet:
    """A collection of dice that can be rolled together."""
    
    def __init__(self):
        self.dice = []
        self._history = []
        
    def add_dice(self, dice: Dice) -> None:
        """Add a dice to the set."""
        self.dice.append(dice)
        
    def roll_all(self) -> Dict[str, List[int]]:
        """
        Roll all dice in the set.
        
        Returns:
            Dict[str, List[int]]: Dictionary mapping dice names to roll results
        """
        results = {}
        for dice in self.dice:
            results[str(dice)] = [dice.roll()]
        self._history.append(results)
        return results
    
    def get_dice_by_type(self, sides: int) -> List[Dice]:
        return [dice for dice in self.dice if dice.sides == sides]