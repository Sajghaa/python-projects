def is_even_modulo(number: int) -> bool:
    return number % 2 == 0

def is_even_bitwise(number: int) -> bool:
    return (number & 1) == 0

def is_even_division(number: int) -> bool:
    return (number / 2) == (number // 2)

def get_number_input(prompt: str = "Enter a number: ") -> int:
    while True:
        try:
            user_input = input(prompt)
            
            # Handle empty input
            if not user_input.strip():
                print(" Please enter a value.")
                continue
                
            # Try to convert to integer
            number = int(user_input)
            return number
            
        except ValueError:
            print(" Invalid input! Please enter a valid integer (e.g., 42, -7, 0).")
            if "." in user_input:
                print("💡 Tip: Enter whole numbers only (no decimals).")
            elif any(c.isalpha() for c in user_input):
                print("💡 Tip: Numbers shouldn't contain letters.")

def check_single_number():
    print("\n" + "="*40)
    print("ODD or EVEN CHECKER")
    print("="*40)
    
    number = get_number_input()
    
    result_modulo = is_even_modulo(number)
    result_bitwise = is_even_bitwise(number)
    result_division = is_even_division(number)
    
    if result_modulo == result_bitwise == result_division:
        parity = "EVEN" if result_modulo else "ODD"
        
        print(f"\n Checking number: {number}")
        print(f" Result: {number} is {parity}")
        
        print(f"\n Mathematical Explanation:")
        print(f"  {number} % 2 = {number % 2}")
        print(f"  {number} ÷ 2 = {number / 2}")
        
        if parity == "EVEN":
            print(f" No remainder when divided by 2")
        else:
            print(f"  Remainder of 1 when divided by 2")
            
        binary_rep = bin(number)[2:]  # Remove '0b' prefix
        last_bit = binary_rep[-1] if binary_rep else '0'
        print(f"\n Binary representation: {binary_rep}")
        print(f"   Last bit: {last_bit} ({'0 = even' if last_bit == '0' else '1 = odd'})")
        
    else:
        print(" Error: Different methods gave different results!")
        print(f"Modulo: {result_modulo}, Bitwise: {result_bitwise}, Division: {result_division}")

def check_multiple_numbers():
    """Check multiple numbers in sequence."""
    print("\n" + "="*40)
    print("MULTIPLE NUMBERS CHECK")
    print("="*40)
    
    numbers = []
    
    print("Enter numbers one by one. Type 'done' to finish.")
    
    while True:
        user_input = input("\nEnter a number (or 'done'): ").strip().lower()
        
        if user_input == 'done':
            break
            
        try:
            number = int(user_input)
            numbers.append(number)
            
            # Immediate feedback
            if is_even_modulo(number):
                print(f"  {number}: EVEN ✓")
            else:
                print(f"  {number}: ODD ✗")
                
        except ValueError:
            print(" Please enter a valid integer or 'done'")
    
    if numbers:
        display_statistics(numbers)

def display_statistics(numbers: list):
    """Display statistics about the numbers checked."""
    print("\n" + "="*40)
    print(" STATISTICS")
    print("="*40)
    
    if not numbers:
        print("No numbers were entered.")
        return
    
    # Count evens and odds
    evens = [n for n in numbers if is_even_modulo(n)]
    odds = [n for n in numbers if not is_even_modulo(n)]
    
    print(f"Total numbers checked: {len(numbers)}")
    print(f"Even numbers: {len(evens)} ({len(evens)/len(numbers)*100:.1f}%)")
    print(f"Odd numbers: {len(odds)} ({len(odds)/len(numbers)*100:.1f}%)")
    
    if evens:
        print(f"\nEven numbers found: {sorted(evens)}")
        print(f"Smallest even: {min(evens)}")
        print(f"Largest even: {max(evens)}")
    
    if odds:
        print(f"\nOdd numbers found: {sorted(odds)}")
        print(f"Smallest odd: {min(odds)}")
        print(f"Largest odd: {max(odds)}")

def show_educational_info():
    """Display educational information about odd and even numbers."""
    print("\n" + "="*40)
    print(" EDUCATIONAL INFO")
    print("="*40)
    
    print("\n What are Odd and Even Numbers?")
    print("""
    • EVEN numbers: Can be divided exactly by 2 without remainder
    • ODD numbers: Leave a remainder of 1 when divided by 2
    
    Examples:
      Even: -4, -2, 0, 2, 4, 6, 8, 10
      Odd:  -3, -1, 1, 3, 5, 7, 9
    
    Properties:
      1. Even + Even = Even
      2. Odd + Odd = Even
      3. Even + Odd = Odd
      4. Even × Any = Even
      5. Odd × Odd = Odd
    """)
    
    print("\n Interesting Facts:")
    print("  • 0 is an even number")
    print("  • Negative numbers can be odd or even too")
    print("  • All even numbers end with 0, 2, 4, 6, or 8")
    print("  • All odd numbers end with 1, 3, 5, 7, or 9")

def show_menu():
    """Display the main menu."""
    print("\n" + "="*40)
    print(" ODD/EVEN CHECKER MENU")
    print("="*40)
    print("1. Check a single number")
    print("2. Check multiple numbers")
    print("3. Learn about odd/even numbers")
    print("4. Run tests")
    print("5. Exit")
    print("="*40)

def run_tests():
    """Run automated tests to verify the program works correctly."""
    print("\n" + "="*40)
    print(" RUNNING TESTS")
    print("="*40)
    
    test_cases = [
        (-10, True),   # Negative even
        (-5, False),   # Negative odd
        (0, True),     # Zero is even
        (1, False),    # Positive odd
        (2, True),     # Positive even
        (100, True),   # Large even
        (101, False),  # Large odd
    ]
    
    passed = 0
    failed = 0
    
    for number, expected_even in test_cases:
        result_modulo = is_even_modulo(number)
        result_bitwise = is_even_bitwise(number)
        result_division = is_even_division(number)
        
        if result_modulo == expected_even == result_bitwise == result_division:
            print(f" Test passed: {number} is {'even' if expected_even else 'odd'}")
            passed += 1
        else:
            print(f" Test failed: {number}")
            print(f"   Expected: {'even' if expected_even else 'odd'}")
            print(f"   Got: Modulo={result_modulo}, Bitwise={result_bitwise}, Division={result_division}")
            failed += 1
    
    print(f"\ Test Results: {passed} passed, {failed} failed")
    if failed == 0:
        print(" All tests passed successfully!")

def main():
    """Main program loop."""
    print(" WELCOME TO THE ODD/EVEN CHECKER ")
    
    while True:
        show_menu()
        
        try:
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == '1':
                check_single_number()
            elif choice == '2':
                check_multiple_numbers()
            elif choice == '3':
                show_educational_info()
            elif choice == '4':
                run_tests()
            elif choice == '5':
                print("\n Thank you for using the Odd/Even Checker!")
                print("Goodbye! ")
                break
            else:
                print(" Please enter a number between 1 and 5.")
                
        except KeyboardInterrupt:
            print("\n\n Program interrupted. Exiting...")
            break
        except Exception as e:
            print(f"\n An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()