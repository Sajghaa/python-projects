def is_prime_basic(n: int) -> bool:
  
    # Special cases: numbers ≤ 1 are not prime
    if n <= 1:
        return False
    
    # Check all numbers from 2 to n-1
    for i in range(2, n):
        # If n ÷ i has no remainder, it's not prime
        if n % i == 0:
            return False
    
    # If no divisors found, it's prime
    return True


def is_prime_optimized(n: int) -> bool:
    # Special cases
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0: 
        return False
    
    limit = int(n ** 0.5) + 1  
    
    for i in range(3, limit, 2):  
        if n % i == 0:
            return False
    
    return True


def check_prime_with_steps(n: int) -> tuple[bool, list[str]]:
    steps = []
    
    if n <= 1:
        steps.append(f"{n} ≤ 1 → NOT PRIME")
        return False, steps
    
    steps.append(f"Checking if {n} is prime...")
    steps.append(f"Divisible by 1? Always ✓")
    
    for i in range(2, n):
        remainder = n % i
        step = f"Divisible by {i}? {n} ÷ {i} = {n//i} remainder {remainder}"
        
        if remainder == 0:
            step += " ✓ (DIVIDES EVENLY!)"
            steps.append(step)
            steps.append(f"Found divisor {i} → NOT PRIME")
            return False, steps
        else:
            step += " ✗"
            steps.append(step)
    
    steps.append(f"Only divisible by 1 and {n} → IS PRIME!")
    return True, steps


def main():
    """Main program with interactive menu."""
    print(" PRIME NUMBER CHECKER")
    print("="*50)
    
    while True:
        print("\n MAIN MENU")
        print("="*30)
        print("1. Check if a number is prime")
        print("2. Show step-by-step checking")
        print("3. Find primes in a range")
        print("4. Compare methods (basic vs optimized)")
        print("5. Exit")
        print("="*30)
        
        choice = input("\nChoose option (1-5): ").strip()
        
        if choice == "1":
            # Simple prime check
            try:
                n = int(input("\nEnter a number to check: "))
                
                if is_prime_optimized(n):
                    print(f" {n} IS a prime number!")
                else:
                    print(f" {n} is NOT a prime number.")
                    
            except ValueError:
                print(" Please enter a valid integer!")
        
        elif choice == "2":
            # Step-by-step check
            try:
                n = int(input("\nEnter a number to check step-by-step: "))
                
                is_prime, steps = check_prime_with_steps(n)
                
                print("\n STEP-BY-STEP CHECK:")
                print("-"*40)
                for step in steps:
                    print(step)
                print("-"*40)
                
                if is_prime:
                    print(f" Final: {n} IS PRIME!")
                else:
                    print(f" Final: {n} is NOT PRIME.")
                    
            except ValueError:
                print(" Please enter a valid integer!")
        
        elif choice == "3":
            # Find primes in range
            try:
                start = int(input("\nStart from: "))
                end = int(input("End at: "))
                
                if start > end:
                    print(" Start must be ≤ end!")
                    continue
                
                print(f"\n Prime numbers between {start} and {end}:")
                print("-"*40)
                
                primes = []
                for num in range(start, end + 1):
                    if is_prime_optimized(num):
                        primes.append(num)
                
                if primes:
                    for prime in primes:
                        print(f" {prime}")
                    print(f"\n Found {len(primes)} prime numbers.")
                else:
                    print("No prime numbers found in this range.")
                    
            except ValueError:
                print(" Please enter valid integers!")
        
        elif choice == "4":
            # Compare methods
            try:
                n = int(input("\nEnter a number to test: "))
                
                import time
                
                start = time.time()
                basic_result = is_prime_basic(n)
                basic_time = time.time() - start
                
                start = time.time()
                optimized_result = is_prime_optimized(n)
                optimized_time = time.time() - start
                
                print("\n PERFORMANCE COMPARISON:")
                print("-"*40)
                print(f"Number: {n}")
                print(f"Basic method:    {basic_time:.6f} seconds")
                print(f"Optimized method: {optimized_time:.6f} seconds")
                print(f"Optimized is {basic_time/optimized_time:.1f}x faster!")
                print(f"Both agree: {basic_result == optimized_result}")
                
            except ValueError:
                print(" Please enter a valid integer!")
        
        elif choice == "5":
            print("\n Goodbye! Keep exploring the world of prime numbers!")
            break
        
        else:
            print(" Please choose 1-5")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()