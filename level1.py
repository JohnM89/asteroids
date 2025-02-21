from state import State 
from userinterface import UserInterface
from player import Player
from shot import Shot   
from asteroid import Asteroid   
from asteroidfield import AsteroidField
from pause import Pause
from circleshape import CircleShape
from walls import Walls
from commonenemyspawns import * 
from pickup import *
from constants import *
import random
import pygame  
import pymunk
import random 

class Level1(State):
    def __init__(self, game):
        super().__init__(game)
        self.space = pymunk.Space()
        self.space.gravity = (0,0)
        self.x = self.GAME_WIDTH / 2
        self.y = self.GAME_HEIGHT / 2
        self.hudd = {"score": 0, "lives": 99}
        self.lives_ui = UserInterface(self.SCREEN_WIDTH - 86, self.SCREEN_HEIGHT - 64, self.SCREEN_WIDTH / 8, 64, "GravityRegular5", "Fonts/GravityRegular5.ttf", "Lives: ","lives", self.hudd)
        self.score_ui = UserInterface(128, 64, 256, 64, "GravityRegular5", "Fonts/GravityRegular5.ttf", "Score: ","score", self.hudd)
        self.walls = Walls(GAME_WIDTH, GAME_HEIGHT, self.space)
        self.asteroids = pygame.sprite.Group()
        self.shots = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.ui = pygame.sprite.Group()
        self.current_alien_count = 0
        self.current_asteroid_count = 0
        self.level = self
        self.asteroidfield = AsteroidField(self, self.asteroids, self.updatable, self.drawable, self.space)
        self.commonenemyspawns = CommonEnemySpawns(self.aliens, self.updatable, self.drawable, self.space, self.canvas, self.current_alien_count)
        self.player = Player(self.x, self.y, self.shots, self.updatable, self.drawable, self.space)
        self.hudd["lives"] = self.player.lives
        self.updatable.add(self.player, self.asteroidfield, self.commonenemyspawns, self.score_ui, self.lives_ui)
        self.drawable.add(self.player)

        self.player_asteroid_handler = self.space.add_collision_handler(1, 2)
        self.shot_asteroid_handler = self.space.add_collision_handler(2, 3)
        self.player_pickup_handler = self.space.add_collision_handler(1, 4)
        ####
        self.player_enemy_handler = self.space.add_collision_handler(1, 5)
        #!
        self.player_enemy_shot_handler = self.space.add_collision_handler(1, 6)
        
        self.enemy_shot_asteroid_handler = self.space.add_collision_handler(6, 2)
        #!
        self.shot_enemy_handler = self.space.add_collision_handler(3, 5)
        #!
        ###
        self.enemy_asteroid_handler = self.space.add_collision_handler(5, 2)
        #!
        ##

        #need a collision handler manager
        self.walls.draw_walls()
        self.player_asteroid_handler.post_solve = self.post_solve_p_a
    
        self.shot_asteroid_handler.post_solve = self.post_solve_s_a
        self.player_enemy_shot_handler.post_solve = self.post_solve_p_e_s

        self.enemy_shot_asteroid_handler.post_solve = self.post_solve_e_s_a
        self.shot_enemy_handler.post_solve = self.post_solve_s_e

        self.player_pickup_handler.begin = self.begin_p_p

        self.player_enemy_handler.post_solve = self.post_solve_p_e
        self.enemy_asteroid_handler.post_solve = self.post_solve_e_a


    def post_solve_p_e_s(self, arbiter, space, data):
        impact_force = arbiter.total_impulse.length
        impact_damage_threshold = 50.0
        objA, objB = arbiter.shapes
        e_shot = objB.game_object
        player = objA.game_object
        if arbiter.is_first_contact == True:
            player.health -= impact_force
        return True

    def post_solve_s_e(self, arbiter, space, data):
        impact_force = arbiter.total_impulse.length
        impact_damage_threshold = 10.0
        objA, objB = arbiter.shapes
        if objA.game_object.shape.collision_type == 3:
            enemy = objB.game_object
            shot = objA.game_object
        else:
            enemy = objA.game_object
            shot = objB.game_object
        print(enemy.damage_accumulated)
        enemy.damage_accumulated += impact_force
        self.hudd["score"] += 1
        if enemy.damage_accumulated >= enemy.split_threshold:
            if hasattr(enemy, "joints") and hasattr(enemy, "rotation_limit_list"):
                for joint in enemy.joints:
                    if joint in self.space.constraints:
                        self.space.remove(joint)
                for rotation in enemy.rotation_limit_list:
                    if rotation in self.space.constraints:
                        self.space.remove(rotation)
            self.commonenemyspawns.current_alien_count -= 1
            print(self.commonenemyspawns.current_alien_count)
            contact = arbiter.contact_point_set.points[0]
            contact_point = contact.point_a
            enemy.kill()
            self.create_drop(contact_point.x, contact_point.y, self.space, self.updatable, self.drawable)
            self.space.remove(enemy.body, enemy.shape)
        return True

    def post_solve_e_s_a(self, arbiter, space, data):
        impact_force = arbiter.total_impulse.length
        impact_damage_threshold = 50.0
        objA, objB = arbiter.shapes
        if objA.game_object.collision_type == 6:
            shot_obj = objA.game_object
            ast_obj = objB.game_object
        else:
            ast_obj = objA.game_object
            shot_obj = objB.game_object
        if arbiter.is_first_contact == True:
            ast_obj.damage_accumulated += impact_force
            if ast_obj.damage_accumulated >= ast_obj.split_threshold:
                shot_obj.kill()
                contact = arbiter.contact_point_set.points[0]
                contact_point = contact.point_a
                self.create_drop(contact_point.x, contact_point.y, self.space, self.updatable, self.drawable)
                normal = arbiter.normal
                impulse = arbiter.total_impulse.length
                ast_obj.split(self.updatable, self.drawable, self.asteroids, self.space, normal, impulse, contact_point)
                self.space.remove(shot_obj.body, shot_obj.shape)
        return True

    def post_solve_e_a(self, arbiter, space, data):
        impact_force = arbiter.total_impulse.length 
        impact_damage_threshold = 60.0
        objA, objB = arbiter.shapes
        if objA.game_object.shape.collision_type == 5:
            enemy = objA.game_object
            asteroid = objB.game_object
        else:
            enemy = objB.game_object
            asteroid = objA.game_object
        #if arbiter.is_first_contact == True:
        enemy.damage_accumulated += impact_force
        asteroid.damage_accumulated += impact_force
        if asteroid.damage_accumulated >= asteroid.split_threshold:
            contact = arbiter.contact_point_set.points[0]
            contact_point = contact.point_a
            self.create_drop(contact_point.x, contact_point.y, self.space, self.updatable, self.drawable)
            normal = arbiter.normal
            asteroid.split(self.updatable, self.drawable, self.asteroids, self.space, normal, impact_force, contact_point)
        if enemy.damage_accumulated >= enemy.split_threshold:
            if hasattr(enemy, "joints") and hasattr(enemy, "rotation_limit_list"):
                for joint in enemy.joints:
                    if joint in self.space.constraints:
                        self.space.remove(joint)
                for rotation in enemy.rotation_limit_list:
                    if rotation in self.space.constraints:
                        self.space.remove(rotation)
            self.commonenemyspawns.current_alien_count -= 1
            print(self.commonenemyspawns.current_alien_count)
            contact = arbiter.contact_point_set.points[0]
            contact_point = contact.point_a
            enemy.kill()
            self.space.remove(enemy.body, enemy.shape)
            self.create_drop(contact_point.x, contact_point.y, self.space, self.updatable, self.drawable)
        return True

    def post_solve_p_e(self, arbiter, space, data):
        impact_force = arbiter.total_impulse.length
        print(impact_force)
        impact_damage_threshold = 40.0
        objA, objB = arbiter.shapes
        if objA.game_object.shape.collision_type == 1:
            player = objA.game_object
        else:
            player = objB.game_object
        if arbiter.is_first_contact == True:
            player.health -= impact_force
            print(player.health)
        return True

    #pymunk collision handling functions
    
    ###
    def post_solve_s_a(self, arbiter, space, data):
        impact_force = arbiter.total_impulse.length
        impact_damage_threshold = 50.0
        objA, objB = arbiter.shapes
        #objA will always be 2 (asteroid) due to how its passed ot handler so you can omit this check 
        shot_obj = objB.game_object
        ast_obj = objA.game_object
        if arbiter.is_first_contact == True:            
            ast_obj.damage_accumulated += impact_force
            self.hudd["score"] += 1
            #make this a standalone funciton 
            if ast_obj.damage_accumulated >= ast_obj.split_threshold:
                shot_obj.kill()
                contact = arbiter.contact_point_set.points[0]
                contact_point = contact.point_a
                self.create_drop(contact_point.x, contact_point.y, self.space, self.updatable, self.drawable)
                normal = arbiter.normal
                impulse = arbiter.total_impulse.length
                print(self.current_asteroid_count)
                ast_obj.split(self.updatable, self.drawable, self.asteroids, self.space, normal, impulse, contact_point)
                self.space.remove(shot_obj.body, shot_obj.shape)
        return True



    def begin_p_p(self, arbiter, space, data):
        objA, objB = arbiter.shapes
        if hasattr(objB.game_object, "fuel"):
            self.player.fuel += objB.game_object.fuel
            objB.game_object.kill()
            self.space.remove(objB.game_object.body, objB.game_object.shape)
        elif hasattr(objB.game_object, "bomb"):
            self.player.bombs += objB.game_object.bomb
            objB.game_object.kill()
            self.space.remove(objB.game_object.body, objB.game_object.shape)
        return False
    #player - asteroid handler  
    def post_solve_p_a(self, arbiter, space, data):
        objA, objB = arbiter.shapes
        impact = arbiter.total_impulse.length
        impact_damage_threshold = 30.0
        if objA.game_object.shape.collision_type == 1:
            player = objA.game_object
            asteroid = objB.game_object
        if arbiter.is_first_contact == True:
            print(impact)
            print(player.health)
            if impact >= impact_damage_threshold:
                if player.lives > 0:
                    if player.respawn_timer <= 0:
                        player.health -= impact  
                        player.respawn_timer = PLAYER_RESPAWN_TIMER
                        self.hudd["lives"] = player.lives
            #else:
                #self.exit_state()
        return True 
    def pre_solve_p_a(self, arbiter, space, data):
        #dampen or conditionally ignore collision if sheilds or something
        #if self.player.respawn_timer > 0 and arbiter.is_first_contact == False:
        #    return False
        return True
        #pass
    #def post_solve_p_a(self, arbiter, space, data):
        #retreive collision impulse or kenetic energy to calculate sound volume and damage amount   
        #impulse = arbiter.total_impulse
        #kenetic_loss = arbiter.total_ke
        #print(impulse)
        #pass
    def separate(arbiter, space, data):
        pass
    ###
    def create_drop(self, position_x, position_y, space, updatable, drawable):
        drops = [FuelDrop(position_x,position_y, space), BombDrop(position_x, position_y, space)]
        new_drop = random.choice(drops)
        updatable.add(new_drop)
        drawable.add(new_drop)
        space.add(new_drop.body, new_drop.shape)

    def collision_check(self):                  
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
        
