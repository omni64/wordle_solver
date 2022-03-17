import pickle
import nltk
from nltk.util import ngrams
import string
from copy import deepcopy as copy
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from matplotlib import rcParams
import matplotlib.gridspec as gridspec
rcParams['figure.figsize'] = (12,9)
rcParams['figure.facecolor'] = '#d9cbd7'
from wordfreq import word_frequency
from tqdm import tqdm
import re
import random
random.seed = 42


def sort_dict(dictionary:dict):
    return dict(sorted(dictionary.items() , key=lambda x: dictionary.get(x[0]), reverse=True))




with open('guesses.csv', 'r') as f:
    words = f.read()
wordbank = words.split('\n')
wordbank = list(map(lambda word: word.upper(), wordbank))
selected =[]
with open('words.csv', 'r') as f:
    words = f.read()
selected = words.split('\n')
selected = list(map(lambda word: word.upper(), selected))




def get_diff(guess, answer):
    ans_grid=[0]*5
    guess = list(guess.upper())
    answer = list(answer.upper())
    idx = 0
    while len(guess) > 0:
        letter = guess.pop(0)
        if letter in answer:
            if answer.index(letter) == idx:
                ans_grid[idx] = 10
            else:
                ans_grid[idx] = 5
            answer[answer.index(letter)] = 0
        idx += 1
    return ans_grid





def get_regex(guess, ans_grid):
    guess = guess.upper()
    possibilities = []
    build = ''
    scraps = []
    for i in range(5):
        if ans_grid[i] == 10:
            build += guess[i]
        elif ans_grid[i] == 5:
            build += f'[^{guess[i]}]'
        else:
            build += '[A-Z]'
    return build









def get_possible_words(guess, ans_grid):
    possibilities = []
    restring = get_regex(guess, ans_grid)
    for word in wordbank:
        if re.match(restring, word):
            possibilities.append(word)
    return possibilities






starters = {}
for word in wordbank:
    starters[word] = []



def best_starter(answer):
    for word in tqdm(selected):
        grid = get_diff(word, answer)
        starters[word].append(len(get_possible_words(word, grid)))






for ans in tqdm(selected):
    best_starter(ans)



