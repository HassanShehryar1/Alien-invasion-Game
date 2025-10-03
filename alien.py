import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    def __init__(self,ai_game):
        super().__init__()

        self.screen=ai_game.screen
        self.setting=ai_game.setting

        self.image=pygame.image.load(ai_game.resource_path("alien.bmp"))
        self.rect=self.image.get_rect()

        self.rect.x=self.rect.width
        self.rect.y=self.rect.height

        self.x=float(self.rect.x)
    
    def check_edges(self):
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)


    def update(self):
    # Move the alien right or left.
        self.x += self.setting.alien_speed * self.setting.fleet_direction
        self.rect.x = self.x

        
