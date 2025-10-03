class Setting:
    def __init__(self):
        """Initialize the game's settings."""
        self.screen_width = 800
        self.screen_height = 600
        self.bg_Color = (230, 230, 230)  # light gray
        self.ship_limit=3

        self.fleet_drop_speed = 10

        
        self.bullet_width=3
        self.bullet_height=14
        self.bullet_color=(128,0,128)
        self.bulletsAllowed=5

        self.speedup_scale=1.1
        self.score_scale=1.5

        self.initialize_dynamic_setting()

    def initialize_dynamic_setting(self):
        self.alien_speed = 1.0
        self.bullet_speed=2.5
        self.ship_speed=1.5

        self.fleet_direction = 1  # 1 = right, -1 = left

        self.alien_points=50

    def increase_speed(self):
        self.alien_speed *= self.speedup_scale
        self.bullet_speed *=self.speedup_scale
        self.ship_speed *=self.speedup_scale

        self.alien_points=int(self.alien_points*self.score_scale)



    






