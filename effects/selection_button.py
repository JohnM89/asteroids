import pygame
import pymunk
import math
import random
import os
from entities.circleshape import *
from game.constants import *

class SelectionButton(pygame.sprite.Sprite):
    def __init__(self, menu, x, y):

        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        #self.explosions = []
        #for img in os.listdir('./assets/sprites/BombExplode/'):
        self.sprite_image = pygame.image.load('./assets/source/Pixel UI & HUD/Sprites/Buttons/White/ButtonDigital_Press.png').convert_alpha()
        self.radius = 52  
        self.image = pygame.Surface((2*self.radius, 2*self.radius), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        #self.sprite_image = random.choice(self.explosions).convert_alpha()
        self.sprite_width = 52
        self.sprite_height = 18
        self.frame_interval = .1 
        self.frame_timer = 0
        self.frame = 0
        self.max_frame = 3
        self.frame_y = 0    
        self.frame_x = self.frame * self.sprite_width 
        self.crop_rect = (self.frame_x, self.frame_y, self.sprite_width, self.sprite_height)
        self.menu = menu

        self.menu.done_animate = False
        self.menu.drawable.add(self, layer=-1)
        self.menu.updatable.add(self)
         
        
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
                self.menu.drawable.remove(self)
                self.menu.updatable.remove(self)
                self.kill()
                self.menu.done_animate = True
        
        else:
            self.frame_timer += dt 
               
