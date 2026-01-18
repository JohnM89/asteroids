import pygame
import pymunk
import os
from entities.circleshape import *
from game.constants import *

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):

        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.radius = radius  
        self.image = pygame.Surface((2*self.radius, 2*self.radius), pygame.SRCALPHA)
        self.image = self.image.convert_alpha()  
        self.rect = self.image.get_rect(center=(x, y))
        # self.sprite_image = pygame.image.load("./assets/sprites/spritesheet.png").convert_alpha()
        self.sprite_image = pygame.image.load("./local_assets/assets/sprites/spritesheet.png").convert_alpha()
        self.sprite_width = 96
        self.sprite_height = 96
        self.frame_interval = .1 
        self.frame_timer = 0
        self.frame = 0
        self.max_frame = 9
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
               
