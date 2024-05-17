# Imports
import json
import pygame

from sprites import *
from utilities import *

# Initialize pygame
pygame.mixer.pre_init()
pygame.init()

# Window settings
WIDTH = 1600
HEIGHT = 900
TITLE = "QuickFire"
FPS = 60

# Stages
START = 0
PLAYING = 1
END = 2

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (110,110,110)
DARKRED = (15,0,0)
RED = (255,0,0)
GROUND_COLOR = (31,0,0)


# Main game class 
class Game:

    def __init__(self):
        self.screen = pygame.display.set_mode([WIDTH, HEIGHT],pygame.FULLSCREEN)
        ''',pygame.FULLSCREEN'''
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

        self.load_assets()
        self.new_game()
        self.quicktime = False
        self.mapx = 0
        self.mapy = 0
        self.map_speed = 0
        self.reload_on = False
        self.offset = 0
        self.spawn_ticks = 0
        self.ticks = 0
        self.score = 0
        self.is_moving = False
        self.mousex = 0
        self.mousey = 0
        self.mouse_locs = []
        self.enemylocs1 = []
        self.moving_ticks = 0
        self.hurt_ticks = 0
        self.death_ticks = 0
        self.spawn_speed = 0
        self.end_ticks = 0
        self.health_note = 0
        self.spawn_note = 0
        self.start_ticks = 255
        self.startup = 0
        

    def load_assets(self):
        self.title_font = Font('assets/fonts/slkscr.ttf', 24)
        self.ttitle_font = Font('assets/fonts/slkscr.ttf', 12)
        self.subtitle_font = Font(None, 32)
        self.title_img = Image('assets/images/Title.png')
        self.fade_img = Image('assets/images/Fade.png')
        self.fade2_img = Image('assets/images/Fade.png')

        self.end_img = Image('assets/images/end_screen.png')

        self.ground = Image('assets/images/ground.png')
        self.vignette = Image('assets/images/vignette.png')
        
        self.ship_img = Image('assets/images/PlayerIdle.png')
        self.laser_img = Image('assets/images/laserBlue.png')

        self.enemy1_img = Image('assets/images/target2.png')
        self.enemy2_img = Image('assets/images/target.png')

        self.bomb_img = Image('assets/images/laserBlue.png')

        self.pew_sfx = Sound('assets/sfx/pew.ogg')
        self.boom_sfx = Sound('assets/sfx/boom.ogg')
        self.click_sfx = Sound('assets/sfx/click.ogg')
        self.reload_sfx = Sound('assets/sfx/reload.ogg')
        self.hit_sfx = Sound('assets/sfx/hit.ogg')
        self.hurt_sfx = Sound('assets/sfx/hurt.ogg')
        self.cough_sfx = Sound('assets/sfx/cough.ogg')
        self.ring_sfx = Sound('assets/sfx/ring.ogg')
        self.squelch_sfx = Sound('assets/sfx/squelch.ogg')
        self.ding_sfx = Sound('assets/sfx/ding.ogg')

        self.g1 = Image("assets/images/gun1.png")
        self.g2 = Image("assets/images/gun2.png")
        self.g3 = Image("assets/images/gun3.png")
        self.g4 = Image("assets/images/gun4.png")
        self.g5 = Image("assets/images/gun5.png")
        self.g6 = Image("assets/images/gun6.png")
        self.g7 = Image("assets/images/gun7.png")

        self.r1 = Image("assets/images/reload1.png")
        self.r2 = Image("assets/images/reload2.png")
        self.r3 = Image("assets/images/reload3.png")

        self.gun_list = [self.g1,self.g2,self.g3,self.g4,self.g5,self.g6,self.g7,self.r1,self.r2,self.r3]

        self.m1 = Image("assets/images/mult1.png")
        self.m2 = Image("assets/images/mult2.png")
        self.m3 = Image("assets/images/mult3.png")
        self.m4 = Image("assets/images/mult4.png")

        self.gun_list2 = [self.m1,self.m2,self.m3,self.m4]
        
        self.d1 = Image("assets/images/death1.png")
        self.d2 = Image("assets/images/death2.png")
        self.d3 = Image("assets/images/death3.png")
        self.d4 = Image("assets/images/death4.png")

        self.death_list = [self.d1,self.d3,self.d2,self.d4]

        self.shadow = Image("assets/images/shadow.png")
        

        self.bar = Image("assets/images/BottomBar.png")
        self.hurt_img = Image("assets/images/hurt.png")

        self.music = Music("assets/music/moosic.ogg",.5)
        self.music.play()

    def new_game(self):
        # Make the ship here so it persists across levels
        self.mapx = 0
        self.player = pygame.sprite.GroupSingle()
        self.ship = Ship(self, self.ship_img, [400, 0],10)
        self.player.add(self.ship)
        
        self.stage = START
        self.load_current_level()

        self.music = Music("assets/music/moosic.ogg",.5)
        self.music.play()

    def load_current_level(self):
        # Add enemies, powerups, etc.
        self.lasers = pygame.sprite.Group()
        self.hitpoints = pygame.sprite.Group()
        self.bombs = pygame.sprite.Group()

        self.enemies = Fleet(self)
        self.bombs = Fleet(self)
        r = random.randrange(-600,600)

        self.quicktime = False
        self.mapx = 0
        self.mapy = 0
        self.map_speed = 0
        self.reload_on = False
        self.offset = 0
        self.spawn_ticks = 0
        self.ticks = 0
        self.is_moving = False
        self.mousex = 0
        self.mousey = 0
        self.mouse_locs = []
        self.enemylocs1 = []
        self.moving_ticks = 0
        self.hurt_ticks = 0
        self.death_ticks = 0
        self.spawn_speed = 0
        self.end_ticks = 0
        self.health_note = 0
        self.spawn_note = 0
        self.start_ticks = 255
        self.startup = 0

    def start(self):
        self.stage = PLAYING
        self.mapx = -800

    def advance(self):
        self.level += 1
        self.load_current_level()
        self.start()

    def end_game(self):
        self.ring_sfx.set_volume(.2)
        self.ring_sfx.play()
        self.music = Music("assets/music/moosic.ogg",.1)
        self.music.play()
        self.hurt_sfx.set_volume(1)
        self.hurt_sfx.play()
        self.health_note = 0
        self.spawn_note = 0
        self.stage = END
        self.is_moving = False

    def show_title_screen(self):
        rect = self.title_img.get_rect()
        rect.centerx = WIDTH // 2
        rect.top = 0
        self.screen.blit(self.title_img, rect)

        text = self.title_font.render("Click To Start", True, WHITE)
        rect = text.get_rect()
        rect.centerx = WIDTH // 2
        rect.bottom = HEIGHT - (HEIGHT // 3)
        self.screen.blit(text, rect)

        text = self.title_font.render(f"Score: {self.score}", True, WHITE)
        rect = text.get_rect()
        rect.centerx = WIDTH // 2
        rect.bottom = HEIGHT - (HEIGHT // 5)
        self.screen.blit(text, rect)

    def show_end_screen(self):
        self.death_ticks += 1
        t = self.death_ticks
        if t < 10:
            self.hurt_ticks = 255
            self.mapy += 160
        elif t < 11:
            self.mapx = -800
        elif t < 20:
            self.mapy -= 150
        elif t < 30:
            self.mapy += 10
        elif t < 45:
            self.mapy -= 5
        elif t < 60:
            self.mapy -= 30
        elif t < 65:
            self.mapy -= 15
        elif t < 70:
            self.mapy -= 90

    def notify_health_up(self):
        text = self.title_font.render("Enemy Health Increased!", True, WHITE)
        rect = text.get_rect()
        rect.centerx = WIDTH // 2
        rect.bottom = HEIGHT // 3
        text.set_alpha(self.health_note)
        self.screen.blit(text, rect)

        if self.score >= 2000:
            if self.score == 2000:
                self.health_note = 500
            self.shield = 2
            
        if self.score >= 6000:
            if self.score == 6000:
                self.health_note = 500
            self.shield = 3
            
        if self.score >= 12000:
            if self.score == 12000:
                self.health_note = 500
            self.shield = 4
            
        if self.score >= 20000:
            if self.score == 20000:
                self.health_note = 500
            self.shield = 5


    def notify_spawn_up(self):
        text = self.title_font.render("Enemy Spawn Rate Increased!", True, WHITE)
        rect = text.get_rect()
        rect.centerx = WIDTH // 2
        rect.bottom = HEIGHT // 3
        text.set_alpha(self.spawn_note)
        self.screen.blit(text, rect)

        if self.score >= 500:
            if self.score == 500:
                self.spawn_note = 500
            self.spawn_speed = 20
            

        if self.score >= 1000:
            if self.score == 1500:
                self.spawn_note = 500
            self.spawn_speed = 25

        if self.score >= 2000:
            if self.score == 2500:
                self.spawn_note = 500
            self.spawn_speed = 30

        if self.score >= 3500:
            if self.score == 3500:
                self.spawn_note = 500
            self.spawn_speed = 35

        if self.score >= 5000:
            if self.score == 5000:
                self.spawn_note = 500
            self.spawn_speed = 40

        if self.score >= 7000:
            if self.score == 7000:
                self.spawn_note = 500
            self.spawn_speed = 45

        if self.score >= 9000:
            if self.score == 9000:
                self.spawn_note = 500
            self.spawn_speed = 50

        if self.score >= 11000:
            if self.score == 11000:
                self.spawn_note = 500
            self.spawn_speed = 55

        if self.score >= 13000:
            if self.score == 13000:
                self.spawn_note = 500
            self.spawn_speed = 60

    def notify_reload(self):
        text = self.ttitle_font.render("RELOAD", True, WHITE)
        rect = text.get_rect()
        rect.centerx = WIDTH // 2
        rect.bottom = HEIGHT // 2 + 23
        text.set_alpha(200)
        self.screen.blit(text, rect)

    def process_input(self):        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

            
            if self.stage == START:
                b1,b2,b3 = pygame.mouse.get_pressed(3)
                if b1 == True:
                    self.score = 0
                    pygame.mouse.set_pos(WIDTH/2,HEIGHT/2)
                    self.mapx = -800
                    self.mapy = 0
                    self.end_ticks = 0
                    
                    for enemy in self.enemies:
                        enemy.rect.centerx = WIDTH/2
                    self.start()                  
                        

            elif event.type == pygame.KEYDOWN:

                if self.stage == PLAYING:
                    if event.key == pygame.K_x:
                        self.end_game()

            if self.stage == PLAYING:
                if self.startup > 5:
                    b1,b2,b3 = pygame.mouse.get_pressed(3)
                    if b1 == True:
                        for ship in self.player:
                            if self.ship.rect.y == -75 and self.reload_on == False and self.ship.ammo > 0 and self.stage == PLAYING:
                                if len(self.lasers) <= 5:
                                    self.ship.shoot()
                            elif self.reload_on == False and self.ship.ammo <= 0:
                                self.ship.click()
                    elif b3 == True:
                        if self.reload_on == False:
                            if self.ship.ammo < 15:
                                self.ship.reload_ticks = 0
                                self.reload_on = True
                                self.click_sfx.stop()
                                self.reload_sfx.play()
                    
        if self.stage == PLAYING:
            self.mapx -= self.mousex

    def count_ticks(self):
        self.ticks += 1
        self.hurt_ticks -= 15
        self.health_note -= 10
        self.spawn_note -= 10
        if self.stage == START:
            self.end_ticks -= 10
        self.start_ticks -= 10
        if self.stage == PLAYING:
            self.startup += 1
            if self.startup < 5:
                self.mapx = -800
        

    def check_moving(self):
        if self.stage == PLAYING:
            self.mousex,self.mousey = pygame.mouse.get_rel()
        if abs(self.mousex) > 0:
            self.moving_ticks = 0
            self.ship.moving()
            self.is_moving = True
        else:
            self.moving_ticks += 1
            if self.moving_ticks > 3:
                self.is_moving = False        

    def enemy_spawn(self):
        r = random.randrange(-600,650)
        enemylocs1 = [(1600-45+r+self.mapx,HEIGHT/2)]
        for loc in enemylocs1:
            self.enemies.add(Enemy(self,self.enemy1_img,loc,1))

    def score_display(self):
        text = self.title_font.render(str(self.score), True, WHITE)
        rect = text.get_rect()
        rect.centerx = WIDTH // 2
        rect.top = 100
        self.screen.blit(text, rect)

    def stat_display(self):
        for ship in self.player:
            pygame.draw.rect(self.screen, DARKRED, (0,800,600,10))
            pygame.draw.rect(self.screen, DARKRED, (0,780,600,10))
            pygame.draw.rect(self.screen, WHITE, (0,800,ship.ammo*40,10))
            pygame.draw.rect(self.screen, RED, (0,780,ship.shield*60,10))

    def update(self):
        if self.stage == START:
            pass
        if self.stage == PLAYING:
            self.enemies.update()          
            self.bombs.update()
            self.check_moving()
            self.spawn_ticks += 1
            spawn = (100-self.spawn_speed)
            if self.spawn_ticks % spawn == 0:
                self.enemy_spawn()
        self.lasers.update()
        self.hitpoints.update()
        
        if self.reload_on == True:
            self.ship.reload()
        self.player.update()
            
        for laser in self.lasers:
            laser.rect.x -= self.mousex

        pygame.mouse.set_visible(False)

    def render(self):
        # Draw sprites
        self.screen.fill(GROUND_COLOR)
        if self.stage == END:
            centerx,centery = self.ship.rect.center
            self.shadow.set_alpha((-30*20) + (self.death_ticks*9.5))
            self.screen.blit(self.shadow,(centerx-(self.shadow.get_width()/2),centery-(self.shadow.get_height()/2)-100))
        if self.stage != START:
            self.screen.blit(self.ground,[self.mapx,self.mapy])
        if self.stage == PLAYING:
            for e in self.enemies:
                self.screen.blit(e.image, [e.rect.x, e.rect.y])
            self.bombs.draw(self.screen)
            self.lasers.draw(self.screen)
            self.hitpoints.draw(self.screen)

        if self.stage != START:
            self.player.draw(self.screen)
        if self.stage == PLAYING:
            # Draw overlays
            for enemy in self.enemies:
                if enemy.hit_true == True:
                    for laser in self.lasers:
                        pygame.draw.rect(self.screen,WHITE,(laser.csx,laser.csy-15,10,10))
                        pygame.draw.rect(self.screen,WHITE,(0,laser.csy-10,5000,1))
                        pygame.draw.rect(self.screen,WHITE,(laser.csx+5,0,1,5000))

            
                
            pygame.draw.rect(self.screen,WHITE,(WIDTH/2 - 7.5,HEIGHT/2 -7.5,15,15),3)            
            self.score_display()
            self.stat_display()

        self.hurt_img.set_alpha(self.hurt_ticks)
        self.screen.blit(self.hurt_img, (0,0))

        self.end_img.set_alpha(self.end_ticks)
        self.screen.blit(self.end_img,(0,0))

        if self.stage == START:
            self.show_title_screen()
        elif self.stage == END:
            self.show_end_screen()
            self.ticks = 0

        self.end_img.set_alpha(self.start_ticks)
        self.screen.blit(self.end_img,(0,0))
        
        pygame.draw.rect(self.screen,BLACK,(0,HEIGHT-75,WIDTH,75))
        pygame.draw.rect(self.screen,BLACK,(0,0,WIDTH,75))
        if self.stage == PLAYING:
            self.notify_health_up()
            self.notify_spawn_up()
            if self.ship.ammo <= 0:
                self.notify_reload()
        
    
        
    def play(self):
        while self.running:
            self.process_input()     
            self.update()     
            self.render()
            self.count_ticks()
            
            pygame.display.update()
            self.clock.tick(FPS)


# Let's do this!
if __name__ == "__main__":
   g = Game()
   g.play()
   pygame.quit()
