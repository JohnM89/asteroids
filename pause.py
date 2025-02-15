import pygame
from state import State 
from userinterface import UserInterface 
class Pause(State):
    def __init__(self, game): 
        super().__init__(game)
        self.hudd = {"State": "Paused"}
        self.menu_box = UserInterface(self.SCREEN_WIDTH / 2 , self.SCREEN_HEIGHT / 2 , 256, 64, "GravityRegular5", "Fonts/GravityRegular5.ttf", self.hudd, "State", "Paused")
        self.updatable.add(self.menu_box)
        self.drawable.add(self.menu_box)

    def update(self, dt):
        super().update(dt)
        self.menu_box.get_hudd(self.hudd)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.exit_state()
        if keys[pygame.K_q]:
            self.exit_state()
            self.exit_state()

    def draw(self):
        super().draw()
        for obj in self.drawable:
            obj.draw()
            self.canvas.blit(obj.image, obj.rect)
        self.screen.blit(self.canvas,(0,0), self.camera.camera_box)

