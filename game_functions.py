import shelve
import sys
import pygame

from bullet import Bullet
from enemy import Enemy
from random import randrange, choice
from time import sleep


def check_events(game_settings, stats,sb, screen, ship, enemies, bullets, play_button):
    """
     Watch for keyboard and mouse events
     :param ship:
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, game_settings, screen, ship, bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(game_settings, screen, stats, sb, play_button, ship, enemies, bullets, mouse_x, mouse_y)


def check_play_button(game_settings, screen, stats, sb, play_button, ship, enemies, bullets, mouse_x, mouse_y):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)

    if button_clicked and not stats.game_active:
        pygame.mouse.set_visible(False)
        game_settings.initialize_dynamic_settings()
        stats.game_active = True

        enemies.empty()
        bullets.empty()
        stats.reset_stats()
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        create_fleet(game_settings, screen, ship, enemies)
        ship.center_ship()


def check_keydown_events(event, game_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_forward = True
    elif event.key == pygame.K_DOWN:
        ship.moving_backward = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(game_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_forward = False
    elif event.key == pygame.K_DOWN:
        ship.moving_backward = False


def update_screen(game_settings, screen, stats, sb, starfield, ship, enemies, bullets, play_button):
    """
    Update images on the screen and flip to the new screen
    :param stats:
    :param stats:
    :param starfield:
    :param bullets:
    :param enemies:
    :param ship:
    :param screen:
    :param game_settings:
    """
    # Redraw the screen each pass through the loop
    screen.fill(game_settings.bg_color)

    # Redraw all bullets behind ship and aliends
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    # Move and draw starfield
    move_and_draw_stars(starfield, screen, game_settings)
    sb.show_score()
    ship.blitme()
    enemies.draw(screen)

    if not stats.game_active:
        play_button.draw_button()

    # Make the most recently draw screen visible
    pygame.display.flip()


def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def update_bullets(game_settings, screen, stats, sb, ship, enemies, bullets):
    """
    Update position of bullets and get rid of old bullets
    """
    bullets.update()

    check_bullet_collisions(game_settings, screen, stats, sb, ship, enemies, bullets)

    # Remove bullets as they disappear
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)


def fire_bullet(game_settings, screen, ship, bullets):
    # Create a new bullet and add it to bullets group
    if len(bullets) < game_settings.bullet_allowed:
        new_bullet = Bullet(game_settings, screen, ship)
        bullets.add(new_bullet)


def check_bullet_collisions(game_settings, screen, stats, sb, ship, enemies, bullets):
    # Check for bullets that hit an enemy
    collisions = pygame.sprite.groupcollide(bullets, enemies, True, True)

    if collisions:
        for enemies in collisions.values():
            stats.score += game_settings.points + len(enemies)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(enemies) == 0:
        bullets.empty()
        game_settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(game_settings, screen, ship, enemies)


def move_and_draw_stars(starfield, screen, game_settings):
    for star in starfield:
        star[1] += star[2]

        if star[1] >= game_settings.screen_height:
            star[1] = 0
            star[0] = randrange(0, 1199)
            star[2] = choice([1, 2, 3])

        if star[2] == 1:
            color = (100, 100, 100)
        elif star[2] == 2:
            color = (190, 190, 190)
        elif star[2] == 3:
            color = (255, 255, 255)

        screen.fill(color, (star[0], star[1], star[2], star[2]))


def get_number_rows(game_settings, ship_height, enemy_height):
    # Determine the number of rows
    available_space_y = (game_settings.screen_height - (3 * enemy_height) - ship_height)
    number_rows = int(available_space_y / (2 * enemy_height))
    return number_rows


def get_number_enemies_x(game_settings, enemy_width):
    # Detemine the number of enemies in a row
    available_space_x = game_settings.screen_width - 2 * enemy_width
    number_enemy_x = int(available_space_x / (2 * enemy_width))
    return number_enemy_x


def create_enemy(game_settings, screen, enemies, enemy_number, row_number):
    enemy = Enemy(game_settings, screen)
    enemy_width = enemy.rect.width
    enemy.x = enemy_width + 2 * enemy_width * enemy_number
    enemy.rect.x = enemy.x
    enemy.rect.y = enemy.rect.height + 2 * enemy.rect.height * row_number
    enemies.add(enemy)


def create_fleet(game_settings, screen, ship, enemies):
    """
    Create a full fleet of enemies
    :param ship:
    :param game_settings:
    :param screen:
    :param enemies:
    :return:
    """
    enemy = Enemy(game_settings, screen)
    number_enemies_x = get_number_enemies_x(game_settings, enemy.rect.width)
    number_rows = get_number_rows(game_settings, ship.rect.height, enemy.rect.height)

    for row_number in range(number_rows):
        for enemy_number in range(number_enemies_x):
            create_enemy(game_settings, screen, enemies, enemy_number, row_number)


def check_fleet_edges(game_settings, enemies):
    for enemy in enemies.sprites():
        if enemy.check_edges():
            change_fleet_direction(game_settings, enemies)
            break


def change_fleet_direction(game_settings, enemies):
    for enemy in enemies.sprites():
        enemy.rect.y += game_settings.fleet_drop_speed
    game_settings.fleet_direction *= -1


def check_enemies_bottom(game_settings, stats, screen, sb, ship, enemies, bullets):
    # Check if enemies reach the bottom of the screen
    screen_rect = screen.get_rect()
    for enemy in enemies.sprites():
        if enemy.rect.bottom >= screen_rect.bottom:
            ship_hit(game_settings, stats, screen, sb, ship, enemies, bullets)
            break


def update_enemies(game_settings, stats, screen, sb, ship, enemies, bullets):
    # Update the position of all enemies
    check_fleet_edges(game_settings, enemies)
    check_enemies_bottom(game_settings, stats, screen, sb, ship, enemies, bullets)
    enemies.update()

    # Detect enemy-ship collisions
    if pygame.sprite.spritecollideany(ship, enemies):
        ship_hit(game_settings, stats, screen, sb, ship, enemies, bullets)


def ship_hit(game_settings, stats, screen, sb, ship, enemies, bullets):
    if stats.ships_left > 0:
        # Respond to ship being hit by an enemy
        stats.ships_left -= 1
        sb.remove_ships()
        sb.prep_ships()

        # Empty the list of enemies and bullets
        enemies.empty()
        bullets.empty()

        # Create a new fleet
        create_fleet(game_settings, screen, ship, enemies)
        ship.center_ship()

        # Pause
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
        save_high_score(stats)


def save_high_score(stats):
    store_score = shelve.open('score.txt')
    store_score['score'] = stats.high_score
    store_score.close()

