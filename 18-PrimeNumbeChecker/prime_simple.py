def is_prime(n):
    if n <= 1:
        return False
    
    for i in range(2, n):
        if n % i == 0:
            return False
    
    return True


def main():
    print(" Prime Checker")
    
    try:
        n = int(input("Enter a number: "))
        
        if is_prime(n):
            print(f" {n} is prime")
        else:
            print(f" {n} is not prime")
            
    except ValueError:
        print("Enter a valid number!")


if __name__ == "__main__":
    main()