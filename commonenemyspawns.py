import pygame
import random
import pymunk
import pymunk.constraints as pc 
from scourge import Scourge 
from flyingsaucer import FlyingSaucer
from centipedehead import CentipedeHead
from centipedebody import CentipedeBody
from constants import *

class CommonEnemySpawns(pygame.sprite.Sprite):
    edges = [
        [
            pymunk.Vec2d(1,0),
            lambda y: pymunk.Vec2d(-ALIEN_MAX_RADIUS, y * GAME_HEIGHT),
        ],
        [
            pymunk.Vec2d(-1,0),
            lambda y: pymunk.Vec2d(GAME_WIDTH + ALIEN_MAX_RADIUS, y * GAME_HEIGHT),
            
        ],
        [
            
            pymunk.Vec2d(0,1),
            lambda x: pymunk.Vec2d(x * GAME_WIDTH, -ALIEN_MAX_RADIUS),
            

        ],
        [
            
            pymunk.Vec2d(0, -1),
            lambda x: pymunk.Vec2d(x * GAME_WIDTH, GAME_HEIGHT + ALIEN_MAX_RADIUS),
            
        ],
    ]

    def __init__(self, aliens, updatable, drawable, space, canvas):
        
        pygame.sprite.Sprite.__init__(self)
        #for debug
        ##
        self.canvas = canvas
        ##
        self.aliens = aliens
        self.updatable = updatable
        self.drawable = drawable
        self.space = space
        self.spawn_timer = 0.0

    def spawn(self, radius, position, velocity):
        types = [FlyingSaucer(position.x, position.y, radius, self.space, self.canvas), Scourge(position.x, position.y, radius, self.space)]
        #alien = random.choice(types)
        alien = types[0]
        alien.body.velocity = velocity
        self.aliens.add(alien)
        self.updatable.add(alien)
        self.drawable.add(alien)
        self.space.add(alien.body, alien.shape)

    def spawn_centipede(self, radius, position, velocity, body_count):
        segments = []
        length = body_count
        for i in range(length):
            if i == 0:
                segment = CentipedeHead(position.x + (i * 2 * radius), position.y, radius, self.space)
            else:
                segment = CentipedeBody(position.x + ((i + 1)*2*radius), position.y, radius, self.space)
            segments.append(segment)
            self.space.add(segment.body, segment.shape)
            self.updatable.add(segment)
            self.drawable.add(segment)
        for i in range(length - 1):
            body_a = segments[i].body   
            body_b = segments[i + 1].body   
            joint = pc.PivotJoint(body_a, body_b, (0,0), (0, 0))
            self.space.add(joint)
            rotation_limit = pc.RotaryLimitJoint(body_a, body_b, -0.25, 0.25)
            self.space.add(rotation_limit)
        #segments[0].body.velocity = velocity
    def update(self, dt):
        self.spawn_timer += dt
        if self.spawn_timer > ALIEN_SPAWN_RATE:
            self.spawn_timer = 0
            edge = random.choice(self.edges)
            speed = random.randint(40,100)
            velocity = edge[0] * speed
            velocity = velocity.rotated(random.randint(-30, 30))
            position = edge[1](random.uniform(0, 1))
            kind = random.randint(1, ALIEN_KINDS)
            print(kind)
            self.spawn(ALIEN_MIN_RADIUS * kind, position, velocity)
            #self.spawn_centipede(ALIEN_MIN_RADIUS * kind, position, velocity,6)
