import random
import tkinter as tk
from tkinter import messagebox

class HangmanGame:
    def __init__(self, word_list):
        """Initialize the game with a list of possible words."""
        self.word_list = word_list
        self.word_to_guess = random.choice(self.word_list).upper()  # Selects a random word from the list
        self.guessed_letters = set()  # Set of letters guessed by the player
        self.attempts_left = 6  # Number of attempts left
        self.correct_guesses = set()  # Set of correct guesses (letters that are in the word)
        
    # Responsible for displaying the word with guessed letters and underscores    
    def display_word(self):
        display = ""
        for letter in self.word_to_guess:
            if letter in self.correct_guesses:
                display += letter + " "
            else:
                display += "_ "
                
        # The strip function removes any whitespaces present at the start and end
        return display.strip()

    # Responsible for checking the guess and updating the stages of the game accordingly
    def make_guess(self, guess):
        # To handle case insensitivity
        
        guess = guess.upper()  
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

    # Responsible for deciding whether the player has won or lost
    def game_status(self):
        if self.attempts_left == 0:
            return "lose"
        if set(self.word_to_guess) == self.correct_guesses:
            return "win"
        return "continue"
    
    def hangman_stages(self):
        if self.attempts_left == 6:
            return '''
        +---+
        |   |
            |
            |
            |
            |
      =========
      '''
        elif self.attempts_left == 5:
          return '''
        +---+
        |   |
        O   |
            |
            |
            |
      =========
        '''
        elif self.attempts_left == 4:
          return '''
        +---+
        |   |
        O   |
        |   |
            |
            |
      =========
        '''
        elif self.attempts_left == 3:
          return '''
        +---+
        |   |
        O   |
       /|   |
            |
            |
      =========
        '''
        elif self.attempts_left == 2:
          return '''
        +---+
        |   |
        O   |
       /|\  |
            |
            |
      =========
        '''
        elif self.attempts_left == 1:
          return '''
        +---+
        |   |
        O   |
       /|\  |
       /    |
            |
      =========
        '''
        elif self.attempts_left == 0:
          return '''
        +---+
        |   |
        O   |
       /|\  |
       /\   |
            |
      =========
        '''
                       
        

# Responsible for handling the UI
class HangmanUI:
    def __init__(self, root, word_list):

        self.root = root
        self.root.title("Hangman Game")
        
        self.game = HangmanGame(word_list)

        # UI Elements
        self.word_label = tk.Label(root, text=self.game.display_word(), font=("Helvetica", 24))
        self.word_label.pack(pady=20)

        self.attempts_label = tk.Label(root, text=f"Attempts Left: {self.game.attempts_left}", font=("Helvetica", 14))
        self.attempts_label.pack()
        
        self.hangman_label = tk.Label(root, text=self.game.hangman_stages(), font=("Courier", 12))
        self.hangman_label.pack()

        self.guessed_label = tk.Label(root, text=f"Guessed Letters: ", font=("Helvetica", 14))
        self.guessed_label.pack(pady=10)

        self.letter_buttons_frame = tk.Frame(root)
        self.letter_buttons_frame.pack()

        self.letter_buttons = {}
        self.create_letter_buttons()
    
    # Create buttons for each letter in the alphabet and arrange them in 3 rows."""
    def create_letter_buttons(self):

        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        num_letters = len(alphabet)
        num_rows = 3
        letters_per_row = num_letters // num_rows  # Determines how many letters per row


        for i, letter in enumerate(alphabet):
            row = i // letters_per_row  # Determines which row the button belongs to
            col = i % letters_per_row  # Determines the column in that row
            
            # Additional case for handling the last row of letters
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

           
    # Responsible for updating the game based on mouse input
    def on_letter_button_click(self, letter):
        
        if not self.game.make_guess(letter):
            # If the guess is invalid or already guessed, do nothing
            return
        
        # Update the word label
        self.word_label.config(text=self.game.display_word())

        # Update the guessed letters label
        self.guessed_label.config(text=f"Guessed Letters: {', '.join(sorted(self.game.guessed_letters))}")

        # Update the attempts label
        self.attempts_label.config(text=f"Attempts Left: {self.game.attempts_left}")
        
        # Update the hangman stage label
        self.hangman_label.config(text=self.game.hangman_stages())

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

    # Responsible for resetting the game 
    def reset_game(self):
        # Creates a new instance of the hangman game with default values
        self.game = HangmanGame(words)
        self.word_label.config(text=self.game.display_word())
        self.attempts_label.config(text=f"Attempts Left: {self.game.attempts_left}")
        self.guessed_label.config(text="Guessed Letters: ")
        
        # Re-enable letter buttons
        for button in self.letter_buttons.values():
            button.config(state=tk.NORMAL)



if __name__ == "__main__":
    words = ["python", "hangman", "development", "code", "programming"]
    
    # Create a Tkinter window
    root = tk.Tk()

    # Create an instance of HangmanUI
    game_ui = HangmanUI(root, words)
    
    # Start the Tkinter event loop
    root.mainloop()
