from game.state import State 
from game.constants import * 
from game.userinterface import UserInterface
#from .highscores import HighScores 
#from effects.selection_button import SelectionButton
import pygame
from .level1_animate import Level1Animate
class SelectCharacter(State):
    def __init__(self, game):
        super().__init__(game)
        self.hudd = {"Start":"___"}
        self.__font = "GravityRegular5"
        # self.__font_path = "./assets/fonts/Fonts/GravityRegular5.ttf"
        self.__font_path = "./local_assets/assets/fonts/Fonts/GravityRegular5.ttf"
        # self.raised_button = pygame.image.load('./assets/source/Pixel UI & HUD/Sprites/Panels/Blue/FrameDigitalB.png')
        self.raised_button = pygame.image.load('./local_assets/assets/source/Pixel UI & HUD/Sprites/Panels/Blue/FrameDigitalB.png')

        # self.spaceshipA = [pygame.image.load('./assets/source/Warped Collection Files/Assets/Space Shooters/Starfighter/sprites/Ships/ship-a/Sprites/ship-a1.png')]
        # self.spaceshipB = [pygame.image.load('./assets/source/Warped Collection Files/Assets/Space Shooters/Starfighter/sprites/Ships/ship-b/Sprites/ship-b1.png')]
        # self.spaceshipC = [pygame.image.load('./assets/battlecruiser.png')]
        self.spaceshipA = [pygame.image.load('./local_assets/assets/source/Warped Collection Files/Assets/Space Shooters/Starfighter/sprites/Ships/ship-a/Sprites/ship-a1.png')]
        self.spaceshipB = [pygame.image.load('./local_assets/assets/source/Warped Collection Files/Assets/Space Shooters/Starfighter/sprites/Ships/ship-b/Sprites/ship-b1.png')]
        self.spaceshipC = [pygame.image.load('./local_assets/assets/battlecruiser.png')]
        

        #self.sprite_array = [pygame.image.load('./assets/source/Pixel UI & HUD/Sprites/Buttons/White/ButtonDigital_Pressed.png'), pygame.image.load('./assets/source/Pixel UI & HUD/Sprites/Buttons/White/ButtonDigital_Pressed.png')]
        self.done_animate = False
        #self.unpressed_button = self.sprite_array.copy()
        #self.background = pygame.image.load('./assets/source/pixelart_starfield_corona.png')
        #self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.title_box = pygame.Rect(self.SCREEN_WIDTH /2, self.SCREEN_HEIGHT / 2 , 128, 256)
        #self.choose_your_character = UserInterface(self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 8, 128,128, self.__font, self.__font_path, "Choose Your Character")
        self.shipA = UserInterface(self.title_box.x - 256, self.title_box.y, 128, 128, self.__font, self.__font_path, "", sprite_array=self.spaceshipA  )
        self.shipB = UserInterface(self.title_box.x , self.title_box.y, 128, 128, self.__font, self.__font_path, "", sprite_array=self.spaceshipB)        
        self.shipC = UserInterface(self.title_box.x + 256, self.title_box.y, 128, 128, self.__font, self.__font_path, "", sprite_array=self.spaceshipC)        
        #self.quit_game = UserInterface(self.title_box.x, self.title_box.y + (64 * 8) , 256, 64, self.__font, self.__font_path, "Quit", sprite_array=None )        
        self.raised_button_image = pygame.Surface((194, 256), pygame.SRCALPHA)
        self.button_fade_overlay = pygame.Surface((194,256), pygame.SRCALPHA)
        self.button_fade_rect = self.button_fade_overlay.get_rect(center=(self.shipA.x, self.shipA.y))
        self.button_fade_overlay.set_alpha(175)
        self.raised_button_rect = self.raised_button_image.get_rect(center=(self.shipA.x,self.shipA.y))
        self.raised_button_copy = self.raised_button.copy()
        self.raised_button_copy = pygame.transform.scale(self.raised_button_copy, (206,256))
        self.selected_sprite = self.shipA.sprite_image
        self.hover = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()
        self.buttons.add(self.shipA, self.shipB, self.shipC)
        self.button_list = list(self.buttons)
        self.updatable.add( self.shipA, self.shipB, self.shipC )
        self.drawable.add( self.shipA, self.shipB, self.shipC )
        self.current_index = 0
        self.current_button = None
        self.last_button = None
        #self.output_font = pygame.font.Font(self.__font_path, 64)  # size it big for editing
        #self.text_surface = self.output_font.render("ASTEROIDS", True, (255, 255, 255))  # white on transparent

        #pygame.image.save(self.text_surface, "title_text.png")
        
    def update(self, dt):
        super().update(dt)
        self.hover.empty()
        for button in self.buttons:
            if button == self.current_button:
                self.selected_sprite = button.sprite_image
                #button.overlay_active = True
                #button_animate = SelectionButton(self, self.title_box.x, button.y)
                #if button != self.last_button:
                #button.sprite_image = self.raised_button.copy()
                    #self.last_button = button
                    #button_animate = SelectionButton(self, self.title_box.x, button.y)
                button.font_colour = (0,0,0)
            
                #elif button == self.last_button:
                    
                    #button_animate
                    #button.sprite_image = self.sprite_array[0]
                #if self.done_animate:
                self.hover.add(button)
                #self.drawable.add(button_animate)
                #self.updatable.add(button_animate)
                self.drawable.remove(button)
            else:
                #button.overlay_active = False
                button.font_colour = (255,255,255)
                self.drawable.add(button)
                #self.drawable.remove(self.button_animate)
                #self.updatable.remove(self.button_animate)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.current_index += 1
                    self.current_button = self.button_list[(self.current_index) % len(self.button_list) - 1]
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.current_index -= 1
                    self.current_button = self.button_list[(self.current_index) % len(self.button_list) - 1]
                if event.key == pygame.K_RETURN:
                    #if self.current_button == self.start_game:
                    new_state = Level1Animate(self.game, self.selected_sprite)
                    new_state.enter_state()
                    #if self.current_button == self.highscore:
                        #new_state = HighScores(self.game)
                        #new_state.enter_state()
                    #if self.current_button == self.quit_game:
                        #self.game.playing = False
                        #self.game.running = False

            

    def draw(self):
        super().draw()
        self.canvas.fill((0,0,0))
        #self.canvas.blit(self.background, (0,0))
        for obj in self.hover:
            #obj.sprite_image = self.sprite_array[0]
            #hover_rect = obj.rect.copy()
            #obj.sprite_image = self.unpressed_button[0]
            #to have it stand out 
            #hover_rect.inflate_ip(20, 10)

            self.raised_button_rect = self.raised_button_image.get_rect(center=(obj.x ,obj.y ))
            self.canvas.blit(obj.image, obj.rect)
            self.canvas.blit(self.raised_button_copy, self.raised_button_rect)
        for obj in self.drawable:
            obj.draw()
            self.button_fade_rect = self.button_fade_overlay.get_rect(center=(obj.x,obj.y))

            #self.raised_button_rect = self.raised_button_image.get_rect(center=(obj.x ,obj.y ))
            self.canvas.blit(obj.image, obj.rect)
            self.button_fade_overlay.fill((0,0,0))

            #self.canvas.blit(self.raised_button_copy, self.raised_button_rect)
            self.canvas.blit(self.button_fade_overlay, self.button_fade_rect)
        self.screen.blit(self.canvas, (0,0), self.camera.camera_box)

