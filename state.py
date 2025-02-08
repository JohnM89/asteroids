
from constants import *
import pygame
#parent state everything else will inherit from 
class State():
    def __init__(self, game):
        self.game = game
        self.prev_state = None
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = SCREEN_WIDTH, SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.updatable = pygame.sprite.Group()
        self.drawable = pygame.sprite.Group()
    def update(self, dt):
        self.updatable.update(dt)
  

    def draw(self):
        #self.drawable.draw(self.screen)
        pass    

    def enter_state(self):
        if len(self.game.state_stack) > 1:
            self.prev_state = self.game.state_stack[-1]
        self.game.state_stack.append(self)

    def exit_state(self):
        self.game.state_stack.pop()
