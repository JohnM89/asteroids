import pygame
from .circleshape import *
from game.constants import *
import math
from effects.explosions.thrust import Thrust
from .bomb import Bomb
from effects.explosions.bomb_explosion import BombExplode
from .yamato import Yamato
from .rocket import Rocket
from .shot import *

class Player(CircleShape):
    def __init__(self, player_sprite, x , y, shot_class, updatable, drawable, space, canvas):
        super().__init__(x, y, 32, mass=.5)
        self.rotation = 0
        #self.angle_degrees = 0
        self.canvas = canvas
        self.player_sprite = player_sprite
        self.image = pygame.Surface((3*self.radius, 3*self.radius), pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        #self.rect = self.image.get_rect(center=(x,y))
        self.rect = self.image.get_rect(center=(self.body.position))
        self.base_image = self.player_sprite
        #self.base_image = pygame.image.load("./assets/images/Red_Player_Ship_9_Small.png")
        self.base_image = pygame.transform.scale(self.base_image, (2*self.radius, 2*self.radius))
        self.sprite_image = self.base_image.copy()
        ###
        #self.sprite_width = 64
        #self.sprite_height = 32
        #self.frame_interval = 0.75
        #self.frame_timer = 0
        #self.frame = 0
        #self.max_frame = 9
        #self.frame_y = 0
        #self.frame_x = 0
        #self.crop_rect = (self.frame_x, self.frame_y, self.sprite_width, self.sprite_height)
        ###
        self.radius = PLAYER_RADIUS
        self.shots = shot_class
        self.updatable = updatable
        self.drawable = drawable
        self.space = space
        self.timer = 0
        self.rocket_timer = 0
        self.yamato_timer = 0   
        self.yamato_charge = 0
        self.player_colour = PLAYER_COLOUR
        self.flicker_colour = FLICKER_COLOUR
        self.current_colour = self.player_colour
        self.time_since_change = 0
        self.flash_interval = FLASH_INTERVAL
        self.respawn_timer = PLAYER_RESPAWN_TIMER
        self.shape.collision_type = 1
        self.shape.filter = pymunk.ShapeFilter(categories=PLAYER_CATEGORY, mask=PLAYER_MASK)
        self.space.add(self.body, self.shape)
        self.thrust = None
        self.lives = 1
        self.health = 100
        self.fuel = 100    
        self.bombs = 99
        self.yamato = 0
        self.multishot = 0
        self.rockets = 99
        self.sheilds = 1    
        self.sheilds_health = 100
        #self.sheild_hit = False
        self.shape.game_object = self


        
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
        self.image.fill((0,0,0,0))
        #pygame.draw.circle(self.sprite_image, self.current_colour, (self.radius, self.radius), self.radius, width=2)


        self.image.blit(self.sprite_image, (0,0))
    #set rotation based on turn speed and delta time
    def rotate(self, dt):
        rotation = math.radians(PLAYER_TURN_SPEED * dt)
        self.rotation += rotation

    #update position based on vector , speed and delta time
    def move(self, dt):
        if self.fuel > 0:

            forward = pymunk.Vec2d(1, 0).rotated(self.rotation)
            if self.body.velocity.length < PLAYER_SPEED:
                acceleration = forward * ACCELERATION * dt
                accel = pymunk.Vec2d(acceleration.x, acceleration.y)
                self.body.velocity += accel
            else:
                self.body.velocity *= DRAG_COEFFICENT
            self.fuel -= 0.0001
            #self.updatable.remove(thrust)
            #self.drawable.remove(thrust)
            #print(self.fuel)
        #else:
            #pass
    def return_stats(self):
        return self.fuel, self.health
    
    #lets just borrow shot cooldown until we refactor event handling for keys in player class 
    def bomb(self):
        if self.bombs > 0 and self.timer <=0:
            self.bombs -= 1

            bomb = Bomb( 150 )
            bomb.explode(self.body.position.x, self.body.position.y, self.space)
            bomb_sprite = BombExplode(self.body.position.x, self.body.position.y)
            self.updatable.add(bomb_sprite)
            self.drawable.add(bomb_sprite)
            self.timer = PLAYER_SHOOT_COOLDOWN
    def health_check(self):
        if self.sheilds_health <= 0:
            if self.sheilds > 0:
                self.sheilds -= 1   
                self.sheilds_health = 100
            else:
                self.sheilds_health = 0
            if self.sheilds <= 0:
                if self.sheilds_health <= 0:
                    if self.health <= 0:
                        if self.lives > 0:
                            self.lives -= 1
                            self.health = 100 
                        else:
                            self.health = 0


    def shoot(self, position, space, rotation):
        if self.timer <= 0:
            shot = Shot(position.x, position.y, space, rotation)
            self.shots.add(shot)
            self.updatable.add(shot)
            self.drawable.add(shot)
            shot.body.velocity = pymunk.Vec2d(1, 0).rotated(self.rotation) * PLAYER_SHOOT_SPEED
            self.space.add(shot.body, shot.shape)
            self.timer = PLAYER_SHOOT_COOLDOWN

    def multishot(self, position, space, rotation):
        if self.timer <= 0:
            shot1 = Shot(position.x, position.y, space, rotation)
            shot2 = Shot(position.x, position.y, space, rotation)
            shot3 = Shot(position.x, position.y, space, rotation) 
            self.updatable.add(shot1, shot2, shot3)
            self.drawable.add(shot1, shot2, shot3)
            shot1.body.velocity = pymunk.Vec2d(1,0).rotated(self.rotation) * PLAYER_SHOOT_SPEED 
            shot2.body.velocity = pymunk.Vec2d(0,1).rotated(self.rotation) * PLAYER_SHOOT_SPEED
            shot3.body.velocity = pymunk.Vec2d(1,1).rotated(self.rotation) * PLAYER_SHOOT_SPEED    
            self.space.add(shot1.body, shot1.shape)
            self.space.add(shot2.body, shot2.shape)
            self.space.add(shot3.body, shot3.shape)
            self.timer = PLAYER_SHOOT_COOLDOWN


    def fire_rocket(self, position, space, rotation, canvas):
        if self.rocket_timer <= 0:
            if self.rockets > 0:
                self.rockets -= 1 
                rocket = Rocket(position.x, position.y, space, rotation, canvas, self.updatable, self.drawable)
                self.updatable.add(rocket)
                self.drawable.add(rocket)
                rocket.body.velocity = pymunk.Vec2d(1, 0).rotated(self.rotation) * (PLAYER_SHOOT_SPEED * 1.5)
                self.space.add(rocket.body, rocket.shape)
                self.rocket_timer = PLAYER_SHOOT_COOLDOWN 
    #def animate_sheild(self):
        #hit = SheildHit(self.body.position.x, self.body.position.y)
    
    #def yamato_cannon(self, position, space):
        #if self.yamato_timer <=0:
            #self.yamato -= 1
            #yamato = YamatoSprite(self, YAMATO_RADIUS)
            #self.yamato_timer = PLAYER_SHOOT_COOLDOWN * 4


    #def charge_yamato(self, yamato):
        #charge_complete = 5
        #if self.yamato_charge < charge_complete:
            #c = YamatoSprite(position.x, position.y, radius)
        #if self.yamato_charge >= charge_complete:
            #self.yamato_charge += dt
            #yamato = Yamato(position.x, position.y, space)
            #self.updatable.add(yamato)
            #self.drawable.add(yamato)
            #self.space.add(yamato.body, yamato.shape)
        

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
        if self.rocket_timer > 0:
            self.rocket_timer -= dt

    def respawn_timer_fn(self, dt):
        if self.respawn_timer > 0:
            self.respawn_timer -= dt    
            self.handle_colour(dt)
        if self.respawn_timer <= 0:
            self.current_colour = self.player_colour

    def update(self, dt):
        self.health_check()
        self.respawn_timer_fn(dt)
        self.shoot_timer(dt)
        angle_degrees = -math.degrees(self.rotation)
        self.sprite_image = pygame.transform.rotate(self.base_image, angle_degrees - 90)
        self.rect = self.sprite_image.get_rect(center=(int(self.body.position.x), int(self.body.position.y)))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.shoot(self.body.position, self.space, self.rotation)
        if keys[pygame.K_m]:
            self.multishot(self.body.position, self.space, self.rotation)
        if keys[pygame.K_r]:
            self.fire_rocket(self.body.position, self.space, self.rotation, self.canvas)
        if keys[pygame.K_w]:
            if not self.thrust:
                self.thrust = Thrust(self, (self.body.position.x, self.body.position.y), self.body.position.rotated(self.rotation))

            self.move(dt)
        if keys[pygame.K_s]:

            self.move(dt * -1)
        if keys[pygame.K_a]:

            self.rotate(dt * -1)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_b]:
            self.bomb()

