from .commonalien import *
from game.constants import *
import pymunk.pygame_util
import math
import os
import random
import pygame   
import pymunk
from game.raycast import RayCast
class Scourge(CommonAlien):
    def __init__(self, x, y, radius, space, level, kind):
        super().__init__(x,y,radius, space)
        self.canvas = level.canvas
        self.skin = []
        for img in os.listdir('./assets/images/scourge'):
            self.skin.append(pygame.image.load(os.path.join('./assets/images/scourge', img )).convert_alpha())
        self.shape.friction = 9.0
        self.shape.elasticity = 0.8
        self.shape.collision_type = 5
        self.max_view_distance = 100
        self.shape.mass = 30 * self.radius
        self.image = pygame.Surface((4*self.radius,4*self.radius), pygame.SRCALPHA)
        #self.image = self.image.convert_alpha()
        #self.x = x  
        #self.y = y
        self.rect = self.image.get_rect(center=(x,y))
        #self.base_image = pygame.image.load("./assets/source/Export/Enemies - Base/0.5x/Enemy_1_A_Small.png")
        self.base_image = random.choice(self.skin)
        self.base_image = pygame.transform.scale(self.base_image, (3*self.radius, 3*self.radius))
        self.sprite_image = self.base_image.copy()
        self.sprite_width = 64
        self.sprite_height = 32
        self.frame_interval = 0.75
        self.frame_timer = 0
        self.frame = 0
        self.max_frame = 9
        self.frame_y = 0
        self.frame_x = 0
        self.crop_rect = pygame.Rect(self.frame_x, self.frame_y, self.sprite_width, self.sprite_height)
        self.ray_cast = RayCast(self.space, self.canvas, self.max_view_distance, self.shape.filter)
    def draw(self):
        self.image.fill((0,0,0,0))
        result = self.ray_cast.cast_ray(self.body.position.x, self.body.position.y)
        #for res in result:
        if hasattr(result, "point"):    
            if result.point != None:
                if hasattr(result, "shape") and hasattr(result.shape, "game_object"):
                    #print('i see')
                    if result.shape.game_object.__class__.__name__ == "Player":
                        x , y = result.point  
                        if x != 0 or y != 0:
                            towards = True
                            self.rotate(x, y, towards)
                            boost = True
                            self.move(boost)

                    else:
                        x , y = result.point
                        if x != 0 or y != 0:
                            self.rotate(x, y)
                            self.move()
        self.image.blit(self.sprite_image,(0,0))             
    def rotate(self,x, y, towards=False):
        if towards == True:
            direction = (pymunk.Vec2d(x, y) - self.body.position).angle
            self.body.angle = direction
        else:
            direction = (pymunk.Vec2d(x, y) - self.body.position).angle
            self.body.angle = (direction - math.pi)
    def move(self, boost=False):
        forward = pymunk.Vec2d(1, 0).rotated(self.body.angle)
        if boost == True:
            if self.body.velocity.length < (PLAYER_SPEED / 2):
                acceleration = forward * ACCELERATION  
                accel = pymunk.Vec2d(acceleration.x, acceleration.y)
                self.body.velocity += accel
        else:
            if self.body.velocity.length < (PLAYER_SPEED / 2):
                acceleration = forward * (ACCELERATION * 0.002)
                accel = pymunk.Vec2d(acceleration.x, acceleration.y)
                self.body.velocity += accel
            else:
                self.body.velocity *= DRAG_COEFFICENT

    def bounds_check(self):
        super().bounds_check()
    def update(self, dt):
        super().update(dt)
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
        self.sprite_image = pygame.transform.rotate(self.base_image, angle_degrees - 90)
        self.rect = self.sprite_image.get_rect(center=(int(self.body.position.x),int(self.body.position.y)))
        #print(self.body.position)
