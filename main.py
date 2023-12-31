from flask import *
from json import *
from flask_cors import CORS

import settings
from HangmanGame import HangmanGame

app = Flask(__name__)
app.secret_key = 'any random string'
settings = settings.Settings()
CORS(app)

@app.route('/create_game/{username}', methods=['POST'])
def create_game(username: str):
    game = HangmanGame(settings)
    state = game.create_game(username)




    res.headers.add('Access-Control-Allow-Origin', '*')
    return res


@app.route('/process_letter/<string:game_id>/<string:letter>', methods=['GET'])
def process_letter(game_id, letter):
    # Get the game from the file
    with open('game_data.json', 'r') as file:
        game_dump = file.read()

    if game_dump:
        game_dict = json.loads(game_dump)
        game = HangmanGame(**game_dict)

        new_state = game.process_letter(str(letter))

        # Save the game back to the file
        game_dump = json.dumps(game.__dict__)
        with open('game_data.json', 'w') as file:
            file.write(game_dump)

        return jsonify(new_state.serialize())
    return 'error - game not found'



if __name__ == '__main__':
    app.run()

# from CreateGame import CreateGame


# if '__main__' == __name__:
#    game = CreateGame()
#    s = game.create_game()
#    while s.game_status == 'ongoing':
#        letter = input('letter: ')
#        s = game.process_letter(letter)
#        print('Current word: ' + str(s.current_word))
#        print('Attempts left: ' + str(s.attempts))
