import pytest
from io import StringIO
from contextlib import redirect_stdout
from dice import Dice
from visualizer import DiceVisualizer


class TestDiceVisualizer:
    """Test cases for DiceVisualizer class."""
    
    def test_d6_art_dictionary(self):
        """Test D6 ASCII art dictionary."""
        assert 1 in DiceVisualizer.D6_ART
        assert 6 in DiceVisualizer.D6_ART
        assert len(DiceVisualizer.D6_ART) == 6
        
        # Check structure of one art piece
        art_1 = DiceVisualizer.D6_ART[1]
        assert isinstance(art_1, list)
        assert len(art_1) == 5
        assert "┌─────────┐" in art_1[0]
        assert "●" in art_1[2]  # Dot in the middle
    
    def test_display_d6_valid(self):
        """Test displaying valid D6 rolls."""
        dice = Dice(6)
        
        # Test roll 1
        with redirect_stdout(StringIO()) as f:
            DiceVisualizer.display_d6(1)
        output = f.getvalue()
        assert "●" in output
        
        # Test roll 6
        with redirect_stdout(StringIO()) as f:
            DiceVisualizer.display_d6(6)
        output = f.getvalue()
        assert "●" in output
        # Should have 6 dots (3 pairs)
        assert output.count("●") == 6
    
    def test_display_d6_invalid(self):
        """Test displaying invalid D6 rolls."""
        with redirect_stdout(StringIO()) as f:
            DiceVisualizer.display_d6(7)  # Invalid for D6
        output = f.getvalue()
        assert "Rolled: 7" in output
        
        with redirect_stdout(StringIO()) as f:
            DiceVisualizer.display_d6(0)
        output = f.getvalue()
        assert "Rolled: 0" in output
    
    def test_display_generic_d6(self):
        """Test generic display for D6."""
        dice = Dice(6)
        
        with redirect_stdout(StringIO()) as f:
            DiceVisualizer.display_generic(dice, 4)
        output = f.getvalue()
        assert "●" in output
    
    def test_display_generic_other(self):
        """Test generic display for non-D6 dice."""
        dice = Dice(20)
        
        with redirect_stdout(StringIO()) as f:
            DiceVisualizer.display_generic(dice, 15)
        output = f.getvalue()
        assert "D20" in output
        assert "15" in output
    
    def test_display_multiple(self):
        """Test displaying multiple dice."""
        results = {
            "D6 (d6)": [4],
            "D20 (d20)": [15]
        }
        
        with redirect_stdout(StringIO()) as f:
            DiceVisualizer.display_multiple(results)
        output = f.getvalue()
        
        assert "D6" in output
        assert "D20" in output
        assert "4" in output
        assert "15" in output