import pygame
from pygame.sprite import Group


from settings import Settings
from ship import Ship
from starfield import Starfield
import game_functions as gf


def run_game():
    """
    Initialize game and create a screen object
    """
    pygame.init()
    game_settings = Settings()
    screen = pygame.display.set_mode((game_settings.screen_width, game_settings.screen_height))
    pygame.display.set_caption("Rebel Defender")
    clock = pygame.time.Clock()

    # Make a ship
    ship = Ship(game_settings, screen)

    # Make a a group of enemies
    enemies = Group()
    gf.create_fleet(game_settings, screen, ship, enemies)

    # Make a cache of bullets
    bullets = Group()

    # Make starfield
    starfield = Starfield(game_settings).generate_starfield()

    # Start the main loop of the game
    while True:
        clock.tick(50)

        gf.check_events(game_settings, screen, ship, bullets)
        ship.update()
        gf.update_bullets(bullets)
        gf.update_enemies(game_settings, enemies)
        gf.update_screen(game_settings, screen, starfield, ship, enemies, bullets)

run_game()
