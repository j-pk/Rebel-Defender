class GameStats():
    """
    Track statistics for Rebel Defender
    """

    def __init__(self, game_settings):
        self.game_settings = game_settings
        self.reset_stats()
        self.game_active = True

    def reset_stats(self):
        # Initialize statistics that can change in the game
        self.ships_left = self.game_settings.ship_limit