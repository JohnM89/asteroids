from game.state import State 
from game.constants import * 
from game.userinterface import UserInterface
from .highscores import HighScores    
import pygame
from levels.level1 import Level1
class StartMenu(State):
    def __init__(self, game):
        super().__init__(game)
        self.hudd = {"Start":"___"}
        self.__font = "GravityRegular5"
        self.__font_path = "./assets/fonts/Fonts/GravityRegular5.ttf"
        self.sprite_array = [pygame.image.load('./assets/source/Super Pixel Sci-Fi UI - Futura Max/window_theme/window_theme_light_gray/panel_focused.png'), pygame.image.load('./assets/source/Super Pixel Sci-Fi UI - Futura Max/window_theme/window_theme_light_gray/panel_unfocused.png')]
        self.background = pygame.image.load('./assets/source/2D_ShootEmUp_GUI/PNG/UserInterface/Background/Background_1.png')
        self.background = pygame.transform.scale(self.background, (self.canvas.get_width(), self.canvas.get_height()))
        self.title_box = pygame.Rect(self.SCREEN_WIDTH /2, self.SCREEN_HEIGHT / 10, 256, 64 * 10)
        self.start_game = UserInterface(self.title_box.x, self.title_box.y + (64 * 2), 256, 64, self.__font, self.__font_path, "New Game", sprite_array=self.sprite_array )
        self.preferences = UserInterface(self.title_box.x , self.title_box.y + (64 * 4), 256, 64, self.__font, self.__font_path, "Preferences", sprite_array=self.sprite_array )        
        self.highscore = UserInterface(self.title_box.x, self.title_box.y + (64 * 6), 256, 64, self.__font, self.__font_path, "HighScore", sprite_array=self.sprite_array )        
        self.quit_game = UserInterface(self.title_box.x, self.title_box.y + (64 * 8) , 256, 64, self.__font, self.__font_path, "Quit", sprite_array=self.sprite_array )        
        self.hover = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()
        self.buttons.add(self.start_game, self.preferences, self.highscore, self.quit_game)
        self.button_list = list(self.buttons)
        self.updatable.add( self.start_game, self.preferences, self.highscore, self.quit_game)
        self.drawable.add(self.start_game, self.preferences, self.highscore, self.quit_game)
        self.current_index = 0
        self.current_button = None
        
    def update(self, dt):
        super().update(dt)
        self.hover.empty()
        for button in self.buttons:
            if button == self.current_button:
                self.hover.add(button)
                self.drawable.remove(button)
            else:
                self.drawable.add(button)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.current_index += 1
                    self.current_button = self.button_list[(self.current_index) % len(self.button_list) - 1]
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.current_index -= 1
                    self.current_button = self.button_list[(self.current_index) % len(self.button_list) - 1]
                if event.key == pygame.K_RETURN:
                    if self.current_button == self.start_game:
                        new_state = Level1(self.game)
                        new_state.enter_state()
                    if self.current_button == self.highscore:
                        new_state = HighScores(self.game)
                        new_state.enter_state()
                    if self.current_button == self.quit_game:
                        self.game.playing = False
                        self.game.running = False

            

    def draw(self):
        super().draw()
        self.canvas.blit(self.background, (0,0))
        for obj in self.hover:
            hover_rect = obj.rect.copy()
            hover_rect.inflate_ip(20, 10)
            self.canvas.blit(obj.image, hover_rect)
        for obj in self.drawable:
            obj.draw()
            self.canvas.blit(obj.image, obj.rect)
        self.screen.blit(self.canvas, (0,0), self.camera.camera_box)

