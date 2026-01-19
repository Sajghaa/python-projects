#!/usr/bin/env python3
"""
Currency Converter
A professional currency converter with static exchange rates.
"""

import os
import sys
import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional


class CurrencyConverter:
    """Main currency converter class with static exchange rates."""
    
    # Static exchange rates (as of a recent date)
    # Base currency: USD (1 USD = X foreign currency)
    EXCHANGE_RATES = {
        # Major Currencies
        'USD': 1.00,      # US Dollar (Base)
        'EUR': 0.92,      # Euro
        'GBP': 0.79,      # British Pound
        'JPY': 148.50,    # Japanese Yen
        'CAD': 1.35,      # Canadian Dollar
        'AUD': 1.52,      # Australian Dollar
        'CHF': 0.88,      # Swiss Franc
        
        # Asian Currencies
        'CNY': 7.18,      # Chinese Yuan
        'INR': 83.10,     # Indian Rupee
        'SGD': 1.34,      # Singapore Dollar
        'KRW': 1320.00,   # South Korean Won
        'HKD': 7.82,      # Hong Kong Dollar
        
        # Middle Eastern Currencies
        'AED': 3.67,      # UAE Dirham
        'SAR': 3.75,      # Saudi Riyal
        
        # European Currencies
        'RUB': 92.00,     # Russian Ruble
        'TRY': 28.50,     # Turkish Lira
        'PLN': 4.02,      # Polish Zloty
        
        # African Currencies
        'ZAR': 18.75,     # South African Rand
        'EGP': 30.90,     # Egyptian Pound
        'NGN': 800.00,    # Nigerian Naira
        
        # South American Currencies
        'BRL': 4.95,      # Brazilian Real
        'ARS': 350.00,    # Argentine Peso
        'MXN': 17.25,     # Mexican Peso
    }
    
    # Currency symbols and names
    CURRENCY_INFO = {
        'USD': {'symbol': '$', 'name': 'US Dollar', 'flag': '🇺🇸'},
        'EUR': {'symbol': '€', 'name': 'Euro', 'flag': '🇪🇺'},
        'GBP': {'symbol': '£', 'name': 'British Pound', 'flag': '🇬🇧'},
        'JPY': {'symbol': '¥', 'name': 'Japanese Yen', 'flag': '🇯🇵'},
        'CAD': {'symbol': 'C$', 'name': 'Canadian Dollar', 'flag': '🇨🇦'},
        'AUD': {'symbol': 'A$', 'name': 'Australian Dollar', 'flag': '🇦🇺'},
        'CHF': {'symbol': 'CHF', 'name': 'Swiss Franc', 'flag': '🇨🇭'},
        'CNY': {'symbol': '¥', 'name': 'Chinese Yuan', 'flag': '🇨🇳'},
        'INR': {'symbol': '₹', 'name': 'Indian Rupee', 'flag': '🇮🇳'},
        'SGD': {'symbol': 'S$', 'name': 'Singapore Dollar', 'flag': '🇸🇬'},
        'KRW': {'symbol': '₩', 'name': 'South Korean Won', 'flag': '🇰🇷'},
        'HKD': {'symbol': 'HK$', 'name': 'Hong Kong Dollar', 'flag': '🇭🇰'},
        'AED': {'symbol': 'د.إ', 'name': 'UAE Dirham', 'flag': '🇦🇪'},
        'SAR': {'symbol': '﷼', 'name': 'Saudi Riyal', 'flag': '🇸🇦'},
        'RUB': {'symbol': '₽', 'name': 'Russian Ruble', 'flag': '🇷🇺'},
        'TRY': {'symbol': '₺', 'name': 'Turkish Lira', 'flag': '🇹🇷'},
        'PLN': {'symbol': 'zł', 'name': 'Polish Zloty', 'flag': '🇵🇱'},
        'ZAR': {'symbol': 'R', 'name': 'South African Rand', 'flag': '🇿🇦'},
        'EGP': {'symbol': 'E£', 'name': 'Egyptian Pound', 'flag': '🇪🇬'},
        'NGN': {'symbol': '₦', 'name': 'Nigerian Naira', 'flag': '🇳🇬'},
        'BRL': {'symbol': 'R$', 'name': 'Brazilian Real', 'flag': '🇧🇷'},
        'ARS': {'symbol': '$', 'name': 'Argentine Peso', 'flag': '🇦🇷'},
        'MXN': {'symbol': 'Mex$', 'name': 'Mexican Peso', 'flag': '🇲🇽'},
    }
    
    # Popular currency pairs for quick selection
    POPULAR_PAIRS = [
        ('USD', 'EUR'),
        ('USD', 'GBP'),
        ('USD', 'JPY'),
        ('EUR', 'GBP'),
        ('EUR', 'CHF'),
        ('GBP', 'JPY'),
        ('USD', 'CAD'),
        ('USD', 'AUD'),
        ('EUR', 'USD'),
        ('GBP', 'USD'),
    ]
    
    def __init__(self):
        """Initialize the currency converter."""
        self.conversion_history = []
        self.base_currency = 'USD'
        self.last_updated = '2024-01-15'  # Static date since rates are fixed
        
    def clear_screen(self) -> None:
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_banner(self) -> None:
        """Display the application banner."""
        banner = """
╔══════════════════════════════════════════════════════╗
║               💱 CURRENCY CONVERTER 💱               ║
║      Convert between 25+ currencies instantly!       ║
╚══════════════════════════════════════════════════════╝
        """
        print(banner)
    
    def display_menu(self) -> None:
        """Display the main menu."""
        print("\n" + "═" * 50)
        print("📋 MAIN MENU")
        print("═" * 50)
        print("1️⃣  Convert currency")
        print("2️⃣  View all exchange rates")
        print("3️⃣  View popular currency pairs")
        print("4️⃣  View currency information")
        print("5️⃣  View conversion history")
        print("6️⃣  Clear history")
        print("7️⃣  Save conversion to file")
        print("8️⃣  About / Help")
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
    
    def format_currency(self, amount: float, currency_code: str) -> str:
        """
        Format currency amount with proper symbol and formatting.
        
        Args:
            amount: Amount to format
            currency_code: Currency code (e.g., 'USD', 'EUR')
            
        Returns:
            Formatted currency string
        """
        currency_info = self.CURRENCY_INFO.get(currency_code, {})
        symbol = currency_info.get('symbol', currency_code)
        
        # Different formatting for different currencies
        if currency_code in ['JPY', 'KRW', 'IDR', 'VND']:
            # No decimal places for these currencies
            formatted = f"{symbol}{amount:,.0f}"
        else:
            # Two decimal places for most currencies
            formatted = f"{symbol}{amount:,.2f}"
        
        return formatted
    
    def get_valid_currency_code(self, prompt: str) -> str:
        """
        Get a valid currency code from user.
        
        Args:
            prompt: Prompt to display to user
            
        Returns:
            Valid currency code
        """
        while True:
            code = input(prompt).upper().strip()
            if code in self.EXCHANGE_RATES:
                return code
            else:
                print(f"❌ Invalid currency code. Available codes: {', '.join(sorted(self.EXCHANGE_RATES.keys()))}")
    
    def get_valid_amount(self, prompt: str) -> float:
        """
        Get a valid amount from user.
        
        Args:
            prompt: Prompt to display to user
            
        Returns:
            Valid positive amount
        """
        while True:
            try:
                amount = input(prompt).strip()
                if not amount:
                    continue
                
                amount = float(amount.replace(',', ''))
                
                if amount <= 0:
                    print("❌ Amount must be greater than 0")
                elif amount > 1000000000:  # 1 billion limit
                    print("❌ Amount is too large (max: 1,000,000,000)")
                else:
                    return amount
                    
            except ValueError:
                print("❌ Please enter a valid number")
    
    def convert_currency(self, amount: float, from_currency: str, to_currency: str) -> float:
        """
        Convert amount from one currency to another.
        
        Args:
            amount: Amount to convert
            from_currency: Source currency code
            to_currency: Target currency code
            
        Returns:
            Converted amount
        """
        if from_currency == to_currency:
            return amount
        
        # Convert to USD first, then to target currency
        # Rate stored as: 1 USD = X foreign currency
        amount_in_usd = amount / self.EXCHANGE_RATES[from_currency]
        converted_amount = amount_in_usd * self.EXCHANGE_RATES[to_currency]
        
        return converted_amount
    
    def display_conversion(self, amount: float, from_currency: str, 
                          to_currency: str, result: float) -> None:
        """
        Display conversion results beautifully.
        
        Args:
            amount: Original amount
            from_currency: Source currency
            to_currency: Target currency
            result: Converted amount
        """
        self.clear_screen()
        print("\n" + "═" * 60)
        print("💱 CONVERSION RESULT")
        print("═" * 60)
        
        # Get currency information
        from_info = self.CURRENCY_INFO.get(from_currency, {})
        to_info = self.CURRENCY_INFO.get(to_currency, {})
        
        # Format amounts
        formatted_from = self.format_currency(amount, from_currency)
        formatted_to = self.format_currency(result, to_currency)
        
        # Display conversion
        print(f"\n{from_info.get('flag', '')} {formatted_from} ({from_currency})")
        print("↓")
        print(f"{to_info.get('flag', '')} {formatted_to} ({to_currency})")
        
        # Calculate and display exchange rate
        exchange_rate = self.get_exchange_rate(from_currency, to_currency)
        inverse_rate = self.get_exchange_rate(to_currency, from_currency)
        
        print("\n" + "─" * 40)
        print("📊 EXCHANGE RATES:")
        print(f"1 {from_currency} = {exchange_rate:.6f} {to_currency}")
        print(f"1 {to_currency} = {inverse_rate:.6f} {from_currency}")
        
        # Add to history
        self.add_to_history(amount, from_currency, to_currency, result)
        
        print("\n" + "═" * 60)
    
    def get_exchange_rate(self, from_currency: str, to_currency: str) -> float:
        """
        Get exchange rate between two currencies.
        
        Args:
            from_currency: Source currency
            to_currency: Target currency
            
        Returns:
            Exchange rate (1 from_currency = X to_currency)
        """
        if from_currency == to_currency:
            return 1.0
        
        # Rate stored as: 1 USD = X foreign currency
        from_rate = self.EXCHANGE_RATES[from_currency]
        to_rate = self.EXCHANGE_RATES[to_currency]
        
        # 1 FROM = (1/from_rate) USD = (1/from_rate) * to_rate TO
        return to_rate / from_rate
    
    def add_to_history(self, amount: float, from_currency: str, 
                      to_currency: str, result: float) -> None:
        """Add conversion to history."""
        entry = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'amount': amount,
            'from_currency': from_currency,
            'to_currency': to_currency,
            'result': result,
            'rate': self.get_exchange_rate(from_currency, to_currency)
        }
        self.conversion_history.append(entry)
    
    def run_conversion_menu(self) -> None:
        """Run the currency conversion menu."""
        self.clear_screen()
        print("\n" + "═" * 50)
        print("💱 CURRENCY CONVERSION")
        print("═" * 50)
        
        # Get amount
        amount = self.get_valid_amount("\nEnter amount to convert: ")
        
        # Get source currency
        print("\nAvailable currencies:")
        self.display_currency_list(5)  # Show 5 per line
        
        from_currency = self.get_valid_currency_code("\nEnter source currency code (e.g., USD): ")
        
        # Get target currency
        to_currency = self.get_valid_currency_code("Enter target currency code (e.g., EUR): ")
        
        # Perform conversion
        result = self.convert_currency(amount, from_currency, to_currency)
        
        # Display result
        self.display_conversion(amount, from_currency, to_currency, result)
        
        input("\nPress Enter to continue...")
    
    def display_currency_list(self, items_per_line: int = 5) -> None:
        """
        Display available currencies in a formatted list.
        
        Args:
            items_per_line: Number of currencies per line
        """
        currencies = sorted(self.EXCHANGE_RATES.keys())
        
        for i, currency in enumerate(currencies, 1):
            info = self.CURRENCY_INFO.get(currency, {})
            flag = info.get('flag', '')
            symbol = info.get('symbol', '')
            
            print(f"{flag} {currency} ({symbol})", end="")
            
            if i % items_per_line == 0:
                print()
            else:
                print("  |  ", end="")
        
        if len(currencies) % items_per_line != 0:
            print()
    
    def display_all_rates(self) -> None:
        """Display all exchange rates relative to base currency."""
        self.clear_screen()
        print("\n" + "═" * 70)
        print("📊 ALL EXCHANGE RATES (Base: USD)")
        print("═" * 70)
        print(f"\nLast updated: {self.last_updated}")
        print(f"Base currency: {self.CURRENCY_INFO['USD']['flag']} USD (US Dollar)")
        print("\n" + "─" * 70)
        
        # Sort currencies alphabetically
        sorted_currencies = sorted(self.EXCHANGE_RATES.items(), key=lambda x: x[0])
        
        print(f"\n{'Currency':<10} {'Flag':<5} {'Name':<20} {'Rate (1 USD =)':>20} {'Symbol':<10}")
        print("-" * 70)
        
        for currency_code, rate in sorted_currencies:
            info = self.CURRENCY_INFO.get(currency_code, {})
            flag = info.get('flag', '')
            name = info.get('name', 'Unknown')
            symbol = info.get('symbol', '')
            
            # Format rate based on value
            if rate > 1000:
                formatted_rate = f"{rate:,.0f}"
            elif rate > 100:
                formatted_rate = f"{rate:,.1f}"
            elif rate > 10:
                formatted_rate = f"{rate:,.2f}"
            elif rate > 1:
                formatted_rate = f"{rate:,.3f}"
            else:
                formatted_rate = f"{rate:,.4f}"
            
            print(f"{currency_code:<10} {flag:<5} {name:<20} {formatted_rate:>20} {symbol:<10}")
        
        print("\n" + "═" * 70)
        input("\nPress Enter to continue...")
    
    def display_popular_pairs(self) -> None:
        """Display popular currency pairs with rates."""
        self.clear_screen()
        print("\n" + "═" * 60)
        print("📈 POPULAR CURRENCY PAIRS")
        print("═" * 60)
        print(f"\nLast updated: {self.last_updated}")
        print("\n" + "─" * 60)
        
        print(f"\n{'Pair':<12} {'Rate':<20} {'Inverse':<20}")
        print("-" * 60)
        
        for from_curr, to_curr in self.POPULAR_PAIRS:
            rate = self.get_exchange_rate(from_curr, to_curr)
            inverse_rate = 1 / rate
            
            # Format rates nicely
            if rate > 1000:
                rate_str = f"{rate:,.0f}"
            elif rate > 100:
                rate_str = f"{rate:,.1f}"
            elif rate > 10:
                rate_str = f"{rate:,.2f}"
            elif rate > 1:
                rate_str = f"{rate:,.3f}"
            else:
                rate_str = f"{rate:,.4f}"
            
            if inverse_rate > 1000:
                inverse_str = f"{inverse_rate:,.0f}"
            elif inverse_rate > 100:
                inverse_str = f"{inverse_rate:,.1f}"
            elif inverse_rate > 10:
                inverse_str = f"{inverse_rate:,.2f}"
            elif inverse_rate > 1:
                inverse_str = f"{inverse_rate:,.3f}"
            else:
                inverse_str = f"{inverse_rate:,.4f}"
            
            from_info = self.CURRENCY_INFO.get(from_curr, {})
            to_info = self.CURRENCY_INFO.get(to_curr, {})
            from_flag = from_info.get('flag', '')
            to_flag = to_info.get('flag', '')
            
            print(f"{from_flag}{from_curr}/{to_flag}{to_curr:<8} 1 {from_curr} = {rate_str:<15} {to_curr} 1 {to_curr} = {inverse_str:<15} {from_curr}")
        
        print("\n" + "═" * 60)
        
        # Quick conversion example
        print("\n💡 Quick Example:")
        usd_to_eur = self.convert_currency(100, 'USD', 'EUR')
        formatted_usd = self.format_currency(100, 'USD')
        formatted_eur = self.format_currency(usd_to_eur, 'EUR')
        print(f"{formatted_usd} = {formatted_eur}")
        
        input("\nPress Enter to continue...")
    
    def display_currency_info(self) -> None:
        """Display detailed information about a specific currency."""
        self.clear_screen()
        print("\n" + "═" * 50)
        print("ℹ️  CURRENCY INFORMATION")
        print("═" * 50)
        
        print("\nAvailable currencies:")
        self.display_currency_list(5)
        
        currency_code = self.get_valid_currency_code("\nEnter currency code to view details: ")
        
        self.clear_screen()
        info = self.CURRENCY_INFO.get(currency_code, {})
        rate = self.EXCHANGE_RATES.get(currency_code, 0)
        
        print("\n" + "═" * 60)
        print(f"{info.get('flag', '')} {currency_code} - {info.get('name', 'Unknown')}")
        print("═" * 60)
        
        print(f"\nSymbol: {info.get('symbol', 'N/A')}")
        print(f"Exchange rate: 1 USD = {rate:.4f} {currency_code}")
        print(f"Inverse rate: 1 {currency_code} = {1/rate:.6f} USD")
        
        # Show conversions to other major currencies
        print("\n" + "─" * 40)
        print("💱 CONVERSIONS (1 unit):")
        print("-" * 40)
        
        major_currencies = ['USD', 'EUR', 'GBP', 'JPY', 'CAD', 'AUD', 'CHF']
        for other_currency in major_currencies:
            if other_currency != currency_code:
                rate_to_other = self.get_exchange_rate(currency_code, other_currency)
                other_info = self.CURRENCY_INFO.get(other_currency, {})
                
                if rate_to_other > 1000:
                    rate_str = f"{rate_to_other:,.0f}"
                elif rate_to_other > 100:
                    rate_str = f"{rate_to_other:,.1f}"
                elif rate_to_other > 10:
                    rate_str = f"{rate_to_other:,.2f}"
                elif rate_to_other > 1:
                    rate_str = f"{rate_to_other:,.3f}"
                else:
                    rate_str = f"{rate_to_other:,.4f}"
                
                print(f"1 {currency_code} = {rate_str} {other_info.get('flag', '')}{other_currency}")
        
        print("\n" + "═" * 60)
        input("\nPress Enter to continue...")
    
    def display_conversion_history(self) -> None:
        """Display conversion history."""
        self.clear_screen()
        print("\n" + "═" * 70)
        print("📜 CONVERSION HISTORY")
        print("═" * 70)
        
        if not self.conversion_history:
            print("\nNo conversions yet!")
            print("Convert some currencies to see history here.")
        else:
            print(f"\nTotal conversions: {len(self.conversion_history)}")
            print("\n" + "─" * 70)
            
            # Show last 10 conversions
            for i, entry in enumerate(reversed(self.conversion_history[-10:]), 1):
                from_amount = self.format_currency(entry['amount'], entry['from_currency'])
                to_amount = self.format_currency(entry['result'], entry['to_currency'])
                
                from_info = self.CURRENCY_INFO.get(entry['from_currency'], {})
                to_info = self.CURRENCY_INFO.get(entry['to_currency'], {})
                
                print(f"\n{i:2d}. {entry['timestamp']}")
                print(f"    {from_info.get('flag', '')} {from_amount} → {to_info.get('flag', '')} {to_amount}")
                print(f"    Rate: 1 {entry['from_currency']} = {entry['rate']:.6f} {entry['to_currency']}")
        
        print("\n" + "═" * 70)
        input("\nPress Enter to continue...")
    
    def clear_history(self) -> None:
        """Clear conversion history."""
        confirm = input("\n⚠️  Are you sure you want to clear all history? (y/N): ").lower()
        if confirm == 'y':
            self.conversion_history.clear()
            print("✅ History cleared!")
        else:
            print("❌ Operation cancelled.")
        input("\nPress Enter to continue...")
    
    def save_conversion_to_file(self) -> None:
        """Save conversion history to a JSON file."""
        if not self.conversion_history:
            print("❌ No conversions to save!")
            input("\nPress Enter to continue...")
            return
        
        filename = input("\nEnter filename (default: conversions.json): ").strip()
        if not filename:
            filename = "conversions.json"
        
        try:
            data = {
                'metadata': {
                    'export_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'total_conversions': len(self.conversion_history),
                    'base_currency': self.base_currency,
                    'last_updated': self.last_updated
                },
                'conversions': self.conversion_history
            }
            
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"✅ Saved {len(self.conversion_history)} conversions to '{filename}'")
            
        except Exception as e:
            print(f"❌ Error saving file: {e}")
        
        input("\nPress Enter to continue...")
    
    def display_about(self) -> None:
        """Display about information and help."""
        self.clear_screen()
        print("\n" + "═" * 60)
        print("ℹ️  ABOUT & HELP")
        print("═" * 60)
        
        print("\n📖 ABOUT THIS CONVERTER:")
        print("This is a static currency converter that uses fixed exchange rates.")
        print(f"Last updated: {self.last_updated}")
        print(f"Total currencies supported: {len(self.EXCHANGE_RATES)}")
        
        print("\n" + "─" * 40)
        print("💡 HOW IT WORKS:")
        print("-" * 40)
        print("1. All rates are relative to USD (US Dollar)")
        print("2. Conversion: Amount → USD → Target Currency")
        print("3. Rates are fixed and don't change in real-time")
        print("4. For real-time rates, use financial APIs")
        
        print("\n" + "─" * 40)
        print("⚠️  DISCLAIMER:")
        print("-" * 40)
        print("• Rates are for demonstration purposes only")
        print("• Not suitable for real financial transactions")
        print("• Always verify rates with official sources")
        print("• No warranty of accuracy provided")
        
        print("\n" + "─" * 40)
        print("🔤 CURRENCY CODES:")
        print("-" * 40)
        print("• USD - US Dollar")
        print("• EUR - Euro")
        print("• GBP - British Pound")
        print("• JPY - Japanese Yen")
        print("• CAD - Canadian Dollar")
        print("• More codes available in the converter")
        
        print("\n" + "═" * 60)
        input("\nPress Enter to continue...")
    
    def run(self) -> None:
        """Main application loop."""
        while True:
            self.clear_screen()
            self.display_banner()
            self.display_menu()
            
            choice = self.get_menu_choice()
            
            if choice == '0':  # Exit
                print("\n👋 Thank you for using Currency Converter!")
                print("Happy converting! 💱")
                break
            
            elif choice == '1':  # Convert currency
                self.run_conversion_menu()
            
            elif choice == '2':  # View all rates
                self.display_all_rates()
            
            elif choice == '3':  # View popular pairs
                self.display_popular_pairs()
            
            elif choice == '4':  # View currency info
                self.display_currency_info()
            
            elif choice == '5':  # View history
                self.display_conversion_history()
            
            elif choice == '6':  # Clear history
                self.clear_history()
            
            elif choice == '7':  # Save to file
                self.save_conversion_to_file()
            
            elif choice == '8':  # About/Help
                self.display_about()


def main():
    """Main function to run the currency converter."""
    try:
        converter = CurrencyConverter()
        converter.run()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! Happy converting!")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")
        print("Please try running the application again.")


if __name__ == "__main__":
    main()