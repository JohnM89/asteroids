from state import State 
from userinterface import UserInterface
from player import Player
from shot import Shot   
from asteroid import Asteroid   
from asteroidfield import AsteroidField
from constants import *
import pygame   

class Level1(State):
    def __init__(self, game):
        super().__init__(game)
        self.x = self.SCREEN_WIDTH / 2
        self.y = self.SCREEN_HEIGHT / 2
        self.hudd = {"score": 0, "lives": 3}
        self.lives_ui = UserInterface((self.SCREEN_WIDTH - self.SCREEN_WIDTH / 8) - (HORIZONTAL_MARGIN / 6), (self.SCREEN_HEIGHT - 64) - (VERTICAL_MARGIN / 4), self.SCREEN_WIDTH / 8, 64, "GravityRegular5", "Fonts/GravityRegular5.ttf", self.hudd, "lives", "Lives: ")
        self.score_ui = UserInterface(HORIZONTAL_MARGIN / 6, VERTICAL_MARGIN / 4, self.SCREEN_WIDTH / 8, 64, "GravityRegular5", "Fonts/GravityRegular5.ttf", self.hudd, "score", "Score: ")
        self.asteroids = pygame.sprite.Group()
        self.shots = pygame.sprite.Group()
        self.asteroidfield = AsteroidField(self.asteroids, self.updatable, self.drawable)
        self.player = Player(self.x, self.y, self.shots, self.updatable, self.drawable)
        
       
        self.updatable.add(self.player, self.asteroidfield, self.score_ui, self.lives_ui)
        self.drawable.add(self.player, self.score_ui, self.lives_ui)

    def collision_check(self):
        for obj in self.asteroids:
            if obj.collisions(self.player):
                if self.player.lives > 0:
                    if self.player.respawn_timer <= 0:
                        self.player.lives -= 1  
                        self.player.respawn_timer = PLAYER_RESPAWN_TIMER
                        self.hudd["lives"] = self.player.lives
                        self.player.position = pygame.Vector2(self.x, self.y)
                else:
                    print("Game Over!")
                    self.exit_state()
                    
            for shot in self.shots:
                if obj.collisions(shot):
                    shot.kill()
                    self.hudd["score"] += 1 
                    obj.split(self.updatable, self.drawable, self.asteroids)

    def update(self, dt):
        super().update(dt)
        self.collision_check()
        self.lives_ui.get_hudd(self.hudd)
        self.score_ui.get_hudd(self.hudd)
        self.updatable.update(dt)

    def draw(self):
        #super().draw()
        self.screen.fill((0, 0, 0))
        for obj in self.drawable:
            obj.draw(self.screen) 
        
