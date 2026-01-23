#!/usr/bin/env python3
"""
Number List Analyzer
Find largest, smallest, and analyze numbers in a list.
"""

import os
import sys
import random
import statistics
import json
from datetime import datetime
from typing import List, Dict, Tuple, Optional, Any


class NumberAnalyzer:
    """Main number analyzer class with multiple analysis functions."""
    
    def __init__(self):
        """Initialize the number analyzer."""
        self.number_lists = []  # Store multiple lists
        self.current_list = []
        self.history = []
        
    def clear_screen(self) -> None:
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_banner(self) -> None:
        """Display the application banner."""
        banner = """
╔══════════════════════════════════════════════════════╗
║              🔢 NUMBER LIST ANALYZER 🔢              ║
║      Find largest, smallest & analyze numbers!       ║
╚══════════════════════════════════════════════════════╝
        """
        print(banner)
    
    def display_menu(self) -> None:
        """Display the main menu."""
        print("\n" + "═" * 50)
        print("📋 MAIN MENU")
        print("═" * 50)
        print("1️⃣  Create/Edit number list")
        print("2️⃣  Find largest & smallest numbers")
        print("3️⃣  Calculate statistics")
        print("4️⃣  Sort numbers")
        print("5️⃣  Find duplicates")
        print("6️⃣  Filter numbers")
        print("7️⃣  Generate random list")
        print("8️⃣  Visualize numbers")
        print("9️⃣  Save/Load lists")
        print("🔟  View history")
        print("0️⃣  Exit")
        print("═" * 50)
    
    def get_menu_choice(self) -> str:
        """Get and validate menu choice."""
        while True:
            try:
                choice = input("\nEnter your choice (0-10): ").strip()
                if choice == '10' or choice in [str(i) for i in range(10)]:
                    return choice
                else:
                    print("❌ Please enter a number between 0 and 10")
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                sys.exit(0)
    
    def create_number_list(self) -> None:
        """Create or edit a number list."""
        self.clear_screen()
        print("\n" + "═" * 50)
        print("📝 CREATE/EDIT NUMBER LIST")
        print("═" * 50)
        
        if self.current_list:
            print(f"\nCurrent list ({len(self.current_list)} numbers):")
            self.display_list_preview(self.current_list)
            
            print("\nOptions:")
            print("1. Add new numbers")
            print("2. Clear list")
            print("3. Edit specific numbers")
            print("4. Keep current list")
            
            option = input("\nChoose option (1-4, default 1): ").strip()
            
            if option == '2':
                self.current_list.clear()
                print("✅ List cleared!")
            elif option == '3':
                self.edit_specific_numbers()
                return
            elif option == '4':
                return
        
        print("\nEnter numbers separated by spaces, commas, or new lines.")
        print("Examples: '1 2 3 4 5' or '10,20,30,40'")
        print("Type 'done' on a new line to finish.")
        print("Type 'cancel' to go back.")
        
        numbers = []
        print("\n" + "─" * 30)
        
        while True:
            try:
                line = input("Enter numbers: ").strip()
                
                if line.lower() == 'done':
                    break
                if line.lower() == 'cancel':
                    print("❌ Operation cancelled.")
                    return
                
                # Parse the input line
                # Replace commas with spaces and split
                line = line.replace(',', ' ').replace(';', ' ')
                parts = line.split()
                
                for part in parts:
                    # Try to convert to number (int or float)
                    try:
                        if '.' in part:
                            num = float(part)
                        else:
                            num = int(part)
                        numbers.append(num)
                    except ValueError:
                        print(f"⚠️  Skipping invalid value: '{part}'")
                
                print(f"✅ Added {len(parts)} numbers. Total: {len(numbers)}")
                
            except KeyboardInterrupt:
                print("\n\n👋 Operation cancelled.")
                return
        
        if numbers:
            # Ask if user wants to replace or append
            if self.current_list and len(self.current_list) > 0:
                print(f"\nCurrent list has {len(self.current_list)} numbers.")
                choice = input("Append to current list? (y/N): ").strip().lower()
                
                if choice == 'y':
                    self.current_list.extend(numbers)
                    print(f"✅ Appended {len(numbers)} numbers. New total: {len(self.current_list)}")
                else:
                    self.current_list = numbers
                    print(f"✅ Created new list with {len(numbers)} numbers")
            else:
                self.current_list = numbers
                print(f"✅ Created list with {len(numbers)} numbers")
            
            # Save to history
            self.add_to_history(f"Created list with {len(numbers)} numbers")
        else:
            print("❌ No valid numbers entered!")
        
        input("\nPress Enter to continue...")
    
    def edit_specific_numbers(self) -> None:
        """Edit specific numbers in the list."""
        print(f"\nCurrent list ({len(self.current_list)} numbers):")
        for i, num in enumerate(self.current_list, 1):
            print(f"{i:3d}. {num}")
        
        print("\nOptions:")
        print("1. Remove number at position")
        print("2. Replace number at position")
        print("3. Insert number at position")
        
        try:
            option = int(input("\nChoose option (1-3): ").strip())
            
            if option == 1:
                pos = int(input("Enter position to remove (1-based): ").strip())
                if 1 <= pos <= len(self.current_list):
                    removed = self.current_list.pop(pos - 1)
                    print(f"✅ Removed {removed} at position {pos}")
                else:
                    print("❌ Invalid position!")
            
            elif option == 2:
                pos = int(input("Enter position to replace (1-based): ").strip())
                if 1 <= pos <= len(self.current_list):
                    new_num = float(input("Enter new number: ").strip())
                    old_num = self.current_list[pos - 1]
                    self.current_list[pos - 1] = new_num
                    print(f"✅ Replaced {old_num} with {new_num} at position {pos}")
                else:
                    print("❌ Invalid position!")
            
            elif option == 3:
                pos = int(input("Enter position to insert (1-based): ").strip())
                if 1 <= pos <= len(self.current_list) + 1:
                    new_num = float(input("Enter number to insert: ").strip())
                    self.current_list.insert(pos - 1, new_num)
                    print(f"✅ Inserted {new_num} at position {pos}")
                else:
                    print("❌ Invalid position!")
            
            else:
                print("❌ Invalid option!")
                
        except ValueError:
            print("❌ Please enter valid numbers!")
        
        input("\nPress Enter to continue...")
    
    def display_list_preview(self, numbers: List[float]) -> None:
        """Display a preview of the number list."""
        if not numbers:
            print("Empty list")
            return
        
        if len(numbers) <= 10:
            print("[" + ", ".join(str(num) for num in numbers) + "]")
        else:
            # Show first 5, last 5
            first_five = numbers[:5]
            last_five = numbers[-5:]
            print("[" + ", ".join(str(num) for num in first_five) + 
                  ", ..., " + ", ".join(str(num) for num in last_five) + "]")
        
        print(f"Total numbers: {len(numbers)}")
    
    def find_min_max(self) -> None:
        """Find the smallest and largest numbers in the list."""
        self.clear_screen()
        print("\n" + "═" * 50)
        print("🔍 FIND LARGEST & SMALLEST NUMBERS")
        print("═" * 50)
        
        if not self.current_list:
            print("\n❌ No numbers in the list!")
            print("Please create a list first.")
            input("\nPress Enter to continue...")
            return
        
        print(f"\nAnalyzing {len(self.current_list)} numbers...")
        
        # Method 1: Using min() and max() functions
        smallest = min(self.current_list)
        largest = max(self.current_list)
        
        # Method 2: Manual algorithm (for educational purposes)
        print("\n" + "─" * 40)
        print("🎯 RESULTS:")
        print("-" * 40)
        print(f"Smallest number: {smallest}")
        print(f"Largest number:  {largest}")
        
        # Find position/index
        min_index = self.current_list.index(smallest) + 1
        max_index = self.current_list.index(largest) + 1
        
        print(f"\nPositions (1-based):")
        print(f"Smallest at position: {min_index}")
        print(f"Largest at position:  {max_index}")
        
        # Find all occurrences
        min_indices = [i+1 for i, x in enumerate(self.current_list) if x == smallest]
        max_indices = [i+1 for i, x in enumerate(self.current_list) if x == largest]
        
        if len(min_indices) > 1:
            print(f"Smallest appears {len(min_indices)} times at positions: {min_indices}")
        if len(max_indices) > 1:
            print(f"Largest appears {len(max_indices)} times at positions: {max_indices}")
        
        # Range calculation
        number_range = largest - smallest
        print(f"\nRange (Largest - Smallest): {number_range}")
        
        # Display algorithm steps
        print("\n" + "─" * 40)
        print("🤖 ALGORITHM EXPLANATION:")
        print("-" * 40)
        print("Finding smallest:")
        print("1. Start with first number as smallest")
        print("2. Compare with each number in list")
        print("3. Update smallest if current number is smaller")
        print("\nFinding largest:")
        print("1. Start with first number as largest")
        print("2. Compare with each number in list")
        print("3. Update largest if current number is larger")
        
        self.add_to_history(f"Found min={smallest}, max={largest}")
        input("\nPress Enter to continue...")
    
    def calculate_statistics(self) -> None:
        """Calculate various statistics for the list."""
        self.clear_screen()
        print("\n" + "═" * 50)
        print("📊 CALCULATE STATISTICS")
        print("═" * 50)
        
        if not self.current_list:
            print("\n❌ No numbers in the list!")
            print("Please create a list first.")
            input("\nPress Enter to continue...")
            return
        
        print(f"\nAnalyzing {len(self.current_list)} numbers...")
        
        # Basic statistics
        smallest = min(self.current_list)
        largest = max(self.current_list)
        total = sum(self.current_list)
        count = len(self.current_list)
        average = total / count if count > 0 else 0
        
        # Using statistics module for more advanced stats
        try:
            median = statistics.median(self.current_list)
            mode = statistics.mode(self.current_list) if len(set(self.current_list)) < count else "No unique mode"
            stdev = statistics.stdev(self.current_list) if count > 1 else 0
            variance = statistics.variance(self.current_list) if count > 1 else 0
        except statistics.StatisticsError:
            mode = "No mode"
            stdev = 0
            variance = 0
        
        # Sort for quartiles
        sorted_list = sorted(self.current_list)
        
        # Quartiles
        q1 = sorted_list[count // 4] if count >= 4 else "N/A"
        q2 = median  # Same as median
        q3 = sorted_list[3 * count // 4] if count >= 4 else "N/A"
        
        # Display results
        print("\n" + "─" * 40)
        print("📈 BASIC STATISTICS:")
        print("-" * 40)
        print(f"Count:          {count}")
        print(f"Sum:            {total:,.2f}")
        print(f"Average (Mean): {average:,.4f}")
        print(f"Minimum:        {smallest}")
        print(f"Maximum:        {largest}")
        print(f"Range:          {largest - smallest:,.4f}")
        
        print("\n" + "─" * 40)
        print("📊 ADVANCED STATISTICS:")
        print("-" * 40)
        print(f"Median:         {median}")
        print(f"Mode:           {mode}")
        print(f"Std Deviation:  {stdev:,.4f}")
        print(f"Variance:       {variance:,.4f}")
        
        print("\n" + "─" * 40)
        print("📐 QUARTILES:")
        print("-" * 40)
        print(f"Q1 (25th %):    {q1}")
        print(f"Q2 (Median):    {q2}")
        print(f"Q3 (75th %):    {q3}")
        print(f"IQR (Q3-Q1):    {(q3 - q1) if isinstance(q1, (int, float)) and isinstance(q3, (int, float)) else 'N/A'}")
        
        # Data quality
        print("\n" + "─" * 40)
        print("🔍 DATA QUALITY:")
        print("-" * 40)
        print(f"Unique values:  {len(set(self.current_list))}")
        print(f"Sorted:         {'Yes' if self.current_list == sorted_list else 'No'}")
        
        # Detect if sorted
        is_sorted_asc = all(self.current_list[i] <= self.current_list[i+1] 
                           for i in range(len(self.current_list)-1))
        is_sorted_desc = all(self.current_list[i] >= self.current_list[i+1] 
                            for i in range(len(self.current_list)-1))
        
        if is_sorted_asc:
            print("Order:          Ascending")
        elif is_sorted_desc:
            print("Order:          Descending")
        else:
            print("Order:          Unsorted")
        
        self.add_to_history("Calculated statistics")
        input("\nPress Enter to continue...")
    
    def sort_numbers(self) -> None:
        """Sort the numbers in various ways."""
        self.clear_screen()
        print("\n" + "═" * 50)
        print("🔢 SORT NUMBERS")
        print("═" * 50)
        
        if not self.current_list:
            print("\n❌ No numbers in the list!")
            print("Please create a list first.")
            input("\nPress Enter to continue...")
            return
        
        print(f"\nCurrent list ({len(self.current_list)} numbers):")
        self.display_list_preview(self.current_list)
        
        print("\nSorting Options:")
        print("1. Sort ascending (smallest to largest)")
        print("2. Sort descending (largest to smallest)")
        print("3. Sort by absolute value")
        print("4. Sort by last digit")
        print("5. Shuffle randomly")
        
        try:
            option = int(input("\nChoose option (1-5): ").strip())
            
            original_list = self.current_list.copy()
            
            if option == 1:
                self.current_list.sort()
                print("✅ Sorted ascending")
                sort_type = "ascending"
            
            elif option == 2:
                self.current_list.sort(reverse=True)
                print("✅ Sorted descending")
                sort_type = "descending"
            
            elif option == 3:
                self.current_list.sort(key=abs)
                print("✅ Sorted by absolute value")
                sort_type = "by absolute value"
            
            elif option == 4:
                self.current_list.sort(key=lambda x: abs(x) % 10)
                print("✅ Sorted by last digit")
                sort_type = "by last digit"
            
            elif option == 5:
                random.shuffle(self.current_list)
                print("✅ Shuffled randomly")
                sort_type = "shuffled"
            
            else:
                print("❌ Invalid option!")
                input("\nPress Enter to continue...")
                return
            
            # Show before and after
            print("\n" + "─" * 40)
            print("📋 BEFORE SORTING:")
            print("-" * 40)
            self.display_list_preview(original_list)
            
            print("\n" + "─" * 40)
            print("📋 AFTER SORTING:")
            print("-" * 40)
            self.display_list_preview(self.current_list)
            
            # Show first 10 numbers sorted
            if len(self.current_list) > 0:
                print("\nFirst 10 sorted numbers:")
                for i, num in enumerate(self.current_list[:10], 1):
                    print(f"{i:2d}. {num}")
            
            self.add_to_history(f"Sorted numbers ({sort_type})")
            
        except ValueError:
            print("❌ Please enter a valid number!")
        
        input("\nPress Enter to continue...")
    
    def find_duplicates(self) -> None:
        """Find duplicate numbers in the list."""
        self.clear_screen()
        print("\n" + "═" * 50)
        print("🔄 FIND DUPLICATES")
        print("═" * 50)
        
        if not self.current_list:
            print("\n❌ No numbers in the list!")
            print("Please create a list first.")
            input("\nPress Enter to continue...")
            return
        
        # Find duplicates
        seen = set()
        duplicates = {}
        duplicate_positions = {}
        
        for i, num in enumerate(self.current_list, 1):
            if num in seen:
                if num not in duplicates:
                    duplicates[num] = 2  # First duplicate + original
                    # Find original position
                    for j, n in enumerate(self.current_list[:i-1], 1):
                        if n == num:
                            duplicate_positions[num] = [j, i]
                            break
                else:
                    duplicates[num] += 1
                    duplicate_positions[num].append(i)
            else:
                seen.add(num)
        
        print(f"\nAnalyzing {len(self.current_list)} numbers...")
        print(f"Unique numbers: {len(seen)}")
        print(f"Duplicate numbers: {len(duplicates)}")
        
        if duplicates:
            print("\n" + "─" * 40)
            print("📊 DUPLICATE ANALYSIS:")
            print("-" * 40)
            
            # Sort duplicates by frequency
            sorted_duplicates = sorted(duplicates.items(), key=lambda x: x[1], reverse=True)
            
            for num, count in sorted_duplicates:
                positions = duplicate_positions[num]
                print(f"\nNumber: {num}")
                print(f"  Appears {count} times")
                print(f"  Positions: {positions}")
                
                # Calculate percentage
                percentage = (count / len(self.current_list)) * 100
                print(f"  Percentage: {percentage:.1f}%")
            
            # Most common duplicate
            most_common = sorted_duplicates[0]
            print(f"\n🎯 Most common duplicate:")
            print(f"  Number: {most_common[0]}")
            print(f"  Frequency: {most_common[1]} times")
        
        else:
            print("\n✅ No duplicates found! All numbers are unique.")
        
        # Create list without duplicates
        unique_list = list(set(self.current_list))
        print(f"\n" + "─" * 40)
        print("💡 UNIQUE NUMBERS:")
        print("-" * 40)
        print(f"Total unique numbers: {len(unique_list)}")
        
        # Ask if user wants to remove duplicates
        if duplicates:
            choice = input("\nRemove duplicates and keep only unique numbers? (y/N): ").strip().lower()
            if choice == 'y':
                self.current_list = unique_list
                print(f"✅ Duplicates removed! New list has {len(unique_list)} numbers.")
                self.add_to_history("Removed duplicates")
        
        self.add_to_history("Found duplicates" if duplicates else "No duplicates found")
        input("\nPress Enter to continue...")
    
    def filter_numbers(self) -> None:
        """Filter numbers based on criteria."""
        self.clear_screen()
        print("\n" + "═" * 50)
        print("🎯 FILTER NUMBERS")
        print("═" * 50)
        
        if not self.current_list:
            print("\n❌ No numbers in the list!")
            print("Please create a list first.")
            input("\nPress Enter to continue...")
            return
        
        print(f"\nCurrent list: {len(self.current_list)} numbers")
        print("\nFilter Options:")
        print("1. Numbers greater than a value")
        print("2. Numbers less than a value")
        print("3. Numbers between two values")
        print("4. Even numbers only")
        print("5. Odd numbers only")
        print("6. Positive numbers only")
        print("7. Negative numbers only")
        print("8. Whole numbers (integers)")
        print("9. Numbers divisible by X")
        
        try:
            option = int(input("\nChoose option (1-9): ").strip())
            filtered_list = []
            description = ""
            
            if option == 1:
                threshold = float(input("Enter minimum value: ").strip())
                filtered_list = [x for x in self.current_list if x > threshold]
                description = f"greater than {threshold}"
            
            elif option == 2:
                threshold = float(input("Enter maximum value: ").strip())
                filtered_list = [x for x in self.current_list if x < threshold]
                description = f"less than {threshold}"
            
            elif option == 3:
                min_val = float(input("Enter minimum value: ").strip())
                max_val = float(input("Enter maximum value: ").strip())
                filtered_list = [x for x in self.current_list if min_val <= x <= max_val]
                description = f"between {min_val} and {max_val}"
            
            elif option == 4:
                filtered_list = [x for x in self.current_list if x % 2 == 0]
                description = "even numbers"
            
            elif option == 5:
                filtered_list = [x for x in self.current_list if x % 2 == 1]
                description = "odd numbers"
            
            elif option == 6:
                filtered_list = [x for x in self.current_list if x > 0]
                description = "positive numbers"
            
            elif option == 7:
                filtered_list = [x for x in self.current_list if x < 0]
                description = "negative numbers"
            
            elif option == 8:
                filtered_list = [x for x in self.current_list if x == int(x)]
                description = "whole numbers"
            
            elif option == 9:
                divisor = int(input("Enter divisor: ").strip())
                filtered_list = [x for x in self.current_list if x % divisor == 0]
                description = f"divisible by {divisor}"
            
            else:
                print("❌ Invalid option!")
                input("\nPress Enter to continue...")
                return
            
            # Display results
            print(f"\n" + "─" * 40)
            print(f"🎯 FILTER RESULTS ({description}):")
            print("-" * 40)
            
            if filtered_list:
                print(f"Found {len(filtered_list)} numbers ({len(filtered_list)/len(self.current_list)*100:.1f}%)")
                print("\nFiltered numbers:")
                self.display_list_preview(filtered_list)
                
                # Show statistics of filtered list
                if filtered_list:
                    print(f"\n📊 Statistics of filtered numbers:")
                    print(f"Min: {min(filtered_list)}")
                    print(f"Max: {max(filtered_list)}")
                    print(f"Avg: {sum(filtered_list)/len(filtered_list):.2f}")
                    
                    # Ask if user wants to replace current list
                    choice = input("\nReplace current list with filtered numbers? (y/N): ").strip().lower()
                    if choice == 'y':
                        self.current_list = filtered_list
                        print("✅ Current list replaced with filtered numbers!")
                        self.add_to_history(f"Filtered list: {description}")
            else:
                print("❌ No numbers match the filter criteria!")
            
        except ValueError:
            print("❌ Please enter valid numbers!")
        
        input("\nPress Enter to continue...")
    
    def generate_random_list(self) -> None:
        """Generate a random list of numbers."""
        self.clear_screen()
        print("\n" + "═" * 50)
        print("🎲 GENERATE RANDOM LIST")
        print("═" * 50)
        
        print("\nRandom List Options:")
        print("1. Random integers in range")
        print("2. Random floats in range")
        print("3. Random numbers with normal distribution")
        print("4. Random even/odd numbers")
        print("5. Fibonacci-like sequence")
        
        try:
            option = int(input("\nChoose option (1-5): ").strip())
            
            if option == 1:
                count = int(input("How many numbers? (1-1000): ").strip())
                min_val = int(input("Minimum value: ").strip())
                max_val = int(input("Maximum value: ").strip())
                
                if count < 1 or count > 1000:
                    print("❌ Count must be between 1 and 1000")
                    input("\nPress Enter to continue...")
                    return
                
                numbers = [random.randint(min_val, max_val) for _ in range(count)]
                description = f"{count} random integers from {min_val} to {max_val}"
            
            elif option == 2:
                count = int(input("How many numbers? (1-1000): ").strip())
                min_val = float(input("Minimum value: ").strip())
                max_val = float(input("Maximum value: ").strip())
                
                if count < 1 or count > 1000:
                    print("❌ Count must be between 1 and 1000")
                    input("\nPress Enter to continue...")
                    return
                
                numbers = [random.uniform(min_val, max_val) for _ in range(count)]
                description = f"{count} random floats from {min_val} to {max_val}"
            
            elif option == 3:
                count = int(input("How many numbers? (1-1000): ").strip())
                mean = float(input("Mean (average): ").strip())
                std_dev = float(input("Standard deviation: ").strip())
                
                numbers = [random.gauss(mean, std_dev) for _ in range(count)]
                description = f"{count} random numbers with mean={mean}, std={std_dev}"
            
            elif option == 4:
                count = int(input("How many numbers? (1-1000): ").strip())
                min_val = int(input("Minimum value: ").strip())
                max_val = int(input("Maximum value: ").strip())
                even_only = input("Even numbers only? (y/N): ").strip().lower() == 'y'
                
                numbers = []
                while len(numbers) < count:
                    num = random.randint(min_val, max_val)
                    if (even_only and num % 2 == 0) or (not even_only and num % 2 == 1):
                        numbers.append(num)
                
                parity = "even" if even_only else "odd"
                description = f"{count} random {parity} numbers from {min_val} to {max_val}"
            
            elif option == 5:
                count = int(input("How many numbers? (2-50): ").strip())
                if count < 2 or count > 50:
                    print("❌ Count must be between 2 and 50")
                    input("\nPress Enter to continue...")
                    return
                
                # Generate Fibonacci-like sequence with some randomness
                numbers = [0, 1]
                for i in range(2, count):
                    # Add some randomness to Fibonacci
                    next_num = numbers[i-1] + numbers[i-2] + random.randint(-2, 2)
                    numbers.append(next_num)
                
                description = f"Fibonacci-like sequence with {count} numbers"
            
            else:
                print("❌ Invalid option!")
                input("\nPress Enter to continue...")
                return
            
            # Set as current list
            self.current_list = numbers
            print(f"\n✅ Generated {description}")
            print(f"List contains {len(numbers)} numbers")
            
            # Show preview
            self.display_list_preview(numbers)
            
            self.add_to_history(f"Generated random list: {description}")
            
        except ValueError:
            print("❌ Please enter valid numbers!")
        
        input("\nPress Enter to continue...")
    
    def visualize_numbers(self) -> None:
        """Visualize numbers with simple ASCII charts."""
        self.clear_screen()
        print("\n" + "═" * 50)
        print("📊 VISUALIZE NUMBERS")
        print("═" * 50)
        
        if not self.current_list:
            print("\n❌ No numbers in the list!")
            print("Please create a list first.")
            input("\nPress Enter to continue...")
            return
        
        print(f"\nCurrent list: {len(self.current_list)} numbers")
        print("\nVisualization Options:")
        print("1. Simple bar chart (first 20 numbers)")
        print("2. Number distribution")
        print("3. Number line visualization")
        print("4. Histogram")
        
        try:
            option = int(input("\nChoose option (1-4): ").strip())
            
            if option == 1:
                # Simple bar chart for first 20 numbers
                display_list = self.current_list[:20]
                max_val = max(display_list) if display_list else 1
                min_val = min(display_list) if display_list else 0
                
                print("\n" + "─" * 60)
                print("📊 BAR CHART (first 20 numbers):")
                print("-" * 60)
                
                for i, num in enumerate(display_list, 1):
                    # Scale to fit in 50 characters
                    bar_length = int((num - min_val) / (max_val - min_val) * 50) if max_val > min_val else 1
                    bar = "█" * bar_length
                    print(f"{i:2d}. {num:8.2f} |{bar}")
                
                print(f"\nScale: █ = {(max_val - min_val)/50:.2f} units")
            
            elif option == 2:
                # Number distribution
                print("\n" + "─" * 60)
                print("📈 NUMBER DISTRIBUTION:")
                print("-" * 60)
                
                if len(self.current_list) > 0:
                    sorted_nums = sorted(self.current_list)
                    min_val = sorted_nums[0]
                    max_val = sorted_nums[-1]
                    
                    # Create 10 bins
                    num_bins = 10
                    bin_size = (max_val - min_val) / num_bins
                    
                    bins = [0] * num_bins
                    for num in self.current_list:
                        if max_val == min_val:
                            bin_index = 0
                        else:
                            bin_index = min(int((num - min_val) / bin_size), num_bins - 1)
                        bins[bin_index] += 1
                    
                    max_bin = max(bins) if bins else 1
                    
                    print(f"\nRange: {min_val:.2f} to {max_val:.2f}")
                    print(f"Bin size: {bin_size:.2f}")
                    print("\nDistribution:")
                    
                    for i in range(num_bins):
                        bin_start = min_val + i * bin_size
                        bin_end = bin_start + bin_size
                        count = bins[i]
                        percentage = (count / len(self.current_list)) * 100
                        
                        bar_length = int((count / max_bin) * 50)
                        bar = "█" * bar_length
                        
                        print(f"[{bin_start:6.2f}-{bin_end:6.2f}]: {count:3d} ({percentage:5.1f}%) {bar}")
            
            elif option == 3:
                # Number line
                print("\n" + "─" * 60)
                print("📏 NUMBER LINE:")
                print("-" * 60)
                
                if len(self.current_list) > 0:
                    sorted_nums = sorted(self.current_list)
                    min_val = sorted_nums[0]
                    max_val = sorted_nums[-1]
                    
                    # Create a simple number line
                    line_length = 60
                    positions = []
                    
                    for num in sorted_nums:
                        if max_val > min_val:
                            pos = int((num - min_val) / (max_val - min_val) * (line_length - 1))
                        else:
                            pos = line_length // 2
                        positions.append(pos)
                    
                    # Create the line
                    number_line = [' '] * line_length
                    for pos in positions:
                        if 0 <= pos < line_length:
                            number_line[pos] = '•'
                    
                    print(f"\n{' ' * 3}{min_val:8.2f}{' ' * (line_length-16)}{max_val:8.2f}")
                    print(f"  └{''.join(number_line)}┘")
                    
                    # Mark specific values
                    if len(sorted_nums) >= 3:
                        q1 = sorted_nums[len(sorted_nums)//4]
                        median = sorted_nums[len(sorted_nums)//2]
                        q3 = sorted_nums[3*len(sorted_nums)//4]
                        
                        print(f"\nKey positions:")
                        print(f"  Q1: {q1:.2f}")
                        print(f"  Median: {median:.2f}")
                        print(f"  Q3: {q3:.2f}")
            
            elif option == 4:
                # Simple histogram
                print("\n" + "─" * 60)
                print("📋 HISTOGRAM:")
                print("-" * 60)
                
                if len(self.current_list) > 0:
                    # Group numbers by their integer part
                    histogram = {}
                    for num in self.current_list:
                        key = int(num)
                        if key not in histogram:
                            histogram[key] = 0
                        histogram[key] += 1
                    
                    # Sort by key
                    sorted_keys = sorted(histogram.keys())
                    max_count = max(histogram.values())
                    
                    print("\nValue   Count   Bar")
                    print("-" * 40)
                    
                    for key in sorted_keys:
                        count = histogram[key]
                        bar_length = int((count / max_count) * 30)
                        bar = "█" * bar_length
                        print(f"{key:6d}  {count:5d}  {bar}")
            
            else:
                print("❌ Invalid option!")
            
            self.add_to_history("Visualized numbers")
            
        except (ValueError, ZeroDivisionError):
            print("❌ Error in visualization!")
        
        input("\nPress Enter to continue...")
    
    def save_load_lists(self) -> None:
        """Save or load number lists."""
        self.clear_screen()
        print("\n" + "═" * 50)
        print("💾 SAVE/LOAD LISTS")
        print("═" * 50)
        
        print("\nOptions:")
        print("1. Save current list to file")
        print("2. Load list from file")
        print("3. Save multiple lists")
        print("4. Load saved lists")
        
        try:
            option = int(input("\nChoose option (1-4): ").strip())
            
            if option == 1:
                # Save current list
                if not self.current_list:
                    print("❌ No list to save!")
                    input("\nPress Enter to continue...")
                    return
                
                filename = input("Enter filename (default: numbers.json): ").strip()
                if not filename:
                    filename = "numbers.json"
                
                data = {
                    'list': self.current_list,
                    'metadata': {
                        'created': datetime.now().isoformat(),
                        'count': len(self.current_list),
                        'min': min(self.current_list),
                        'max': max(self.current_list),
                        'avg': sum(self.current_list)/len(self.current_list)
                    }
                }
                
                with open(filename, 'w') as f:
                    json.dump(data, f, indent=2)
                
                print(f"✅ Saved {len(self.current_list)} numbers to '{filename}'")
                self.add_to_history(f"Saved list to {filename}")
            
            elif option == 2:
                # Load list from file
                filename = input("Enter filename to load: ").strip()
                
                try:
                    with open(filename, 'r') as f:
                        data = json.load(f)
                    
                    if 'list' in data:
                        self.current_list = data['list']
                        print(f"✅ Loaded {len(self.current_list)} numbers from '{filename}'")
                        
                        if 'metadata' in data:
                            meta = data['metadata']
                            print(f"   Created: {meta.get('created', 'Unknown')}")
                            print(f"   Count: {meta.get('count', 'Unknown')}")
                        
                        self.add_to_history(f"Loaded list from {filename}")
                    else:
                        print("❌ Invalid file format!")
                
                except FileNotFoundError:
                    print(f"❌ File '{filename}' not found!")
                except json.JSONDecodeError:
                    print(f"❌ Invalid JSON file!")
            
            elif option == 3:
                # Save multiple lists
                if not self.number_lists:
                    print("❌ No lists to save!")
                else:
                    filename = input("Enter filename (default: all_lists.json): ").strip()
                    if not filename:
                        filename = "all_lists.json"
                    
                    data = {
                        'lists': self.number_lists,
                        'metadata': {
                            'saved': datetime.now().isoformat(),
                            'total_lists': len(self.number_lists)
                        }
                    }
                    
                    with open(filename, 'w') as f:
                        json.dump(data, f, indent=2)
                    
                    print(f"✅ Saved {len(self.number_lists)} lists to '{filename}'")
            
            elif option == 4:
                # Load saved lists
                filename = input("Enter filename to load: ").strip()
                
                try:
                    with open(filename, 'r') as f:
                        data = json.load(f)
                    
                    if 'lists' in data:
                        self.number_lists = data['lists']
                        print(f"✅ Loaded {len(self.number_lists)} lists from '{filename}'")
                        
                        # Ask which list to set as current
                        if self.number_lists:
                            print(f"\nAvailable lists:")
                            for i, lst in enumerate(self.number_lists, 1):
                                print(f"{i}. List with {len(lst)} numbers")
                            
                            choice = input("\nSelect list number to load as current (or Enter to skip): ").strip()
                            if choice:
                                idx = int(choice) - 1
                                if 0 <= idx < len(self.number_lists):
                                    self.current_list = self.number_lists[idx]
                                    print(f"✅ Loaded list {idx+1} as current")
                    else:
                        print("❌ Invalid file format!")
                
                except FileNotFoundError:
                    print(f"❌ File '{filename}' not found!")
                except json.JSONDecodeError:
                    print(f"❌ Invalid JSON file!")
            
            else:
                print("❌ Invalid option!")
        
        except ValueError:
            print("❌ Please enter a valid number!")
        
        input("\nPress Enter to continue...")
    
    def view_history(self) -> None:
        """View operation history."""
        self.clear_screen()
        print("\n" + "═" * 50)
        print("📜 OPERATION HISTORY")
        print("═" * 50)
        
        if not self.history:
            print("\nNo history yet!")
            print("Perform operations to see history here.")
        else:
            print(f"\nTotal operations: {len(self.history)}")
            print("\n" + "─" * 30)
            
            for i, entry in enumerate(reversed(self.history[-20:]), 1):
                timestamp = entry.get('timestamp', 'Unknown')
                action = entry.get('action', 'Unknown')
                print(f"{i:2d}. {timestamp} - {action}")
        
        print("\n" + "═" * 50)
        input("\nPress Enter to continue...")
    
    def add_to_history(self, action: str) -> None:
        """Add an action to history."""
        entry = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'action': action
        }
        self.history.append(entry)
        
        # Keep only last 100 entries
        if len(self.history) > 100:
            self.history = self.history[-100:]
    
    def run(self) -> None:
        """Main application loop."""
        while True:
            self.clear_screen()
            self.display_banner()
            
            # Show current list info
            if self.current_list:
                print(f"\n📋 Current list: {len(self.current_list)} numbers")
                if len(self.current_list) <= 15:
                    print(f"   Numbers: {self.current_list}")
                else:
                    print(f"   Preview: {self.current_list[:5]} ... {self.current_list[-5:]}")
            else:
                print("\n📋 No current list. Create one first!")
            
            self.display_menu()
            
            choice = self.get_menu_choice()
            
            if choice == '0':  # Exit
                print("\n👋 Thank you for using Number Analyzer!")
                print("Happy analyzing! 🔢")
                break
            
            elif choice == '1':  # Create/Edit list
                self.create_number_list()
            
            elif choice == '2':  # Find min/max
                self.find_min_max()
            
            elif choice == '3':  # Calculate statistics
                self.calculate_statistics()
            
            elif choice == '4':  # Sort numbers
                self.sort_numbers()
            
            elif choice == '5':  # Find duplicates
                self.find_duplicates()
            
            elif choice == '6':  # Filter numbers
                self.filter_numbers()
            
            elif choice == '7':  # Generate random list
                self.generate_random_list()
            
            elif choice == '8':  # Visualize numbers
                self.visualize_numbers()
            
            elif choice == '9':  # Save/Load lists
                self.save_load_lists()
            
            elif choice == '10':  # View history
                self.view_history()


def main():
    """Main function to run the number analyzer."""
    try:
        analyzer = NumberAnalyzer()
        analyzer.run()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! Happy analyzing!")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")
        print("Please try running the application again.")


if __name__ == "__main__":
    main()