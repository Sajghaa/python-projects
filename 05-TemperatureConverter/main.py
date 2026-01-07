def c_to_f(c: float) -> float:
    return (c * 9/5) + 32

def f_to_c(f: float) -> float:
    return (f - 32) * 5/9

def main():
    print("Temperature Converter")

    try:
        temp = float(input("\n Enter Temperature: "))
    
    except ValueError:
        print("Please enter a valid number")
        return
    
    unit = input("From (C)elisius or (F)ahrenheit?: ").strip().upper()

    if unit == 'C':
        result = c_to_f(temp)
        print(f"\n {temp} C = {result:.1f} F")
    elif unit == 'F':
        result = f_to_c(temp)
        print(f"\n {temp} F = {result:.1f} C")
    else:
        print("Please enter C or F")

if __name__ == "__main__":
    main()