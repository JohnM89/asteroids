import pygame
import random
from circleshape import *
from constants import *
#created in AsteroidField class
class Asteroid(CircleShape):
    def __init__(self, x, y, radius, space, mass=5.0):
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
        self.shape.game_object = self
        self.time_to_live = ASTEROID_TTL
        self.damage_accumulated = 0
        self.split_threshold = 100

    #draw as circle with white colouring
    def draw(self):
        pass
        #self.image.fill((0,0,0,0))
        #pygame.draw.circle(self.image,(255,255,255), (self.radius, self.radius), self.radius, width=2)
        #canvas.blit(self.image,self.rect)
    #split method for breaking up asteroid on collision with shot
    def split(self, updatable, drawable, asteroid, space):
        self.kill()
        space.remove(self.body, self.shape)
        if self.body in space.bodies:
            space.remove(self.body, self.shape)
        #if radius is less than or equal to the min radius do nothing
        if self.radius <= ASTEROID_MIN_RADIUS:

            return
        else:
            #create an angle between 20 and 50 degrees
            angle = random.uniform(20, 50)
            #using rotate on asteroids velocity to create 2 new vectors going in opposite directions rotated by angle
            #vector1 = self.velocity.rotate(angle)
            vector1 = self.body.velocity.rotated(angle)
            #vector2 = self.velocity.rotate(-angle)
            vector2 = self.body.velocity.rotated(-angle)

            #new radius is old radius minus the value of min radius
            radius = self.radius - ASTEROID_MIN_RADIUS
            #create 2 new asteroids, add velocity and accelerate by 1.2 
            #asteroid1 = Asteroid(self.position.x, self.position.y, radius)
            asteroid1 = Asteroid(self.body.position.x, self.body.position.y, radius, space)
            #asteroid1.velocity = vector1 * 1.2
            asteroid1.body.velocity = vector1 * 1.2
            #asteroid2 = Asteroid(self.position.x, self.position.y, radius)
            asteroid2 = Asteroid(self.body.position.x, self.body.position.y, radius, space)
            asteroid2.body.velocity = vector2 * 1.2
            #asteroid2.velocity = vector2 * 1.2
            updatable.add(asteroid1, asteroid2)
            drawable.add(asteroid1, asteroid2)
            asteroid.add(asteroid1, asteroid2)
            space.add(asteroid1.body, asteroid1.shape)
            space.add(asteroid2.body, asteroid2.shape)

    def bounds_check(self):
        if self.body.position.x > GAME_WIDTH or self.body.position.x < 0 or self.body.position.y > GAME_HEIGHT or self.body.position.y < 0:
            return True
    def update(self, dt):
        #self.position = pygame.Vector2(self.body.position.x, self.body.position.y)
        #self.position += (self.velocity * dt)
        #self.position += self.body.velocity * dt
        #self.rect.center = self.position
        self.time_to_live -= dt 
        if self.time_to_live <= dt and self.bounds_check() == True:
            self.kill()
            self.space.remove(self.body, self.shape)
        self.rect.center = (int(self.body.position.x), int(self.body.position.y))
