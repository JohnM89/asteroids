import pygame
import pymunk
from circleshape import *
from constants import *

class YamatoSprite(pygame.sprite.Sprite):
    def __init__(self, player, radius):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.player = player
        self.radius = radius
        self.space = player.space   
        self.canvas = player.canvas 
        self.x = player.body.position.x 
        self.y = player.body.position.y  
        self.image = pygame.Surface((2*self.radius, 2*self.radius), pygame.SRCALPHA)
        self.image = self.image.convert_alpha()  
        self.rect = self.image.get_rect(center=(self.x , self.y))
        #pygame.draw.circle(self.image,(255,255,255), (self.radius, self.radius), self.radius, width=2)
    def draw(self):
        self.image.fill((0,0,0,0))
        pygame.draw.circle(self.image,(255,255,255), (self.radius, self.radius), self.radius, width=2)
        
    def update(self,dt):
        charge_complete = 5
        
        self.radius = (self.radius ** dt)
        self.image = pygame.Surface((2*self.radius, 2*self.radius),pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x ,y))
           
