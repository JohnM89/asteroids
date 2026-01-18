import pygame
import pymunk
import math
import random
import os
from entities.circleshape import *
from game.constants import *

class BombExplode(pygame.sprite.Sprite):
    def __init__(self, x, y, assets):

        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.assets = assets
        # OLD: Load images manually with os.path.join + pygame.image.load
        # for img in os.listdir('./assets/sprites/BombExplode/'):
        #     self.explosions.append(pygame.image.load(os.path.join('./assets/sprites/BombExplode/', img)))
        # for img in os.listdir('./local_assets/assets/sprites/BombExplode/'):
        #     self.explosions.append(pygame.image.load(os.path.join('./local_assets/assets/sprites/BombExplode/', img)))

        # NEW: Use AssetManager
        self.explosions = self.assets.images_in('sprites/BombExplode')
        self.radius = 80  
        self.image = pygame.Surface((2*self.radius, 2*self.radius), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        self.sprite_image = random.choice(self.explosions).convert_alpha()
        self.sprite_width = 160
        self.sprite_height = 160
        self.frame_interval = .1 
        self.frame_timer = 0
        self.frame = 0
        self.max_frame = 14
        self.frame_y = 0    
        self.frame_x = self.frame * self.sprite_width 
        self.crop_rect = (self.frame_x, self.frame_y, self.sprite_width, self.sprite_height)
         
        
    def draw(self):
        self.image.fill((0,0,0,0))
        self.image.blit(self.sprite_image, (0, 0), self.crop_rect)
    def update(self, dt):
        if self.frame_timer > self.frame_interval:
            if self.frame < self.max_frame:
                self.frame += 1
                self.frame_x = self.frame * self.sprite_width
                self.crop_rect = (self.frame_x, self.frame_y, self.sprite_width, self.sprite_height)
                self.frame_timer = 0
            else:
                self.kill()
        
        else:
            self.frame_timer += dt 
               
