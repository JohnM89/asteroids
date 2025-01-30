import pygame
import random
from circleshape import *
from constants import *
#created in AsteroidField class
class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x , y, radius)
    #draw as circle with white colouring
    def draw(self, screen):
        pygame.draw.circle(screen,(255,255,255), self.position, self.radius, width=2)
    #split method for breaking up asteroid on collision with shot
    def split(self):
        self.kill()
        #if radius is less than or equal to the min radius do nothing
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        else:
            #create an angle between 20 and 50 degrees
            angle = random.uniform(20, 50)
            #using rotate on asteroids velocity to create 2 new vectors going in opposite directions rotated by angle
            vector1 = self.velocity.rotate(angle)
            vector2 = self.velocity.rotate(-angle)
            #new radius is old radius minus the value of min radius
            radius = self.radius - ASTEROID_MIN_RADIUS
            #create 2 new asteroids, add velocity and accelerate by 1.2 
            asteroid1 = Asteroid(self.position.x, self.position.y, radius)
            asteroid1.velocity = vector1 * 1.2    
            asteroid2 = Asteroid(self.position.x, self.position.y, radius)
            asteroid2.velocity = vector2 * 1.2
    def update(self, dt):
        self.position += (self.velocity * dt)

