import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, game_settings, screen):
        """
        Initialize the ship and set its starting position
        """
        super(Ship, self).__init__()
        self.screen = screen
        self.game_settings = game_settings

        # Load the ship image and get its rect
        self.image = pygame.image.load('images/m_falcon.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start each new ship at the bottom center of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom - 5

        # Store decimal value of ship's center
        self.center = float(self.rect.centerx)
        self.bottom = float(self.rect.bottom)

        # Movement flag
        self.moving_right = False
        self.moving_left = False
        self.moving_forward = False
        self.moving_backward = False

        # Set movement parameters
        self.moving_foward_parameter = self.screen_rect.bottom - 75
        self.moving_backward_parameter = self.screen_rect.bottom - 5

    def update(self):
        # Update ship position based on movement flag
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.game_settings.ship_speed_factor

        if self.moving_left and self.rect.left > 0:
            self.center -= self.game_settings.ship_speed_factor

        if self.moving_forward and self.rect.bottom > self.moving_foward_parameter:
            self.bottom -= self.game_settings.ship_speed_factor

        if self.moving_backward and self.rect.bottom < self.moving_backward_parameter:
            self.bottom += self.game_settings.ship_speed_factor

        # Update rect object from self.center
        self.rect.centerx = self.center
        self.rect.bottom = self.bottom

    def center_ship(self):
        self.center = self.screen_rect.centerx

    def blitme(self):
        """
        Draw the ship at its current location
        """
        self.screen.blit(self.image, self.rect)
