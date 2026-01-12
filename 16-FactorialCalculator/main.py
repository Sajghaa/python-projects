import math

def factorial_loop(n):
    result = 1
    steps = []
    for i in range(1, n+1):
        result *= i
        steps.append(f"× {i}")
    return result, steps

def factorial_recursive(n):
    if n <= 1:
        return 1
    return n * factorial_recursive(n-1)

def main():
    print(" FACTORIAL CALCULATOR")
    print("="*40)
    
    try:
        # Get input with error handling
        n = int(input("Enter a number: "))
        
        if n < 0:
            print(" Factorial not defined for negative numbers!")
            return
        
        print("\n CALCULATION METHODS:")
        print("-"*40)
        
        # Method 1: Built-in
        print("1. Built-in (math.factorial):")
        print(f"   {math.factorial(n):,}")
        
        # Method 2: Loop (show steps) as I've explained in readme.md
        print("\n2. Loop method:")
        result, steps = factorial_loop(n)
        steps_str = "1 " + " ".join(steps)
        print(f"   {steps_str} = {result:,}")
        
        # Method 3: Recursive I also explained it in readme.md but It's also more understandable
        print("\n3. Recursive method:")
        print(f"   {factorial_recursive(n):,}")
        
        print("-"*40)
        print(f" {n}! = {math.factorial(n):,}")
        
    except ValueError:
        print(" Please enter a valid integer!")
    except OverflowError:
        print(" Number too large!")

if __name__ == "__main__":
    main()