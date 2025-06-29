import pygame
from game.state import State 
from game.userinterface import UserInterface 
class Pause(State):
    def __init__(self, game): 
        super().__init__(game)
        self.hudd = {"State": "Paused"}
        self.menu_box = UserInterface(self.SCREEN_WIDTH / 2 , self.SCREEN_HEIGHT / 2 , 256, 64, "GravityRegular5", "./assets/fonts/Fonts/GravityRegular5.ttf", "Paused")
        self.updatable.add(self.menu_box)
        self.drawable.add(self.menu_box)

    def update(self, dt):
        super().update(dt)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.exit_state()
                if event.key == pygame.K_q:
                    self.exit_state()
                    self.exit_state()
                    self.exit_state()

    def draw(self):
        super().draw()
        for obj in self.drawable:
            obj.draw()
            self.canvas.blit(obj.image, obj.rect)
        self.screen.blit(self.canvas,(0,0), self.camera.camera_box)

