import pygame
from pygame.sprite import Sprite


class IconShip(Sprite):
    def __init__(self, game_settings, screen):
        """
        Initialize the ship and set its starting position
        """
        super(IconShip, self).__init__()
        self.screen = screen
        self.game_settings = game_settings

        # Load the ship image and get its rect
        self.image = pygame.image.load('images/m_falcon.png').convert()
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.size = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(self.size[0]/2), int(self.size[1]/2)))

    def blitme(self):
        """
        Draw the ship at its current location
        """
        self.screen.blit(self.image, [100, 100])