import random
from json import JSONEncoder

from gamestate import GameState


def get_word():
    with open('dictionary.txt', 'r') as file:
        dictionary = file.read().split(', ')
    word = random.choice(dictionary)
    return word


class HangmanGame:
    def __init__(self):
        self.current_word = ''
        self.attempts = 0
        self.game_id = 0
        self.letter = ''

    def get_game_satus(self):
        if self.word == self.current_word:
            return 'won'
        elif self.attempts == 0:
            return 'lost'
        else:
            return 'ongoing'

    # API method
    def create_game(self):

        self.word = get_word()
        print(len(self.word) * '_')
        self.current_word = '_' * len(self.word)
        self.attempts = 6
        self.game_id += 1

        gamestate = GameState(self.game_id, self.get_game_satus(), self.current_word, self.attempts)
        return gamestate

    def set_letter(self, letter):
        i = 0
        tempword = ''
        for item in self.word:
            if item == letter:
                tempword += letter
            else:
                tempword += self.current_word[i]
            i += 1
        return tempword

    # API call
    def process_letter(self, letter):

        if letter in self.word:
            self.current_word = self.set_letter(letter)
            print(self.current_word)
        else:
            self.attempts -= 1

        gamestate = GameState(self.game_id, self.get_game_satus(), self.current_word, self.attempts)
        return gamestate
