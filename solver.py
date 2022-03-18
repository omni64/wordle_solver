import random
import re
import emoji
import json
import pickle
from wordfreq import word_frequency
from time import sleep
class WordleSolver():
    def __init__(self) -> None:
        random.seed(42)
        self.small_path = 'words.csv'
        self.large_path = 'guesses.csv'

    def load_words(self, small = False):
        wordbank = []
        if small:
            with open(self.small_path, 'r') as f:
                words = f.read()
            wordbank = words.split('\n')
            wordbank = list(map(lambda word: word.upper(), wordbank))
        else:
            with open(self.large_path, 'r') as f:
                words = f.read()
            wordbank = words.split('\n')
            wordbank = list(map(lambda word: word.upper(), wordbank))
        return wordbank

    

    def get_regex(self, guess, ans_grid):
        guess = guess.upper()
        discarded = []
        misplaced = []
        build = ''
        for i in range(5):
            if ans_grid[i] == 0:
                discarded.append(guess[i])
        for i in range(5):
            if ans_grid[i] == 2:
                build += guess[i]
            elif ans_grid[i] == 1:
                misplaced.append(guess[i])
                build += f'[^{guess[i]}{"".join(discarded)}]'
            else:
                build+= f'[^{"".join(discarded)}]'
        return build, misplaced

    def get_possible_words(self, guess, ans_grid, wordbank = []):
        if not wordbank:
            wordbank = self.load_words()
        possibilities = []
        restring, misplaced = self.get_regex(guess, ans_grid)
        for word in wordbank:
            if re.match(restring, word):
                possibilities.append(word)
        filtered = []
        for letter in misplaced:
            for word in possibilities:
                if letter not in word:
                    filtered.append(word)
        for word in set(filtered):
            possibilities.remove(word)
        possibilities = sorted(possibilities, key=lambda x: word_frequency(x, 'en'), reverse=True)
        return possibilities
    
    def assistant(self,wordbank = [], random_word = True):
        guess = input('Please enter guess : ')
        ans_grid = input('Please enter answer grid:\n0 - letter not in word\n1 - letter in word but wrong position\n2 - letter in correct position:\n')
        ans_grid = list(map(lambda x: int(x), list(ans_grid)))
        possible = self.get_possible_words(guess, ans_grid, wordbank)
        if len(possible) == 1 or sum(ans_grid) == 10:
            print('Congratulations. The answer is :', possible[0])
            sleep(2)
            exit()
        if len(possible) > 15:
            if random_word:
                print(f'{len(possible)} possibilities. Choosing random word: {random.choice(possible)}')
            else:
                print(f'{len(possible)} possibilities. Choosing most frequent word: {possible[0]}')
        else:
            print(f'{len(possible)} possibilities:\n{possible} ')
        proceed = input('Continue? (Y/N): ')
        
        if proceed.upper() == 'Y':
            self.assistant(possible)
        else:
            print("Thanks for playing")
            sleep(2)

if __name__ == '__main__':
    solver = WordleSolver()
    solver.assistant()