import pygame
import json
import os
import re
from game.constants import *
from game.state import State 
from game.userinterface import UserInterface 
class HighScores(State):
    def __init__(self, game, assets): 
        super().__init__(game)
        self.assets = assets
        self.highscores = ''
        # self.background = pygame.image.load('./assets/images/blue-preview.png')
        # self.background = pygame.image.load('./local_assets/assets/images/blue-preview.png')
        self.background = self.assets.image('images/blue-preview.png')
        self.background = pygame.transform.scale(self.background, (self.camera.camera_box.width, self.camera.camera_box.height))
        # self.highscore_banner = [pygame.image.load('./assets/source/2D_ShootEmUp_GUI/PNG/UserInterface/Leaderboard_Menu/Highscore_Bar_BG.png').convert_alpha()]
        # self.score_window = [pygame.image.load('./assets/source/Super Pixel Sci-Fi UI - Futura Max/premade/512x512/window_theme/window_theme_yellow/panel_unfocused.png').convert_alpha()]
        # self.highscore_banner = [pygame.image.load('./local_assets/assets/source/2D_ShootEmUp_GUI/PNG/UserInterface/Leaderboard_Menu/Highscore_Bar_BG.png').convert_alpha()]
        # self.score_window = [pygame.image.load('./local_assets/assets/source/Super Pixel Sci-Fi UI - Futura Max/premade/512x512/window_theme/window_theme_yellow/panel_unfocused.png').convert_alpha()]
        self.highscore_banner = [self.assets.image('source/2D_ShootEmUp_GUI/PNG/UserInterface/Leaderboard_Menu/Highscore_Bar_BG.png')]
        self.score_window = [self.assets.image('source/Super Pixel Sci-Fi UI - Futura Max/premade/512x512/window_theme/window_theme_yellow/panel_unfocused.png')]
        self.score_box = UserInterface(self.SCREEN_WIDTH /2, self.SCREEN_HEIGHT / 2, 512, 512, sprite_array=self.score_window)
        self.updatable.add(self.score_box)
        self.drawable.add(self.score_box)
        self.add_score()


    
    def add_score(self):
        try:
            if os.path.isfile("./highscores/high_score.txt"):
                high_score_file = open("./highscores/high_score.txt", "r")
                lines = high_score_file.readlines()
                sorted_lines = sorted(lines, key=lambda line: int(re.search(r'\d+', line).group()) if re.search(r'\d', line) else 0, reverse=True)
                count = 1
                for line in sorted_lines:
                    if count <= 10:
                        score = line.strip()
                        # new_score = UserInterface(self.score_box.x, (self.score_box.y / 2) + (34 * count), 500, 32, "GravityRegular5", "./assets/fonts/Fonts/GravityRegular5.ttf", score, sprite_array=self.highscore_banner )
                        new_score = UserInterface(self.score_box.x, (self.score_box.y / 2) + (34 * count), 500, 32, "GravityRegular5", "./local_assets/assets/fonts/Fonts/GravityRegular5.ttf", score, sprite_array=self.highscore_banner )
                        self.updatable.add(new_score)
                        self.drawable.add(new_score)
                        count += 1
                    else:
                        break   
                high_score_file.close()
            else:
                # no_score = UserInterface(self.score_box.x, self.score_box.y + (32 * 5), 400, 64, "GravityRegular5", "./assets/fonts/Fonts/GravityRegular5.ttf", "No High Score yet bud")
                no_score = UserInterface(self.score_box.x, self.score_box.y + (32 * 5), 400, 64, "GravityRegular5", "./local_assets/assets/fonts/Fonts/GravityRegular5.ttf", "No High Score yet bud")
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
        self.canvas.blit(self.background, (0,0), self.camera.camera_box)
        for obj in self.drawable:
            obj.draw()
            self.canvas.blit(obj.image, obj.rect)
        self.screen.blit(self.canvas,(0,0), self.camera.camera_box)

