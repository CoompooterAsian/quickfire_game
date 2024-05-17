# Imports
import pygame
import random
import math

from quickfire import *

''' 
Each of our sprites will extend the pygame Sprite class. That means our 
sprites get all of the useful features of a pygame Sprite plus any additional
features we decide to add.
'''


class Ship(pygame.sprite.Sprite):

    def __init__(self, game, image, loc, shield):
        # Call the init method in the Sprite class
        super().__init__()

        # Add any additional attributes we need
        self.game = game

        self.death_anim_list = self.game.death_list
        self.death_index = 0
        
        self.gun_anim_list = self.game.gun_list
        self.gun_index = 0
        self.image = self.gun_anim_list[self.gun_index]

        self.gun_anim_list2 = self.game.gun_list2
        self.gun_index2 = 0
        
        self.rect = self.image.get_rect()
        self.rect.center = loc
        self.shield = shield
        self.speedx = 0
        self.speedy = 0

        self.anim_run = False
        self.anim_ticks = 0

        self.rect.x = 0
        self.rect.y = -70

        self.ammo = 15

        self.gun1 = True

        self.reload_ticks = 0

    def shoot(self):
        self.ammo -= 1
        if self.ammo >= 0:
            self.gun_index = 0
            self.anim_run = True
            self.game.pew_sfx.play()

            laser = Laser(self.game,self.game.laser_img,(1050,460))
            self.game.lasers.add(laser)
       

    def animate(self):
        if self.gun1 == True:
            if self.game.reload_on == False:
                if self.anim_run == True:
                    self.anim_ticks += 1
                    if self.anim_ticks % 2 == 0:
                        self.gun_index += 1

                    if self.ammo > 0:
                        if self.gun_index > 6:
                            self.gun_index = 0
                            self.anim_run = False
                    else:
                        if self.gun_index > 7:
                            self.gun_index = 7
                            self.anim_run = False
                        
                if self.ammo > 0:      
                    if self.anim_run == False:
                        self.gun_index = 0
                else:
                    if self.anim_run == False:
                        self.gun_index = 7
                        
                if self.game.is_moving == True:
                    self.image.set_alpha(180)
                else:
                    self.image.set_alpha(255)
                self.image = self.gun_anim_list[self.gun_index]
            if self.game.stage == END:
                
                t = self.game.death_ticks
                if t < 70:
                    self.rect.x = 0
                    self.rect.y = 1000
                elif t < 74:
                    self.rect.y -= 160
                elif t < 76:
                    self.rect.y -= 190
                elif t < 80:
                    self.rect.y += 10
                elif t < 84:
                    self.rect.y -= 12
                elif t < 90:
                    self.rect.y -= 5
                elif t < 100:
                    pass
                elif t < 120:
                    if t == 100:
                        self.game.cough_sfx.set_volume(1)
                        self.game.cough_sfx.play()
                        self.game.hurt_ticks = 255
                    self.death_index = 1
                elif t < 150:
                    if t == 120:
                        self.game.hurt_ticks = 255
                    self.death_index = 2
                elif t < 160:
                    if t == 150:
                        self.game.hurt_ticks = 400
                    self.death_index = 3
                elif 200 < t < 300:
                    self.game.hurt_ticks += 15
                    self.game.end_ticks += 5
                    if self.game.end_ticks > 300:
                        self.game.end_ticks >= 300
                elif t > 300:
                    self.game.new_game()


                self.image = self.death_anim_list[self.death_index]
        else:
            if self.game.reload_on == False:
                if self.anim_run == True:
                    self.anim_ticks += 1
                    if self.anim_ticks % 2 == 0:
                        self.gun_index2 += 1

                    if self.ammo > 0:
                        if self.gun_index2 > 3:
                            self.gun_index2 = 0
                            self.anim_run = False
                    else:
                        if self.gun_index2 > 3:
                            self.gun_index2 = 0
                            self.anim_run = False
                        
                if self.ammo > 0:      
                    if self.anim_run == False:
                        self.gun_index2 = 0
                else:
                    if self.anim_run == False:
                        self.gun_index2 = 0
                        
                if self.game.is_moving == True:
                    self.image.set_alpha(180)
                else:
                    self.image.set_alpha(255)
                self.image = self.gun_anim_list2[self.gun_index2]
            
            
    def reload(self):
        self.reload_ticks += 1
        if 0 <= self.reload_ticks <= 9:
            self.rect.y += 60
            self.rect.x += 15
        elif 9 < self.reload_ticks <= 30:
            self.rect.y = 350
            self.rect.x = 200
        elif 30 < self.reload_ticks <= 35:
            self.gun_index = 8
            self.rect.y -= 45
            self.rect.x -= 2
        elif 35 < self.reload_ticks <= 40:
            self.rect.y -= 15
            self.rect.x -= 1
        elif 40 < self.reload_ticks <= 50:
            self.rect.y -= 5
            self.rect.x -= 4
        elif 50 < self.reload_ticks <= 60:
            self.rect.y += 25
            self.gun_index = 9
        elif 60 < self.reload_ticks <= 65:
            self.rect.y += 8
            self.ammo = 15
        elif 65 < self.reload_ticks <= 75:
            self.rect.y -= 1
            self.gun_index = 0
        else:
            self.game.reload_on = False
        
        self.image = self.gun_anim_list[self.gun_index]
        
    def moving(self):
        if self.game.reload_on == False:
            if self.game.ticks % 2 == 0:
                self.rect.y = abs(self.game.mousex)/2 - 75
                self.rect.x = abs(self.game.mousex)/2

    def click(self):
        self.game.click_sfx.play()       
        

    def death(self):
        if self.shield <= 0:
            self.game.end_game()

    def update(self):
        self.moving()
        if self.game.stage != END:
            self.death()
        self.animate()

        

class Laser(pygame.sprite.Sprite):

    def __init__(self, game, image, loc):
        # Call the init method in the Sprite class
        super().__init__()

        # Add any additional attributes we need
        self.game = game
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = loc
        
        r = random.randrange(-10,10)
        ry = random.randrange(-3,3)
            
        self.csx = WIDTH/2 - 10
        self.csy = HEIGHT/2 + 9
        
        x,y = pygame.mouse.get_pos()


        self.speed = 30
        self.dx = (self.csx - self.rect.centerx)
        self.dy = (self.csy - self.rect.centery)

        self.hyp = math.sqrt(((self.dx)**2)+((self.dy)**2))

        self.vx = (self.speed*self.dx)/self.hyp
        self.vy = (self.speed*self.dy)/self.hyp
        
        laser_image = self.image
        self.rect.center = loc
        self.image = laser_image
        self.rect = self.image.get_rect()
        self.rect.center = loc

        self.speed_decrease = 1

        self.time_ticks = 0

        self.scale = 0

        self.rectangle = self.image.get_rect()

        self.pmx = self.rect.centerx
        self.pmy = self.rect.centery

        self.distance = math.hypot(self.csx-self.pmx,self.csy-self.pmy)


    def drop(self):
        self.speed_decrease += .13
        self.pmx = self.rect.centerx
        self.pmy = self.rect.centery
        self.rect.centery += self.vy / self.speed_decrease
        self.rect.centerx += self.vx / self.speed_decrease
        pressed = pygame.key.get_pressed()

        self.distance = math.hypot(self.csx-self.pmx,self.csy-self.pmy)
        self.csx -= self.game.mousex
        
        w, h = pygame.display.get_surface().get_size()
        if self.time_ticks > .15 or self.distance < 15:
            self.kill()

    def animate(self):
        self.time_ticks += .01
        x = self.image.get_width()
        self.scale = x*(1.79**(-2.5*self.time_ticks))
        laser_copy = pygame.transform.scale(self.image,(self.scale,self.scale))
        new_rect = laser_copy.get_rect()
        new_rect.center = self.rect.center
        self.image = laser_copy
        self.rect = new_rect


    def update(self):
        self.drop()
        self.animate()
        

class Enemy(pygame.sprite.Sprite):

    def __init__(self, game, image, loc, shield):
        # Call the init method in the Sprite class
        super().__init__()

        # Add any additional attributes we need
        self.game = game
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = loc
        self.shield = shield

        self.shoot_start = 0
        self.hit_true = False
        self.hit_ticks = 0

            
        if self.game.score >= 2000:
            self.shield = 2
            
        if self.game.score >= 6000:
            self.shield = 3
            
        if self.shield >= 12000:
            self.shield = 4
            
        if self.shield >= 20000:
            self.shield = 5

        
    def drop_bomb(self):
        r = random.randrange(0,100)
        if r == 0:
            self.game.pew_sfx.play()
            bomb = Bomb(self.game,self.game.bomb_img,self.rect.center)
            self.game.bombs.add(bomb)
        

    def hurt(self):
        hits = pygame.sprite.spritecollide(self,self.game.lasers,False)

        
        for laser in hits:
            if laser.image.get_width() < 5:
                self.hit_true = True
            else:
                self.hit_true = False
            if laser.image.get_width() < 3:
                self.hit_true = False
                self.shield -= 1
                self.game.hit_sfx.play()
                laser.kill()
                
    def death(self):
        if self.shield <= 0:
            self.game.score += 100
            self.kill()

    def ready_shoot(self):
        self.shoot_start += 1

    def show_health(self):
        x,y = self.rect.midbottom
        pygame.draw.rect(self.game.screen,WHITE,(x, y,self.shield * 10,10))
        

    def update(self):
        self.ready_shoot()
        if self.game.stage == PLAYING:
            self.hurt()
            self.death()
            if self.shoot_start > 60:
                self.image = self.game.enemy2_img
                if len(self.game.bombs) <= 0:
                    self.drop_bomb()
            self.show_health()


class Bomb(pygame.sprite.Sprite):

    def __init__(self, game, image, loc):
        # Call the init method in the Sprite class
        super().__init__()

        # Add any additional attributes we need
        self.game = game
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = loc

        miss_list = [(-1000,HEIGHT),(WIDTH+1000,HEIGHT),(-1000,0),(WIDTH+1000,0)]
        hit_list = [(WIDTH/2,-1000)]

        self.hit = False

        r = random.randrange(0,5)
        if r == 0:
            self.speed = 10
            x,y = random.choice(hit_list)
            self.hit = True
            
        else:
            self.speed = 70
            x,y = random.choice(miss_list)
            self.hit = False

        r = random.randrange(-30,30)
        self.dx = (x - self.rect.centerx)+ r
        self.dy = (y - self.rect.centery)+ r

        self.hyp = math.sqrt(((self.dx)**2)+((self.dy)**2))

        self.vx = (self.speed*self.dx)/self.hyp
        self.vy = (self.speed*self.dy)/self.hyp

        self.angle = math.atan2(y-self.rect.centery,
                                x - self.rect.centerx)*(180/math.pi)

        bomb_image = pygame.transform.rotate(self.image,90-self.angle)
        self.image = bomb_image

        self.time_ticks = 0

        
    def drop(self):
        self.rect.y += self.vy
        self.rect.x += self.vx 

        w, h = pygame.display.get_surface().get_size()

        if self.hit == True:
            if self.rect.top < 0 and self.rect.bottom > h:
                self.kill()
                self.game.ship.shield -= 1
                self.game.hurt_ticks = 300
                self.game.hit_sfx.play()
        else:
            if self.rect.right > w:
                self.kill()
            if self.rect.left < 0:
                self.kill()
                

    def animate(self):
        self.time_ticks += .05
        x = self.image.get_width()
        self.scale = x *(1.5**self.time_ticks)
        bomb_copy = pygame.transform.scale(self.image,(self.scale,self.scale))
        new_rect = bomb_copy.get_rect()
        new_rect.center = self.rect.center
        self.image = bomb_copy
        self.rect = new_rect
        

    def update(self):
        self.drop()
        self.animate()


class Fleet(pygame.sprite.Group):

    def __init__(self, game, *sprites):
        super().__init__(*sprites)

        self.game = game
        
        self.vx = 2
    
    def move(self):
        w, h = pygame.display.get_surface().get_size()

        for enemy in self.sprites():
            enemy.rect.x -= self.game.mousex



    def update(self, *args):
        super().update(*args)
        self.move()


class BG(pygame.sprite.Sprite):
    pass

        

