class GameState:

    def __init__(self, game_id, game_status, current_word, attempts):
        self.current_word = current_word
        self.attempts = attempts
        self.game_status = game_status
        self.game_id = game_id

    def serialize(self):
        return {"game_id": self.game_id,
                "current_word": self.current_word,
                "game_status": self.game_status,
                "attempts": self.game_status}
