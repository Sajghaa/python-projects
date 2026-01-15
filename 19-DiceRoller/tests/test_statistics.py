"""
Unit tests for statistics.py module.
"""
import pytest
import json
import tempfile
from datetime import datetime
from dice import Dice
from statistics import StatisticsTracker, RollRecord


class TestRollRecord:
    """Test cases for RollRecord dataclass."""
    
    def test_roll_record_creation(self):
        """Test creating roll records."""
        timestamp = "2024-01-01T12:00:00"
        record = RollRecord(
            timestamp=timestamp,
            dice_type="D20",
            sides=20,
            result=15
        )
        
        assert record.timestamp == timestamp
        assert record.dice_type == "D20"
        assert record.sides == 20
        assert record.result == 15
    
    def test_asdict_conversion(self):
        """Test converting to dictionary."""
        record = RollRecord(
            timestamp="2024-01-01T12:00:00",
            dice_type="D6",
            sides=6,
            result=4
        )
        
        record_dict = {
            "timestamp": "2024-01-01T12:00:00",
            "dice_type": "D6",
            "sides": 6,
            "result": 4
        }
        
        assert vars(record) == record_dict


class TestStatisticsTracker:
    """Test cases for StatisticsTracker class."""
    
    def test_initialization(self):
        """Test tracker initialization."""
        tracker = StatisticsTracker()
        
        assert tracker.records == []
        assert isinstance(tracker._session_start, datetime)
    
    def test_add_record(self):
        """Test adding roll records."""
        tracker = StatisticsTracker()
        dice = Dice(6)
        
        tracker.add_record(dice, 4)
        tracker.add_record(dice, 6)
        
        assert len(tracker.records) == 2
        
        first_record = tracker.records[0]
        assert first_record.dice_type == "D6"
        assert first_record.sides == 6
        assert first_record.result == 4
        
        second_record = tracker.records[1]
        assert second_record.result == 6
    
    def test_empty_session_stats(self):
        """Test statistics with empty session."""
        tracker = StatisticsTracker()
        
        stats = tracker.get_session_stats()
        
        assert stats["total_rolls"] == 0
        assert "session_duration" in stats
    
    def test_session_stats_with_records(self):
        """Test statistics with records."""
        tracker = StatisticsTracker()
        d6 = Dice(6)
        d20 = Dice(20)
        
        # Add some records
        tracker.add_record(d6, 3)
        tracker.add_record(d6, 5)
        tracker.add_record(d20, 15)
        tracker.add_record(d20, 18)
        tracker.add_record(d20, 1)
        
        stats = tracker.get_session_stats()
        
        assert stats["total_rolls"] == 5
        assert "session_duration" in stats
        assert "session_start" in stats
        
        # Check dice type breakdown
        assert "dice_types" in stats
        dice_stats = stats["dice_types"]
        
        assert "D6" in dice_stats
        assert "D20" in dice_stats
        
        d6_stats = dice_stats["D6"]
        assert d6_stats["count"] == 2
        assert d6_stats["average"] == 4.0  # (3+5)/2
        assert d6_stats["min"] == 3
        assert d6_stats["max"] == 5
        
        d20_stats = dice_stats["D20"]
        assert d20_stats["count"] == 3
        assert d20_stats["average"] == pytest.approx(11.333, rel=0.001)  # (15+18+1)/3
        assert d20_stats["min"] == 1
        assert d20_stats["max"] == 18
    
    def test_export_to_json(self):
        """Test exporting statistics to JSON file."""
        tracker = StatisticsTracker()
        dice = Dice(6)
        
        # Add some records
        tracker.add_record(dice, 4)
        tracker.add_record(dice, 6)
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            # Export to file
            tracker.export_to_json(tmp_path)
            
            # Read and verify
            with open(tmp_path, 'r') as f:
                data = json.load(f)
            
            assert "session_info" in data
            assert "records" in data
            
            session_info = data["session_info"]
            assert "start" in session_info
            assert "end" in session_info
            assert session_info["total_rolls"] == 2
            
            records = data["records"]
            assert len(records) == 2
            assert records[0]["dice_type"] == "D6"
            assert records[0]["result"] == 4
            
        finally:
            # Clean up
            import os
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    
    def test_clear_statistics(self):
        """Test clearing statistics."""
        tracker = StatisticsTracker()
        dice = Dice(6)
        
        # Add some records
        tracker.add_record(dice, 4)
        tracker.add_record(dice, 6)
        
        assert len(tracker.records) == 2
        
        # Store old session start
        old_start = tracker._session_start
        
        # Clear statistics
        tracker.clear_stats()
        
        assert len(tracker.records) == 0
        assert tracker._session_start != old_start
        assert isinstance(tracker._session_start, datetime)