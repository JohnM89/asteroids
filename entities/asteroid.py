import pygame
import random
import math
import os
from .circleshape import *
from game.constants import *
from effects.debris import Debris
#created in AsteroidField class
class Asteroid(CircleShape):
    def __init__(self, x, y, radius, space, level, kind, assets):
        super().__init__(x , y, radius)
        self.assets = assets
        self.meteor_types_small = self.assets.images_in('sprites/Asteroids_small')
        self.meteor_types_medium = self.assets.images_in('sprites/Asteroids_mid')
        self.meteor_types_large = self.assets.images_in('sprites/Asteroids_large')
        self.meteor_debris = self.assets.images_in('sprites/Asteroids_bits')
        self.kind = kind
        if self.kind == 1:
            self.base_image = random.choice(self.meteor_types_small)
        elif self.kind == 2:
            self.base_image = random.choice(self.meteor_types_medium)
        else:
            self.base_image = random.choice(self.meteor_types_large)
        self.image = pygame.Surface((3*self.radius,3*self.radius), pygame.SRCALPHA)
        #self.image = self.image.convert_alpha()
        #self.rect = self.image.get_rect(center=(x,y))
        self.rect = self.image.get_rect(center=(self.body.position))
        #self.base_image = img
        #self.base_image = pygame.image.load("./Export/Meteors - Chunks/0.5x/Meteor_4_A_Small.png")
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

        #self.image = pygame.Surface((2*self.radius, 2*self.radius), pygame.SRCALPHA)
        #self.image = self.image.convert_alpha()
        #self.rect = self.image.get_rect(center=(self.body.position))
        #self.rect.center = (int(self.body.position.x), int(self.body.position.y))
        #pygame.draw.circle(self.image, (255,255,255), (self.radius, self.radius), self.radius, width=2)
        self.space = space
        self.shape.friction = 9.0
        self.shape.elasticity = 0.2
        self.shape.collision_type = 2
        self.shape.mass = 100 * self.radius
        self.shape.filter = pymunk.ShapeFilter(categories=ASTEROID_CATEGORY, mask=ASTEROID_MASK)
        self.shape.game_object = self
        self.time_to_live = ASTEROID_TTL
        self.damage_accumulated = 0
        self.split_threshold = 5 * self.radius
        self.level = level
    
    #draw as circle with white colouring
    def draw(self):
        self.image.fill((0,0,0,0))
        #pygame.draw.circle(self.image,(255,255,255), (self.radius,self.radius), self.radius, 2)
        self.image.blit(self.sprite_image,(0,0))
        #pass
    #split method for breaking up asteroid on collision with shot
    def split(self, updatable, drawable, asteroid, space, normal, impulse, contact_point):
        self.kill()
        original_velocity = self.body.velocity
        space.remove(self.body, self.shape)
        self.level.current_asteroid_count -= 1
        print(self.level.current_asteroid_count)
        if self.body in space.bodies:
            space.remove(self.body, self.shape)
        #if radius is less than or equal to the min radius do nothing
        if self.radius <= ASTEROID_MIN_RADIUS:

            return
        else:
            self.kind -= 1
            #create an angle between 20 and 50 degrees
            angle_degrees = random.uniform(20, 50)
            angle = math.radians(angle_degrees)
            offset = normal * (self.radius)
            spawn_point = contact_point - offset
            #currently this is sorta accurate physics wise but its kinda lame for a shooter 
            #give a boost based on shot type 
            #either get rid of original_velocity reference or multiply by inverse impulse or something
            boost = 0.5
            #using rotate on asteroids velocity to create 2 new vectors going in opposite directions rotated by angle
            vector1 = normal.rotated(angle)
            vector2 = normal.rotated(-angle)
            ## for debris   
            vector3 = normal.rotated(angle / 2)
            vector4 = normal.rotated(angle * 2)
            vector5 = normal.rotated(-angle / 2)
            vector6 = normal.rotated(-angle * 2)
            extra_velocity3 = vector3 * (-impulse * boost)   
            extra_velocity4 = vector4 * (-impulse * boost)
            extra_velocity5 = vector5 * (-impulse * boost)
            extra_velocity6 = vector6 * (-impulse * boost)
            ### so much repition.. need to FIX
            extra_velocity1 = vector1 * (-impulse * boost)
            extra_velocity2 = vector2 * (-impulse * boost)
            #new radius is old radius minus the value of min radius
            radius = self.radius - ASTEROID_MIN_RADIUS
            #create 2 new asteroids, add velocity and accelerate by 1.2 
            self.level.current_asteroid_count += 1
            asteroid1 = Asteroid(spawn_point.x, spawn_point.y, radius, space, self.level, self.kind, self.assets)
            asteroid1.body.velocity = original_velocity + extra_velocity1
            self.level.current_asteroid_count += 1
            asteroid2 = Asteroid(spawn_point.x, spawn_point.y, radius, space, self.level, self.kind, self.assets)
            asteroid2.body.velocity = original_velocity + extra_velocity2
            debris1 = Debris(spawn_point.x, spawn_point.y, space, self.body.angle, random.choice(self.meteor_debris))
            debris1.body.velocity = original_velocity + extra_velocity3
            debris2 = Debris(spawn_point.x, spawn_point.y, space, self.body.angle, random.choice(self.meteor_debris))
            debris2.body.velocity = original_velocity + extra_velocity4
            debris3 = Debris(spawn_point.x, spawn_point.y, space, self.body.angle, random.choice(self.meteor_debris))
            debris3.body.velocity = original_velocity + extra_velocity5
            debris4 = Debris(spawn_point.x, spawn_point.y, space, self.body.angle, random.choice(self.meteor_debris))
            debris4.body.velocity = original_velocity + extra_velocity6
            updatable.add(asteroid1, asteroid2, debris1, debris2, debris3, debris4)
            drawable.add(asteroid1, asteroid2, debris1, debris2, debris3, debris4)
            asteroid.add(asteroid1, asteroid2)
            space.add(asteroid1.body, asteroid1.shape)
            space.add(asteroid2.body, asteroid2.shape)
            space.add(debris1.body, debris1.shape)
            space.add(debris2.body, debris2.shape)
            space.add(debris3.body, debris3.shape)
            space.add(debris4.body, debris4.shape)
    def bounds_check(self):
        if self.body.position.x > GAME_WIDTH or self.body.position.x < 0 or self.body.position.y > GAME_HEIGHT or self.body.position.y < 0:
            return True
    def update(self, dt):
        #if self.frame_timer > self.frame_interval:
        #    self.frame += 1
        #    if self.frame <= self.max_frame:
        #        self.frame_timer = 0
        #    else:
        #        self.frame = 0
        #else:
        #    self.frame_timer += dt

        #self.frame_x = self.frame * self.sprite_width
        #self.crop_rect = pygame.Rect(self.frame_x, self.frame_y, self.sprite_width, self.sprite_height)
        #sub_surf = self.base_image.subsurface(self.crop_rect)
        #angle_degrees = -math.degrees(self.body.angle)
        #self.sprite_image = pygame.transform.rotate(self.base_image, angle_degrees)
        #self.sprite_image = pygame.transform.rotate(sub_surf, angle_degrees)
        self.rect = self.sprite_image.get_rect(center=(int(self.body.position.x),int(self.body.position.y)))


        self.time_to_live -= dt 
        if self.time_to_live <= dt and self.bounds_check() == True:
            self.kill()
            self.level.current_asteroid_count -= 1
            self.space.remove(self.body, self.shape)
        self.rect.center = (int(self.body.position.x), int(self.body.position.y))
