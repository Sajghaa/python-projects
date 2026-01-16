#!/usr/bin/env python3
"""
Rock, Paper, Scissors Game
A clean, professional implementation of the classic game.
"""

import random
import os
import time
from datetime import datetime
from typing import Tuple, Dict, List


class RockPaperScissors:
    """Main game class implementing Rock, Paper, Scissors logic."""
    
    # Game constants
    MOVES = {
        'R': 'Rock',
        'P': 'Paper', 
        'S': 'Scissors'
    }
    
    WINNING_RULES = {
        'R': 'S',  # Rock beats Scissors
        'P': 'R',  # Paper beats Rock
        'S': 'P'   # Scissors beats Paper
    }
    
    EMOJIS = {
        'R': '🪨',
        'P': '📄',
        'S': '✂️'
    }
    
    def __init__(self):
        """Initialize the game with default settings."""
        self.player_score = 0
        self.computer_score = 0
        self.ties = 0
        self.game_history = []
        self.player_name = "Player"
        
    def clear_screen(self) -> None:
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_welcome(self) -> None:
        """Display welcome message and game instructions."""
        self.clear_screen()
        print("\n" + "="*50)
        print("🎮 ROCK, PAPER, SCISSORS GAME")
        print("="*50)
        print("\nWelcome to the classic Rock, Paper, Scissors game!")
        print("\nHOW TO PLAY:")
        print("- Type 'R' for Rock 🪨")
        print("- Type 'P' for Paper 📄")
        print("- Type 'S' for Scissors ✂️")
        print("- Type 'Q' to quit the game")
        print("- Type 'S' to see your statistics")
        print("\n" + "="*50)
        
        # Get player name
        name = input("\nEnter your name (or press Enter for 'Player'): ").strip()
        if name:
            self.player_name = name
        
        print(f"\nHello, {self.player_name}! Let's play! 🎯")
        time.sleep(2)
    
    def get_player_move(self) -> str:
        """Get and validate player's move."""
        while True:
            print("\n" + "-"*30)
            print("MAKE YOUR MOVE:")
            print("-"*30)
            print(f"{self.EMOJIS['R']} Rock (R)")
            print(f"{self.EMOJIS['P']} Paper (P)")
            print(f"{self.EMOJIS['S']} Scissors (S)")
            print("📊 Statistics (STATS)")
            print("🚪 Quit (Q)")
            
            choice = input("\nEnter your choice: ").upper().strip()
            
            if choice in ['R', 'P', 'S']:
                return choice
            elif choice == 'Q':
                return 'QUIT'
            elif choice == 'STATS' or choice == 'S':
                self.show_statistics()
                continue
            else:
                print("\n❌ Invalid choice! Please enter R, P, S, STATS, or Q")
                time.sleep(1)
    
    def get_computer_move(self) -> str:
        """Generate computer's move randomly."""
        return random.choice(['R', 'P', 'S'])
    
    def determine_winner(self, player_move: str, computer_move: str) -> str:
        """
        Determine the winner of a round.
        
        Returns:
            str: 'PLAYER', 'COMPUTER', or 'TIE'
        """
        if player_move == computer_move:
            return 'TIE'
        elif self.WINNING_RULES[player_move] == computer_move:
            return 'PLAYER'
        else:
            return 'COMPUTER'
    
    def display_moves(self, player_move: str, computer_move: str) -> None:
        """Display both player and computer moves."""
        print("\n" + "="*50)
        print("🔄 ROUND RESULTS")
        print("="*50)
        
        player_text = f"{self.EMOJIS[player_move]} {self.MOVES[player_move]}"
        computer_text = f"{self.EMOJIS[computer_move]} {self.MOVES[computer_move]}"
        
        print(f"\n{self.player_name}: {player_text}")
        print(f"Computer: {computer_text}")
        
        # Add a little animation effect
        print("\n" + "VS".center(50))
        time.sleep(0.5)
    
    def display_round_result(self, result: str) -> None:
        """Display the result of a round."""
        print("\n" + "-"*30)
        
        if result == 'TIE':
            print("🤝 IT'S A TIE!")
            self.ties += 1
        elif result == 'PLAYER':
            print(f"🎉 {self.player_name} WINS THIS ROUND!")
            self.player_score += 1
        else:
            print("💻 COMPUTER WINS THIS ROUND!")
            self.computer_score += 1
        
        print("-"*30)
        time.sleep(1.5)
    
    def update_history(self, player_move: str, computer_move: str, result: str) -> None:
        """Update game history."""
        round_data = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'player_move': self.MOVES[player_move],
            'computer_move': self.MOVES[computer_move],
            'result': result
        }
        self.game_history.append(round_data)
    
    def show_statistics(self) -> None:
        """Display game statistics."""
        self.clear_screen()
        print("\n" + "="*50)
        print("📊 GAME STATISTICS")
        print("="*50)
        
        total_games = self.player_score + self.computer_score + self.ties
        
        if total_games == 0:
            print("\nNo games played yet!")
            print("\nPlay a round to see statistics!")
        else:
            print(f"\n👤 Player: {self.player_name}")
            print(f"📅 Games Played: {total_games}")
            print("\n" + "-"*30)
            print("SCOREBOARD:")
            print(f"🎯 {self.player_name}: {self.player_score}")
            print(f"💻 Computer: {self.computer_score}")
            print(f"🤝 Ties: {self.ties}")
            print("-"*30)
            
            # Calculate percentages
            player_percent = (self.player_score / total_games) * 100
            computer_percent = (self.computer_score / total_games) * 100
            tie_percent = (self.ties / total_games) * 100
            
            print("\nWIN RATES:")
            print(f"{self.player_name}: {player_percent:.1f}%")
            print(f"Computer: {computer_percent:.1f}%")
            print(f"Ties: {tie_percent:.1f}%")
            
            # Show winning streak
            if self.game_history:
                print("\n" + "-"*30)
                print("LAST 5 GAMES:")
                print("-"*30)
                for game in self.game_history[-5:]:
                    result_emoji = "🎉" if game['result'] == 'PLAYER' else "💻" if game['result'] == 'COMPUTER' else "🤝"
                    print(f"{game['timestamp']}: {game['player_move']} vs {game['computer_move']} = {result_emoji}")
        
        input("\nPress Enter to continue...")
    
    def display_scoreboard(self) -> None:
        """Display current scoreboard."""
        print("\n" + "="*50)
        print("🏆 CURRENT SCOREBOARD")
        print("="*50)
        print(f"\n🎯 {self.player_name}: {self.player_score}")
        print(f"💻 Computer: {self.computer_score}")
        print(f"🤝 Ties: {self.ties}")
        print("="*50)
    
    def play_round(self) -> bool:
        """Play a single round of the game."""
        self.clear_screen()
        
        # Display current score
        self.display_scoreboard()
        
        # Get moves
        player_move = self.get_player_move()
        
        if player_move == 'QUIT':
            return False
        
        computer_move = self.get_computer_move()
        
        # Show moves
        self.display_moves(player_move, computer_move)
        
        # Determine winner
        result = self.determine_winner(player_move, computer_move)
        
        # Show result
        self.display_round_result(result)
        
        # Update history
        self.update_history(player_move, computer_move, result)
        
        return True
    
    def end_game(self) -> None:
        """Display final results and statistics."""
        self.clear_screen()
        print("\n" + "="*50)
        print("🎮 GAME OVER - FINAL RESULTS")
        print("="*50)
        
        total_games = self.player_score + self.computer_score + self.ties
        
        if total_games == 0:
            print("\nThanks for playing! No games were played.")
            return
        
        print(f"\n👤 Player: {self.player_name}")
        print(f"📅 Total Games: {total_games}")
        print("\n" + "-"*30)
        print("FINAL SCORE:")
        print(f"🎯 {self.player_name}: {self.player_score}")
        print(f"💻 Computer: {self.computer_score}")
        print(f"🤝 Ties: {self.ties}")
        print("-"*30)
        
        # Determine overall winner
        if self.player_score > self.computer_score:
            print(f"\n🏆 FINAL RESULT: {self.player_name} WINS! 🎉")
            print("\nCongratulations! You beat the computer! 👑")
        elif self.computer_score > self.player_score:
            print("\n🏆 FINAL RESULT: COMPUTER WINS! 🤖")
            print("\nBetter luck next time! The computer was too strong! 💪")
        else:
            print("\n🏆 FINAL RESULT: IT'S A TIE! ⚖️")
            print("\nWhat a close match! Well played! 🤝")
        
        # Show statistics
        print("\n" + "="*50)
        print("📊 FINAL STATISTICS")
        print("="*50)
        
        player_percent = (self.player_score / total_games) * 100
        computer_percent = (self.computer_score / total_games) * 100
        
        print(f"\n{self.player_name} Win Rate: {player_percent:.1f}%")
        print(f"Computer Win Rate: {computer_percent:.1f}%")
        
        # Show move history
        if self.game_history:
            print("\n" + "-"*30)
            print("GAME HISTORY:")
            print("-"*30)
            for i, game in enumerate(self.game_history[-10:], 1):
                result_emoji = "🎉" if game['result'] == 'PLAYER' else "💻" if game['result'] == 'COMPUTER' else "🤝"
                print(f"Game {i}: {game['player_move']} vs {game['computer_move']} = {result_emoji}")
        
        print("\n" + "="*50)
        print("\nThanks for playing Rock, Paper, Scissors! 👋")
        print("Created with ❤️ using Python")
        print("="*50)
    
    def run(self) -> None:
        """Main game loop."""
        self.display_welcome()
        
        playing = True
        while playing:
            playing = self.play_round()
            
            # Ask to continue after each round
            if playing:
                print("\n" + "-"*30)
                continue_game = input("Play another round? (Y/N): ").upper().strip()
                if continue_game not in ['Y', 'YES']:
                    playing = False
        
        self.end_game()


def main():
    """Main function to run the game."""
    try:
        game = RockPaperScissors()
        game.run()
    except KeyboardInterrupt:
        print("\n\n👋 Game interrupted. Thanks for playing!")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("Please try running the game again.")


if __name__ == "__main__":
    main()