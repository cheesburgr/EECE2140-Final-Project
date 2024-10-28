# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 11:56:32 2024

@author: lmk51
"""

import random

class wordPicker:
    animals = ['Dog',
               'Cat', 
               'Iguana',
               'Elephant',
               '',
               '',
               '',
               '',
               '',
               '',
               '',
               '',
               ]
    food = ['', 
            '', 
            '']
    countries = ['', 
            '', 
            '']
    
    def __init__(self, category):
        self.category = category
        if category.lower() == "animals":
            self.category = self.animals
        if category.lower() == 'food':
            self.category = self.food
        if category.lower() == 'countries':
            self.category = self.countries
        if category.lower() == 'all':
            self.category = self.countries + self.animals + self.food
    
    @classmethod
    def printBank():
        print(self.wordBank)
        
        
choose = wordPicker()