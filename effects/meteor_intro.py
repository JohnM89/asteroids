import pygame
import pymunk
import os
from entities.circleshape import *
from game.constants import *

class MeteorIntro(pygame.sprite.Sprite):
    def __init__(self, title, x, y, radius):

        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.radius = radius 
        self.title = title
        self.x = x  
        self.y = y
        self.image = pygame.Surface((4*self.radius, 4*self.radius), pygame.SRCALPHA)
        self.image = self.image.convert_alpha()  
        self.rect = self.image.get_rect(center=(x, y))
        self.sprite_image = pygame.image.load("./assets/source/Legacy Collection/Assets/Misc/spaceship-unit/Spritesheets/Spritesheet_thrust_updated.png").convert_alpha()
        #self.sprite_image = pygame.transform.scale(self.sprite_image, (2, 2))
        self.sprite_width = 106
        self.sprite_height = 77
        self.frame_interval = .1 
        self.frame_timer = 0
        self.frame = 0
        self.max_frame = 7
        self.frame_y = 0    
        self.frame_x = self.frame * self.sprite_width 
        self.crop_rect = (self.frame_x, self.frame_y, self.sprite_width, self.sprite_height)
         
        
    def draw(self):
        self.image.fill((0,0,0,0))
        ##upscaling the cropped frame and centering it in the Surface so its not cut off 
        frame_surface = self.sprite_image.subsurface(self.crop_rect)
        new_size = (
            int(self.sprite_width * 2),
            int(self.sprite_height * 2)
        )
        scaled_frame = pygame.transform.scale(frame_surface, new_size)

        blit_x = (self.image.get_width() - scaled_frame.get_width()) // 2
        blit_y = (self.image.get_height() - scaled_frame.get_height()) // 2

        self.image.blit(scaled_frame, (blit_x, blit_y))
        #self.image.blit(self.sprite_image, (0, 0), self.crop_rect)
    def update(self, dt):
        self.rect.center = (self.x, self.y)
        if self.frame_timer > self.frame_interval:
            if self.frame < self.max_frame:
                self.frame += 1
                self.frame_x = self.frame * self.sprite_width
                self.crop_rect = (self.frame_x, self.frame_y, self.sprite_width, self.sprite_height)
                self.frame_timer = 0
            else:
                self.frame = 0
                #self.title.drawable.remove(self)
                #self.title.updatable.remove(self)
                #self.kill()
        
        else:
            self.frame_timer += dt

        #self.rect = self.image.get_rect(center=(self.x, self.y))
               
