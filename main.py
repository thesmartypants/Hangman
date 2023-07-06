from flask import *

from HangmanGame import HangmanGame

app = Flask(__name__)
app.secret_key = 'any random string'


@app.route('/create_game', methods=['GET'])
def create_game():
    game = HangmanGame()
    state = game.create_game()
    game_dump = json.dumps(game.__dict__)
    #session['game '+str(game.game_id)] = game_dump
    session['game'] = game_dump
    session.modified = True
    #return jsonify(state.serialize())
    return jsonify(json.dumps(state.__dict__))


@app.route('/process_letter/<string:game_id>/<string:letter>', methods=['GET'])
def process_letter(game_id, letter):
    #game_dump = session.get('game '+str(game_id))
    #game_dump = session.get('game')
    game_dump = session['game']
    if game_dump:
        game_dict = json.loads(game_dump)
        game = HangmanGame(**game_dict)
        processed_letter = game.process_letter(str(letter))
        return jsonify(processed_letter.serialize())
    return 'error - game not found'


if __name__ == '__main__':
    app.run()


# from HangmanGame import HangmanGame


# if '__main__' == __name__:
#    game = HangmanGame()
#    s = game.create_game()
#    while s.game_status == 'ongoing':
#        letter = input('letter: ')
#        s = game.process_letter(letter)
#        print('Current word: ' + str(s.current_word))
#        print('Attempts left: ' + str(s.attempts))
