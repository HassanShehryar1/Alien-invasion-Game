import pygame
from pygame.sprite import Sprite



class Ship(Sprite):
    def __init__(self, ai_game):
        """Initialize the ship and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings=ai_game.setting
        self.screen_rect = ai_game.screen.get_rect()

        # Load the ship image
        self.image = pygame.image.load(ai_game.resource_path("ship.bmp"))
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        self.x=float(self.rect.x)
        self.y=float(self.rect.y)

        self.moving_right=False
        self.moving_left = False
        self.moving_up=False
        self.moving_down=False


    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)
    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        

        self.rect.x=self.x
        self.rect.y=self.y

    def center_ship(self):
        self.rect.midbottom=self.screen_rect.midbottom
        self.x=float(self.rect.x)