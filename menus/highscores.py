import pygame
import json
import os
from game.constants import *
from game.state import State 
from game.userinterface import UserInterface 
class HighScores(State):
    def __init__(self, game): 
        super().__init__(game)
        self.highscores = ''
        self.score_box = pygame.Rect(self.SCREEN_WIDTH /2, self.SCREEN_HEIGHT / 4, 500, 500)
        self.add_score()


    
    def add_score(self):
        try:
            if os.path.isfile("./highscores/high_score.txt"):
                high_score_file = open("./highscores/high_score.txt", "r")
                lines = high_score_file.readlines()
                count = 1
                for line in lines:
                    if count <= 10:
                        score = line.strip()
                        new_score = UserInterface(self.score_box.x, self.score_box.y + (32 * count), 500, 32, "GravityRegular5", "./assets/fonts/Fonts/GravityRegular5.ttf", score )
                        self.updatable.add(new_score)
                        self.drawable.add(new_score)
                        count += 1
                    else:
                        break   
                high_score_file.close()
            else:
                no_score = UserInterface(self.score_box.x, self.score_box.y + (32 * 5), 400, 64, "GravityRegular5", "./assets/fonts/Fonts/GravityRegular5.ttf", "No High Score yet bud")
        except Exception as e:
            print("error", e)

    def update(self, dt):
        super().update(dt)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.exit_state()
                if event.key == pygame.K_q:
                    self.exit_state()

    def draw(self):
        super().draw()
        for obj in self.drawable:
            obj.draw()
            self.canvas.blit(obj.image, obj.rect)
        self.screen.blit(self.canvas,(0,0), self.camera.camera_box)

