import random
from json import JSONEncoder

from gamestate import GameState
from database import *
from settings import Settings


class HangmanGame:

    def __init__(self, settings: Settings):
        self.settings=settings
        self.db = Database(settings.CONNECTION_STR)
        self.initial_attempts = 6

    def get_new_word(self) -> str:
        with open(self.settings.DICTIONARY_PATH, 'r') as file:
            dictionary = file.read().split(', ')
        new_word = random.choice(dictionary)
        return new_word

    def get_game_satus(self, game_id: int):
        game = self.db.get_game(game_id)
        status = game['game_status']
        return status
        # if self.word == self.current_word:
        #     return 'won'
        # elif self.attempts == 0:
        #     return 'lost'
        # else:
        #     return 'ongoing'

    # API method
    def create_game(self, username):
        game_id = self.db.create_game(self.initial_attempts, self.get_new_word(), username)
        return game_id

    def set_letter(self, letter, word, current_word):
        i = 0
        new_current_word = ''
        for ch in word:
            if ch == letter:
                new_current_word += letter
            else:
                new_current_word += current_word[i]
            i += 1
        return new_current_word

    # API call
    def process_letter(self, game_id, letter):
        game = self.db.get_game(game_id)
        word = game["word"]
        current_word = game["current_word"]
        attempts = game["attempts"]

        if letter in word:
            current_word = self.set_letter(letter, word, current_word)
        else:
            attempts -= 1

        if attempts < 1:
            status = "lost"
        elif current_word == word:
            status = "won"
        else:
            status = "ongoing"
        self.db.update_game(game_id, attempts, current_word, status)

        return status
