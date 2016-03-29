import pygame
from pygame.sprite import Sprite


class Enemy(Sprite):
    def __init__(self, game_settings, screen):
        """
        Initialize the enemy and set its starting position
        :param game_settings:
        :param screen:
        :return:
        """
        super(Enemy, self).__init__()
        self.screen = screen
        self.game_settings = game_settings

        # Load the enemy image and sets its rect attributes
        self.image = pygame.image.load('images/xwing.png')
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the enemy's exact position
        self.x = float(self.rect.x)

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        # Move enemy to the right
        self.x += (self.game_settings.enemy_speed_factor * self.game_settings.fleet_direction)
        self.rect.x = self.x

    def blitme(self):
        # Draw the enemy at its current location
        self.screen.blit(self.image, self.rect)
