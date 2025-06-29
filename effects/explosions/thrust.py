import pygame
import pymunk
import random
import math
import os
from entities.circleshape import *
from game.constants import *

class Thrust(pygame.sprite.Sprite):
    def __init__(self, player, contact_point, rotation):

        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        #self.explosions = []
        self.player = player
        #for img in os.listdir('./assets/sprites/ShotImpact/'):
        self.base_image = pygame.image.load('./assets/source/Super Pixel Projectiles Pack 2/spritesheet/pj2_helix_beam_large_orange/spritesheet.png').convert_alpha()
        self.radius = 32
        self.rotation = rotation
        #self.enemy_position = target.body.position
        self.contact_point = contact_point 
        #self.relative_offset = (self.contact_point - self.enemy_position)
        self.image = pygame.Surface((2*self.radius, 2*self.radius), pygame.SRCALPHA)
        self.offset_x = 32
        self.offset_y = 32
        self.rect = self.image.get_rect(center=(self.contact_point))
        #self.base_image = random.choice(self.explosions).convert_alpha()
        self.sprite_image = self.base_image.copy()
        self.sprite_width = 64
        self.sprite_height = 32
        self.frame_interval = .05     
        self.frame_timer = 0
        self.frame = 0
        #self.max_frame = int(self.base_image.get_width() // self.sprite_width)
        self.max_frame = 29
        self.frame_y = 0    
        self.frame_x = self.frame * self.sprite_width 
        self.crop_rect = pygame.Rect(self.frame_x, self.frame_y, self.sprite_width, self.sprite_height)
        self.player.updatable.add(self)
        self.player.drawable.add(self, layer=-1)
         
        
    def draw(self):
        self.image.fill((0,0,0,0))
        #img_rect_local = self.image.get_rect()
        #pygame.draw.rect(self.image, (0, 0, 0), img_rect_local, 2)
        #spr_rect_local = self.sprite_image.get_rect()
        #pygame.draw.rect(self.sprite_image, (0, 255, 0), spr_rect_local, 2)
        self.image.blit(self.sprite_image, (0, 0))
    def update(self, dt):
        #self.contact_point = (self.player.body.position.x, self.player.body.position.y)
        #self.rotation = self.player.rotation
        if self.frame_timer > self.frame_interval:
            self.frame += 1
            #if self.frame > self.max_frame:
                #self.frame = 0
            if self.frame < self.max_frame:
                self.frame_timer = 0
            elif self.frame >= self.max_frame:
                self.player.updatable.remove(self)
                self.player.updatable.remove(self)
                self.player.thrust = None
                self.kill()
        
        else:
            self.frame_timer += dt 
        self.frame_x = self.frame * self.sprite_width
        self.crop_rect = pygame.Rect(self.frame_x, self.frame_y, self.sprite_width, self.sprite_height)
        sub_surf = self.base_image.subsurface(self.crop_rect)
        #this may be expensive

        #self.rotation = self.player.body.position.rotated(self.player.rotation)
        self.rotation = pymunk.Vec2d(1,0).rotated(self.player.rotation)
        thrust_distance = 30
        offset_vector = -self.rotation * thrust_distance
        self.contact_point = (self.player.body.position + offset_vector)
        angle_radians = math.atan2(self.rotation.x, self.rotation.y)
        angle_degrees = math.degrees(angle_radians)  
        self.sprite_image = pygame.transform.rotate(sub_surf, angle_degrees - 90)
        
        #self.rotation = self.player.body.position.rotated(self.player.rotation)

        ## offsettign the contact point so that the animation correctly alligns with contact point and not just centered 
        #offset_x = 0
        #offset_y = -48
        #cosA = math.cos(-angle_radians)
        #sinA = math.sin(-angle_radians)
        #rotated_offset_x = offset_x * cosA - offset_y * sinA
        #rotated_offset_y = offset_x * sinA + offset_y * cosA

        #explosion_x = self.player.body.position.x + rotated_offset_x
        #explosion_y = self.player.body.position.y + rotated_offset_y
        self.rect = self.sprite_image.get_rect(center=(self.contact_point))
        #self.rect = self.sprite_image.get_rect(center=(explosion_x, explosion_y))

            
