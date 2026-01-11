num = int(input("Enter number: "))

print("\nChoose table type:")
print("1. Standard (1-10)")
print("2. Custom range")
print("3. Reverse table")

choice = input("Choice (1-3): ")

if choice == "1":

    print(f"\n Table of {num}: ")
    for i in range (1, 11):
        print(f"{num} x {i:2} = {num * i:3}")

elif choice == "2":
    start = int(input("Start from: "))
    end = int(input("End at: "))

    print(f"\n Table of {num} ({start} to {end}): ")
    for i in range(start, end + 1):
        print(f"{num} x {i:2} = {num * i:3}")

elif choice == "3":
    print(f"\n Reverse Table of {num}:")
    for i in range(10, 0, -1):
        print(f"{num} x {i:2} = {num * i:3}")