from game.state import State
from game.constants import *
from game.userinterface import UserInterface
import pygame
import os
from .startmenu import StartMenu
#from level1 import Level1   
class Title(State):
    def __init__(self, game):
        super().__init__(game)
        self.background = pygame.image.load(os.path.join('assets', 'images',"blue-preview.png"))
        self.background = pygame.transform.scale(self.background, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        #self.canvas.blit(self.background, (0, 0))
        self.hudd = {"Start":"Game"}       
        self.title_box = UserInterface(self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2 , 256, 64, "GravityRegular5", "./assets/fonts/Fonts/GravityRegular5.ttf", "Asteroids")
        self.updatable.add(self.title_box)
        self.drawable.add(self.title_box)
    
    def update(self, dt):
        super().update(dt)
        
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                print("registered")
                if event.key == pygame.K_SPACE:
                    new_state = StartMenu(self.game)
                    new_state.enter_state()
    
    def draw(self):
        #pass
        super().draw()
        #self.canvas.fill((0, 0, 0))
        self.canvas.blit(self.background, (0,0))
        for obj in self.drawable:
            obj.draw()
            self.canvas.blit(obj.image, obj.rect)
        self.screen.blit(self.canvas, (0,0), self.camera.camera_box)
        #self.screen.fill((254, 0, 0))
        #self.title_box.draw()
