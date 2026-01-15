class DiceVisualizer:
    """Creates ASCII art representations of dice rolls."""
    
    # ASCII art for standard D6 dice faces (1-6)
    D6_ART = {
        1: [
            "┌─────────┐",
            "│         │",
            "│    ●    │",
            "│         │",
            "└─────────┘",
        ],
        2: [
            "┌─────────┐",
            "│ ●       │",
            "│         │",
            "│       ● │",
            "└─────────┘",
        ],
        3: [
            "┌─────────┐",
            "│ ●       │",
            "│    ●    │",
            "│       ● │",
            "└─────────┘",
        ],
        4: [
            "┌─────────┐",
            "│ ●     ● │",
            "│         │",
            "│ ●     ● │",
            "└─────────┘",
        ],
        5: [
            "┌─────────┐",
            "│ ●     ● │",
            "│    ●    │",
            "│ ●     ● │",
            "└─────────┘",
        ],
        6: [
            "┌─────────┐",
            "│ ●     ● │",
            "│ ●     ● │",
            "│ ●     ● │",
            "└─────────┘",
        ],
    }
    
    # Simple text representation for other dice types
    OTHER_DICE_TEMPLATE = [
        "┌──────────────┐",
        "│    D{sides:2d}     │",
        "│              │",
        "│    {result:3d}      │",
        "│              │",
        "└──────────────┘",
    ]
    
    @staticmethod
    def display_d6(result: int) -> None:
        """
        Display ASCII art for a standard D6 dice roll.
        
        Args:
            result (int): Roll result (1-6)
        """
        if result not in range(1, 7):
            print(f"Rolled: {result}")
            return
            
        print("\n".join(DiceVisualizer.D6_ART[result]))
        
    @staticmethod
    def display_generic(dice: 'Dice', result: int) -> None:
        """
        Display generic dice representation.
        
        Args:
            dice (Dice): The dice object
            result (int): Roll result
        """
        if dice.sides == 6:
            DiceVisualizer.display_d6(result)
        else:
            art = [line.format(sides=dice.sides, result=result) 
                  for line in DiceVisualizer.OTHER_DICE_TEMPLATE]
            print("\n".join(art))
    
    @staticmethod
    def display_multiple(results: dict) -> None:
        """
        Display multiple dice side by side.
        
        Args:
            results (dict): Dictionary of dice names to results
        """
        # This would be more complex - would need to align ASCII art
        # For simplicity, showing each dice separately
        for dice_name, roll_results in results.items():
            print(f"\n{dice_name}:")
            for result in roll_results:
                print(f"  Rolled: {result}")