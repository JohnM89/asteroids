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
        # self.sprite_image = pygame.image.load('./assets/source/Pixel UI & HUD/Sprites/Buttons/Blue/ButtonDigital_Press.png').convert_alpha()
        self.sprite_image = pygame.image.load('./local_assets/assets/source/Pixel UI & HUD/Sprites/Buttons/Blue/ButtonDigital_Press.png').convert_alpha()
        self.radius = 400  
        self.image = pygame.Surface((2*self.radius, 2*self.radius), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        #self.sprite_image = random.choice(self.explosions).convert_alpha()
        self.sprite_width = 52
        self.sprite_height = 18
        self.frame_interval = .05 
        self.frame_timer = 0
        self.frame = 0
        self.max_frame = 3
        self.frame_y = 0    
        self.frame_x = self.frame * self.sprite_width 
        self.crop_rect = (self.frame_x, self.frame_y, self.sprite_width, self.sprite_height)
        #self.sprite_image = pygame.transform.scale(self.sprite_image, (w, h))
        self.menu = menu
        self.previous_button = self.menu.current_button
        self.menu.done_animate = False
        self.menu.drawable.add(self, layer=-1)
        self.menu.updatable.add(self)
         
        
    def draw(self):
        self.image.fill((0,0,0,0))
        ##upscaling the cropped frame and centering it in the Surface so its not cut off
        frame_surface = self.sprite_image.subsurface(self.crop_rect)
        new_size = (
            int(self.sprite_width * 10),
            int(self.sprite_height * 3)
        )
        scaled_frame = pygame.transform.scale(frame_surface, new_size)

        blit_x = (self.image.get_width() - scaled_frame.get_width()) // 2
        blit_y = (self.image.get_height() - scaled_frame.get_height()) // 2

        self.image.blit(scaled_frame, (blit_x, blit_y))
        #img_rect_local = self.image.get_rect()
        #pygame.draw.rect(self.image, (0, 0, 0), img_rect_local, 2)
        #spr_rect_local = self.sprite_image.get_rect()
        #pygame.draw.rect(self.sprite_image, (0, 255, 0), spr_rect_local, 2)
        #self.image.blit(self.sprite_image, (0, 0), self.crop_rect)
    def update(self, dt):
        if self.frame_timer > self.frame_interval:
            if self.frame < self.max_frame:
                self.frame += 1
                self.frame_x = self.frame * self.sprite_width
                self.crop_rect = (self.frame_x, self.frame_y, self.sprite_width, self.sprite_height)
                self.frame_timer = 0
            else:
                if self.previous_button == self.menu.current_button:
                    self.frame = 3
                else:
                    self.menu.drawable.remove(self)
                    self.menu.updatable.remove(self)
                    self.kill()
                    self.menu.done_animate = True
        
        else:
            self.frame_timer += dt 
               
