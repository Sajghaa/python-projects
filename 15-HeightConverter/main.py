cm = float(input("Enter height in cm: "))

inches = cm / 2.54
feet = cm / 30.48

print(f"\n {cm} cm equals: ")
print(f" {inches:.2f} inches")
print(f" {feet:.2f} feet")
print(f" {int(feet)} feet {round((feet - int(feet)) *12):.0f} inches")
