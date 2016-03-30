class Settings:
    # A class to store all settings for Alien Invasion

    def __init__(self):
        # Initialize the game's settings.
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)

        # Ship settings
        self.ship_speed_factor = 1.5
        self.ship_limit = 3

        # Enemy settings
        self.enemy_speed_factor = 1
        self.fleet_drop_speed = 100
        # 1 right, -1 left
        self.fleet_direction = 1

        # Bullet settings
        self.bullet_speed_factor = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (0, 94, 237)
        self.bullet_allowed = 3

        # Starfield settings
        self.max_stars = 150
        self.star_speed = 2
