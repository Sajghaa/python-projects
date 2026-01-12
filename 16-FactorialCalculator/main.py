import math  # Import Python's math toolbox

def factorial_loop(n):
    result = 1           # Start with 1 (identity for multiplication)
    steps = []           # Empty list to store each step
    
    for i in range(1, n+1):      # For i = 1, 2, 3, ..., n
        result *= i               # Multiply: result = result × i
        steps.append(f"× {i}")    # Save step as string "× 1", "× 2", etc.
    
    return result, steps         # Return TWO values: (result, steps list)

def factorial_recursive(n):
    if n <= 1:                    # BASE CASE: n=0 or n=1
        return 1                  # Return 1 immediately
    return n * factorial_recursive(n-1)  # RECURSIVE CASE

def main():
    print(" FACTORIAL CALCULATOR")  # Title
    print("="*40)                     # Separator line
    
    try:  # Try to run this code, catch errors if they happen
        n = int(input("Enter a number: "))  # Convert input to integer
        
        if n < 0:  # Check for negative numbers
            print(" Factorial not defined for negative numbers!")
            return  # Exit function early
        print("\n CALCULATION METHODS:")
        print("-"*40)
        
        # Method 1: Built-in (simplest)
        print("1. Built-in (math.factorial):")
        print(f"   {math.factorial(n):,}")  # :, adds commas (1,000)
                # Method 2: Loop (show steps)
        print("\n2. Loop method:")
        result, steps = factorial_loop(n)  # Get BOTH return values
        
        # Build step string: "1 × 1 × 2 × 3 × 4 × 5"
        steps_str = "1 " + " ".join(steps)  # Join steps with spaces
        
        print(f"   {steps_str} = {result:,}")  # Show full calculation
                # Method 3: Recursive
        print("\n3. Recursive method:")
        print(f"   {factorial_recursive(n):,}")
        
        print("-"*40)
        print(f" {n}! = {math.factorial(n):,}")

    except ValueError:  # If int() conversion fails
        print(" Please enter a valid integer!")
    except OverflowError:  # If number is too large
        print(" Number too large!")

if __name__ == "__main__":
    main()