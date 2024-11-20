import random
import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkfont  # Import the font module for loading custom fonts
from PIL import Image, ImageTk

class WordBank:
    def __init__(self, words):
        """Initialize the WordBank with a list of words."""
        self.words = words  # Sets the words that will be included in the bank

    def get_random_word(self):
        """Select and return a random word from the word bank."""
        if not self.words:
            return None  # Return None if the word bank is empty
        return random.choice(self.words)  # returns a random word from the word bank

class HangmanGame:
    def __init__(self):
        """Initialize the game with a list of possible words."""
        self.guessed_letters = set()  # Set of letters guessed by the player
        self.attempts_left = 6  # Number of attempts (hangman stages)
        self.correct_guesses = set()  # Set of correct guesses (letters that are in the word)
        
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
    
class HangmanUI:
    def __init__(self, root):
        """Initialize the UI and game logic."""
        self.root = root
        self.root.title("Hangman Game")
        
        # Set up the background image
        self.set_background()

        self.game = HangmanGame()
        
        # Background color RGB: (15, 118, 53) → Hex #0F7635
        self.bg_color = "#0F7635"
        
        # Load the custom font directly by its name (if installed on the system)
        self.custom_font = tkfont.Font(family="EraserDust", size=16)  # Assuming "EraserDust" is installed

        # Category selection screen (move everything down with padding)
        self.pick_category_label = tk.Label(root, text="Pick a category:", font=self.custom_font, bg=self.bg_color)
        self.pick_category_label.pack(side='top', pady=(100, 10))  # Increased padding to move it down
        
        self.var = tk.IntVar()
        self.btn1 = tk.Button(root, text='fruits', command=lambda: [self.game.setcategory("fruits"), self.var.set(1)], 
                              bg=self.bg_color, relief="flat", highlightthickness=0, font=self.custom_font) 
        self.btn1.pack(side='top', pady=5)
        self.btn2 = tk.Button(root, text='places', command=lambda: [self.game.setcategory("places"), self.var.set(1)], 
                              bg=self.bg_color, relief="flat", highlightthickness=0, font=self.custom_font) 
        self.btn2.pack(side='top', pady=5)   
        self.btn3 = tk.Button(root, text='coding', command=lambda: [self.game.setcategory("coding"), self.var.set(1)], 
                              bg=self.bg_color, relief="flat", highlightthickness=0, font=self.custom_font) 
        self.btn3.pack(side='top', pady=5)   
        self.btn4 = tk.Button(root, text='all', command=lambda: [self.game.setcategory("all"), self.var.set(1)], 
                              bg=self.bg_color, relief="flat", highlightthickness=0, font=self.custom_font) 
        self.btn4.pack(side='top', pady=5)   
        
        # Wait until a button is pressed and then clears selection screen elements
        self.btn1.wait_variable(self.var)
        self.btn1.destroy()
        self.btn2.destroy()
        self.btn3.destroy()
        self.btn4.destroy()
        self.pick_category_label.destroy()

        # UI Elements (move all elements down with padding)
        self.wins = 0
        self.wins_label = tk.Label(root, text=f"Wins: {self.wins}", font=self.custom_font, bg=self.bg_color)
        self.wins_label.pack(side='top', pady=(80, 10))  # Increased padding to move it further down
        
        self.word_label = tk.Label(root, text=self.game.display_word(), font=self.custom_font, bg=self.bg_color)
        self.word_label.pack(pady=20)

        self.attempts_label = tk.Label(root, text=f"Attempts Left: {self.game.attempts_left}", font=self.custom_font, bg=self.bg_color)
        self.attempts_label.pack(pady=(10, 5))
        
        self.guessed_label = tk.Label(root, text=f"Guessed Letters: ", font=self.custom_font, bg=self.bg_color)
        self.guessed_label.pack(pady=10)

        # Hangman Canvas (add more padding to ensure it stays below the text)
        self.canvas = tk.Canvas(root, width=200, height=300, bg=self.bg_color)  # Remove grey background
        self.canvas.pack(pady=(20, 30))  # Increased padding to give more space between the canvas and text

        # Load images for each hangman stage
        self.hangman_images = [
            Image.open("assets/hangman_0.png"),  # Only Stand
            Image.open("assets/hangman_1.png"),  # Head
            Image.open("assets/hangman_2.png"),  # Head + Body
            Image.open("assets/hangman_3.png"),  # Head + Body + Left Leg
            Image.open("assets/hangman_4.png"),  # Head + Body + Both Legs
            Image.open("assets/hangman_5.png"),  # Head + Body + Both Legs + Left Arm
            Image.open("assets/hangman_6.png"),  # Full hangman
        ]

        self.hangman_images = [img.resize((200, 300), Image.Resampling.LANCZOS) for img in self.hangman_images]
        self.hangman_photo_images = [ImageTk.PhotoImage(img) for img in self.hangman_images]

        # Load the stand image
        self.stand_image = Image.open("assets/hangman_0.png")
        self.stand_image = self.stand_image.resize((200, 250), Image.Resampling.LANCZOS)  # Resize to fit canvas
        self.stand_photo_image = ImageTk.PhotoImage(self.stand_image)
        
        
        # Letter buttons (move all buttons down a bit)
        self.letter_buttons_frame = tk.Frame(root, bg=self.bg_color)  # Remove background color from frame
        self.letter_buttons_frame.pack(pady=(20, 40))  # Increased padding to move buttons further down
    
        self.letter_buttons = {}
        self.create_letter_buttons()

    def set_background(self):
        """Set the background image for the game."""
        # Load an image
        self.bg_image = Image.open("assets/background.png")  # Use your own image path here
        self.bg_image = self.bg_image.resize((1000, 1000), Image.Resampling.LANCZOS)  # Resize to fit window size
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Create a label to display the background image
        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)  # Cover entire window

    def create_letter_buttons(self):
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        num_letters = len(alphabet)
        num_rows = 3
        letters_per_row = num_letters // num_rows  # Determines how many letters per row

        for i, letter in enumerate(alphabet):
            row = i // letters_per_row  # Determines which row the button belongs to
            col = i % letters_per_row  # Determines the column in that row

            if row == num_rows:
                button = tk.Button(self.letter_buttons_frame, text=letter, width=4, height=2, 
                               command=lambda letter=letter: self.on_letter_button_click(letter),
                               bg=self.bg_color, relief="flat", highlightthickness=0, font=self.custom_font)  # Button with custom font
                button.grid(row=row, column=col + 3, padx=2, pady=2)
            
            else:

                button = tk.Button(self.letter_buttons_frame, text=letter, width=4, height=2, 
                                    command=lambda letter=letter: self.on_letter_button_click(letter),
                                bg=self.bg_color, relief="flat", highlightthickness=0, font=self.custom_font)  # Button with custom font
                button.grid(row=row, column=col, padx=2, pady=2)
                self.letter_buttons[letter] = button

    def on_letter_button_click(self, letter):
        if not self.game.make_guess(letter):
            return
        
        self.word_label.config(text=self.game.display_word())
        self.guessed_label.config(text=f"Guessed Letters: {', '.join(sorted(self.game.guessed_letters))}")
        self.attempts_label.config(text=f"Attempts Left: {self.game.attempts_left}")

        self.letter_buttons[letter].config(state=tk.DISABLED)

        # Update hangman shape based on attempts left
        self.update_hangman(self.game.attempts_left)

        status = self.game.game_status()
        if status == "win":
            messagebox.showinfo("Congratulations!", f"You guessed the word: {self.game.word_to_guess}")
            self.wins += 1
            self.reset_game()
        elif status == "lose":
            messagebox.showinfo("Game Over", f"You lost! The word was: {self.game.word_to_guess}")
            self.reset_game()

    def update_hangman(self, attempts_left):
        """Update the hangman drawing based on remaining attempts."""
        self.canvas.delete("all")  # Clear previous hangman image

        # Only display the appropriate hangman image based on the number of attempts left
        self.canvas.create_image(100, 150, image=self.hangman_photo_images[6 - attempts_left])



    def reset_game(self):
        """Reset the game and show only the category selection buttons."""
        self.game = HangmanGame()

        # Remove all UI elements related to the game
        try:
            self.word_label.destroy()
            self.attempts_label.destroy()
            self.guessed_label.destroy()
            self.wins_label.destroy()
            self.canvas.destroy()
            self.letter_buttons_frame.destroy()
        except AttributeError:
            pass  # Handle if elements are already destroyed in case of multiple game resets

        # Show the category selection screen again
        self.pick_category_label = tk.Label(self.root, text="Pick a category:", font=self.custom_font, bg=self.bg_color)
        self.pick_category_label.pack(side='top', pady=(100, 10))  # Increased padding to move it down

        self.var = tk.IntVar()
        self.btn1 = tk.Button(self.root, text='fruits', command=lambda: [self.game.setcategory("fruits"), self.var.set(1)], 
                    bg=self.bg_color, relief="flat", highlightthickness=0, font=self.custom_font) 
        self.btn1.pack(side='top', pady=5)
        self.btn2 = tk.Button(self.root, text='places', command=lambda: [self.game.setcategory("places"), self.var.set(1)], 
                    bg=self.bg_color, relief="flat", highlightthickness=0, font=self.custom_font) 
        self.btn2.pack(side='top', pady=5)   
        self.btn3 = tk.Button(self.root, text='coding', command=lambda: [self.game.setcategory("coding"), self.var.set(1)], 
                    bg=self.bg_color, relief="flat", highlightthickness=0, font=self.custom_font) 
        self.btn3.pack(side='top', pady=5)   
        self.btn4 = tk.Button(self.root, text='all', command=lambda: [self.game.setcategory("all"), self.var.set(1)], 
                    bg=self.bg_color, relief="flat", highlightthickness=0, font=self.custom_font) 
        self.btn4.pack(side='top', pady=5)

        # Wait until a button is pressed and then clear the selection screen elements
        self.btn1.wait_variable(self.var)
        self.btn1.destroy()
        self.btn2.destroy()
        self.btn3.destroy()
        self.btn4.destroy()
        self.pick_category_label.destroy()

        # Recreate the game UI elements (word display, attempts, guessed letters, and canvas)
        self.wins_label = tk.Label(self.root, text=f"Wins: {self.wins}", font=self.custom_font, bg=self.bg_color)
        self.wins_label.pack(side='top', pady=(80, 10))  # Increased padding to move it further down

        self.word_label = tk.Label(self.root, text=self.game.display_word(), font=self.custom_font, bg=self.bg_color)
        self.word_label.pack(pady=20)

        self.attempts_label = tk.Label(self.root, text=f"Attempts Left: {self.game.attempts_left}", font=self.custom_font, bg=self.bg_color)
        self.attempts_label.pack(pady=(10, 5))

        self.guessed_label = tk.Label(self.root, text=f"Guessed Letters: ", font=self.custom_font, bg=self.bg_color)
        self.guessed_label.pack(pady=10)

        # Hangman Canvas (add more padding to ensure it stays below the text)
        self.canvas = tk.Canvas(self.root, width=200, height=300, bg=self.bg_color)  # Remove grey background
        self.canvas.pack(pady=(20, 30))  # Increased padding to give more space between the canvas and text

        # Letter buttons (move all buttons down a bit)
        self.letter_buttons_frame = tk.Frame(self.root, bg=self.bg_color)  # Remove background color from frame
        self.letter_buttons_frame.pack(pady=(20, 40))  # Increased padding to move buttons further down

        self.create_letter_buttons()

        # Reset the hangman state and image
        self.canvas.delete("all")  # Clear the canvas
        self.canvas.create_image(100, 250, image=self.stand_photo_image, anchor=tk.S)  # Show initial hangman stand image
        self.update_hangman(self.game.attempts_left)




# Example usage:
if __name__ == "__main__":
    # categories
    fruits = ["apple", "banana", "cherry", "date", "elderberry"]
    coding = ["python", "psudeocode", "development", "code", "programming"]
    places = ["allston", "fenway", "brookline", "cambridge", "boston"]

    fruitsBank = WordBank(fruits)
    placesBank = WordBank(places)
    codingBank = WordBank(coding)
    allBank = WordBank(fruits + places + coding)
    
    root = tk.Tk()
    game_ui = HangmanUI(root)
    root.mainloop()
