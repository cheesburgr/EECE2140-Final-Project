# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 11:13:58 2024

@author: lmk51
"""

import random

class WordBank:
    def __init__(self, words):
        """Initialize the WordBank with a list of words."""
        self.words = words

    def add_word(self, word):
        """Add a new word to the word bank."""
        self.words.append(word)

    def get_random_word(self):
        """Select and return a random word from the word bank."""
        if not self.words:
            return None  # Return None if the word bank is empty
        return random.choice(self.words)

# Example usage

fruits = WordBank(["apple", "banana", "cherry", "date", "elderberry"])
places = WordBank(["australia", "california", ""])

    # Get a random word
random_word = places.get_random_word()
print(f"Randomly selected word: {random_word}")
