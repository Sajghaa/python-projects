word = input("Enter word: ").lower()
is_palindrome = word == word[::-1]
print(" Palindrome!" if is_palindrome else "Not a palindrome")