import pygame
import pymunk
import random
import math
import os
from entities.circleshape import *
from game.constants import *

class RocketImpact(pygame.sprite.Sprite):
    def __init__(self, contact_point, rotation, target):

        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.explosions = []
        for img in os.listdir('./assets/sprites/RocketImpact/'):
            self.explosions.append(pygame.image.load(os.path.join('./assets/sprites/RocketImpact/', img)))
        self.radius = 48
        self.rotation = rotation
        self.enemy_position = target.body.position
        self.contact_point = contact_point 
        self.relative_offset = (self.contact_point - self.enemy_position)
        self.image = pygame.Surface((6*self.radius, 6*self.radius), pygame.SRCALPHA)
        self.offset_x = 0
        self.offset_y = 0
        self.rect = self.image.get_rect(center=(self.contact_point))
        self.base_image = random.choice(self.explosions).convert_alpha()
        self.sprite_image = self.base_image.copy()
        self.sprite_width = 96
        self.sprite_height = 96
        self.frame_interval = .1 
        self.frame_timer = 0
        self.frame = 0
        self.max_frame = 13
        self.frame_y = 0    
        self.frame_x = self.frame * self.sprite_width 
        self.crop_rect = pygame.Rect(self.frame_x, self.frame_y, self.sprite_width, self.sprite_height)
         
        
    def draw(self):
        self.image.fill((0,0,0,0))
        #img_rect_local = self.image.get_rect()
        #pygame.draw.rect(self.image, (0, 0, 0), img_rect_local, 2)
        #spr_rect_local = self.sprite_image.get_rect()
        #pygame.draw.rect(self.sprite_image, (0, 255, 0), spr_rect_local, 2)
        self.image.blit(self.sprite_image, (0, 0))
    def update(self, dt):
        if self.frame_timer > self.frame_interval:
            self.frame += 1
            if self.frame < self.max_frame:
                self.frame_timer = 0
            elif self.frame == self.max_frame:
                self.kill()
        
        else:
            self.frame_timer += dt 
        self.frame_x = self.frame * self.sprite_width
        self.crop_rect = pygame.Rect(self.frame_x, self.frame_y, self.sprite_width, self.sprite_height)
        sub_surf = self.base_image.subsurface(self.crop_rect)
        #this may be expensive 
        angle_radians = math.atan2(self.rotation.x, self.rotation.y)
        angle_degrees = math.degrees(angle_radians)  
        self.sprite_image = pygame.transform.rotate(sub_surf, angle_degrees)

        ## offsettign the contact point so that the animation correctly alligns with contact point and not just centered 
        offset_x = 0
        offset_y = -48
        cosA = math.cos(-angle_radians)
        sinA = math.sin(-angle_radians)
        rotated_offset_x = offset_x * cosA - offset_y * sinA
        rotated_offset_y = offset_x * sinA + offset_y * cosA

        explosion_x = self.contact_point.x + rotated_offset_x
        explosion_y = self.contact_point.y + rotated_offset_y

        self.rect = self.sprite_image.get_rect(center=(explosion_x, explosion_y))

            
