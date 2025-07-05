from .commonalien import *
from entities.enemy_shot import EnemyShot
from entities.enemy_shoot import EnemyShoot
from game.constants import * 
import math
import os
import random
import pygame   
import pymunk.pygame_util
from game.raycast import RayCast
class FlyingSaucer(CommonAlien):
    def __init__(self, x, y, radius, space, level, kind):

        super().__init__(x , y, radius, space)
        ##debug     
        #self.canvas = level.canvas
        ## 
        self.skin = []
        for img in os.listdir('./assets/images/flyingsaucer'):
            self.skin.append(pygame.image.load(os.path.join('./assets/images/flyingsaucer', img)))
        self.rotation = 0
        self.updatable = level.updatable
        self.drawable = level.drawable   
        self.canvas = level.canvas
        self.shape.friction = 9.0
        self.shape.elasticity = 0.6
        self.shape.collision_type = 5
        self.shape.mass = 40 * self.radius
        self.image = pygame.Surface((4*self.radius,4*self.radius), pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect(center=(x,y))

        #self.rect = self.image.get_rect(center=(self.body.position))
        #self.base_image = pygame.image.load("./assets/source/Export/Enemies - Base/0.5x/Enemy_1_B_Small.png")
        self.base_image = random.choice(self.skin)
        self.base_image = pygame.transform.scale(self.base_image, (3*self.radius, 3*self.radius))
        self.sprite_image = self.base_image.copy()
        #self.sprite_width = 64
        #self.sprite_height = 32
        #self.frame_interval = 0.75
        #self.frame_timer = 0
        #self.frame = 0
        #self.max_frame = 9
        #self.frame_y = 0
        #self.frame_x = 0
        #self.crop_rect = pygame.Rect(self.frame_x, self.frame_y, self.sprite_width, self.sprite_height)



        self.max_view_distance = 150
        self.ray_cast = RayCast(self.space, self.canvas, self.max_view_distance, self.shape.filter, self.radius)
        #add diagonal directions as well
        self.timer = 0

    def draw(self):
        self.image.fill((0,0,0,0))
        result = self.ray_cast.cast_ray(self.body.position.x, self.body.position.y)
        #for res in result:
        #if hasattr(result, "point"):
            #if result.point != None:
        if hasattr(result, "shape") and hasattr(result.shape, "game_object"):
            if result.shape.game_object.__class__.__name__ == "Player":
                x , y = result.point
                if x != 0 or y != 0:
                    towards = True
                    self.rotate(x, y, towards)
                    self.shoot(x, y)
            else:
                x , y = result.point 
                if x != 0 or y != 0:
                    self.rotate(x , y)
                    self.move()
        #pass
        self.image.blit(self.sprite_image,(0,0))
    def rotate(self, x, y, towards=False):
        if towards == True:
            direction = (pymunk.Vec2d(x, y) - self.body.position).angle
            self.body.angle = direction 
        else:
            direction = (pymunk.Vec2d(x , y) - self.body.position).angle
            self.body.angle = (direction - math.pi)
    def move(self):
        if self.body.velocity.length < (PLAYER_SPEED / 2):
            forward = pymunk.Vec2d(1, 0).rotated(self.body.angle)
            acceleration = forward * (ACCELERATION * .002)
            accel = pymunk.Vec2d(acceleration.x, acceleration.y)
            self.body.velocity += accel
        else:
            self.body.velocity *= DRAG_COEFFICENT

    def shoot(self, x, y):
        if self.timer <= 0:
            #print(f"shooting{x}{y}")
            shot = EnemyShoot(self.body.position.x, self.body.position.y, self.space, self.body.angle)
            self.updatable.add(shot)
            self.drawable.add(shot)
            shot.body.velocity = pymunk.Vec2d(1,0).rotated(self.body.angle) * 300
            self.space.add(shot.body, shot.shape)
            self.timer = PLAYER_SHOOT_COOLDOWN * 2
    def shoot_timer(self, dt):
        if self.timer > 0:
            self.timer -= dt    
    def bounds_check(self):
        super().bounds_check()
    def update(self, dt):
        super().update(dt)
        #if self.frame_timer > self.frame_interval:
         #   self.frame += 1
          #  if self.frame <= self.max_frame:
           #     self.frame_timer = 0
            #else:
             #   self.frame = 0
        #else:
         #   self.frame_timer += dt

        #self.frame_x = self.frame * self.sprite_width
        #self.crop_rect = pygame.Rect(self.frame_x, self.frame_y, self.sprite_width, self.sprite_height)
        #sub_surf = self.base_image.subsurface(self.crop_rect)
        angle_degrees = -math.degrees(self.body.angle)
        #self.sprite_image = pygame.transform.rotate(sub_surf, angle_degrees)
        self.sprite_image = pygame.transform.rotate(self.base_image, angle_degrees - 90)
        self.rect = self.sprite_image.get_rect(center=(int(self.body.position.x),int(self.body.position.y)))
        self.shoot_timer(dt)
