import pygame
import random
import pymunk
from asteroid import Asteroid
from constants import *

class AsteroidField(pygame.sprite.Sprite):
    #define the edges of the screen by mappin
    edges = [
        [
            #Vector2 defines the direction for the velocity of the asteroid when it spawns
            #points right along the x-axis
            #pygame.Vector2(1,0),
            pymunk.Vec2d(1,0),
            #lambda function to generate a starting position for the asteroid on the screen's edge
            #ASTEROID_MAX_RADIUS ensures the asteroid starts off screen
            #y is the multiplyer for SCREEN_HEIGHT ( or x for SCREEN_WIDTH below) determining where along the edge the asteroid will appear
            #updating screen for game height after adding camera class  
            #lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * GAME_HEIGHT),
            lambda y: pymunk.Vec2d(-ASTEROID_MAX_RADIUS, y * GAME_HEIGHT),
        ],
        [
            #points left on x-axis
            #pygame.Vector2(-1,0),
            pymunk.Vec2d(-1,0),
            lambda y: pymunk.Vec2d(GAME_WIDTH + ASTEROID_MAX_RADIUS, y * GAME_HEIGHT),
            #lambda y: pygame.Vector2(GAME_WIDTH + ASTEROID_MAX_RADIUS, y * GAME_HEIGHT),
        ],
        [
            #points up on y-axis
            #pygame.Vector2(0,1),
            pymunk.Vec2d(0,1),
            lambda x: pymunk.Vec2d(x * GAME_WIDTH, -ASTEROID_MAX_RADIUS),
            #lambda x: pygame.Vector2(x * GAME_WIDTH, -ASTEROID_MAX_RADIUS),

        ],
        [
            #points down on y-axis
            #pygame.Vector2(0,-1),
            pymunk.Vec2d(0, -1),
            lambda x: pymunk.Vec2d(x * GAME_WIDTH, GAME_HEIGHT + ASTEROID_MAX_RADIUS),
            #lambda x: pygame.Vector2(x * GAME_WIDTH, GAME_HEIGHT + ASTEROID_MAX_RADIUS),
        ],
    ]

    def __init__(self, asteroids, updatable, drawable, space):
        #pygame.sprite.Sprite.__init__(self, self.containers)
        pygame.sprite.Sprite.__init__(self)
        #initalize timer at 0
        #self.asteroid_count = 0
        self.asteroids = asteroids
        self.updatable = updatable
        self.drawable = drawable
        self.space = space
        self.spawn_timer = 0.0

    def spawn(self, radius, position, velocity, space):
        asteroid = Asteroid(position.x, position.y, radius, space)
        #update asteroid with given velocity
        #asteroid.velocity = velocity
        asteroid.body.velocity = velocity
        self.asteroids.add(asteroid)
        self.updatable.add(asteroid)
        self.drawable.add(asteroid)
        self.space.add(asteroid.body, asteroid.shape)

    def update(self, dt):
        self.spawn_timer += dt
        #if spawn_timer overtakes spawn rate reset spawn_timer and spawn new asteroid
        if self.spawn_timer > ASTEROID_SPAWN_RATE:
            self.spawn_timer = 0
            #self.asteroid_count += 1
            #spawn a new asteroid at random edge
            edge = random.choice(self.edges)
            #determine a random speed in range
            speed = random.randint(40,100)
            #velocity takes vector point and multiplys by speed
            velocity = edge[0] * speed
            #randomly rotates within in a range
            #velocity = velocity.rotate(random.randint(-30, 30))
            velocity = velocity.rotated(random.randint(-30, 30))
            #determine inital position
            #uses float between 0 and 1 as the multiplyer against height or width giving a random position on the "edge" without surpassing max height or width
            position = edge[1](random.uniform(0, 1))
            #type of asteroid is an int between 1 and 20, which will determine radius
            kind = random.randint(1, ASTEROID_KINDS)
            #spawn a new instance of an asteroid
            self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity, self.space)
