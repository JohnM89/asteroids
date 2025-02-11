import pygame
import random
from circleshape import *
from constants import *
#created in AsteroidField class
class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x , y, radius)
        
        self.image = pygame.Surface((2*self.radius, 2*self.radius))
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect(center=(self.position))

    #draw as circle with white colouring
    def draw(self):
        self.image.fill((0,0,0,0))
        pygame.draw.circle(self.image,(255,255,255), (self.radius, self.radius), self.radius, width=2)
        #canvas.blit(self.image,self.rect)
    #split method for breaking up asteroid on collision with shot
    def split(self, updatable, drawable, asteroid):
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
            updatable.add(asteroid1, asteroid2)
            drawable.add(asteroid1, asteroid2)
            asteroid.add(asteroid1, asteroid2)
    def update(self, dt):
        self.position += (self.velocity * dt)
        self.rect.center = self.position
