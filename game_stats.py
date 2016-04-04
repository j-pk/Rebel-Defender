import shelve


class GameStats:
    """
    Track statistics for Rebel Defender
    """

    def __init__(self, game_settings):
        self.game_settings = game_settings
        self.reset_stats()
        self.game_active = False
        self.get_high_score()

    def reset_stats(self):
        # Initialize statistics that can change in the game
        self.ships_left = self.game_settings.ship_limit
        self.score = 0
        self.level = 1

    def get_high_score(self):
        get_score = shelve.open('score.txt')
        if 'score' in get_score:
            test = get_score['score']
            self.high_score = get_score['score']
        else:
            get_score['score'] = 0
        get_score.close()
