import pygame
from circleshape import *
from constants import *
import math
from shot import *

class Player(CircleShape):
    def __init__(self, x , y, shot_class, updatable, drawable, space):
        super().__init__(x, y, PLAYER_RADIUS, mass=.5)
        self.rotation = 0
        self.radius = PLAYER_RADIUS
        self.shots = shot_class
        self.updatable = updatable
        self.drawable = drawable
        self.space = space
        self.timer = 0
        self.player_colour = PLAYER_COLOUR
        self.flicker_colour = FLICKER_COLOUR
        self.current_colour = self.player_colour
        self.time_since_change = 0
        self.flash_interval = FLASH_INTERVAL
        self.respawn_timer = PLAYER_RESPAWN_TIMER
        self.shape.collision_type = 1
        self.shape.filter = pymunk.ShapeFilter(categories=0b00001)
        self.space.add(self.body, self.shape)
        self.lives = 99
        self.fuel = 50.0    
        self.bombs = 0
        self.game_object = self

        #requirement for utilizing sprite groups, currently just set to transparent
        self.image = pygame.Surface((2*self.radius, 2*self.radius), pygame.SRCALPHA)
        self.image = self.image.convert_alpha() 
        self.rect = self.image.get_rect(center=(self.body.position))

        
    #define the triangle
    def triangle(self):
        position = (self.radius , self.radius)
        rotation = math.radians(self.rotation)
        forward = pymunk.Vec2d(0, 1).rotated(self.rotation)
        right = pymunk.Vec2d(0, 1).rotated(rotation + 90) * self.radius / 1.5
        a = position + forward * self.radius
        b = position - forward * self.radius - right
        c = position - forward * self.radius + right
        return [a, b, c]
    #draw updated object to screen
    def draw(self):
        #pass
        self.image.fill((0,0,0,0))
        pygame.draw.polygon(self.image, self.current_colour, self.triangle(), width=2)
        #pygame.draw.circle(self.image, self.current_colour,(self.radius, self.radius), self.radius, width=2 )
    #set rotation based on turn speed and delta time
    def rotate(self, dt):
        rotation = math.radians(PLAYER_TURN_SPEED * dt)
        self.rotation += rotation
        #self.body.velocity.rotated(self.rotation)
        #self.rect.rotate(self.rotation)
    #update position based on vector , speed and delta time
    def move(self, dt):
        forward = pymunk.Vec2d(0, 1).rotated(self.rotation)
        if self.body.velocity.length < PLAYER_SPEED:
            acceleration = forward * ACCELERATION * dt
            self.body.velocity *= DRAG_COEFFICENT
            accel = pymunk.Vec2d(acceleration.x, acceleration.y)
            self.body.velocity += accel

    #def bomb(self):
        #if self.player.bombs > 0:
            #bomb = Bomb(position.x, position.y, space)
            #self.updatable.add(bomb)
            #self.drawable.add(bomb)

        
       


    def shoot(self, position, space):
        if self.timer <= 0:
            shot = Shot(position.x, position.y, space)
            self.shots.add(shot)
            self.updatable.add(shot)
            self.drawable.add(shot)
            shot.body.velocity = pymunk.Vec2d(0, 1).rotated(self.rotation) * PLAYER_SHOOT_SPEED
            self.space.add(shot.body, shot.shape)
            self.timer = PLAYER_SHOOT_COOLDOWN

    def handle_colour(self, dt):
        if self.respawn_timer > 0:
            self.respawn_timer -= dt    
            self.time_since_change += dt    

            if self.time_since_change >= self.flash_interval:
                if self.current_colour == self.player_colour:
                    self.current_colour = self.flicker_colour
                    self.time_since_change = 0
                else:
                    self.current_colour = self.player_colour
        #listener for a,w,s,d, and calling respective movement functions

    def shoot_timer(self, dt):
        if self.timer > 0:
            self.timer -= dt    

    def respawn_timer_fn(self, dt):
        if self.respawn_timer > 0:
            self.respawn_timer -= dt    
            self.handle_colour(dt)
        if self.respawn_timer <= 0:
            self.current_colour = self.player_colour

    def update(self, dt):
        self.respawn_timer_fn(dt)
        self.shoot_timer(dt)
        self.rect.center = (int(self.body.position.x), int(self.body.position.y))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.shoot(self.body.position, self.space)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(dt * -1)
        if keys[pygame.K_a]:
            self.rotate(dt * -1)
        if keys[pygame.K_d]:
            self.rotate(dt)

