def is_palindrome(text: str)-> bool:
    cleaned = ''.join(char.lower() for char in text if char.isalnum())
    return cleaned == cleaned[::-1]


def main():
    print("PALINDROME CHECKER")
    print("="*20)

    while True:
        text = input("\nEnter text (or 'quit' to exist): ").strip()

        if text.lower() == 'quit':
            print("\n Goodbye my friend!")
            break

        if not text:
            print(" Please enter some text")
            continue

        if is_palindrome(text):
            print(f" '{text}' Is a Palindrome")
            cleaned = ''.join(char.lower() for char in text if char.isalnum())
            print(f" {cleaned} to {cleaned[::-1]}")
        else:
            print(f"'{text}' Is Not a Palindrome")
            cleaned = ''.join(char.lower() for char in text if char.isalnum())

            for i in range(len(cleaned)):
                if cleaned[i] !=cleaned[-(i+1)]:
                    print(f" First mismatch:  '{cleaned[i]}' != '{cleaned[-(i+1)]}'")
                    break

if __name__ == "__main__":
    main()
