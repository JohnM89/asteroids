from state import State 
from userinterface import UserInterface
from player import Player
from shot import Shot   
from asteroid import Asteroid   
from asteroidfield import AsteroidField
from pause import Pause
#from camera import Camera
from constants import *
import random
import pygame   

class Level1(State):
    def __init__(self, game):
        super().__init__(game)
        #this maintains scale   
        self.x = self.GAME_WIDTH / 2
        self.y = self.GAME_HEIGHT / 2
        self.hudd = {"score": 0, "lives": 3}
        #modify the screen variables to utilize camera 
        self.lives_ui = UserInterface((self.SCREEN_WIDTH - self.SCREEN_WIDTH / 8) - (HORIZONTAL_MARGIN / 6), (self.SCREEN_HEIGHT - 64) - (VERTICAL_MARGIN / 4), self.SCREEN_WIDTH / 8, 64, "GravityRegular5", "Fonts/GravityRegular5.ttf", self.hudd, "lives", "Lives: ")
        self.score_ui = UserInterface(HORIZONTAL_MARGIN / 6, VERTICAL_MARGIN / 4, self.SCREEN_WIDTH / 8, 64, "GravityRegular5", "Fonts/GravityRegular5.ttf", self.hudd, "score", "Score: ")
        #self.score_ui = UserInterface(0, 0, self.SCREEN_WIDTH / 8, 64, "GravityRegular5", "Fonts/GravityRegular5.ttf", self.hudd, "score", "Score: ")
        self.asteroids = pygame.sprite.Group()
        self.shots = pygame.sprite.Group()
        self.ui = pygame.sprite.Group()
        self.asteroidfield = AsteroidField(self.asteroids, self.updatable, self.drawable)
        self.player = Player(self.x, self.y, self.shots, self.updatable, self.drawable)
        #self.camera = Camera(self.player)
       
        self.updatable.add(self.player, self.asteroidfield, self.score_ui, self.lives_ui)
        self.drawable.add(self.player)

    def collision_check(self):
        for obj in self.asteroids:
            #find a way to make objects collide on occasion randomly
            #if obj.collisions(obj in self.asteroids):
                #if randint(1, 100) > 80:
                

            if obj.collisions(self.player):
                if self.player.lives > 0:
                    if self.player.respawn_timer <= 0:
                        self.player.lives -= 1  
                        self.player.respawn_timer = PLAYER_RESPAWN_TIMER
                        
                        self.hudd["lives"] = self.player.lives
                        
                        #make player and object trajectory and velcocity change after collision needs work !
                        #add and use mass property to determine return velocity?
                        temp_velocity = obj.velocity
                        previous_player_velocity = self.player.velocity
                        previous_player_velocity *= DRAG_COEFFICENT
                        temp_velocity *= DRAG_COEFFICENT
                        self.player.velocity = temp_velocity * 2
                        #obj.velocity = obj.velocity - previous_player_velocity / 2
                        #obj.velocity.rotate(obj.radius * DRAG_COEFFICENT)
                        #obj.velocity.rotate(random.uniform(20, 50))
                        #self.player.position = pygame.Vector2(obj.position.x + obj.radius, obj.position.y + obj.radius)

                else:
                    print("Game Over!")
                    self.exit_state()
                    
            for shot in self.shots:
                if obj.collisions(shot):
                    shot.kill()
                    self.hudd["score"] += 1 
                    obj.split(self.updatable, self.drawable, self.asteroids)
        #simple boundary wrapping for player need to put in player class
        #camera will follow player 
        if self.player.position.x > self.GAME_WIDTH:
            self.player.position.x = 0
        if self.player.position.x < 0:
            self.player.position.x = self.GAME_WIDTH
        if self.player.position.y > self.GAME_HEIGHT:
            self.player.position.y = 0
        if self.player.position.y < 0:
            self.player.position.y = self.GAME_HEIGHT

    def update(self, dt):
        super().update(dt)
        #self.camera.update_camera(self.player)
        self.collision_check()
        self.lives_ui.get_hudd(self.hudd)
        self.score_ui.get_hudd(self.hudd)
        self.updatable.update(dt)
        ###
        self.camera.update_camera(self.player)
        
        

        ###
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p]:
            new_state = Pause(self.game)
            new_state.enter_state()

    def draw(self):
        super().draw()
        #self.canvas.fill((253, 0, 0))
        #self.screen.fill((0,0,0))
        #self.camera.update_camera(self.player)        
        for obj in self.drawable:
            #obj_adjusted_rect = self.camera.apply(obj)
            #print(f"drawing {obj} at {obj_adjusted_rect}")
            obj.draw()
            #self.canvas.blit(obj.image, obj_adjusted_rect)
            self.canvas.blit(obj.image, obj.rect)

        self.screen.blit(self.canvas,(0,0), self.camera.camera_box)
        for obj in self.ui:
            obj.draw(self.screen)
        #self.lives_ui.draw()
        #self.score_ui.draw()
        #self.screen.blit(self.canvas,(0,0), self.camera.camera_box)

        
