import math


def circle_area(radius: float) -> float:
    return math.pi * radius * radius

def rectangle_area(length: float, width: float) -> float:
    return length * width

def triangle_area(base: float, height: float) -> float:
    return 0.5 * base * height

def main():
    print("Area Calculator")
    print("1. Circle 2. Rectangle 3. Triangle")

    choice = input("Choice: ").strip()

    try:
        if choice == "1":
            r = float(input("Radius: "))
            area = circle_area(r)
            print(f"Area: {area:.2f}")

        elif choice == "2":
            l = float(input("Length: "))
            w = float(input("Width: "))
            area = rectangle_area(l, w)
            print(f"Area: {area:.2f}")

        elif choice == "3":
            b = float(input("Base: "))
            h = float(input("Height: "))
            area = triangle_area(b, h)
            print(f"Area: {area:.2f}")

        else:
            print("Choose 1-3")
    except ValueError:
        print("Enter numbers only")

if __name__ == "__main__":
    main()
