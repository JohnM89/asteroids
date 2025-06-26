from game.state import State 
from game.constants import * 
from game.userinterface import UserInterface
from .highscores import HighScores 
from effects.selection_button import SelectionButton
import pygame
from levels.level1 import Level1
class StartMenu(State):
    def __init__(self, game):
        super().__init__(game)
        self.hudd = {"Start":"___"}
        self.__font = "GravityRegular5"
        self.__font_path = "./assets/fonts/Fonts/GravityRegular5.ttf"
        self.raised_button = pygame.image.load('./assets/source/Pixel UI & HUD/Sprites/Buttons/White/ButtonDigital_Pressed.png')
        self.sprite_array = [pygame.image.load('./assets/source/Pixel UI & HUD/Sprites/Buttons/White/ButtonDigital_Pressed.png'), pygame.image.load('./assets/source/Pixel UI & HUD/Sprites/Buttons/White/ButtonDigital_Pressed.png')]
        self.done_animate = False
        self.unpressed_button = self.sprite_array.copy()
        self.background = pygame.image.load('./assets/source/pixelart_starfield_corona.png')
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
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
                button.sprite_image = self.raised_button.copy()
                button_animate = SelectionButton(self, button.x, button.y)
                if self.done_animate:
                    self.hover.add(button)
                #self.drawable.add(button_animate)
                #self.updatable.add(button_animate)
                self.drawable.remove(button)
            else:
                #button.sprite_image = self.sprite_array[0]
                self.drawable.add(button)
                #self.drawable.remove(self.button_animate)
                #self.updatable.remove(self.button_animate)

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
            #obj.sprite_image = self.raised_button.copy()
            hover_rect = obj.rect.copy()
            #obj.sprite_image = self.unpressed_button[0]
            #to have it stand out 
            #hover_rect.inflate_ip(20, 10)
            
            self.canvas.blit(obj.image, hover_rect)
        for obj in self.drawable:
            obj.draw()
            self.canvas.blit(obj.image, obj.rect)
        self.screen.blit(self.canvas, (0,0), self.camera.camera_box)

