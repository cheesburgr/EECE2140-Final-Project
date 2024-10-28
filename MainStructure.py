import random



# chosen_word = random.choice(word_list)

guessed_letters = set()

max_attempts = 6
attempts = 0

def display_hangman(attempts):
    stages = [
        """  -----
          |   |
          |   O
          |  /|\\
          |  / \\
          |
        """,
        """  -----
          |   |
          |   O
          |  /|\\
          |  /
          |
        """,
        """  -----
          |   |
          |   O
          |  /|
          |
          |
        """,
        """  -----
          |   |
          |   O
          |
          |
          |
        """,
        """  -----
          |   |
          |
          |
          |
          |
        """,
        """  -----
          |
          |
          |
          |
          |
        """,
        """  
        """
    ]
    return stages[attempts]

def display_word(chosen_word, guessed_letters):
    return "" #Still need to implement

def main():
    global attempts
    print("Welcome to Hangman!")
    
    while attempts < max_attempts:
        print(display_hangman(attempts))
        print(display_word(chosen_word, guessed_letters))
        
        guess = input("Guess a letter: ").lower()
        
        if len(guess) != 1 or not guess.isalpha():
            print("Please enter a single letter.")
            continue
        
        if guess in guessed_letters:
            print("You've already guessed that letter.")
            continue
        
        guessed_letters.add(guess)
        
        if guess not in chosen_word:
            attempts += 1
        
        if all(letter in guessed_letters for letter in chosen_word):
            print(f"Congratulations! You've guessed the word: {chosen_word}")
            break
    else:
        print(display_hangman(attempts))
        print(f"Sorry, you've run out of attempts! The word was: {chosen_word}")


