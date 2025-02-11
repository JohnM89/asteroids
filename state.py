
from constants import *
from camera import Camera
import pygame
#parent state everything else will inherit from 
class State():
    def __init__(self, game):
        self.game = game
        self.prev_state = None
        self.GAME_WIDTH, self.GAME_HEIGHT = GAME_WIDTH, GAME_HEIGHT
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = SCREEN_WIDTH, SCREEN_HEIGHT
        self.canvas = pygame.Surface((self.GAME_WIDTH, self.GAME_HEIGHT))
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.camera = Camera(self.screen, self.canvas)
        self.updatable = pygame.sprite.Group()
        self.drawable = pygame.sprite.Group()
    def update(self, dt):
        self.updatable.update(dt)
        #self.camera.update_camera()

    def draw(self):
        self.canvas.fill((254, 0, 0))
        self.screen.fill((0,0,0))
        #self.screen.blit(self.canvas,(0,0), self.camera.camera_box)
        #self.drawable.draw(self.screen)

        #pass    

    def enter_state(self):
        if len(self.game.state_stack) > 1:
            self.prev_state = self.game.state_stack[-1]
        self.game.state_stack.append(self)

    def exit_state(self):
        self.game.state_stack.pop()

#future note use .convert() or convert_alpha() (for transparent bg) on images when loading them for performance 
