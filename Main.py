import random
import tkinter as tk
from tkinter import messagebox


class WordBank:
    def __init__(self, words):
        """Initialize the WordBank with a list of words."""
        self.words = words # Sets the words that will be included in the bank

    def get_random_word(self):
        """Select and return a random word from the word bank."""
        if not self.words:
            return None  # Return None if the word bank is empty
        return random.choice(self.words) #returns a random word from the word bank

class HangmanGame:
    def __init__(self):
        """Initialize the game with a list of possible words."""
        self.guessed_letters = set()  # Set of letters guessed by the player
        self.attempts_left = 6  # Number of attempts (hangman stages)
        self.correct_guesses = set()  # Set of correct guesses (letters that are in the word)
        
        
        """Chooses a random word from category"""
    def setcategory(self, bank):
        if bank == "fruits":
            self.word_to_guess = fruitsBank.get_random_word().upper()  
        if bank == "places":
            self.word_to_guess = placesBank.get_random_word().upper()  
        if bank == "coding":
            self.word_to_guess = codingBank.get_random_word().upper()
        if bank == "all":
            self.word_to_guess = allBank.get_random_word().upper()
        
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


class HangmanUI:
    def __init__(self, root):
        """Initialize the UI and game logic."""
        self.root = root
        self.root.title("Hangman Game")
        
        self.game = HangmanGame()
        
        """Category selection screen"""
        self.pick_category_label = tk.Label(root, text="Pick a category:", font=("Helvetica", 14))
        self.pick_category_label.pack(side = 'top')
        
        self.var = tk.IntVar()
        self.btn1 = tk.Button(root, text = 'fruits', command =lambda: [self.game.setcategory("fruits"), self.var.set(1)]) 
        self.btn1.pack(side = 'top')
        self.btn2 = tk.Button(root, text = 'places', command =lambda: [self.game.setcategory("places"), self.var.set(1)]) 
        self.btn2.pack(side = 'top')   
        self.btn3 = tk.Button(root, text = 'coding', command =lambda: [self.game.setcategory("coding"), self.var.set(1)]) 
        self.btn3.pack(side = 'top')   
        self.btn4 = tk.Button(root, text = 'all', command =lambda: [self.game.setcategory("all"), self.var.set(1)]) 
        self.btn4.pack(side = 'top')   
        
        # Waits until a button is pressed and then clears selection screen elements
        self.btn1.wait_variable(self.var)
        self.btn1.destroy()
        self.btn2.destroy()
        self.btn3.destroy()
        self.btn4.destroy()
        self.pick_category_label.destroy()
        

        # UI Elements
        self.wins = 0
        self.wins_label = tk.Label(root, text=f"Wins: {self.wins}", font=("Helvetica", 14))
        self.wins_label.pack(side = 'top')
        
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
            self.wins += 1
            self.reset_game()
        elif status == "lose":
            messagebox.showinfo("Game Over", f"You lost! The word was: {self.game.word_to_guess}")
            self.reset_game()

    # Responsible for resetting the game 
    def reset_game(self):
        # Creates a new instance of the hangman game with default values
        self.game = HangmanGame()
        
        
        # Brings back the selection screen
        self.pick_category_label = tk.Label(root, text="Pick a category:", font=("Helvetica", 14))
        self.pick_category_label.pack(side = 'top')
        self.var = tk.IntVar()
        self.btn1 = tk.Button(root, text = 'fruits', command =lambda: [self.game.setcategory("fruits"), self.var.set(1)]) 
        self.btn1.pack(side = 'top')
        self.btn2 = tk.Button(root, text = 'places', command =lambda: [self.game.setcategory("places"), self.var.set(1)]) 
        self.btn2.pack(side = 'top')   
        self.btn3 = tk.Button(root, text = 'coding', command =lambda: [self.game.setcategory("coding"), self.var.set(1)]) 
        self.btn3.pack(side = 'top')   
        self.btn4 = tk.Button(root, text = 'all', command =lambda: [self.game.setcategory("all"), self.var.set(1)]) 
        self.btn4.pack(side = 'top') 
        
        self.btn1.wait_variable(self.var)
        self.btn1.destroy()
        self.btn2.destroy()
        self.btn3.destroy()
        self.btn4.destroy()
        self.pick_category_label.destroy()
        
        
        
        self.word_label.config(text=self.game.display_word())
        self.attempts_label.config(text=f"Attempts Left: {self.game.attempts_left}")
        self.guessed_label.config(text="Guessed Letters: ")
        self.wins_label.config(text=f"Wins: {self.wins}")
        
        # Re-enable letter buttons
        for button in self.letter_buttons.values():
            button.config(state=tk.NORMAL)


# Example usage:
if __name__ == "__main__":
    #categories
    fruits = ["apple", "banana", "cherry", "date", "elderberry"]
    coding = ["python", "psudeocode", "development", "code", "programming"]
    places = ["allston", "fenway", "brookline", "cambridge", "boston"]

    # Create wordbank instances for each category
    fruitsBank = WordBank(fruits)
    placesBank = WordBank(places)
    codingBank = WordBank(coding)
    allBank = WordBank(fruits + places + coding)
    
    # Create a Tkinter window
    root = tk.Tk()

    # Create an instance of HangmanUI
    game_ui = HangmanUI(root)
    
    # Start the Tkinter event loop
    root.mainloop()