def calculate_bmi(weight: float, height: float) -> float:
    return weight / (height **2)

def classify_bmi(bmi: float) -> str:
    
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"

def main():
    print(" ==== BMI ==== ")

    try:
        weight =float(input("Weight (Kg): "))
        height =float(input("Height(m): "))

        bmi = calculate_bmi(weight, height)
        category = classify_bmi(bmi)

        print(f"\n BMI: {bmi: .1f}")
        print(f" Category: {category}")
    except ValueError:
        print(" Please enter valid number")

if __name__ == "__main__":
    main()