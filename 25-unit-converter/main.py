#!/usr/bin/env python3
"""
Enhanced Unit Converter with Smart Input Parsing
"""

import os
import sys

class SmartUnitConverter:
    """Unit converter with intelligent input parsing."""
    
    # Conversion factors
    UNITS = {
        'length': {
            'mm': 0.001, 'cm': 0.01, 'm': 1.0, 'km': 1000.0,
            'in': 0.0254, 'ft': 0.3048, 'yd': 0.9144, 'mi': 1609.344,
        },
        'weight': {
            'mg': 0.001, 'g': 1.0, 'kg': 1000.0, 't': 1000000.0,
            'oz': 28.3495, 'lb': 453.592, 'st': 6350.29,
        }
    }
    
    # Unit aliases for flexible input
    ALIASES = {
        'mm': ['millimeter', 'millimeters', 'milimeter'],
        'cm': ['centimeter', 'centimeters', 'centimetre', 'centimetres'],
        'm': ['meter', 'meters', 'metre', 'metres'],
        'km': ['kilometer', 'kilometers', 'kilometre', 'kilometres'],
        'in': ['inch', 'inches', '"'],
        'ft': ['foot', 'feet', "'"],
        'yd': ['yard', 'yards'],
        'mi': ['mile', 'miles'],
        
        'mg': ['milligram', 'milligrams'],
        'g': ['gram', 'grams', 'gramme', 'grammes'],
        'kg': ['kilogram', 'kilograms', 'kilo', 'kilos'],
        't': ['ton', 'tons', 'tonne', 'tonnes', 'metric ton'],
        'oz': ['ounce', 'ounces'],
        'lb': ['pound', 'pounds', 'lbs'],
        'st': ['stone', 'stones'],
    }
    
    def parse_input(self, input_str: str):
        """Parse input like '10km', '5.5 lb', '3.14 meters'."""
        input_str = input_str.strip()
        
        if not input_str:
            return None, None
        
        # Find where the number ends
        i = 0
        found_digit = False
        found_decimal = False
        
        while i < len(input_str):
            char = input_str[i]
            
            # Check if character is part of a number
            if char.isdigit():
                found_digit = True
                i += 1
            elif char == '.' and not found_decimal:
                found_decimal = True
                i += 1
            elif char == '-' and i == 0:  # Negative sign at start
                i += 1
            elif char == '+' and i == 0:  # Positive sign at start
                i += 1
            elif char == 'e' or char == 'E':  # Scientific notation
                # Check if next char is +, -, or digit
                if i + 1 < len(input_str) and (input_str[i+1].isdigit() or 
                                               input_str[i+1] in '+-'):
                    i += 2  # Skip 'e' and the sign
                    # Skip digits after exponent
                    while i < len(input_str) and input_str[i].isdigit():
                        i += 1
                else:
                    break
            else:
                break
        
        # Extract number and unit
        number_part = input_str[:i].strip()
        unit_part = input_str[i:].strip()
        
        if not number_part:
            return None, None
        
        try:
            value = float(number_part.replace(',', ''))
        except ValueError:
            return None, None
        
        # Normalize unit
        if unit_part:
            unit = self.normalize_unit(unit_part)
            if unit:
                return value, unit
        
        return value, None
    
    def normalize_unit(self, unit_str: str) -> str:
        """Convert any unit input to standard symbol."""
        unit_str = unit_str.lower().strip(' .,;:')
        
        # Check direct match with symbols
        for symbol in self.UNITS['length']:
            if unit_str == symbol:
                return symbol
        
        for symbol in self.UNITS['weight']:
            if unit_str == symbol:
                return symbol
        
        # Check aliases
        for symbol, aliases in self.ALIASES.items():
            if unit_str in aliases:
                return symbol
        
        # Try partial matches
        for symbol, aliases in self.ALIASES.items():
            for alias in aliases:
                if alias.startswith(unit_str) or unit_str.startswith(alias):
                    return symbol
        
        return ""
    
    def detect_category(self, unit: str) -> str:
        """Detect if unit is length or weight."""
        if unit in self.UNITS['length']:
            return 'length'
        elif unit in self.UNITS['weight']:
            return 'weight'
        return ''
    
    def convert(self, value: float, from_unit: str, to_unit: str, category: str) -> float:
        """Convert between units."""
        if from_unit == to_unit:
            return value
        
        factor_from = self.UNITS[category][from_unit]
        factor_to = self.UNITS[category][to_unit]
        
        return value * factor_from / factor_to
    
    def get_unit_input(self, prompt: str, category: str = '') -> str:
        """Get unit input from user with suggestions."""
        while True:
            user_input = input(prompt).strip().lower()
            
            if not user_input:
                print("❌ Please enter a unit")
                continue
            
            # Normalize the unit
            unit = self.normalize_unit(user_input)
            
            if not unit:
                print(f"❌ Unknown unit: '{user_input}'")
                
                # Show suggestions
                if category:
                    print(f"   Available {category} units:")
                    symbols = list(self.UNITS[category].keys())
                    print(f"   {', '.join(symbols)}")
                else:
                    print("   Available units:")
                    all_units = list(self.UNITS['length'].keys()) + list(self.UNITS['weight'].keys())
                    print(f"   {', '.join(all_units[:10])}...")
                
                continue
            
            # If category specified, verify unit belongs to it
            if category:
                detected = self.detect_category(unit)
                if detected != category:
                    print(f"❌ '{unit}' is a {detected} unit, not {category}")
                    continue
            
            return unit
    
    def run(self):
        """Main application loop."""
        print("=" * 50)
        print("🔄 ENHANCED UNIT CONVERTER")
        print("=" * 50)
        print("\n💡 You can enter values like:")
        print("   • '10km' or '10 km'")
        print("   • '5.5 lb' or '5.5 pounds'")
        print("   • '3.14m' or '3.14 meters'")
        print("   • Or just the number and choose units separately")
        
        while True:
            print("\n" + "-" * 40)
            print("1. Convert length")
            print("2. Convert weight")
            print("3. Exit")
            
            choice = input("\nSelect option (1-3): ").strip()
            
            if choice == '3':
                print("\n👋 Goodbye!")
                break
            
            if choice == '1':
                category = 'length'
                category_name = 'Length'
            elif choice == '2':
                category = 'weight'
                category_name = 'Weight'
            else:
                print("❌ Invalid choice")
                continue
            
            print(f"\n📏 {category_name.upper()} CONVERSION")
            print("-" * 30)
            
            # Get input value
            while True:
                input_str = input(f"\nEnter value (e.g., '10km', '5.5', '100 {category}'): ").strip()
                
                value, detected_unit = self.parse_input(input_str)
                
                if value is None:
                    print("❌ Could not parse input. Please try again.")
                    continue
                
                # If unit was detected
                if detected_unit:
                    # Verify it's the right category
                    detected_category = self.detect_category(detected_unit)
                    if detected_category == category:
                        from_unit = detected_unit
                        print(f"✅ Detected: {value} {from_unit}")
                        break
                    else:
                        print(f"⚠️  '{detected_unit}' is a {detected_category} unit, not {category}")
                        # Continue to manual unit selection
                
                # Get source unit
                print(f"\nSelect source unit for {value}:")
                from_unit = self.get_unit_input("Source unit: ", category)
                break
            
            # Get target unit
            print(f"\nConvert {value} {from_unit} to:")
            to_unit = self.get_unit_input("Target unit: ", category)
            
            # Perform conversion
            result = self.convert(value, from_unit, to_unit, category)
            
            # Display result
            print("\n" + "=" * 40)
            print("✅ CONVERSION RESULT")
            print("=" * 40)
            print(f"{value} {from_unit} = {result:.6g} {to_unit}")
            
            # Show conversion factor
            factor = self.UNITS[category][from_unit] / self.UNITS[category][to_unit]
            print(f"\nConversion factor: 1 {from_unit} = {factor:.6g} {to_unit}")
            print("=" * 40)


def main():
    """Main function."""
    try:
        converter = SmartUnitConverter()
        converter.run()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()