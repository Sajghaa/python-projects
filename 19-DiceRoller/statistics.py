import json
from typing import List, Dict, Any
from datetime import datetime
from dataclasses import dataclass, asdict
from collections import defaultdict


@dataclass
class RollRecord:
    """Data class for storing individual roll records."""
    timestamp: str
    dice_type: str
    sides: int
    result: int
    
    
class StatisticsTracker:
    """Tracks statistics for dice rolls."""
    
    def __init__(self):
        self.records: List[RollRecord] = []
        self._session_start = datetime.now()
        
    def add_record(self, dice: 'Dice', result: int) -> None:
        """Add a roll record to the statistics."""
        record = RollRecord(
            timestamp=datetime.now().isoformat(),
            dice_type=dice.name,
            sides=dice.sides,
            result=result
        )
        self.records.append(record)
    
    def get_session_stats(self) -> Dict[str, Any]:
        """Get statistics for the current session."""
        if not self.records:
            return {"total_rolls": 0}
        
        stats = {
            "total_rolls": len(self.records),
            "session_duration": str(datetime.now() - self._session_start),
            "session_start": self._session_start.isoformat(),
        }
        
        # Group by dice type
        by_dice_type = defaultdict(list)
        for record in self.records:
            by_dice_type[record.dice_type].append(record.result)
        
        dice_stats = {}
        for dice_type, results in by_dice_type.items():
            dice_stats[dice_type] = {
                "count": len(results),
                "average": sum(results) / len(results),
                "min": min(results),
                "max": max(results),
            }
        
        stats["dice_types"] = dice_stats
        return stats
    
    def export_to_json(self, filename: str = "dice_stats.json") -> None:
        """Export statistics to a JSON file."""
        data = {
            "session_info": {
                "start": self._session_start.isoformat(),
                "end": datetime.now().isoformat(),
                "total_rolls": len(self.records)
            },
            "records": [asdict(record) for record in self.records]
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
    
    def clear_stats(self) -> None:
        """Clear all statistics."""
        self.records.clear()
        self._session_start = datetime.now()