import unittest

from HangmanGame import HangmanGame
from database import Database
from settings import Settings


class TestHangmanGame(unittest.TestCase):
    #conn_str = 'user=postgres password=postgres host=127.0.0.1 port=5432 dbname=tst_hangman_game'
    def setUp(self):
        self.settings = Settings()
        self.settings.CONNECTION_STR='user=postgres password=postgres host=127.0.0.1 port=5432 dbname=tst_hangman_game'
        self.settings.DICTIONARY_PATH = '../dictionary.txt'
        db = Database(self.settings.CONNECTION_STR)
        db.init_db()

    def tearDown(self):
        db = Database(self.settings.CONNECTION_STR)
        db.delete_all_tables()
    def test_set_letter(self):
        self.assertEqual(True, False)  # add assertion here

    def test_process_letter_loss(self):
        hg = HangmanGame(self.settings)
        game_id = hg.create_game("Alex")
        db = Database(self.settings.CONNECTION_STR)
        game = db.get_game(game_id)
        word = game['word']
        attempts = game['attempts']
        status = game['game_status']
        # is status ongoing?
        self.assertEqual(status, "ongoing")


        # pass correct letter
        hg.process_letter(game_id, word[1])

        game = db.get_game(game_id)
        attempts = game['attempts']
        status = game['game_status']

        # is status ongoing?
        self.assertEqual(status, "ongoing")
        # did attempts decrement?
        self.assertEqual(attempts, 6)


        #pass incorrect letters
        for i in range(len(word)-1):
            alpha = "qwertyuiopasdfghjklzxcvbnm"
            for wrong_letter in alpha:
                if wrong_letter not in word:
                    hg.process_letter(game_id, wrong_letter)
                    break

        game = db.get_game(game_id)
        attempts = game['attempts']
        status = game['game_status']
        # is status ongoing?
        self.assertEqual(status, "lost")
        # did attempts decrement?
        self.assertEqual(attempts, 0)



    def test_process_letter_win(self):
        hg = HangmanGame(self.settings)
        game_id = hg.create_game("Alex")
        db = Database(self.settings.CONNECTION_STR)
        game = db.get_game(game_id)
        word = game['word']
        attempts = game['attempts']
        status = game['game_status']
        # is status ongoing?
        self.assertEqual(status, "ongoing")

        #pass incorrect letter
        alpha = "qwertyuiopasdfghjklzxcvbnm"
        for letter in alpha:
            if letter not in word:
                hg.process_letter(game_id, letter)
                break

        game = db.get_game(game_id)
        attempts = game['attempts']
        status = game['game_status']
        # is status ongoing?
        self.assertEqual(status, "ongoing")
        # did attempts decrement?
        self.assertEqual(attempts, 5)


        # pass correct letters
        for correct_letter in word:
            hg.process_letter(game_id, correct_letter)

        game = db.get_game(game_id)
        attempts = game['attempts']
        status = game['game_status']

        # is status ongoing?
        self.assertEqual(status, "won")
        # did attempts decrement?
        self.assertEqual(attempts, 5)






if __name__ == '__main__':
    unittest.main()
