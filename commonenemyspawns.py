import pygame
import random
import math
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
            lambda y: pymunk.Vec2d(ALIEN_MAX_RADIUS, y * GAME_HEIGHT),
        ],
        [
            pymunk.Vec2d(-1,0),
            lambda y: pymunk.Vec2d(GAME_WIDTH - ALIEN_MAX_RADIUS, y * GAME_HEIGHT),
            
        ],
        [
            
            pymunk.Vec2d(0,1),
            lambda x: pymunk.Vec2d(x * GAME_WIDTH, ALIEN_MAX_RADIUS),
            

        ],
        [
            
            pymunk.Vec2d(0, -1),
            lambda x: pymunk.Vec2d(x * GAME_WIDTH, GAME_HEIGHT - ALIEN_MAX_RADIUS),
            
        ],
    ]

    def __init__(self, aliens, updatable, drawable, space, canvas, current_alien_count):
        
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
        self.alien_count = ALIEN_MAX_COUNT
        self.current_alien_count = current_alien_count

    def spawn(self, radius, position, velocity):
        types = [FlyingSaucer(position.x, position.y, radius, self.updatable, self.drawable, self.space, self.canvas, self.current_alien_count), Scourge(position.x, position.y, radius, self.space, self.canvas, self.current_alien_count)]
        alien = random.choice(types)
        #alien = types[1]
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
                segment = CentipedeHead(position.x + (1 * 2 * radius), position.y, radius, self.space, self.canvas, self.current_alien_count)
            else:
                segment = CentipedeBody(position.x + ((i + 1)*2*radius), position.y, radius, self.space)
            segments.append(segment)
            self.space.add(segment.body, segment.shape)
            self.updatable.add(segment)
            self.drawable.add(segment)
        for i in range(length - 1):
            body_a = segments[i].body   
            body_b = segments[i + 1].body   
            joint = pc.PinJoint(body_a, body_b, (0,0))
            joint.collide_bodies = False
            joint.stiffness = 1000.0
            self.space.add(joint)
            rotation_limit = pc.RotaryLimitJoint(body_a, body_b, math.pi / 6, -math.pi / 6)
            #rotation_limit.collide_bodies = False
            self.space.add(rotation_limit)
        segments[0].body.velocity = velocity
    def update(self, dt):
        self.spawn_timer += dt
        if self.spawn_timer > ALIEN_SPAWN_RATE and self.current_alien_count < self.alien_count:
            self.spawn_timer = 0
            self.current_alien_count += 1
            edge = random.choice(self.edges)
            speed = random.randint(40,100)
            velocity = edge[0] * speed
            velocity = velocity.rotated(random.randint(-30, 30))
            position = edge[1](random.uniform(0, 1))
            kind = random.randint(1, ALIEN_KINDS)
            if kind < 3:
                self.spawn(ALIEN_MIN_RADIUS * kind, position, velocity)
            else:
                self.spawn_centipede(ALIEN_MIN_RADIUS, position, velocity,6)
