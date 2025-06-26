import pygame
import pymunk
import math
#import random
#import os
from entities.circleshape import *
from game.constants import *

class SheildHit(pygame.sprite.Sprite):
    def __init__(self, x, y):

        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        #self.explosions = []
        #for img in os.listdir('./assets/sprites/BombExplode/'):
            #self.explosions.append(pygame.image.load(os.path.join('./assets/sprites/BombExplode/', img)))
        self.x = x  
        self.y = y
        self.radius = 64  
        self.image = pygame.Surface((2*self.radius, 2*self.radius), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        #self.sprite_image = random.choice(self.explosions).convert_alpha()
        self.sprite_image = pygame.image.load('./assets/images/Bubble_2.png').convert_alpha()
        self.sprite_image = pygame.transform.scale(self.sprite_image, (128, 128))
        self.time_to_live = .3
        #self.sprite_width = 160
        #self.sprite_height = 160
        #self.frame_interval = .1 
        #self.frame_timer = 0
        #self.frame = 0
        #self.max_frame = 14
        #self.frame_y = 0    
        #self.frame_x = self.frame * self.sprite_width 
        #self.crop_rect = (self.frame_x, self.frame_y, self.sprite_width, self.sprite_height)
         
        
    def draw(self):
        self.image.fill((0,0,0,0))
        self.image.blit(self.sprite_image, (0, 0))
    

    def update(self, dt):
        self.time_to_live -= dt 
        if self.time_to_live <= dt:
            self.kill()
        #if self.frame_timer > self.frame_interval:
        #    if self.frame < self.max_frame:
        #        self.frame += 1
        #        self.frame_x = self.frame * self.sprite_width
         #       self.crop_rect = (self.frame_x, self.frame_y, self.sprite_width, self.sprite_height)
        #        self.frame_timer = 0
        #    else:
        #        self.kill()
        
        #else:
            #self.frame_timer += dt
        self.rect = self.sprite_image.get_rect(center=(int(self.x), int(self.y)))
               
