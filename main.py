from flask import *
from json import *

from HangmanGame import HangmanGame

app = Flask(__name__)
app.secret_key = 'any random string'


@app.route('/create_game', methods=['GET'])
def create_game():
    game = HangmanGame()
    state = game.create_game()
    game_dump = json.dumps(game.__dict__)

    # Write game_dump into a file
    with open('game_data.json', 'w') as file:
        file.write(game_dump)
    res = jsonify(json.dumps(state.__dict__))

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
