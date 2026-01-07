def is_leap_year(year: int) -> bool:
    return (year % 4 == 0) and (year % 100 != 0 or year % 400 == 0)

def get_valid_year() -> int:
    while True:
        try:
            year = int(input("Enter year: ").strip())
            if year >= 0:
                return year
            print("Year must be positive.")
        except ValueError:
            print("Please enter a valid year (e.g., 2024).")

def main():
    print("Leap Year Checker\n")
    
    year = get_valid_year()

    if is_leap_year(year):
        print(f"\n {year} is a LEAP YEAR")
    else:
        print(f"\n {year} is NOT a leap year")

if __name__ == "__main__":
    main()