import pygame
import json
import os   
from state import State 
from userinterface import UserInterface 
class GameOver(State):
    def __init__(self, game, score): 
        super().__init__(game)
        self.score = score
        self.hudd = {"State": "Game Over"}
        self.menu_box = UserInterface(self.SCREEN_WIDTH / 2 , self.SCREEN_HEIGHT / 2 , 256, 64, "GravityRegular5", "Fonts/GravityRegular5.ttf", "Game Over!")
        self.updatable.add(self.menu_box)
        self.drawable.add(self.menu_box)

    def add_score(self):


    def update(self, dt):
        super().update(dt)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.exit_state()
                    self.exit_state()
                if event.key == pygame.K_q:
                    self.exit_state()
                    self.exit_state()

    def draw(self):
        super().draw()
        for obj in self.drawable:
            obj.draw()
            self.canvas.blit(obj.image, obj.rect)
        self.screen.blit(self.canvas,(0,0), self.camera.camera_box)

