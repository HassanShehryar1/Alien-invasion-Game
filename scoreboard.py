import pygame.font
from pygame.sprite import Group
from ship_module import Ship

class ScoreBoard():

    def __init__(self, ai_game):

        self.ai_game=ai_game    
        self.screen = ai_game.screen
        self.screen_rect=self.screen.get_rect()
        self.setting= ai_game.setting
        self.stats=ai_game.stats

        self.text_color=(30,30,30)
        self.font=pygame.font.SysFont(None, 48)

        self.prep_score()
        self.prep_HighScore()
        self.prepLevel()
        self.prepShips()

    def prepShips(self):
        self.ships=Group()

        for shipNumber in range(self.stats.ships_left):
            ship=Ship(self.ai_game)
            ship.rect.x=10 + shipNumber * ship.rect.width
            ship.rect.y=10
            self.ships.add(ship)

    def prepLevel(self):
        level_str=str(self.stats.level)
        self.level_image=self.font.render(level_str,True,self.text_color,self.setting.bg_Color)

        self.level_rect=self.level_image.get_rect()
        self.level_rect.right=self.score_rect.right
        self.level_rect.top=self.score_rect.bottom + 10

    def prep_HighScore(self):
        highScore=round(self.stats.highScore,-1)
        highScore_str=f"{highScore:,}"
        self.highScore_image=self.font.render(highScore_str,True,self.text_color,self.setting.bg_Color)

        self.highScore_image_rect=self.highScore_image.get_rect()
        self.highScore_image_rect.centerx=self.screen_rect.centerx
        self.highScore_image_rect.top= self.score_rect.top

    def prep_score(self):
        rounded_score=round(self.stats.score,-1)
        score_str=f"{rounded_score:,}"
        score_str=str(self.stats.score)
        self.score_image= self.font.render(score_str,True,self.text_color,self.setting.bg_Color)

        self.score_rect= self.score_image.get_rect()
        self.score_rect.right=self.screen_rect.right - 20
        self.score_rect.top=20

    def check_HighScore(self):
        if self.stats.score > self.stats.highScore:
            self.stats.highScore=self.stats.score
            self.prep_HighScore()

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.highScore_image,self.highScore_image_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)