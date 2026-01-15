import sys
import argparse
from typing import Optional

# Import our modules
from dice import Dice, DiceSet
from visualizer import DiceVisualizer
from statistics import StatisticsTracker


class DiceRollerApp:
    """Main application class for Dice Rolling Simulator."""
    
    def __init__(self):
        self.stats_tracker = StatisticsTracker()
        self.dice_set = DiceSet()
        self.setup_default_dice()
        
    def setup_default_dice(self) -> None:
        """Setup some default dice."""
        for sides in [4, 6, 8, 10, 12, 20]:
            self.dice_set.add_dice(Dice(sides))
    
    def roll_single_dice(self, sides: int, times: int = 1, show_ascii: bool = True) -> None:
        """Roll a single dice multiple times."""
        dice = Dice(sides)
        
        print(f"\n🎲 Rolling {dice.name} {times} time{'s' if times > 1 else ''}...")
        
        for i in range(times):
            result = dice.roll()
            self.stats_tracker.add_record(dice, result)
            
            if show_ascii:
                DiceVisualizer.display_generic(dice, result)
            else:
                print(f"Roll {i+1}: {result}")
        
        if times > 1:
            print(f"\n📊 Summary: Total={sum(dice.get_history())}, "
                  f"Average={dice.get_average():.2f}")
    
    def roll_custom_dice(self, dice_definitions: list, show_ascii: bool = True) -> None:
        """Roll multiple custom dice."""
        print(f"\n🎲 Rolling custom dice combination...")
        
        total = 0
        for i, (sides, count) in enumerate(dice_definitions):
            dice = Dice(sides)
            results = dice.roll_multiple(count)
            
            for result in results:
                self.stats_tracker.add_record(dice, result)
            
            total += sum(results)
            print(f"\n{dice.name} (x{count}): {results}")
            
            if show_ascii and count == 1:
                DiceVisualizer.display_generic(dice, results[0])
        
        print(f"\n📊 Total sum: {total}")
    
    def show_statistics(self) -> None:
        """Display session statistics."""
        stats = self.stats_tracker.get_session_stats()
        
        print("\n" + "="*50)
        print("📈 SESSION STATISTICS")
        print("="*50)
        
        if stats["total_rolls"] == 0:
            print("No rolls recorded yet.")
            return
        
        print(f"Total rolls: {stats['total_rolls']}")
        print(f"Session duration: {stats['session_duration']}")
        
        if "dice_types" in stats:
            print("\nBreakdown by dice type:")
            for dice_type, dice_stats in stats["dice_types"].items():
                print(f"  {dice_type}:")
                print(f"    Rolls: {dice_stats['count']}")
                print(f"    Average: {dice_stats['average']:.2f}")
                print(f"    Range: {dice_stats['min']}-{dice_stats['max']}")
    
    def export_statistics(self, filename: str) -> None:
        """Export statistics to a file."""
        try:
            self.stats_tracker.export_to_json(filename)
            print(f"📁 Statistics exported to {filename}")
        except Exception as e:
            print(f"❌ Error exporting statistics: {e}")
    
    def interactive_mode(self) -> None:
        """Run the interactive mode."""
        self.print_welcome()
        
        while True:
            self.print_menu()
            choice = input("\nEnter your choice: ").strip()
            
            if choice == '1':
                self.handle_single_roll()
            elif choice == '2':
                self.handle_multiple_rolls()
            elif choice == '3':
                self.handle_custom_combination()
            elif choice == '4':
                self.show_statistics()
            elif choice == '5':
                self.export_statistics("dice_statistics.json")
            elif choice == '6':
                self.clear_statistics()
            elif choice == '0':
                print("\nThanks for rolling! Goodbye! 🎲")
                break
            else:
                print("\n❌ Invalid choice. Please try again.")
    
    def print_welcome(self) -> None:
        """Print welcome message."""
        print("\n" + "="*50)
        print("🎲 DICE ROLLING SIMULATOR")
        print("="*50)
        print("A professional dice rolling application")
        print("="*50)
    
    def print_menu(self) -> None:
        """Print the main menu."""
        print("\n" + "-"*30)
        print("MAIN MENU")
        print("-"*30)
        print("1. Roll a single dice")
        print("2. Roll multiple dice")
        print("3. Roll custom combination")
        print("4. Show statistics")
        print("5. Export statistics")
        print("6. Clear statistics")
        print("0. Exit")
    
    def handle_single_roll(self) -> None:
        """Handle single dice roll in interactive mode."""
        print("\nAvailable dice types:")
        for sides, name in Dice.DICE_TYPES.items():
            print(f"  {name} (d{sides})")
        
        try:
            sides = int(input("\nEnter number of sides: "))
            if sides not in Dice.DICE_TYPES:
                print(f"⚠️  Note: {sides} is not a standard dice type, but we'll roll it anyway!")
            
            times = int(input("Number of rolls (default 1): ") or "1")
            
            show_ascii = input("Show ASCII art? (y/n, default y): ").lower() != 'n'
            
            self.roll_single_dice(sides, times, show_ascii)
            
        except ValueError:
            print("❌ Please enter valid numbers.")
    
    def handle_multiple_rolls(self) -> None:
        """Handle multiple dice rolls in interactive mode."""
        try:
            sides = int(input("\nEnter number of sides: "))
            count = int(input("How many dice? "))
            
            dice = Dice(sides)
            results = dice.roll_multiple(count)
            
            print(f"\n🎲 Rolling {count} {dice.name}(s)...")
            print(f"Results: {results}")
            print(f"Total: {sum(results)}")
            
            for result in results:
                self.stats_tracker.add_record(dice, result)
                
        except ValueError:
            print("❌ Please enter valid numbers.")
    
    def handle_custom_combination(self) -> None:
        """Handle custom dice combination in interactive mode."""
        dice_definitions = []
        
        print("\nEnter dice combinations (e.g., '6 2' for 2d6)")
        print("Enter 'done' when finished")
        
        while True:
            entry = input("Dice (sides count): ").strip()
            if entry.lower() == 'done':
                break
            
            try:
                sides, count = map(int, entry.split())
                dice_definitions.append((sides, count))
            except ValueError:
                print("❌ Please enter in format 'sides count'")
        
        if dice_definitions:
            show_ascii = input("\nShow ASCII art? (y/n, default y): ").lower() != 'n'
            self.roll_custom_dice(dice_definitions, show_ascii)
    
    def clear_statistics(self) -> None:
        """Clear all statistics."""
        confirm = input("\nAre you sure you want to clear all statistics? (y/n): ")
        if confirm.lower() == 'y':
            self.stats_tracker.clear_stats()
            print("✅ Statistics cleared.")
        else:
            print("Operation cancelled.")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Dice Rolling Simulator - A professional dice rolling application",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -s 6           # Roll a single D6
  %(prog)s -s 20 -t 3     # Roll a D20 three times
  %(prog)s -i             # Interactive mode
        """
    )
    
    parser.add_argument('-s', '--sides', type=int, help='Number of dice sides')
    parser.add_argument('-t', '--times', type=int, default=1, help='Number of rolls')
    parser.add_argument('-n', '--no-ascii', action='store_true', help='Disable ASCII art')
    parser.add_argument('-i', '--interactive', action='store_true', help='Run in interactive mode')
    parser.add_argument('-c', '--combination', type=str, 
                       help='Dice combination (e.g., "2d6+1d20")')
    parser.add_argument('--stats', action='store_true', help='Show statistics')
    parser.add_argument('--export', type=str, help='Export statistics to file')
    
    args = parser.parse_args()
    app = DiceRollerApp()
    
    # Handle command line arguments
    if args.interactive:
        app.interactive_mode()
    elif args.stats:
        app.show_statistics()
    elif args.export:
        app.export_statistics(args.export)
    elif args.combination:
        # Parse dice combination like "2d6+1d20"
        # Implementation left as exercise
        print("Dice combination feature coming soon!")
    elif args.sides:
        app.roll_single_dice(args.sides, args.times, not args.no_ascii)
    else:
        # No arguments, show help and start interactive
        parser.print_help()
        print("\n" + "="*50)
        if input("\nStart interactive mode? (y/n): ").lower() == 'y':
            app.interactive_mode()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        sys.exit(1)