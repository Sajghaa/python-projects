def fibonacci_method1(n: int):

    if n <= 0:
        return []
    
    sequence = []
    a, b = 0, 1

    for i in range(n):
        sequence.append(a)
        a, b = b, a + b

    return sequence

def main():
    print("FIBONACCI GENERATOR - METHOD 1")
    print("="*50)

    try:
        n =  int(input("How many Fibonacci numbers do you want?: "))

        if n <0: 
            print("Please enter a positive number!")
            return
        
        result = fibonacci_method1(n)
        print("-"*40)

        for i, num in enumerate(result, 1):
            print(f"F ({i-1}) = {num}")

        print("-"*40)
        print(f"full sequence: {result}")
        print(f"\n EFFICIENCY: Only use 2 variables (a, b), not the whole list!")
    except ValueError:
        print("Please enter a valid integer!")

if __name__ == "__main__":
    main()