from random import randrange, choice


class Starfield:
    def __init__(self, game_settings):
        """
        Initialize starfield
        :param screen:
        :return:
        """
        self.game_settings = game_settings


    def generate_starfield(self):
        starfield = []
        for index in range(self.game_settings.max_stars):
            star = [randrange(0, self.game_settings.screen_width - 1), randrange(0, self.game_settings.screen_height - 1), choice([1, 2, 3])]
            starfield.append(star)
        return starfield

