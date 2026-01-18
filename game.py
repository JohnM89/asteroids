import pygame
import os
from game.constants import *
from game.asset_manager import AssetManager
from menus.title import Title 

class Game():
    def __init__(self):
        pygame.init()
        self.game_clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.dt = 0
        self.prev_time = 0
        self.running, self.playing = True, True
        self.default_state = None
        self.state_stack = []
        #load assets    
        self.assets = AssetManager('./local_assets/assets')
        self.start_state()

    def run(self):
        while self.playing:
                
            self.get_dt()
            self.handle_events()
            self.update()
            self.draw()

    def start_state(self):
        self.default_state = Title(self, self.assets)
        self.state_stack.append(self.default_state)                  
            
    def get_dt(self):
        #self.game_clock.tick(60)
        now = pygame.time.get_ticks()
        self.dt = (now - self.prev_time) / 1000.00
        self.prev_time = now
       

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
        if self.state_stack:
            self.state_stack[-1].handle_events(events)

    def update(self):
        if self.state_stack:
            self.state_stack[-1].update(self.dt)
    def draw(self):
        if self.state_stack:
            self.state_stack[-1].draw()      
        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    while game.running:
        game.run()
