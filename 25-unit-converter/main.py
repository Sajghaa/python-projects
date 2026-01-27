#!/usr/bin/env python3
"""
Simple Unit Converter - Length & Weight
Convert between various units of length and weight.
"""

import os
import sys
import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any


class UnitConverter:
    """Main unit converter class for length and weight conversions."""
    
    # Conversion factors relative to base unit (meter for length, gram for weight)
    LENGTH_UNITS = {
        # Metric
        'millimeter': 0.001,
        'centimeter': 0.01,
        'meter': 1.0,
        'kilometer': 1000.0,
        
        # Imperial/US Customary
        'inch': 0.0254,
        'foot': 0.3048,
        'yard': 0.9144,
        'mile': 1609.344,
        
        # Nautical
        'nautical mile': 1852.0,
        
        # Astronomical
        'astronomical unit': 149597870700.0,
        'light year': 9460730472580800.0,
    }
    
    WEIGHT_UNITS = {
        # Metric
        'milligram': 0.001,
        'gram': 1.0,
        'kilogram': 1000.0,
        'metric ton': 1000000.0,
        
        # Imperial/US Customary
        'ounce': 28.3495,
        'pound': 453.592,
        'stone': 6350.29,
        'US ton': 907185.0,
        'UK ton': 1016047.0,
        
        # Asian
        'catty': 604.79,      # Used in some Asian countries
        'tael': 37.7994,      # Traditional Chinese unit
    }
    
    # Unit categories and their display names
    UNIT_CATEGORIES = {
        'length': {
            'name': '📏 Length',
            'units': LENGTH_UNITS,
            'base_unit': 'meter'
        },
        'weight': {
            'name': '⚖️ Weight',
            'units': WEIGHT_UNITS,
            'base_unit': 'gram'
        }
    }
    
    # Unit symbols for display
    UNIT_SYMBOLS = {
        'millimeter': 'mm',
        'centimeter': 'cm',
        'meter': 'm',
        'kilometer': 'km',
        'inch': 'in',
        'foot': 'ft',
        'yard': 'yd',
        'mile': 'mi',
        'nautical mile': 'nmi',
        'astronomical unit': 'AU',
        'light year': 'ly',
        
        'milligram': 'mg',
        'gram': 'g',
        'kilogram': 'kg',
        'metric ton': 't',
        'ounce': 'oz',
        'pound': 'lb',
        'stone': 'st',
        'US ton': 'US ton',
        'UK ton': 'UK ton',
        'catty': 'catty',
        'tael': 'tael',
    }
    
    # Common conversions for quick access
    COMMON_CONVERSIONS = [
        # Length
        ('meter', 'foot'),
        ('kilometer', 'mile'),
        ('centimeter', 'inch'),
        ('mile', 'kilometer'),
        ('inch', 'centimeter'),
        
        # Weight
        ('kilogram', 'pound'),
        ('gram', 'ounce'),
        ('pound', 'kilogram'),
        ('ounce', 'gram'),
        ('kilogram', 'stone'),
    ]
    
    # Unit descriptions for help
    UNIT_DESCRIPTIONS = {
        'millimeter': '1/1000 of a meter, used for small measurements',
        'centimeter': '1/100 of a meter, common for everyday measurements',
        'meter': 'Base unit of length in metric system',
        'kilometer': '1000 meters, used for distances',
        'inch': '1/12 of a foot, US customary unit',
        'foot': '12 inches, equal to 0.3048 meters',
        'yard': '3 feet, equal to 0.9144 meters',
        'mile': '5280 feet, used for road distances',
        'nautical mile': 'Used in aviation and maritime, 1852 meters',
        'astronomical unit': 'Distance from Earth to Sun (~149.6 million km)',
        'light year': 'Distance light travels in one year (~9.46 trillion km)',
        
        'milligram': '1/1000 of a gram, used for small weights',
        'gram': 'Base unit of mass in metric system',
        'kilogram': '1000 grams, standard unit for weight',
        'metric ton': '1000 kilograms',
        'ounce': '1/16 of a pound, US customary unit',
        'pound': '16 ounces, equal to 453.592 grams',
        'stone': '14 pounds, used in UK for body weight',
        'US ton': '2000 pounds (short ton)',
        'UK ton': '2240 pounds (long ton)',
        'catty': 'Traditional Asian unit (~604.79 grams)',
        'tael': 'Traditional Chinese unit (~37.8 grams)',
    }
    
    def __init__(self):
        """Initialize the unit converter."""
        self.conversion_history = []
        self.favorite_conversions = []
        
    def clear_screen(self) -> None:
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_banner(self) -> None:
        """Display the application banner."""
        banner = """
╔══════════════════════════════════════════════════════╗
║              🔄 UNIT CONVERTER 🔄                    ║
║      Convert length & weight units instantly!        ║
╚══════════════════════════════════════════════════════╝
        """
        print(banner)
    
    def display_menu(self) -> None:
        """Display the main menu."""
        print("\n" + "═" * 50)
        print("📋 MAIN MENU")
        print("═" * 50)
        print("1️⃣  Convert units")
        print("2️⃣  Quick conversions")
        print("3️⃣  View all units")
        print("4️⃣  Unit information")
        print("5️⃣  Conversion history")
        print("6️⃣  Favorite conversions")
        print("7️⃣  Save/Load conversions")
        print("8️⃣  About & Help")
        print("0️⃣  Exit")
        print("═" * 50)
    
    def get_menu_choice(self) -> str:
        """Get and validate menu choice."""
        while True:
            try:
                choice = input("\nEnter your choice (0-8): ").strip()
                if choice in [str(i) for i in range(9)]:
                    return choice
                else:
                    print("❌ Please enter a number between 0 and 8")
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                sys.exit(0)
    
    def get_valid_number(self, prompt: str) -> float:
        """
        Get a valid number from user.
        
        Args:
            prompt: Prompt to display
            
        Returns:
            Valid number
        """
        while True:
            try:
                value = input(prompt).strip()
                
                # Handle negative numbers
                if value.startswith('-'):
                    sign = -1
                    value = value[1:]
                else:
                    sign = 1
                
                # Remove commas for thousands
                value = value.replace(',', '')
                
                num = float(value) * sign
                
                # Validate range
                if abs(num) > 1e100:
                    print("❌ Number is too large!")
                else:
                    return num
                    
            except ValueError:
                print("❌ Please enter a valid number")
    
    def get_valid_unit(self, category: str, prompt: str) -> str:
        """
        Get a valid unit from user.
        
        Args:
            category: 'length' or 'weight'
            prompt: Prompt to display
            
        Returns:
            Valid unit name
        """
        units = self.UNIT_CATEGORIES[category]['units']
        
        while True:
            print(f"\nAvailable {category} units:")
            self.display_unit_list(category)
            
            unit = input(prompt).strip().lower()
            
            # Check if unit exists
            for unit_name in units.keys():
                if unit_name.lower() == unit:
                    return unit_name
            
            # Check by symbol
            for unit_name, symbol in self.UNIT_SYMBOLS.items():
                if symbol.lower() == unit and unit_name in units:
                    return unit_name
            
            print(f"❌ Invalid unit! Please enter a valid {category} unit.")
    
    def display_unit_list(self, category: str, items_per_line: int = 4) -> None:
        """
        Display available units for a category.
        
        Args:
            category: 'length' or 'weight'
            items_per_line: Number of units per line
        """
        units = self.UNIT_CATEGORIES[category]['units']
        
        unit_list = list(units.keys())
        for i, unit in enumerate(unit_list, 1):
            symbol = self.UNIT_SYMBOLS.get(unit, unit[:3])
            print(f"  {unit:<20} ({symbol})", end="")
            
            if i % items_per_line == 0:
                print()
            else:
                print("  |  ", end="")
        
        if len(unit_list) % items_per_line != 0:
            print()
    
    def convert_units(self, value: float, from_unit: str, to_unit: str, category: str) -> float:
        """
        Convert value from one unit to another.
        
        Args:
            value: Value to convert
            from_unit: Source unit
            to_unit: Target unit
            category: 'length' or 'weight'
            
        Returns:
            Converted value
        """
        if from_unit == to_unit:
            return value
        
        units = self.UNIT_CATEGORIES[category]['units']
        base_unit = self.UNIT_CATEGORIES[category]['base_unit']
        
        # Convert to base unit first
        value_in_base = value * units[from_unit]
        
        # Convert from base unit to target unit
        converted_value = value_in_base / units[to_unit]
        
        return converted_value
    
    def format_number(self, num: float) -> str:
        """
        Format number for display.
        
        Args:
            num: Number to format
            
        Returns:
            Formatted string
        """
        if num == 0:
            return "0"
        
        abs_num = abs(num)
        
        if abs_num >= 1_000_000_000_000:
            return f"{num / 1_000_000_000_000:.4g} trillion"
        elif abs_num >= 1_000_000_000:
            return f"{num / 1_000_000_000:.4g} billion"
        elif abs_num >= 1_000_000:
            return f"{num / 1_000_000:.4g} million"
        elif abs_num >= 10_000:
            return f"{num:,.0f}"
        elif abs_num >= 1_000:
            return f"{num:,.1f}"
        elif abs_num >= 100:
            return f"{num:,.2f}"
        elif abs_num >= 10:
            return f"{num:,.3f}"
        elif abs_num >= 1:
            return f"{num:,.4f}"
        elif abs_num >= 0.1:
            return f"{num:,.5f}"
        elif abs_num >= 0.01:
            return f"{num:,.6f}"
        elif abs_num >= 0.001:
            return f"{num:,.7f}"
        elif abs_num >= 0.0001:
            return f"{num:,.8f}"
        else:
            return f"{num:.4e}"
    
    def display_conversion(self, value: float, from_unit: str, to_unit: str, 
                          result: float, category: str) -> None:
        """
        Display conversion results.
        
        Args:
            value: Original value
            from_unit: Source unit
            to_unit: Target unit
            result: Converted value
            category: 'length' or 'weight'
        """
        self.clear_screen()
        print("\n" + "═" * 60)
        print("🔄 CONVERSION RESULT")
        print("═" * 60)
        
        from_symbol = self.UNIT_SYMBOLS.get(from_unit, from_unit[:3])
        to_symbol = self.UNIT_SYMBOLS.get(to_unit, to_unit[:3])
        
        # Format numbers nicely
        formatted_value = self.format_number(value)
        formatted_result = self.format_number(result)
        
        # Get category emoji
        category_emoji = "📏" if category == 'length' else "⚖️"
        
        print(f"\n{category_emoji} {category.title()} Conversion")
        print("─" * 40)
        
        print(f"\n{formatted_value} {from_symbol} ({from_unit})")
        print("↓")
        print(f"{formatted_result} {to_symbol} ({to_unit})")
        
        # Calculate and display conversion factors
        units = self.UNIT_CATEGORIES[category]['units']
        
        # 1 from_unit = X to_unit
        from_to_factor = units[from_unit] / units[to_unit]
        
        # 1 to_unit = Y from_unit
        to_from_factor = units[to_unit] / units[from_unit]
        
        print("\n" + "─" * 40)
        print("📊 CONVERSION FACTORS:")
        print(f"1 {from_symbol} = {from_to_factor:.8g} {to_symbol}")
        print(f"1 {to_symbol} = {to_from_factor:.8g} {from_symbol}")
        
        # Add to history
        self.add_to_history(value, from_unit, to_unit, result, category)
        
        print("\n" + "═" * 60)
    
    def add_to_history(self, value: float, from_unit: str, to_unit: str, 
                      result: float, category: str) -> None:
        """Add conversion to history."""
        entry = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'value': value,
            'from_unit': from_unit,
            'to_unit': to_unit,
            'result': result,
            'category': category
        }
        self.conversion_history.append(entry)
        
        # Keep only last 100 entries
        if len(self.conversion_history) > 100:
            self.conversion_history = self.conversion_history[-100:]
    
    def run_conversion_menu(self) -> None:
        """Run the main conversion menu."""
        self.clear_screen()
        print("\n" + "═" * 50)
        print("🔄 CONVERT UNITS")
        print("═" * 50)
        
        print("\nSelect category:")
        print("1. 📏 Length")
        print("2. ⚖️ Weight")
        print("3. ↩️ Back to main menu")
        
        try:
            choice = int(input("\nChoose category (1-3): ").strip())
            
            if choice == 1:
                category = 'length'
            elif choice == 2:
                category = 'weight'
            elif choice == 3:
                return
            else:
                print("❌ Invalid choice!")
                input("\nPress Enter to continue...")
                return
            
            # Get value to convert
            value = self.get_valid_number("\nEnter value to convert: ")
            
            # Get source unit
            from_unit = self.get_valid_unit(category, "\nEnter source unit: ")
            
            # Get target unit
            to_unit = self.get_valid_unit(category, "Enter target unit: ")
            
            # Perform conversion
            result = self.convert_units(value, from_unit, to_unit, category)
            
            # Display result
            self.display_conversion(value, from_unit, to_unit, result, category)
            
        except ValueError:
            print("❌ Please enter a valid number!")
        
        input("\nPress Enter to continue...")
    
    def run_quick_conversions(self) -> None:
        """Run quick conversions for common unit pairs."""
        self.clear_screen()
        print("\n" + "═" * 50)
        print("⚡ QUICK CONVERSIONS")
        print("═" * 50)
        
        # Group common conversions by category
        length_conversions = [c for c in self.COMMON_CONVERSIONS 
                             if c[0] in self.LENGTH_UNITS]
        weight_conversions = [c for c in self.COMMON_CONVERSIONS 
                             if c[0] in self.WEIGHT_UNITS]
        
        print("\n📏 LENGTH CONVERSIONS:")
        print("-" * 40)
        
        for i, (from_unit, to_unit) in enumerate(length_conversions, 1):
            from_symbol = self.UNIT_SYMBOLS.get(from_unit, from_unit[:3])
            to_symbol = self.UNIT_SYMBOLS.get(to_unit, to_unit[:3])
            print(f"{i}. {from_symbol} → {to_symbol}")
        
        print("\n⚖️ WEIGHT CONVERSIONS:")
        print("-" * 40)
        
        for i, (from_unit, to_unit) in enumerate(weight_conversions, 1):
            from_symbol = self.UNIT_SYMBOLS.get(from_unit, from_unit[:3])
            to_symbol = self.UNIT_SYMBOLS.get(to_unit, to_unit[:3])
            print(f"{i + len(length_conversions)}. {from_symbol} → {to_symbol}")
        
        print(f"\n{len(self.COMMON_CONVERSIONS) + 1}. Custom quick conversion")
        print(f"{len(self.COMMON_CONVERSIONS) + 2}. Back to main menu")
        
        try:
            choice = int(input(f"\nSelect conversion (1-{len(self.COMMON_CONVERSIONS) + 2}): ").strip())
            
            if choice == len(self.COMMON_CONVERSIONS) + 2:
                return
            elif choice == len(self.COMMON_CONVERSIONS) + 1:
                self.run_custom_quick_conversion()
                return
            
            if 1 <= choice <= len(self.COMMON_CONVERSIONS):
                from_unit, to_unit = self.COMMON_CONVERSIONS[choice - 1]
                
                # Determine category
                if from_unit in self.LENGTH_UNITS:
                    category = 'length'
                else:
                    category = 'weight'
                
                # Get value
                value = self.get_valid_number(f"\nEnter value in {from_unit}: ")
                
                # Perform conversion
                result = self.convert_units(value, from_unit, to_unit, category)
                
                # Display result
                self.display_conversion(value, from_unit, to_unit, result, category)
            else:
                print("❌ Invalid choice!")
        
        except ValueError:
            print("❌ Please enter a valid number!")
        
        input("\nPress Enter to continue...")
    
    def run_custom_quick_conversion(self) -> None:
        """Run a custom quick conversion."""
        print("\n" + "═" * 50)
        print("🎯 CUSTOM QUICK CONVERSION")
        print("═" * 50)
        
        print("\nSelect category:")
        print("1. 📏 Length")
        print("2. ⚖️ Weight")
        
        try:
            choice = int(input("\nChoose category (1-2): ").strip())
            
            if choice == 1:
                category = 'length'
            elif choice == 2:
                category = 'weight'
            else:
                print("❌ Invalid choice!")
                return
            
            # Get value
            value = self.get_valid_number("\nEnter value to convert: ")
            
            # Get source unit
            from_unit = self.get_valid_unit(category, "Enter source unit: ")
            
            # Show common target units for this source unit
            units = self.UNIT_CATEGORIES[category]['units']
            print(f"\nCommon conversions from {from_unit}:")
            
            # Find 5 most relevant target units
            target_units = []
            
            # Same system first (metric to metric, imperial to imperial)
            from_is_metric = from_unit in ['millimeter', 'centimeter', 'meter', 'kilometer', 
                                          'milligram', 'gram', 'kilogram', 'metric ton']
            
            for unit in units.keys():
                if unit != from_unit:
                    unit_is_metric = unit in ['millimeter', 'centimeter', 'meter', 'kilometer',
                                             'milligram', 'gram', 'kilogram', 'metric ton']
                    
                    if from_is_metric == unit_is_metric:
                        target_units.append(unit)
            
            # If not enough same-system units, add others
            if len(target_units) < 5:
                for unit in units.keys():
                    if unit != from_unit and unit not in target_units:
                        target_units.append(unit)
                    if len(target_units) >= 5:
                        break
            
            # Display options
            for i, unit in enumerate(target_units[:5], 1):
                symbol = self.UNIT_SYMBOLS.get(unit, unit[:3])
                print(f"{i}. {symbol} ({unit})")
            
            print("6. Enter custom target unit")
            
            target_choice = int(input("\nSelect target unit (1-6): ").strip())
            
            if target_choice == 6:
                to_unit = self.get_valid_unit(category, "Enter target unit: ")
            elif 1 <= target_choice <= 5:
                to_unit = target_units[target_choice - 1]
            else:
                print("❌ Invalid choice!")
                return
            
            # Perform conversion
            result = self.convert_units(value, from_unit, to_unit, category)
            
            # Display result
            self.display_conversion(value, from_unit, to_unit, result, category)
            
        except ValueError:
            print("❌ Please enter valid numbers!")
        
        input("\nPress Enter to continue...")
    
    def display_all_units(self) -> None:
        """Display all available units with their conversion factors."""
        self.clear_screen()
        print("\n" + "═" * 70)
        print("📋 ALL AVAILABLE UNITS")
        print("═" * 70)
        
        for category_key, category_info in self.UNIT_CATEGORIES.items():
            print(f"\n{category_info['name']}:")
            print("─" * 70)
            
            units = category_info['units']
            base_unit = category_info['base_unit']
            base_value = units[base_unit]
            
            print(f"\n{'Unit':<25} {'Symbol':<10} {'To Base Factor':<20} {'Description'}")
            print("-" * 70)
            
            for unit_name, factor in units.items():
                symbol = self.UNIT_SYMBOLS.get(unit_name, unit_name[:3])
                description = self.UNIT_DESCRIPTIONS.get(unit_name, "")
                
                # Calculate factor relative to base
                if unit_name == base_unit:
                    factor_str = "1 (base)"
                else:
                    factor_str = f"1 {symbol} = {factor:.8g} {self.UNIT_SYMBOLS.get(base_unit, base_unit[:3])}"
                
                print(f"{unit_name:<25} {symbol:<10} {factor_str:<20} {description[:40]}")
        
        print("\n" + "═" * 70)
        input("\nPress Enter to continue...")
    
    def display_unit_information(self) -> None:
        """Display detailed information about a specific unit."""
        self.clear_screen()
        print("\n" + "═" * 50)
        print("ℹ️  UNIT INFORMATION")
        print("═" * 50)
        
        print("\nSelect category:")
        print("1. 📏 Length units")
        print("2. ⚖️ Weight units")
        
        try:
            choice = int(input("\nChoose category (1-2): ").strip())
            
            if choice == 1:
                category = 'length'
                units = self.LENGTH_UNITS
            elif choice == 2:
                category = 'weight'
                units = self.WEIGHT_UNITS
            else:
                print("❌ Invalid choice!")
                input("\nPress Enter to continue...")
                return
            
            print(f"\nAvailable {category} units:")
            for i, unit in enumerate(units.keys(), 1):
                symbol = self.UNIT_SYMBOLS.get(unit, unit[:3])
                print(f"{i}. {unit} ({symbol})")
            
            unit_choice = int(input(f"\nSelect unit (1-{len(units)}): ").strip())
            
            if 1 <= unit_choice <= len(units):
                unit_name = list(units.keys())[unit_choice - 1]
                self.display_single_unit_info(unit_name, category)
            else:
                print("❌ Invalid choice!")
        
        except ValueError:
            print("❌ Please enter valid numbers!")
        
        input("\nPress Enter to continue...")
    
    def display_single_unit_info(self, unit_name: str, category: str) -> None:
        """Display information about a single unit."""
        self.clear_screen()
        
        symbol = self.UNIT_SYMBOLS.get(unit_name, unit_name[:3])
        description = self.UNIT_DESCRIPTIONS.get(unit_name, "No description available.")
        
        print("\n" + "═" * 60)
        print(f"ℹ️  UNIT INFORMATION: {unit_name.upper()} ({symbol})")
        print("═" * 60)
        
        print(f"\n📖 Description:")
        print(f"   {description}")
        
        units = self.UNIT_CATEGORIES[category]['units']
        base_unit = self.UNIT_CATEGORIES[category]['base_unit']
        base_symbol = self.UNIT_SYMBOLS.get(base_unit, base_unit[:3])
        
        # Conversion factors
        factor = units[unit_name]
        
        print(f"\n📊 Conversion Factors:")
        print(f"   1 {symbol} = {factor:.8g} {base_symbol}")
        print(f"   1 {base_symbol} = {1/factor:.8g} {symbol}")
        
        # Common conversions
        print(f"\n🔄 Common Conversions:")
        
        # Find 5 other units in same category
        other_units = []
        for other_unit in units.keys():
            if other_unit != unit_name:
                other_units.append(other_unit)
                if len(other_units) >= 5:
                    break
        
        for other_unit in other_units:
            other_symbol = self.UNIT_SYMBOLS.get(other_unit, other_unit[:3])
            conversion_factor = factor / units[other_unit]
            
            if conversion_factor >= 1:
                print(f"   1 {symbol} = {conversion_factor:.4g} {other_symbol}")
            else:
                print(f"   1 {other_symbol} = {1/conversion_factor:.4g} {symbol}")
        
        # Real-world examples
        print(f"\n🎯 Real-World Examples:")
        
        if category == 'length':
            if unit_name == 'meter':
                print("   • Height of door: ~2 meters")
                print("   • Olympic swimming pool: 50 meters")
                print("   • Football field: ~100 meters")
            elif unit_name == 'kilometer':
                print("   • Walking distance: 1-5 km")
                print("   • Marathon: 42.195 km")
                print("   • Distance NYC to Boston: ~306 km")
            elif unit_name == 'mile':
                print("   • 5K run: ~3.1 miles")
                print("   • Marathon: 26.2 miles")
                print("   • Distance LA to SF: ~382 miles")
            elif unit_name == 'inch':
                print("   • Smartphone screen: 5-6 inches")
                print("   • Laptop screen: 13-15 inches")
                print("   • TV screen: 32-65 inches")
        
        elif category == 'weight':
            if unit_name == 'kilogram':
                print("   • Bag of sugar: 1 kg")
                print("   • Laptop: 1-3 kg")
                print("   • Newborn baby: 3-4 kg")
            elif unit_name == 'pound':
                print("   • Loaf of bread: ~1 lb")
                print("   • Bag of apples: 5 lbs")
                print("   • Average cat: 8-10 lbs")
            elif unit_name == 'gram':
                print("   • Paperclip: ~1 g")
                print("   • Smartphone: 150-200 g")
                print("   • Chocolate bar: 100 g")
        
        print("\n" + "═" * 60)
    
    def display_conversion_history(self) -> None:
        """Display conversion history."""
        self.clear_screen()
        print("\n" + "═" * 70)
        print("📜 CONVERSION HISTORY")
        print("═" * 70)
        
        if not self.conversion_history:
            print("\nNo conversions yet!")
            print("Convert some units to see history here.")
        else:
            print(f"\nTotal conversions: {len(self.conversion_history)}")
            print("\n" + "─" * 70)
            
            # Show last 15 conversions
            for i, entry in enumerate(reversed(self.conversion_history[-15:]), 1):
                timestamp = entry['timestamp']
                value = self.format_number(entry['value'])
                result = self.format_number(entry['result'])
                
                from_symbol = self.UNIT_SYMBOLS.get(entry['from_unit'], entry['from_unit'][:3])
                to_symbol = self.UNIT_SYMBOLS.get(entry['to_unit'], entry['to_unit'][:3])
                
                category_emoji = "📏" if entry['category'] == 'length' else "⚖️"
                
                print(f"{i:2d}. {timestamp} {category_emoji}")
                print(f"    {value} {from_symbol} → {result} {to_symbol}")
                print()
            
            # Statistics
            print("\n" + "─" * 40)
            print("📊 HISTORY STATISTICS:")
            print("-" * 40)
            
            length_count = sum(1 for entry in self.conversion_history 
                             if entry['category'] == 'length')
            weight_count = sum(1 for entry in self.conversion_history 
                             if entry['category'] == 'weight')
            
            print(f"Length conversions:  {length_count}")
            print(f"Weight conversions:  {weight_count}")
            
            if self.conversion_history:
                # Most common conversion
                conversions_by_type = {}
                for entry in self.conversion_history:
                    key = f"{entry['from_unit']}→{entry['to_unit']}"
                    if key not in conversions_by_type:
                        conversions_by_type[key] = 0
                    conversions_by_type[key] += 1
                
                if conversions_by_type:
                    most_common = max(conversions_by_type.items(), key=lambda x: x[1])
                    print(f"Most common: {most_common[0]} ({most_common[1]} times)")
        
        print("\n" + "═" * 70)
        
        # Options
        if self.conversion_history:
            print("\nOptions:")
            print("1. Clear history")
            print("2. Export history to file")
            print("3. Back to menu")
            
            try:
                choice = int(input("\nChoose option (1-3): ").strip())
                
                if choice == 1:
                    confirm = input("Are you sure you want to clear all history? (y/N): ").lower()
                    if confirm == 'y':
                        self.conversion_history.clear()
                        print("✅ History cleared!")
                
                elif choice == 2:
                    self.export_history_to_file()
                
            except ValueError:
                pass
        
        input("\nPress Enter to continue...")
    
    def manage_favorite_conversions(self) -> None:
        """Manage favorite conversions."""
        self.clear_screen()
        print("\n" + "═" * 50)
        print("⭐ FAVORITE CONVERSIONS")
        print("═" * 50)
        
        if not self.favorite_conversions:
            print("\nNo favorite conversions yet!")
            print("Add some conversions to favorites for quick access.")
        else:
            print(f"\nYou have {len(self.favorite_conversions)} favorite conversions:")
            print("\n" + "─" * 40)
            
            for i, fav in enumerate(self.favorite_conversions, 1):
                from_symbol = self.UNIT_SYMBOLS.get(fav['from_unit'], fav['from_unit'][:3])
                to_symbol = self.UNIT_SYMBOLS.get(fav['to_unit'], fav['to_unit'][:3])
                category_emoji = "📏" if fav['category'] == 'length' else "⚖️"
                
                print(f"{i}. {category_emoji} {fav['value']} {from_symbol} → {to_symbol}")
                if 'name' in fav:
                    print(f"   Name: {fav['name']}")
                print()
        
        print("\nOptions:")
        print("1. Add current conversion to favorites")
        print("2. Use a favorite conversion")
        print("3. Remove a favorite")
        print("4. Clear all favorites")
        print("5. Back to menu")
        
        try:
            choice = int(input("\nChoose option (1-5): ").strip())
            
            if choice == 1:
                self.add_to_favorites()
            elif choice == 2:
                self.use_favorite_conversion()
            elif choice == 3:
                self.remove_favorite()
            elif choice == 4:
                self.clear_favorites()
            
        except ValueError:
            print("❌ Please enter a valid number!")
        
        input("\nPress Enter to continue...")
    
    def add_to_favorites(self) -> None:
        """Add the last conversion to favorites."""
        if not self.conversion_history:
            print("❌ No recent conversions to add to favorites!")
            return
        
        last_conversion = self.conversion_history[-1]
        
        # Check if already in favorites
        for fav in self.favorite_conversions:
            if (fav['from_unit'] == last_conversion['from_unit'] and
                fav['to_unit'] == last_conversion['to_unit']):
                print("❌ This conversion is already in favorites!")
                return
        
        # Ask for a name
        name = input("Enter a name for this favorite (or press Enter to skip): ").strip()
        
        favorite_entry = {
            'from_unit': last_conversion['from_unit'],
            'to_unit': last_conversion['to_unit'],
            'category': last_conversion['category'],
            'value': 1.0,  # Default value
            'added': datetime.now().strftime("%Y-%m-%d")
        }
        
        if name:
            favorite_entry['name'] = name
        
        self.favorite_conversions.append(favorite_entry)
        print("✅ Added to favorites!")
    
    def use_favorite_conversion(self) -> None:
        """Use a favorite conversion."""
        if not self.favorite_conversions:
            print("❌ No favorite conversions!")
            return
        
        print("\nSelect a favorite conversion:")
        for i, fav in enumerate(self.favorite_conversions, 1):
            from_symbol = self.UNIT_SYMBOLS.get(fav['from_unit'], fav['from_unit'][:3])
            to_symbol = self.UNIT_SYMBOLS.get(fav['to_unit'], fav['to_unit'][:3])
            
            display_name = fav.get('name', f"{from_symbol} → {to_symbol}")
            print(f"{i}. {display_name}")
        
        try:
            choice = int(input(f"\nSelect favorite (1-{len(self.favorite_conversions)}): ").strip())
            
            if 1 <= choice <= len(self.favorite_conversions):
                fav = self.favorite_conversions[choice - 1]
                
                # Get value
                from_symbol = self.UNIT_SYMBOLS.get(fav['from_unit'], fav['from_unit'][:3])
                value = self.get_valid_number(f"\nEnter value in {from_symbol}: ")
                
                # Perform conversion
                result = self.convert_units(value, fav['from_unit'], fav['to_unit'], fav['category'])
                
                # Display result
                self.display_conversion(value, fav['from_unit'], fav['to_unit'], result, fav['category'])
            else:
                print("❌ Invalid choice!")
        
        except ValueError:
            print("❌ Please enter a valid number!")
    
    def remove_favorite(self) -> None:
        """Remove a favorite conversion."""
        if not self.favorite_conversions:
            print("❌ No favorite conversions to remove!")
            return
        
        print("\nSelect a favorite to remove:")
        for i, fav in enumerate(self.favorite_conversions, 1):
            from_symbol = self.UNIT_SYMBOLS.get(fav['from_unit'], fav['from_unit'][:3])
            to_symbol = self.UNIT_SYMBOLS.get(fav['to_unit'], fav['to_unit'][:3])
            
            display_name = fav.get('name', f"{from_symbol} → {to_symbol}")
            print(f"{i}. {display_name}")
        
        try:
            choice = int(input(f"\nSelect favorite to remove (1-{len(self.favorite_conversions)}): ").strip())
            
            if 1 <= choice <= len(self.favorite_conversions):
                removed = self.favorite_conversions.pop(choice - 1)
                print("✅ Favorite removed!")
            else:
                print("❌ Invalid choice!")
        
        except ValueError:
            print("❌ Please enter a valid number!")
    
    def clear_favorites(self) -> None:
        """Clear all favorite conversions."""
        if not self.favorite_conversions:
            print("❌ No favorite conversions to clear!")
            return
        
        confirm = input("Are you sure you want to clear all favorites? (y/N): ").lower()
        if confirm == 'y':
            self.favorite_conversions.clear()
            print("✅ All favorites cleared!")
    
    def save_load_conversions(self) -> None:
        """Save or load conversions."""
        self.clear_screen()
        print("\n" + "═" * 50)
        print("💾 SAVE/LOAD CONVERSIONS")
        print("═" * 50)
        
        print("\nOptions:")
        print("1. Save conversion history to file")
        print("2. Load conversion history from file")
        print("3. Save favorite conversions")
        print("4. Load favorite conversions")
        print("5. Back to menu")
        
        try:
            choice = int(input("\nChoose option (1-5): ").strip())
            
            if choice == 1:
                self.export_history_to_file()
            elif choice == 2:
                self.import_history_from_file()
            elif choice == 3:
                self.export_favorites_to_file()
            elif choice == 4:
                self.import_favorites_from_file()
            
        except ValueError:
            print("❌ Please enter a valid number!")
        
        input("\nPress Enter to continue...")
    
    def export_history_to_file(self) -> None:
        """Export conversion history to a JSON file."""
        if not self.conversion_history:
            print("❌ No history to export!")
            return
        
        filename = input("\nEnter filename (default: conversions_history.json): ").strip()
        if not filename:
            filename = "conversions_history.json"
        
        try:
            data = {
                'metadata': {
                    'export_date': datetime.now().isoformat(),
                    'total_conversions': len(self.conversion_history)
                },
                'conversions': self.conversion_history
            }
            
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"✅ Saved {len(self.conversion_history)} conversions to '{filename}'")
            
        except Exception as e:
            print(f"❌ Error saving file: {e}")
    
    def import_history_from_file(self) -> None:
        """Import conversion history from a JSON file."""
        filename = input("\nEnter filename to import: ").strip()
        
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            if 'conversions' in data:
                imported = data['conversions']
                self.conversion_history.extend(imported)
                print(f"✅ Imported {len(imported)} conversions from '{filename}'")
                
                # Keep only last 100 entries
                if len(self.conversion_history) > 100:
                    self.conversion_history = self.conversion_history[-100:]
            else:
                print("❌ Invalid file format!")
        
        except FileNotFoundError:
            print(f"❌ File '{filename}' not found!")
        except json.JSONDecodeError:
            print(f"❌ Invalid JSON file!")
        except Exception as e:
            print(f"❌ Error loading file: {e}")
    
    def export_favorites_to_file(self) -> None:
        """Export favorite conversions to a JSON file."""
        if not self.favorite_conversions:
            print("❌ No favorites to export!")
            return
        
        filename = input("\nEnter filename (default: favorites.json): ").strip()
        if not filename:
            filename = "favorites.json"
        
        try:
            data = {
                'metadata': {
                    'export_date': datetime.now().isoformat(),
                    'total_favorites': len(self.favorite_conversions)
                },
                'favorites': self.favorite_conversions
            }
            
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"✅ Saved {len(self.favorite_conversions)} favorites to '{filename}'")
            
        except Exception as e:
            print(f"❌ Error saving file: {e}")
    
    def import_favorites_from_file(self) -> None:
        """Import favorite conversions from a JSON file."""
        filename = input("\nEnter filename to import: ").strip()
        
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            if 'favorites' in data:
                imported = data['favorites']
                self.favorite_conversions.extend(imported)
                print(f"✅ Imported {len(imported)} favorites from '{filename}'")
            else:
                print("❌ Invalid file format!")
        
        except FileNotFoundError:
            print(f"❌ File '{filename}' not found!")
        except json.JSONDecodeError:
            print(f"❌ Invalid JSON file!")
        except Exception as e:
            print(f"❌ Error loading file: {e}")
    
    def display_about(self) -> None:
        """Display about information and help."""
        self.clear_screen()
        print("\n" + "═" * 60)
        print("ℹ️  ABOUT & HELP")
        print("═" * 60)
        
        print("\n📖 ABOUT THIS CONVERTER:")
        print("A simple yet powerful unit converter for length and weight.")
        print("Supports metric, imperial, and other measurement systems.")
        
        print("\n" + "─" * 40)
        print("🎯 HOW TO USE:")
        print("-" * 40)
        print("1. Select 'Convert units' from main menu")
        print("2. Choose length or weight category")
        print("3. Enter the value to convert")
        print("4. Select source and target units")
        print("5. View the conversion result")
        
        print("\n" + "─" * 40)
        print("📊 SUPPORTED UNITS:")
        print("-" * 40)
        
        print("📏 LENGTH (13 units):")
        print("  Metric: mm, cm, m, km")
        print("  Imperial: in, ft, yd, mi")
        print("  Other: nautical mile, AU, light year")
        
        print("\n⚖️ WEIGHT (11 units):")
        print("  Metric: mg, g, kg, metric ton")
        print("  Imperial: oz, lb, stone, US ton, UK ton")
        print("  Asian: catty, tael")
        
        print("\n" + "─" * 40)
        print("🔧 FEATURES:")
        print("-" * 40)
        print("• Accurate conversion between all units")
        print("• Quick access to common conversions")
        print("• Conversion history tracking")
        print("• Favorite conversions")
        print("• Save/load functionality")
        print("• Unit information and descriptions")
        
        print("\n" + "─" * 40)
        print("📐 CONVERSION FORMULA:")
        print("-" * 40)
        print("All units are converted through base units:")
        print("• Length: meter (m)")
        print("• Weight: gram (g)")
        print("\nFormula:")
        print("target_value = (source_value × source_to_base) ÷ target_to_base")
        
        print("\n" + "─" * 40)
        print("⚠️  IMPORTANT NOTES:")
        print("-" * 40)
        print("• Weight conversions assume standard gravity")
        print("• Some units (stone, catty) are region-specific")
        print("• Astronomical units are for reference only")
        print("• Results are rounded for display purposes")
        
        print("\n" + "═" * 60)
        input("\nPress Enter to continue...")
    
    def run(self) -> None:
        """Main application loop."""
        while True:
            self.clear_screen()
            self.display_banner()
            
            # Show quick stats
            if self.conversion_history:
                recent = len(self.conversion_history)
                print(f"\n📊 Recent conversions: {recent}")
                
                if recent > 0:
                    last = self.conversion_history[-1]
                    from_symbol = self.UNIT_SYMBOLS.get(last['from_unit'], last['from_unit'][:3])
                    to_symbol = self.UNIT_SYMBOLS.get(last['to_unit'], last['to_unit'][:3])
                    print(f"   Last: {last['value']} {from_symbol} → {last['result']} {to_symbol}")
            
            self.display_menu()
            
            choice = self.get_menu_choice()
            
            if choice == '0':  # Exit
                print("\n👋 Thank you for using Unit Converter!")
                print("Happy converting! 🔄")
                break
            
            elif choice == '1':  # Convert units
                self.run_conversion_menu()
            
            elif choice == '2':  # Quick conversions
                self.run_quick_conversions()
            
            elif choice == '3':  # View all units
                self.display_all_units()
            
            elif choice == '4':  # Unit information
                self.display_unit_information()
            
            elif choice == '5':  # Conversion history
                self.display_conversion_history()
            
            elif choice == '6':  # Favorite conversions
                self.manage_favorite_conversions()
            
            elif choice == '7':  # Save/Load
                self.save_load_conversions()
            
            elif choice == '8':  # About & Help
                self.display_about()


def main():
    """Main function to run the unit converter."""
    try:
        converter = UnitConverter()
        converter.run()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! Happy converting!")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")
        print("Please try running the application again.")


if __name__ == "__main__":
    main()