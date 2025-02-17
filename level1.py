from state import State 
from userinterface import UserInterface
from player import Player
from shot import Shot   
from asteroid import Asteroid   
from asteroidfield import AsteroidField
from pause import Pause
from circleshape import CircleShape
from constants import *
import random
import pygame  
import pymunk

class Level1(State):
    def __init__(self, game):
        super().__init__(game)
        self.space = pymunk.Space()
        self.space.gravity = (0,0)
        self.x = self.GAME_WIDTH / 2
        self.y = self.GAME_HEIGHT / 2
        self.hudd = {"score": 0, "lives": 99}
        self.lives_ui = UserInterface(self.SCREEN_WIDTH - 86, self.SCREEN_HEIGHT - 64, self.SCREEN_WIDTH / 8, 64, "GravityRegular5", "Fonts/GravityRegular5.ttf", self.hudd, "lives", "Lives: ")
        self.score_ui = UserInterface(128, 64, 256, 64, "GravityRegular5", "Fonts/GravityRegular5.ttf", self.hudd, "score", "Score: ")
        self.asteroids = pygame.sprite.Group()
        self.shots = pygame.sprite.Group()
        self.ui = pygame.sprite.Group()
        self.asteroidfield = AsteroidField(self.asteroids, self.updatable, self.drawable, self.space)
        self.player = Player(self.x, self.y, self.shots, self.updatable, self.drawable, self.space)
        self.hudd["lives"] = self.player.lives
        self.updatable.add(self.player, self.asteroidfield, self.score_ui, self.lives_ui)
        self.drawable.add(self.player)
        self.player_asteroid_handler = self.space.add_collision_handler(1, 2)
        self.shot_asteroid_handler = self.space.add_collision_handler(2, 3)
        self.shot_player_handler = self.space.add_collision_handler(1, 3)

        self.player_asteroid_handler.begin = self.begin_p_a
        self.player_asteroid_handler.post_solve = self.post_solve_p_a
        self.player_asteroid_handler.pre_solve = self.pre_solve_p_a
    
        self.shot_asteroid_handler.post_solve = self.post_solve_s_a
        #self.shot_asteroid_handler.post_solve
        #self.shot_asteroid_handler.pre_solve


    #pymunk collision handling functions
    ###
    def post_solve_s_a(self, arbiter, space, data):
        impact_force = arbiter.total_impulse.length
        print(impact_force)
        impact_damage_threshold = 50.0
        objA, objB = arbiter.shapes
        if objB.collision_type == 3:
            shot_obj = objB.game_object
            ast_obj = objA.game_object
        elif objA.collision_type == 3:
            shot_obj = objA.game_object
            ast_obj = objB.game_object
        if arbiter.is_first_contact == True:            
            ast_obj.damage_accumulated += impact_force
            self.hudd["score"] += 1
            if ast_obj.damage_accumulated >= ast_obj.split_threshold:
                shot_obj.kill()
                ast_obj.split(self.updatable, self.drawable, self.asteroids, self.space )
                self.space.remove(shot_obj.body, shot_obj.shape)
        return True


    #player - asteroid handler  
    def begin_p_a(self, arbiter, space, data):
        objA, objB = arbiter.shapes
        if arbiter.is_first_contact == True:
            if self.player.lives > 0:
                if self.player.respawn_timer <= 0:
                    self.player.lives -= 1  
                    self.player.respawn_timer = PLAYER_RESPAWN_TIMER
                    self.hudd["lives"] = self.player.lives
            #else:
                #self.exit_state()
        return True 
    def pre_solve_p_a(self, arbiter, space, data):
        #dampen or conditionally ignore collision if sheilds or something
        #if self.player.respawn_timer > 0 and arbiter.is_first_contact == False:
        #    return False
        return True
        #pass
    def post_solve_p_a(self, arbiter, space, data):
        #retreive collision impulse or kenetic energy to calculate sound volume and damage amount   
        #impulse = arbiter.total_impulse
        #kenetic_loss = arbiter.total_ke
        #print(impulse)
        pass
    def separate(arbiter, space, data):
        pass
    ###

    def collision_check(self):
        for obj in self.asteroids:
            #find a way to make objects collide on occasion randomly
            #if obj.collisions(obj in self.asteroids):
                #if randint(1, 100) > 80:
                
            pass                    
        #simple boundary wrapping for player need to put in player class
        if self.player.body.position.x > self.GAME_WIDTH:
            self.player.body.position = (0, self.player.body.position.y)
        if self.player.body.position.x < 0:
            self.player.body.position = (self.GAME_WIDTH, self.player.body.position.y)
        if self.player.body.position.y > self.GAME_HEIGHT:
            self.player.body.position = (self.player.body.position.x, 0)
        if self.player.body.position.y < 0:
            self.player.body.position = (self.player.body.position.x,self.GAME_HEIGHT)
    
    def end_game(self):
        if self.player.lives <= 0:
            self.exit_state()

    def update(self, dt):
        super().update(dt)
        self.space.step(dt)
        self.collision_check()
        self.end_game()
        self.lives_ui.get_hudd(self.hudd)
        self.score_ui.get_hudd(self.hudd)
        self.updatable.update(dt)
        ###
        self.camera.update_camera(self.player)
        

        circle_shapes = [obj for obj in self.drawable if isinstance(obj, CircleShape)]
        for obj in circle_shapes:
            for obj2 in circle_shapes:
                if obj is not obj2:
                    obj.apply_gravity(obj2, dt)

        ###
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p]:
            new_state = Pause(self.game)
            new_state.enter_state()

    def draw(self):
        super().draw()   
        for obj in self.drawable:
            obj.draw()
            self.canvas.blit(obj.image, obj.rect)

        self.screen.blit(self.canvas,(0,0), self.camera.camera_box)
        self.lives_ui.draw(self.screen)
        self.score_ui.draw(self.screen)
        
