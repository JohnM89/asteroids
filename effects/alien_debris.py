import pygame
import pymunk
from entities.circleshape import *
from game.constants import *

class AlienDebris(CircleShape):
    def __init__(self, x, y, space, rotation,  img):
        super().__init__(x, y, 8, mass=0.5)
        self.body.angle = rotation
        self.image = pygame.Surface((10*self.radius, 10*self.radius), pygame.SRCALPHA)
        self.image = self.image.convert_alpha()  
        self.rect = self.image.get_rect(center=(x, y))
        self.space = space
        #self.shape.collision_type = 3
        self.shape.filter = pymunk.ShapeFilter(categories=BACKGROUND_OBJECTS_CATEGORY,mask=BACKGROUND_OBJECTS)
        self.shape.game_object = self
        self.base_image = img
        #self.base_image = pygame.transform.scale(self.base_image, (2*self.radius, 2*self.radius))
        self.sprite_image = self.base_image.copy()
        #self.sprite_width = 32
        #self.sprite_height = 16
        #self.frame_interval = 0.75
        #self.frame_timer = 0
        #self.frame = 0
        #self.max_frame = 29
        #self.frame_y = 0
        #self.frame_x = 0
        #self.crop_rect = pygame.Rect(self.frame_x, self.frame_y, self.sprite_width, self.sprite_height)
        #pygame.draw.circle(self.image,(255,255,255), (self.radius, self.radius), self.radius, width=2)
        self.time_to_live = 3.5
    def draw(self):
        self.image.fill((0,0,0,0))
        self.image.blit(self.sprite_image,(0,0))
        #pygame.draw.circle(self.image,(255,255,255), (self.radius, self.radius), self.radius, width=2)
        pass
    def update(self, dt):
        #if self.frame_timer > self.frame_interval:
            #self.frame += 1
            #if self.frame <= self.max_frame:
                #self.frame_timer = 0
            #else:
                #self.frame = 0
        #else:
            #self.frame_timer += dt

        #self.frame_x = self.frame * self.sprite_width
        #self.crop_rect = pygame.Rect(self.frame_x, self.frame_y, self.sprite_width, self.sprite_height)
        #sub_surf = self.base_image.subsurface(self.crop_rect)
        angle_degrees = -math.degrees(self.body.angle)
        #self.sprite_image = pygame.transform.rotate(sub_surf, angle_degrees)
        self.sprite_image = pygame.transform.rotate(self.base_image, angle_degrees)
        self.rect = self.sprite_image.get_rect(center=(int(self.body.position.x),int(self.body.position.y)))
        self.time_to_live -= dt
        if self.time_to_live < dt:
            self.kill()
            self.space.remove(self.body, self.shape)
        #else:
            #self.rect.center = (int(self.body.position.x), int(self.body.position.y))
