import unittest

from database import Database


class MyTestCase(unittest.TestCase):
    conn_str = 'user=postgres password=postgres host=127.0.0.1 port=5432 dbname=tst_hangman_game'

    def setUp(self):
        db = Database(self.conn_str)
        db.init_db()

    def tearDown(self):
        db = Database(self.conn_str)
        db.delete_all_tables()

    def test_insert_read(self):

        db = Database(self.conn_str)
        game_id = db.create_game(6,'cat','Alex')
        game = db.get_game(game_id)

        self.assertEqual(game['attempts'], 6)  # add assertion here
        print(game)

    def test_insert_update(self):
        db = Database(self.conn_str)
        game_id = db.create_game(6,'cat','Alex')
        game = db.get_game(game_id)
        self.assertEqual(game['attempts'], 6)

        db.update_game(game_id, 5, game['current_word'], game['game_status'])
        game = db.get_game(game_id)
        self.assertEqual(game['attempts'], 5)

if __name__ == '__main__':
    unittest.main()
