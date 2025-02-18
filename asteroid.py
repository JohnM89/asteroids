import pygame
import random
import math
from circleshape import *
from constants import *
#created in AsteroidField class
class Asteroid(CircleShape):
    def __init__(self, x, y, radius, space):
        super().__init__(x , y, radius)
        
        self.image = pygame.Surface((2*self.radius, 2*self.radius), pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect(center=(self.body.position))
        self.rect.center = (int(self.body.position.x), int(self.body.position.y))
        pygame.draw.circle(self.image, (255,255,255), (self.radius, self.radius), self.radius, width=2)
        self.space = space
        self.shape.friction = 9.0
        self.shape.elasticity = 0.2
        self.shape.collision_type = 2
        self.shape.mass = 100 * self.radius
        self.shape.filter = pymunk.ShapeFilter(categories=0b00010)
        self.shape.game_object = self
        self.time_to_live = ASTEROID_TTL
        self.damage_accumulated = 0
        self.split_threshold = 10 * self.radius
    
    #draw as circle with white colouring
    def draw(self):
        pass
    #split method for breaking up asteroid on collision with shot
    def split(self, updatable, drawable, asteroid, space, normal, impulse, contact_point):
        self.kill()
        original_velocity = self.body.velocity
        space.remove(self.body, self.shape)
        if self.body in space.bodies:
            space.remove(self.body, self.shape)
        #if radius is less than or equal to the min radius do nothing
        if self.radius <= ASTEROID_MIN_RADIUS:

            return
        else:
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
            extra_velocity1 = vector1 * (impulse * boost)
            extra_velocity2 = vector2 * (impulse * boost)
            #new radius is old radius minus the value of min radius
            radius = self.radius - ASTEROID_MIN_RADIUS
            #create 2 new asteroids, add velocity and accelerate by 1.2 
            asteroid1 = Asteroid(spawn_point.x, spawn_point.y, radius, space)
            asteroid1.body.velocity = original_velocity + extra_velocity1
            asteroid2 = Asteroid(spawn_point.x, spawn_point.y, radius, space)
            asteroid2.body.velocity = original_velocity + extra_velocity2
            updatable.add(asteroid1, asteroid2)
            drawable.add(asteroid1, asteroid2)
            asteroid.add(asteroid1, asteroid2)
            space.add(asteroid1.body, asteroid1.shape)
            space.add(asteroid2.body, asteroid2.shape)

    def bounds_check(self):
        if self.body.position.x > GAME_WIDTH or self.body.position.x < 0 or self.body.position.y > GAME_HEIGHT or self.body.position.y < 0:
            return True
    def update(self, dt):
        self.time_to_live -= dt 
        if self.time_to_live <= dt and self.bounds_check() == True:
            self.kill()
            self.space.remove(self.body, self.shape)
        self.rect.center = (int(self.body.position.x), int(self.body.position.y))
