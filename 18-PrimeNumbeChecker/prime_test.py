from prime_checker import is_prime_basic, is_prime_optimized

def test_primes():

    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    
    non_primes = [1, 4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20]
    
    print(" TESTING PRIME CHECKER")
    print("="*40)
    
    print("\n Testing prime numbers:")
    for num in primes:
        basic = is_prime_basic(num)
        optimized = is_prime_optimized(num)
        print(f"{num:3} - Basic: {str(basic):5} | Optimized: {str(optimized):5}")
    
    print("\n Testing non-prime numbers:")
    for num in non_primes:
        basic = is_prime_basic(num)
        optimized = is_prime_optimized(num)
        print(f"{num:3} - Basic: {str(basic):5} | Optimized: {str(basic):5}")
    
    print("\n All tests completed!")


if __name__ == "__main__":
    test_primes()