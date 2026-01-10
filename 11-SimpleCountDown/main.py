import time

def countdown(seconds: int):
    print(f"Starting {seconds} second timer...\n")

    for i in range(seconds, 0, -1):
        mins, secs = divmod(i, 60)
        timer = f"{mins:02d}:{secs:02d}"
        print(f"Time remaining: {timer}", end='\r')
        time.sleep(1)
    print("\n TIME'S UP!")

def main():
    print("Simple Countdown Timer")

    try:
        secs = int(input("Enter seconds: "))
        if secs > 0:
            countdown(secs)
        else:
            print("Enter positive number")
    except ValueError:
        print("Enter a valid number")

if __name__ == "__main__":
    main()
