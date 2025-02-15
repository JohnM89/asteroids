from state import State
from constants import *
from userinterface import UserInterface
import pygame
from startmenu import StartMenu
#from level1 import Level1   
class Title(State):
    def __init__(self, game):
        super().__init__(game)
        self.hudd = {"Start":"Game"}       
        self.title_box = UserInterface(self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2 , 256, 64, "GravityRegular5", "Fonts/GravityRegular5.ttf", self.hudd, "Start", "Title Screen")
        self.updatable.add(self.title_box)
        self.drawable.add(self.title_box)
    
    def update(self, dt):
        super().update(dt)
        self.title_box.get_hudd(self.hudd)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            new_state = StartMenu(self.game)
            new_state.enter_state()
    
    def draw(self):
        #pass
        super().draw()
        #self.canvas.fill((0, 0, 0))
        for obj in self.drawable:
            obj.draw()
            self.canvas.blit(obj.image, obj.rect)
        self.screen.blit(self.canvas, (0,0), self.camera.camera_box)
        #self.screen.fill((254, 0, 0))
        #self.title_box.draw()
