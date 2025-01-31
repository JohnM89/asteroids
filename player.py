import pygame
from circleshape import *
from constants import *
from shot import *

class Player(CircleShape):
    def __init__(self, x , y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.timer = 0
        self.respawn_timer = PLAYER_RESPAWN_TIMER
        #set a lives value starting with 3
        self.lives = 3
    #define the triangle
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    #draw updated object to screen
    def draw(self, screen):
        pygame.draw.polygon(screen, (255, 255, 255), self.triangle(), width=2)
    #set rotation based on turn speed and delta time
    def rotate(self, dt):
        self.rotation += (PLAYER_TURN_SPEED * dt)
    #update position based on vector , speed and delta time
    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt
    def shoot(self, position):
        if self.timer <= 0:
            shot = Shot(position.x, position.y)
            shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
            self.timer = PLAYER_SHOOT_COOLDOWN
        #listener for a,w,s,d, and calling respective movement functions
    def update(self, dt):
        if self.respawn_timer > 0:
            self.respawn_timer -= dt
        if self.timer > 0:
            self.timer -= dt
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.shoot(self.position)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(dt * -1)
        if keys[pygame.K_a]:
            self.rotate(dt * -1)
        if keys[pygame.K_d]:
            self.rotate(dt)

