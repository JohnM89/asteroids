import pygame
from circleshape import *
from constants import *
from shot import *

class Player(CircleShape):
    def __init__(self, x , y, shot_class, updatable, drawable):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shots = shot_class
        self.updatable = updatable
        self.drawable = drawable
        self.velocity = pygame.Vector2(0, 0)
        self.timer = 0
        self.player_colour = PLAYER_COLOUR
        self.flicker_colour = FLICKER_COLOUR
        self.current_colour = self.player_colour
        self.time_since_change = 0
        self.flash_interval = FLASH_INTERVAL
        self.respawn_timer = PLAYER_RESPAWN_TIMER
        #set a lives value starting with 3
        self.lives = 3

        #requirement for utilizing sprite groups, currently just set to transparent
        self.image = pygame.Surface((2*self.radius, 2*self.radius), pygame.SRCALPHA)
        self.image = self.image.convert_alpha() 
        self.rect = self.image.get_rect(center=(self.position))

        
        #self.rect = self.image.get_rect(center=(x, y))
    #define the triangle
    def triangle(self):
        position = (self.radius , self.radius)
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = position + forward * self.radius
        b = position - forward * self.radius - right
        c = position - forward * self.radius + right
        return [a, b, c]
    #draw updated object to screen
    def draw(self):
        self.image.fill((0,0,0,0))
            #pygame.draw.polygon(screen, self.current_colour, self.triangle(), width=2)
        #pygame.draw.polygon(self.image, self.current_colour, self.triangle(), width=2)
        pygame.draw.circle(self.image, self.current_colour,(self.radius, self.radius), self.radius, width=2 )
        #canvas.blit(self.image, self.rect)
    #set rotation based on turn speed and delta time
    def rotate(self, dt):
        
        self.rotation += (PLAYER_TURN_SPEED * dt)
        #self.position.rotate(self.rotation)
    #update position based on vector , speed and delta time
    def move(self, dt):
        if dt >= 0:
            forward = pygame.Vector2(0, 1).rotate(self.rotation)
        elif dt < 0:
            forward = pygame.Vector2(0, -1).rotate(self.rotation)
        if self.velocity.length() < PLAYER_SPEED:
            acceleration = forward * ACCELERATION
            self.velocity += acceleration * dt  
            self.velocity *= DRAG_COEFFICENT
            self.position += self.velocity * dt
    #continue flying after stopping acceleration
    def lingering_movement(self, dt):
        self.velocity *= DRAG_COEFFICENT
        self.position += self.velocity * dt


        
       


    def shoot(self, position):
        if self.timer <= 0:
            shot = Shot(position.x, position.y)
            self.shots.add(shot)
            self.updatable.add(shot)
            self.drawable.add(shot)
            shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
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
        self.lingering_movement(dt)
        self.rect.center = (self.position)
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
        #self.rect.center = (self.position.x, self.position.y)

