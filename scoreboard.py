import pygame.font
from pygame.sprite import Group

from icon_ship import IconShip


class Scoreboard:
    def __init__(self, game_settings, screen, stats):
        self.game_setting = game_settings
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.stats = stats

        self.text_color = (30, 255, 30)
        self.font = pygame.font.SysFont(None, 48)

        self.score_rect = None
        self.score_string = None
        self.score_image = None
        self.high_score_image = None
        self.high_score_rect = None
        self.level_rect = None
        self.level_image = None

        self.prep_score()
        self.prep_high_score()
        self.prep_level()

        self.ships = Group()

    def prep_score(self):
        rounded_score = int(round(self.stats.score, -1))
        self.score_string = "{:,}".format(rounded_score)
        self.score_image = self.font.render(self.score_string, True, self.text_color, self.game_setting.bg_color)

        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        high_score = int(round(self.stats.high_score, -1))
        high_score_string = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_string, True, self.text_color, self.game_setting.bg_color)

        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        self.level_image = self.font.render(str(self.stats.level), True, self.text_color,
                                            self.game_setting.bg_color)

        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        for ship_number in range(self.stats.ships_left):
            ship = IconShip(self.game_setting, self.screen)
            ship.rect.x = 10 + ship_number * (ship.rect.width / 2)
            ship.rect.y = 10
            self.ships.add(ship)

    def remove_ships(self):
        self.ships.remove(self.ships, self)

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)
