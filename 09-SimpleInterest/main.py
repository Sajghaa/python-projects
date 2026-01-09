def simple_interest(principal: float, rate: float, time: float) -> float:
    return principal * (rate / 100) * time

def main():
    print(" Simple Interest Calculator")
    
    try:
        principal = float(input("Principal amount: $"))
        rate = float(input("Annual rate (%): "))
        time = float(input("Time (years): "))

        interest = simple_interest(principal, rate, time)
        total = principal + interest
        
        print(f"\n Results:")
        print(f"Interest: ${interest:,.2f}")
        print(f"Total:    ${total:,.2f}")
        
    except ValueError:
        print(" Please enter valid numbers")

if __name__ == "__main__":
    main()