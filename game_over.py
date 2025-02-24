import pygame
import json
import os.path   
from state import State 
from userinterface import UserInterface
from font import FontManager    
class GameOver(State):
    def __init__(self, game, score): 
        super().__init__(game)
        self.score = score
        self.hudd = {"State": "Game Over"}
        self.player_input = ""
        self.menu_box = UserInterface(self.SCREEN_WIDTH / 2 , self.SCREEN_HEIGHT / 2 , 256, 64, "GravityRegular5", "Fonts/GravityRegular5.ttf", "Game Over!")
        self.user_input = UserInterface(self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 4, 256, 64, "GravityRegular5", "Fonts/GravityRegular5.ttf", self.player_input)
        self.updatable.add(self.menu_box, self.user_input)
        self.drawable.add(self.menu_box, self.user_input)
        self.active = True

    def add_score(self):

        try:
            if os.path.isfile("./high_score.txt"):
                high_score_file = open("./high_score.txt", "a", newline="\n")
                high_score_file.write(f"{self.player_input} : {self.score}\n")
                high_score_file.close()
            else:
                high_score_file = open("./high_score.txt", "w", newline="\n")
                high_score_file.write(f"{self.player_input} : {self.score}\n")
                high_score_file.close()

        except Exception as e:
            print("error", e)
            


        

    def update(self, dt):
        super().update(dt)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.player_input = self.player_input[:-1]
                    self.user_input.text = self.player_input
                elif event.key == pygame.K_RETURN:
                    self.add_score()
                    self.exit_state()
                    self.exit_state()
                    
                elif event.key == pygame.K_ESCAPE:
                    self.exit_state()
                    self.exit_state()
                else:
                    self.player_input += event.unicode
                    self.user_input.text = self.player_input

    def draw(self):
        super().draw()
        for obj in self.drawable:
            obj.draw()
            self.canvas.blit(obj.image, obj.rect)
        self.screen.blit(self.canvas,(0,0), self.camera.camera_box)

