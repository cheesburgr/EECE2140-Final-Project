import random
import tkinter as tk
from tkinter import messagebox

class HangmanGame:
    def __init__(self, word_list):
        """Initialize the game with a list of possible words."""
        self.word_list = word_list
        self.word_to_guess = random.choice(self.word_list).upper()  # Select a random word
        self.guessed_letters = set()  # Set of letters guessed by the player
        self.attempts_left = 6  # Number of attempts (hangman stages)
        self.correct_guesses = set()  # Set of correct guesses (letters that are in the word)
        
    def display_word(self):
        """Display the current state of the word with underscores for unguessed letters."""
        display = ""
        for letter in self.word_to_guess:
            if letter in self.correct_guesses:
                display += letter + " "
            else:
                display += "_ "
        return display.strip()

    def make_guess(self, guess):
        """Make a guess, and update the game state accordingly."""
        guess = guess.upper()  # Convert to uppercase to handle case insensitivity
        if len(guess) != 1 or not guess.isalpha():
            return False
        
        if guess in self.guessed_letters:
            return False
        
        self.guessed_letters.add(guess)

        if guess in self.word_to_guess:
            self.correct_guesses.add(guess)
        else:
            self.attempts_left -= 1
        
        return True

    def game_status(self):
        """Check if the game has been won or lost."""
        if self.attempts_left == 0:
            return "lose"
        if set(self.word_to_guess) == self.correct_guesses:
            return "win"
        return "continue"


class HangmanUI:
    def __init__(self, root, word_list):
        """Initialize the UI and game logic."""
        self.root = root
        self.root.title("Hangman Game")
        
        self.game = HangmanGame(word_list)

        # UI Elements
        self.word_label = tk.Label(root, text=self.game.display_word(), font=("Helvetica", 24))
        self.word_label.pack(pady=20)

        self.attempts_label = tk.Label(root, text=f"Attempts Left: {self.game.attempts_left}", font=("Helvetica", 14))
        self.attempts_label.pack()

        self.guessed_label = tk.Label(root, text=f"Guessed Letters: ", font=("Helvetica", 14))
        self.guessed_label.pack(pady=10)

        self.letter_buttons_frame = tk.Frame(root)
        self.letter_buttons_frame.pack()

        self.letter_buttons = {}
        self.create_letter_buttons()

    def create_letter_buttons(self):
        """Create buttons for each letter in the alphabet and arrange them in 3 rows."""
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        num_letters = len(alphabet)
        num_rows = 3
        letters_per_row = num_letters // num_rows  # Determine how many letters per row

        # Create letter buttons and place them in 3 rows
        for i, letter in enumerate(alphabet):
            row = i // letters_per_row  # Determine which row the button belongs to
            col = i % letters_per_row  # Determine the column in that row
            
            if row == num_rows:
                button = tk.Button(self.letter_buttons_frame, text=letter, width=4, height=2, 
                                   command=lambda letter=letter: self.on_letter_button_click(letter))
                button.grid(row=row, column=col + 3, padx=2, pady=2)
                self.letter_buttons[letter] = button
            
            else:
                button = tk.Button(self.letter_buttons_frame, text=letter, width=4, height=2, 
                                   command=lambda letter=letter: self.on_letter_button_click(letter))
                button.grid(row=row, column=col, padx=2, pady=2)
                self.letter_buttons[letter] = button

           

    def on_letter_button_click(self, letter):
        """Handle the click event for a letter button."""
        if not self.game.make_guess(letter):
            # If the guess is invalid or already guessed, do nothing
            return
        
        # Update the word label
        self.word_label.config(text=self.game.display_word())

        # Update the guessed letters label
        self.guessed_label.config(text=f"Guessed Letters: {', '.join(sorted(self.game.guessed_letters))}")

        # Update the attempts label
        self.attempts_label.config(text=f"Attempts Left: {self.game.attempts_left}")

        # Disable the button after it's clicked
        self.letter_buttons[letter].config(state=tk.DISABLED)

        # Check if the game has ended
        status = self.game.game_status()
        if status == "win":
            messagebox.showinfo("Congratulations!", f"You guessed the word: {self.game.word_to_guess}")
            self.reset_game()
        elif status == "lose":
            messagebox.showinfo("Game Over", f"You lost! The word was: {self.game.word_to_guess}")
            self.reset_game()

    def reset_game(self):
        """Reset the game and the UI for a new game."""
        self.game = HangmanGame(words)
        self.word_label.config(text=self.game.display_word())
        self.attempts_label.config(text=f"Attempts Left: {self.game.attempts_left}")
        self.guessed_label.config(text="Guessed Letters: ")
        
        # Re-enable letter buttons
        for button in self.letter_buttons.values():
            button.config(state=tk.NORMAL)


# Example usage:
if __name__ == "__main__":
    words = ["python", "hangman", "development", "code", "programming"]
    
    # Create a Tkinter window
    root = tk.Tk()

    # Create an instance of HangmanUI
    game_ui = HangmanUI(root, words)
    
    # Start the Tkinter event loop
    root.mainloop()
