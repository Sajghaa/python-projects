#!/usr/bin/env python3
"""
Password Generator
A professional, secure password generator with multiple options.
"""

import random
import string
import secrets
import os
import sys
import time
import json
import hashlib
from datetime import datetime
from typing import List, Dict, Optional, Tuple


class PasswordGenerator:
    """Main password generator class with multiple generation strategies."""
    
    # Character sets
    CHARACTER_SETS = {
        'lowercase': string.ascii_lowercase,
        'uppercase': string.ascii_uppercase,
        'digits': string.digits,
        'symbols': '!@#$%^&*()_+-=[]{}|;:,.<>?',
        'similar': 'il1Lo0O',  # Characters that look similar
    }
    
    # Password strength levels
    STRENGTH_LEVELS = {
        'weak': {'length': 8, 'sets': ['lowercase', 'digits']},
        'medium': {'length': 12, 'sets': ['lowercase', 'uppercase', 'digits']},
        'strong': {'length': 16, 'sets': ['lowercase', 'uppercase', 'digits', 'symbols']},
        'very_strong': {'length': 20, 'sets': ['lowercase', 'uppercase', 'digits', 'symbols']},
    }
    
    # Common passwords to avoid (top 20 most common)
    COMMON_PASSWORDS = [
        'password', '123456', '12345678', '1234', 'qwerty',
        '12345', 'dragon', 'baseball', 'football', 'letmein',
        'monkey', 'abc123', '111111', 'mustang', 'access',
        'shadow', 'master', 'michael', 'superman', '696969'
    ]
    
    def __init__(self):
        """Initialize the password generator."""
        self.generated_passwords = []
        self.stats = {
            'total_generated': 0,
            'strength_counts': {'weak': 0, 'medium': 0, 'strong': 0, 'very_strong': 0},
            'history': []
        }
        
    def clear_screen(self) -> None:
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_banner(self) -> None:
        """Display the application banner."""
        banner = """
╔══════════════════════════════════════════════════╗
║            🔐 PASSWORD GENERATOR 🔐              ║
║    Generate secure passwords with ease!          ║
╚══════════════════════════════════════════════════╝
        """
        print(banner)
    
    def display_menu(self) -> None:
        """Display the main menu."""
        print("\n" + "═" * 50)
        print("📋 MAIN MENU")
        print("═" * 50)
        print("1️⃣  Generate password by strength level")
        print("2️⃣  Generate custom password")
        print("3️⃣  Generate multiple passwords")
        print("4️⃣  Generate memorable password")
        print("5️⃣  Password strength checker")
        print("6️⃣  View generated passwords")
        print("7️⃣  View statistics")
        print("8️⃣  Export passwords to file")
        print("9️⃣  Clear history")
        print("0️⃣  Exit")
        print("═" * 50)
    
    def get_menu_choice(self) -> str:
        """Get and validate menu choice."""
        while True:
            try:
                choice = input("\nEnter your choice (0-9): ").strip()
                if choice in [str(i) for i in range(10)]:
                    return choice
                else:
                    print("❌ Please enter a number between 0 and 9")
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                sys.exit(0)
    
    def get_character_set(self, include_lower: bool = True, 
                         include_upper: bool = True, 
                         include_digits: bool = True, 
                         include_symbols: bool = True,
                         exclude_similar: bool = False,
                         exclude_ambiguous: bool = False) -> str:
        """
        Build character set based on options.
        
        Args:
            include_lower: Include lowercase letters
            include_upper: Include uppercase letters
            include_digits: Include digits
            include_symbols: Include symbols
            exclude_similar: Exclude similar looking characters
            exclude_ambiguous: Exclude ambiguous characters
            
        Returns:
            String of characters to use for generation
        """
        chars = ''
        
        if include_lower:
            chars += self.CHARACTER_SETS['lowercase']
        if include_upper:
            chars += self.CHARACTER_SETS['uppercase']
        if include_digits:
            chars += self.CHARACTER_SETS['digits']
        if include_symbols:
            chars += self.CHARACTER_SETS['symbols']
        
        # Remove similar characters if requested
        if exclude_similar:
            for similar_char in self.CHARACTER_SETS['similar']:
                chars = chars.replace(similar_char, '')
        
        # Remove ambiguous characters if requested
        if exclude_ambiguous:
            ambiguous = '"\'`~'
            for amb_char in ambiguous:
                chars = chars.replace(amb_char, '')
        
        if not chars:
            raise ValueError("At least one character set must be selected")
        
        return chars
    
    def generate_by_strength(self, strength_level: str = 'strong') -> str:
        """
        Generate password based on predefined strength level.
        
        Args:
            strength_level: 'weak', 'medium', 'strong', or 'very_strong'
            
        Returns:
            Generated password
        """
        if strength_level not in self.STRENGTH_LEVELS:
            raise ValueError(f"Invalid strength level. Choose from: {list(self.STRENGTH_LEVELS.keys())}")
        
        config = self.STRENGTH_LEVELS[strength_level]
        length = config['length']
        char_sets = config['sets']
        
        # Build character set
        chars = ''
        for char_set in char_sets:
            chars += self.CHARACTER_SETS.get(char_set, '')
        
        # Generate password
        password = ''.join(secrets.choice(chars) for _ in range(length))
        
        # Update statistics
        self.stats['strength_counts'][strength_level] += 1
        self._add_to_history(password, strength_level)
        
        return password
    
    def generate_custom(self, length: int = 16, **options) -> str:
        """
        Generate custom password with specified options.
        
        Args:
            length: Password length
            **options: Character set options
            
        Returns:
            Generated password
        """
        if length < 4:
            raise ValueError("Password length must be at least 4 characters")
        if length > 100:
            raise ValueError("Password length cannot exceed 100 characters")
        
        # Get character set
        chars = self.get_character_set(**options)
        
        # Ensure we have enough characters
        if len(chars) < 4:
            raise ValueError("Character set too small. Include more character types.")
        
        # Generate password
        password = ''.join(secrets.choice(chars) for _ in range(length))
        
        # Determine strength
        strength = self._estimate_strength(password)
        self._add_to_history(password, 'custom')
        self.stats['strength_counts'][strength] += 1
        
        return password
    
    def generate_multiple(self, count: int = 5, strength: str = 'strong') -> List[str]:
        """
        Generate multiple passwords at once.
        
        Args:
            count: Number of passwords to generate
            strength: Strength level
            
        Returns:
            List of generated passwords
        """
        if count < 1:
            raise ValueError("Count must be at least 1")
        if count > 50:
            raise ValueError("Cannot generate more than 50 passwords at once")
        
        passwords = []
        for i in range(count):
            password = self.generate_by_strength(strength)
            passwords.append(password)
        
        return passwords
    
    def generate_memorable(self, word_count: int = 4, separator: str = '-', 
                          capitalize: bool = True, include_number: bool = True) -> str:
        """
        Generate a memorable password using words.
        
        Args:
            word_count: Number of words to use
            separator: Separator between words
            capitalize: Capitalize each word
            include_number: Include a random number
            
        Returns:
            Memorable password
        """
        # Common words list (100 common words)
        words = [
            'apple', 'banana', 'cherry', 'dog', 'elephant', 'flower', 'garden',
            'house', 'island', 'jungle', 'king', 'lion', 'mountain', 'night',
            'ocean', 'piano', 'queen', 'river', 'sun', 'tree', 'umbrella',
            'violet', 'water', 'xylophone', 'yellow', 'zebra', 'air', 'bird',
            'cat', 'desk', 'earth', 'fire', 'grass', 'heart', 'ice', 'jacket',
            'kite', 'light', 'moon', 'note', 'orange', 'paper', 'quiet',
            'rain', 'star', 'time', 'unit', 'voice', 'wind', 'year', 'zone',
            'book', 'chair', 'door', 'edge', 'fish', 'glass', 'hat', 'ink',
            'jump', 'key', 'lamp', 'map', 'nest', 'open', 'park', 'quiz',
            'road', 'ship', 'train', 'user', 'view', 'wall', 'xray', 'yarn'
        ]
        
        # Select random words
        selected_words = secrets.SystemRandom().sample(words, word_count)
        
        # Apply options
        if capitalize:
            selected_words = [word.capitalize() for word in selected_words]
        
        # Add number if requested
        if include_number:
            number = str(secrets.randbelow(100))
            selected_words.append(number)
        
        # Join with separator
        password = separator.join(selected_words)
        
        self._add_to_history(password, 'memorable')
        
        return password
    
    def check_strength(self, password: str) -> Dict[str, any]:
        """
        Check the strength of a password.
        
        Args:
            password: Password to check
            
        Returns:
            Dictionary with strength analysis
        """
        if not password:
            return {'score': 0, 'strength': 'Very Weak', 'issues': ['Password is empty']}
        
        score = 0
        issues = []
        suggestions = []
        
        # Check length
        if len(password) >= 12:
            score += 3
        elif len(password) >= 8:
            score += 2
        elif len(password) >= 6:
            score += 1
        else:
            issues.append("Password is too short (minimum 6 characters)")
        
        # Check character variety
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_symbol = any(not c.isalnum() for c in password)
        
        char_types = sum([has_lower, has_upper, has_digit, has_symbol])
        
        if char_types >= 4:
            score += 3
        elif char_types >= 3:
            score += 2
        elif char_types >= 2:
            score += 1
        else:
            issues.append("Use more character types (lowercase, uppercase, digits, symbols)")
        
        # Check for common patterns
        if password.lower() in self.COMMON_PASSWORDS:
            score = 0
            issues.append("Password is too common")
        
        # Check for sequences
        if any(password[i:i+3].isdigit() and 
               int(password[i]) + 1 == int(password[i+1]) and 
               int(password[i+1]) + 1 == int(password[i+2]) 
               for i in range(len(password)-2)):
            issues.append("Contains sequential numbers")
            score -= 1
        
        # Check for repeated characters
        if any(password[i] == password[i+1] == password[i+2] 
               for i in range(len(password)-2)):
            issues.append("Contains repeated characters")
            score -= 1
        
        # Calculate entropy (rough estimate)
        charset_size = 0
        if has_lower:
            charset_size += 26
        if has_upper:
            charset_size += 26
        if has_digit:
            charset_size += 10
        if has_symbol:
            charset_size += len(self.CHARACTER_SETS['symbols'])
        
        if charset_size > 0:
            entropy = len(password) * (charset_size ** 0.5)
        else:
            entropy = 0
        
        # Determine strength level
        if score >= 5:
            strength = "Very Strong" if entropy > 80 else "Strong"
        elif score >= 3:
            strength = "Medium"
        elif score >= 1:
            strength = "Weak"
        else:
            strength = "Very Weak"
        
        # Add suggestions
        if not has_lower:
            suggestions.append("Add lowercase letters")
        if not has_upper:
            suggestions.append("Add uppercase letters")
        if not has_digit:
            suggestions.append("Add digits")
        if not has_symbol:
            suggestions.append("Add symbols")
        if len(password) < 12:
            suggestions.append("Make password longer (at least 12 characters)")
        
        return {
            'score': min(max(score, 0), 6),
            'strength': strength,
            'length': len(password),
            'entropy': round(entropy, 2),
            'has_lower': has_lower,
            'has_upper': has_upper,
            'has_digit': has_digit,
            'has_symbol': has_symbol,
            'issues': issues,
            'suggestions': suggestions
        }
    
    def _estimate_strength(self, password: str) -> str:
        """Estimate password strength for statistics."""
        analysis = self.check_strength(password)
        score = analysis['score']
        
        if score >= 5:
            return 'strong'
        elif score >= 3:
            return 'medium'
        else:
            return 'weak'
    
    def _add_to_history(self, password: str, password_type: str) -> None:
        """Add password to history."""
        entry = {
            'password': password,
            'type': password_type,
            'timestamp': datetime.now().isoformat(),
            'strength': self._estimate_strength(password)
        }
        self.generated_passwords.append(entry)
        self.stats['history'].append(entry)
        self.stats['total_generated'] += 1
    
    def view_generated(self) -> None:
        """View generated passwords."""
        self.clear_screen()
        print("\n" + "═" * 60)
        print("📋 GENERATED PASSWORDS HISTORY")
        print("═" * 60)
        
        if not self.generated_passwords:
            print("\nNo passwords generated yet!")
            return
        
        for i, entry in enumerate(reversed(self.generated_passwords[-20:]), 1):
            timestamp = datetime.fromisoformat(entry['timestamp']).strftime("%H:%M:%S")
            strength_emoji = "🟢" if entry['strength'] == 'strong' else "🟡" if entry['strength'] == 'medium' else "🔴"
            print(f"\n{i:2d}. {strength_emoji} [{entry['type'].upper():10}] {timestamp}")
            print(f"    {entry['password']}")
        
        print(f"\nTotal generated: {self.stats['total_generated']}")
    
    def view_statistics(self) -> None:
        """View generation statistics."""
        self.clear_screen()
        print("\n" + "═" * 50)
        print("📊 GENERATION STATISTICS")
        print("═" * 50)
        
        print(f"\n📈 Total Passwords Generated: {self.stats['total_generated']}")
        
        if self.stats['total_generated'] > 0:
            print("\n" + "─" * 30)
            print("Strength Distribution:")
            print("─" * 30)
            
            for strength, count in self.stats['strength_counts'].items():
                if count > 0:
                    percentage = (count / self.stats['total_generated']) * 100
                    bar = "█" * int(percentage / 5)
                    print(f"{strength.upper():12} [{bar:20}] {count:3d} ({percentage:.1f}%)")
            
            # Most recent passwords
            print("\n" + "─" * 30)
            print("Recent Passwords:")
            print("─" * 30)
            for entry in self.stats['history'][-5:]:
                time_str = datetime.fromisoformat(entry['timestamp']).strftime("%H:%M")
                print(f"{time_str} - {entry['type']}: {entry['password'][:20]}...")
    
    def export_to_file(self, filename: str = "passwords.txt") -> None:
        """Export generated passwords to a file."""
        if not self.generated_passwords:
            print("❌ No passwords to export!")
            return
        
        try:
            with open(filename, 'w') as f:
                f.write("=" * 60 + "\n")
                f.write("🔐 GENERATED PASSWORDS\n")
                f.write("=" * 60 + "\n\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total: {len(self.generated_passwords)}\n\n")
                
                for i, entry in enumerate(self.generated_passwords, 1):
                    timestamp = datetime.fromisoformat(entry['timestamp']).strftime("%Y-%m-%d %H:%M:%S")
                    f.write(f"{i:3d}. {entry['password']}\n")
                    f.write(f"     Type: {entry['type']}, Strength: {entry['strength']}, Time: {timestamp}\n\n")
                
                f.write("=" * 60 + "\n")
                f.write("⚠️  SECURITY WARNING:\n")
                f.write("1. Store this file securely\n")
                f.write("2. Consider using a password manager\n")
                f.write("3. Never share passwords via email\n")
                f.write("=" * 60 + "\n")
            
            print(f"✅ Passwords exported to '{filename}'")
            print(f"📁 Total passwords saved: {len(self.generated_passwords)}")
            
        except Exception as e:
            print(f"❌ Error exporting passwords: {e}")
    
    def clear_history(self) -> None:
        """Clear password history."""
        confirm = input("\n⚠️  Are you sure you want to clear all history? (y/N): ").lower()
        if confirm == 'y':
            self.generated_passwords.clear()
            self.stats = {
                'total_generated': 0,
                'strength_counts': {'weak': 0, 'medium': 0, 'strong': 0, 'very_strong': 0},
                'history': []
            }
            print("✅ History cleared!")
        else:
            print("❌ Operation cancelled.")
    
    def display_password_with_strength(self, password: str, analysis: Dict = None) -> None:
        """Display password with strength analysis."""
        if analysis is None:
            analysis = self.check_strength(password)
        
        strength_colors = {
            'Very Strong': '🟢',
            'Strong': '🟢',
            'Medium': '🟡',
            'Weak': '🟠',
            'Very Weak': '🔴'
        }
        
        emoji = strength_colors.get(analysis['strength'], '⚪')
        
        print("\n" + "═" * 50)
        print("🔐 GENERATED PASSWORD")
        print("═" * 50)
        print(f"\nPassword:    {password}")
        print(f"Length:      {len(password)} characters")
        print(f"Strength:    {emoji} {analysis['strength']}")
        print(f"Score:       {analysis['score']}/6")
        
        # Display character types
        print("\nCharacter Types:")
        types = []
        if analysis['has_lower']:
            types.append("Lowercase ✓")
        if analysis['has_upper']:
            types.append("Uppercase ✓")
        if analysis['has_digit']:
            types.append("Digits ✓")
        if analysis['has_symbol']:
            types.append("Symbols ✓")
        
        if types:
            print("  " + " | ".join(types))
        
        # Display issues if any
        if analysis['issues']:
            print("\n⚠️  Issues:")
            for issue in analysis['issues']:
                print(f"  • {issue}")
        
        # Display suggestions
        if analysis['suggestions']:
            print("\n💡 Suggestions:")
            for suggestion in analysis['suggestions']:
                print(f"  • {suggestion}")
        
        print("\n" + "═" * 50)
    
    def run_strength_level_menu(self) -> Optional[str]:
        """Run strength level selection menu."""
        self.clear_screen()
        print("\n" + "═" * 50)
        print("📊 SELECT STRENGTH LEVEL")
        print("═" * 50)
        
        levels = {
            '1': ('weak', '🟡 Weak', '8 chars, lowercase & digits'),
            '2': ('medium', '🟠 Medium', '12 chars, lowercase, uppercase & digits'),
            '3': ('strong', '🟢 Strong', '16 chars, all character types'),
            '4': ('very_strong', '🔵 Very Strong', '20 chars, all character types'),
        }
        
        for key, (level, name, desc) in levels.items():
            print(f"{key}. {name:20} - {desc}")
        
        print("\n0. Back to main menu")
        
        while True:
            choice = input("\nSelect strength level (1-4): ").strip()
            if choice == '0':
                return None
            elif choice in levels:
                return levels[choice][0]
            else:
                print("❌ Invalid choice. Please enter 0-4.")
    
    def run_custom_generator_menu(self) -> Optional[str]:
        """Run custom password generator menu."""
        self.clear_screen()
        print("\n" + "═" * 50)
        print("🔧 CUSTOM PASSWORD GENERATOR")
        print("═" * 50)
        
        try:
            # Get length
            while True:
                try:
                    length = input("\nEnter password length (8-32, default 16): ").strip()
                    if not length:
                        length = 16
                        break
                    length = int(length)
                    if 8 <= length <= 32:
                        break
                    else:
                        print("❌ Length must be between 8 and 32")
                except ValueError:
                    print("❌ Please enter a valid number")
            
            # Get character set options
            print("\nSelect character sets to include:")
            
            options = {
                'include_lower': input("Include lowercase letters? (Y/n): ").strip().lower() != 'n',
                'include_upper': input("Include uppercase letters? (Y/n): ").strip().lower() != 'n',
                'include_digits': input("Include digits? (Y/n): ").strip().lower() != 'n',
                'include_symbols': input("Include symbols? (Y/n): ").strip().lower() != 'n',
                'exclude_similar': input("Exclude similar characters (i, l, 1, L, o, 0, O)? (y/N): ").strip().lower() == 'y',
                'exclude_ambiguous': input("Exclude ambiguous characters (\", ', `, ~)? (y/N): ").strip().lower() == 'y',
            }
            
            # Generate password
            password = self.generate_custom(length, **options)
            analysis = self.check_strength(password)
            
            return password
            
        except ValueError as e:
            print(f"❌ Error: {e}")
            input("\nPress Enter to continue...")
            return None
        except KeyboardInterrupt:
            return None
    
    def run_multiple_passwords_menu(self) -> Optional[List[str]]:
        """Run multiple passwords generator menu."""
        self.clear_screen()
        print("\n" + "═" * 50)
        print("🔢 GENERATE MULTIPLE PASSWORDS")
        print("═" * 50)
        
        try:
            # Get count
            while True:
                try:
                    count = input("\nHow many passwords to generate? (1-20, default 5): ").strip()
                    if not count:
                        count = 5
                        break
                    count = int(count)
                    if 1 <= count <= 20:
                        break
                    else:
                        print("❌ Count must be between 1 and 20")
                except ValueError:
                    print("❌ Please enter a valid number")
            
            # Get strength
            strength = self.run_strength_level_menu()
            if strength is None:
                return None
            
            # Generate passwords
            passwords = self.generate_multiple(count, strength)
            
            return passwords
            
        except ValueError as e:
            print(f"❌ Error: {e}")
            input("\nPress Enter to continue...")
            return None
    
    def run_memorable_password_menu(self) -> Optional[str]:
        """Run memorable password generator menu."""
        self.clear_screen()
        print("\n" + "═" * 50)
        print("🧠 MEMORABLE PASSWORD GENERATOR")
        print("═" * 50)
        
        try:
            # Get word count
            while True:
                try:
                    word_count = input("\nNumber of words? (3-6, default 4): ").strip()
                    if not word_count:
                        word_count = 4
                        break
                    word_count = int(word_count)
                    if 3 <= word_count <= 6:
                        break
                    else:
                        print("❌ Word count must be between 3 and 6")
                except ValueError:
                    print("❌ Please enter a valid number")
            
            # Get separator
            separator = input("Separator between words (default '-'): ").strip()
            if not separator:
                separator = '-'
            
            # Get other options
            capitalize = input("Capitalize each word? (Y/n): ").strip().lower() != 'n'
            include_number = input("Include a random number? (Y/n): ").strip().lower() != 'n'
            
            # Generate password
            password = self.generate_memorable(
                word_count=word_count,
                separator=separator,
                capitalize=capitalize,
                include_number=include_number
            )
            
            return password
            
        except Exception as e:
            print(f"❌ Error: {e}")
            input("\nPress Enter to continue...")
            return None
    
    def run_strength_checker_menu(self) -> None:
        """Run password strength checker."""
        self.clear_screen()
        print("\n" + "═" * 50)
        print("🔍 PASSWORD STRENGTH CHECKER")
        print("═" * 50)
        
        password = input("\nEnter password to check (or press Enter to go back): ").strip()
        
        if not password:
            return
        
        # Check strength
        analysis = self.check_strength(password)
        
        self.clear_screen()
        self.display_password_with_strength(password, analysis)
        
        input("\nPress Enter to continue...")
    
    def run(self) -> None:
        """Main application loop."""
        while True:
            self.clear_screen()
            self.display_banner()
            self.display_menu()
            
            choice = self.get_menu_choice()
            
            if choice == '0':  # Exit
                print("\n👋 Thank you for using Password Generator!")
                print("Stay secure! 🔒")
                break
            
            elif choice == '1':  # Generate by strength
                strength = self.run_strength_level_menu()
                if strength:
                    password = self.generate_by_strength(strength)
                    analysis = self.check_strength(password)
                    self.clear_screen()
                    self.display_password_with_strength(password, analysis)
                    input("\nPress Enter to continue...")
            
            elif choice == '2':  # Custom generator
                password = self.run_custom_generator_menu()
                if password:
                    analysis = self.check_strength(password)
                    self.clear_screen()
                    self.display_password_with_strength(password, analysis)
                    input("\nPress Enter to continue...")
            
            elif choice == '3':  # Multiple passwords
                passwords = self.run_multiple_passwords_menu()
                if passwords:
                    self.clear_screen()
                    print("\n" + "═" * 50)
                    print("🔢 MULTIPLE PASSWORDS GENERATED")
                    print("═" * 50)
                    
                    for i, password in enumerate(passwords, 1):
                        strength = self._estimate_strength(password)
                        emoji = "🟢" if strength == 'strong' else "🟡" if strength == 'medium' else "🔴"
                        print(f"\n{i:2d}. {emoji} {password}")
                    
                    print(f"\n✅ Generated {len(passwords)} passwords")
                    input("\nPress Enter to continue...")
            
            elif choice == '4':  # Memorable password
                password = self.run_memorable_password_menu()
                if password:
                    analysis = self.check_strength(password)
                    self.clear_screen()
                    self.display_password_with_strength(password, analysis)
                    input("\nPress Enter to continue...")
            
            elif choice == '5':  # Strength checker
                self.run_strength_checker_menu()
            
            elif choice == '6':  # View generated
                self.view_generated()
                input("\nPress Enter to continue...")
            
            elif choice == '7':  # View statistics
                self.view_statistics()
                input("\nPress Enter to continue...")
            
            elif choice == '8':  # Export to file
                filename = input("\nEnter filename (default: passwords.txt): ").strip()
                if not filename:
                    filename = "passwords.txt"
                self.export_to_file(filename)
                input("\nPress Enter to continue...")
            
            elif choice == '9':  # Clear history
                self.clear_history()
                input("\nPress Enter to continue...")


def main():
    """Main function to run the password generator."""
    try:
        generator = PasswordGenerator()
        generator.run()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! Stay secure!")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")
        print("Please try running the application again.")


if __name__ == "__main__":
    main()