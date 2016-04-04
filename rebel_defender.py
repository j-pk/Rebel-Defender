import pygame
from pygame.sprite import Group


from settings import Settings
from ship import Ship
from icon_ship import IconShip
from starfield import Starfield
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
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

    # Make play button
    play_button = Button(game_settings, screen, "Play")

    # Store game statistics
    stats = GameStats(game_settings)

    # Scoreboard
    sb = Scoreboard(game_settings, screen, stats)

    # Make a ship
    ship = Ship(game_settings, screen)
    icon_ship = IconShip(game_settings, screen)

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

        gf.check_events(game_settings, stats, sb, screen, ship, enemies, bullets, play_button)

        if stats.game_active:
            ship.update()
            gf.update_bullets(game_settings, screen, stats, sb, ship, enemies, bullets)
            gf.update_enemies(game_settings, stats, screen, sb, ship, enemies, bullets)

        gf.update_screen(game_settings, screen, stats, sb, starfield, ship, enemies, bullets, play_button)

run_game()
