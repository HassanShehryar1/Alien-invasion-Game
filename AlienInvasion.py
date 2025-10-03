import sys
from time import sleep
import sys
import os



import pygame
from Setting import Setting
from gamestats import Gamestats
from ship_module import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from scoreboard import ScoreBoard


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.game_active=True
        self.setting = Setting()
        self.clock = pygame.time.Clock()

        self.game_active=False
        self.paused=False

        # Create the screen FIRST
        self.screen = pygame.display.set_mode(
            (self.setting.screen_width, self.setting.screen_height)
        )
        pygame.display.set_caption("Alien Invasion")

        # for play button
        self.play_button=Button(self,'Play')

        #for game stats
        self.stats=Gamestats(self)
        self.sb=ScoreBoard(self)

        # Now create the ship
        self.ship = Ship(self)
        self.bullets=pygame.sprite.Group()
        self.aliens=pygame.sprite.Group()
        self.create_fleet()
    
    @staticmethod
    def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)


    def check_alien_bottom(self):
        for alien in self.aliens.sprites():
            if alien.rect.bottom>=self.setting.screen_height:
                self.ship_hit()
                break
                

    def ship_hit(self):
        if self.stats.ships_left>0:

            self.stats.ships_left-=1
            self.sb.prepShips()

            self.bullets.empty()
            self.aliens.empty()

            self.create_fleet()
            self.ship.center_ship()

            sleep(0.5)
        else:
            self.game_active=False
            pygame.mouse.set_visible(True)
            

            


    def create_fleet(self):

        alien=Alien(self)
        alien_width, alien_height=alien.rect.size

        current_x , current_y =alien_width, alien_height
        
        maxAlienRows=4
        currentRows=0

        while currentRows < maxAlienRows and current_y <(self.setting.screen_height-3*alien_height):
            while current_x < (self.setting.screen_width - 2* alien_width):
                self.create_alien(current_x,current_y)
                current_x+= 2* alien_width
            current_x=alien_width
            current_y+=2+alien_height
            currentRows+=1

    def create_alien(self, x_position, y_position):
        newAlien=Alien(self)
        newAlien.x=x_position 
        newAlien.rect.x=x_position
        newAlien.rect.y=y_position
        self.aliens.add(newAlien)


    def run_game(self):
        """Start the main loop for the game."""
        while True:
            # Watch for keyboard and mouse events.
            self.check_events()
            if self.game_active and not self.paused:
                self.ship.update()
                self.update_bullets()
                self.update_aliens()
            self.update_screen()
            self.clock.tick(60)

    def update_aliens(self):
        self.check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self.ship_hit()
        self.check_alien_bottom()



    def check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self.change_fleet_direction()
                break   # break ONLY after a change

    def change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.setting.fleet_drop_speed
        self.setting.fleet_direction *= -1

    
    

    def check_events(self):
        """Handle keyboard and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.check_keyDown(event)
            elif event.type == pygame.KEYUP:
                self.check_keyUp(event)
            elif event.type==pygame.MOUSEBUTTONDOWN:
                mouse_pos=pygame.mouse.get_pos()
                self.check_play_button(mouse_pos)
            

            
    def check_play_button(self,mouse_pos):
        button_clicked= self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self.setting.initialize_dynamic_setting()
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prepLevel()
            self.sb.prepShips()
            
            self.game_active=True

            self.aliens.empty()
            self.bullets.empty()

            self.create_fleet()
            self.ship.center_ship()

            pygame.mouse.set_visible(False)

            
                

    def check_keyDown(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        
        elif event.key== pygame.K_q:
                sys.exit()
        elif event.key == pygame.K_SPACE:
            self.fire_bullet()
        elif event.key == pygame.K_ESCAPE:
            if self.game_active and not self.paused:
                self.paused=True
                pygame.mouse.set_visible(self.paused)
            elif self.paused:
                self.paused=False
                pygame.mouse.set_visible(self.paused)

    def check_keyUp(self,event):
        if event.key == pygame.K_RIGHT:
           self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        
        

    def fire_bullet(self):
        if len(self.bullets) < self.setting.bulletsAllowed:
            newBullet=Bullet(self)
            self.bullets.add(newBullet)

    def update_bullets(self):
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <=0:
                self.bullets.remove(bullet)

        self.check_bullet_alien_collision()
        

    def check_bullet_alien_collision(self):
        collisions=pygame.sprite.groupcollide(self.bullets,self.aliens,True,True)

        if not self.aliens:
            self.bullets.empty()
            self.create_fleet()
            self.setting.increase_speed()

            self.stats.level+=1
            self.sb.prepLevel()

        if collisions:
            self.stats.score+=self.setting.alien_points
            self.sb.prep_score()
            self.sb.check_HighScore()
    
    def update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        # Redraw the screen each pass through the loop
        self.screen.fill(self.setting.bg_Color)

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        self.sb.show_score()

        if not self.game_active:
            self.play_button.draw_button()
        elif self.paused:
            # Draw pause overlay or text here
            font = pygame.font.SysFont(None, 48)
            pause_text = font.render("Paused", True, (255, 0, 0))
            text_rect = pause_text.get_rect(center=self.screen.get_rect().center)
            self.screen.blit(pause_text, text_rect)

        # Make the most recently drawn screen visible.
        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()