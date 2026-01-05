import random
import os
from typing import Tuple, Optional

class NumberGuessingGame:
    
    def __init__(self, min_number: int = 1, max_number: int = 100):
        self.min_number = min_number
        self.max_number = max_number
        self.target_number = None
        self.attempts = 0
        self.best_score = None
        
    def generate_random_number(self) -> int:
        """Generate a random number within range."""
        return random.randint(self.min_number, self.max_number)
    
    def get_user_guess(self) -> Optional[int]:
        """Get and validate user's guess."""
        try:
            guess_input = input(f"Enter your guess ({self.min_number}-{self.max_number}): ")
            guess = int(guess_input)
            
            if guess < self.min_number:
                print(f" Too low! Minimum is {self.min_number}.")
                return None
            elif guess > self.max_number:
                print(f" Too high! Maximum is {self.max_number}.")
                return None
                
            return guess
            
        except ValueError:
            print(f" Please enter a valid whole number.")
            return None
    
    def give_hint(self, guess: int) -> str:
     
        # Calculate how far off the guess is
        difference = abs(guess - self.target_number)
        
        if difference == 0:
            return " Correct! You got it!"
        elif difference <= 5:
            return " Very hot!"
        elif difference <= 15:
            return " Hot"
        elif difference <= 25:
            return " Warm"
        elif difference <= 40:
            return " Cool"
        else:
            return " Cold"
    
    def play_one_round(self):
        """Play a single round of the game."""
        # Generate new target number
        self.target_number = self.generate_random_number()
        self.attempts = 0
        
        print(f"\n{'='*40}")
        print(f"I'm thinking of a number between {self.min_number} and {self.max_number}")
        print(f"{'='*40}")
        
        # Game loop
        while True:
            self.attempts += 1
            
            # Get valid guess from user
            guess = self.get_user_guess()
            if guess is None:
                self.attempts -= 1  # Don't count invalid attempts
                continue  # Ask again
            
            # Give hint
            hint = self.give_hint(guess)
            print(f"Attempt #{self.attempts}: {hint}")
            
            # Check if won
            if guess == self.target_number:
                print(f"\n You won in {self.attempts} attempts!")
                print(f" The number was {self.target_number}")
                break  # Exit the game loop
    
    def run(self):
        """Start the game."""
        # Clear the screen for better experience
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print(" Welcome to the Number Guessing Game! ")
        self.play_one_round()
        print("\nThanks for playing!")

if __name__ == "__main__":
    game = NumberGuessingGame()
    game.run()