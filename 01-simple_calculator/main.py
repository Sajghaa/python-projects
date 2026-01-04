print("Welcome to my Simple Calculator CLI Based")
nbr1 = float(input("Enter your 1st number: "))
nbr2 = float(input("Enter your 2nd number: "))

print("\operations")
print("Addition")
print("Subtraction")
print("Multiplication")
print("Division")

operands = input("Enter (+, -, *, /)")

if operands == '+':
    results = nbr1 + nbr2
elif operands == '-':
    results = nbr1 - nbr2
elif operands == '*':
    results = nbr1 * nbr2
elif operands == '/':
    if nbr2 !=0:
        results = nbr1 / nbr2

    else:
        results ="Error: Division by zero"
else:
    results ="Invalid operation"

print(f"Result: {results}")
