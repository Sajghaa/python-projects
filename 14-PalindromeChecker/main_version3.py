def check_palindrome():
    text = input("Enter text: ").lower()
    cleaned = ''.join(c for c in text if c.isalnum())

    if cleaned == cleaned[::-1]:
        print(f" '{text}' is  a palindrome ")
    
    else:
        print(f" '{text}' is not a palindrome")

check_palindrome()