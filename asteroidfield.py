import pygame
import random
from asteroid import Asteroid
from constants import *

class AsteroidField(pygame.sprite.Sprite):
    #define the edges of the screen by mappin
    edges = [
        [
            #Vector2 defines the direction for the velocity of the asteroid when it spawns
            #points right along the x-axis
            pygame.Vector2(1,0),
            #lambda function to generate a starting position for the asteroid on the screen's edge
            #ASTEROID_MAX_RADIUS ensures the asteroid starts off screen
            #y is the multiplyer for SCREEN_HEIGHT ( or x for SCREEN_WIDTH below) determining where along the edge the asteroid will appear
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ],
        [
            #points left on x-axis
            pygame.Vector2(-1,0),
            lambda y: pygame.Vector2(SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ],
        [
            #points up on y-axis
            pygame.Vector2(0,1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),

        ],
        [
            #points down on y-axis
            pygame.Vector2(0,-1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS),
        ],
    ]

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        #initalize timer at 0
        self.spawn_timer = 0.0

    def spawn(self, radius, position, velocity):
        asteroid = Asteroid(position.x, position.y, radius)
        #update asteroid with given velocity
        asteroid.velocity = velocity

    def update(self, dt):
        self.spawn_timer += dt
        #if spawn_timer overtakes spawn rate reset spawn_timer and spawn new asteroid
        if self.spawn_timer > ASTEROID_SPAWN_RATE:
            self.spawn_timer = 0
            #spawn a new asteroid at random edge
            edge = random.choice(self.edges)
            #determine a random speed in range
            speed = random.randint(40,100)
            #velocity takes vector point and multiplys by speed
            velocity = edge[0] * speed
            #randomly rotates within in a range
            velocity = velocity.rotate(random.randint(-30, 30))
            #determine inital position
            #uses float between 0 and 1 as the multiplyer against height or width giving a random position on the "edge" without surpassing max height or width
            position = edge[1](random.uniform(0, 1))
            #type of asteroid is an int between 1 and 20, which will determine radius
            kind = random.randint(1, ASTEROID_KINDS)
            #spawn a new instance of an asteroid
            self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity)
