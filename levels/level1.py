from game.state import State 
from game.userinterface import UserInterface
from entities.player import Player
from entities.shot import Shot   
from entities.asteroid import Asteroid 
from effects.explosions.explosion_animate import Explosion 
from .asteroidfield import AsteroidField
from menus.pause import Pause
from menus.game_over import GameOver  
from entities.circleshape import CircleShape
from effects.explosions.rocket_impact_explosion import RocketImpact
from effects.explosions.shot_impact import ShotImpact
from effects.explosions.shot_splat import ShotSplat
from effects.explosions.blood_splat import BloodSplat
from effects.explosions.sheild_hit import SheildHit
from entities.walls import Walls
from .commonenemyspawns import * 
from entities.pickup import *
from game.constants import *
from game.headsup import HeadsUp
from game.collision_manager import CollisionManager
import random
import pygame  
import pymunk
import random 

class Level1(State):
    def __init__(self, game, player_sprite):
        super().__init__(game)
        ###
        self.space = pymunk.Space()
        self.collision_manager = CollisionManager()
        self.space.gravity = (0,0)
        self.player_sprite = player_sprite
        ###
        self.x = self.GAME_WIDTH / 2
        self.y = self.GAME_HEIGHT / 2
        self.score = 0  
        self.scaling_factor = 1 #+ math.floor((self.score * 0.001))
        self.max_asteroids = MAX_ASTEROIDS #* self.scaling_factor
        self.alien_max_count = ALIEN_MAX_COUNT #* self.scaling_factor
        self.asteroid_spawn_rate = ASTEROID_SPAWN_RATE #* self.scaling_factor
        self.alien_spawn_rate = ALIEN_SPAWN_RATE #* self.scaling_factor
        self.acceleration = ACCELERATION #* self.scaling_factor
        self.current_alien_count = 0
        self.current_asteroid_count = 0
        ###

        self.background_layer = pygame.image.load('./assets/source/Bright/blue_green.png').convert_alpha()        #for img in self.background_layers:
        self.background_layer_stars1 = pygame.image.load('./assets/source/stars_blue.png').convert_alpha()
        
        self.background_layer_stars2 = pygame.image.load('./assets/source/stars_yellow.png').convert_alpha()

        self.background_layer_stars1 = pygame.transform.scale(self.background_layer_stars1, (GAME_WIDTH, GAME_HEIGHT))
        self.background_layer_stars2 = pygame.transform.scale(self.background_layer_stars2, (GAME_WIDTH, GAME_HEIGHT))
        self.background_layer_stars2 = pygame.transform.rotate(self.background_layer_stars2, 90)
        self.background_layer = pygame.transform.scale(self.background_layer, (GAME_WIDTH, GAME_HEIGHT))
        #self.canvas_background = pygame.image.load('./assets/images/layer2.png').convert_alpha()
        #self.canvas_background = pygame.transform.scale_by(self.canvas_background, 3)
       # self.hud_display = HeadsUp()
        ###
        self.hudd = {"score": 0, "lives": 99, "fuel": 50,"health": 100, "sheilds_health": 100}
        self.hud_display = HeadsUp(256 + 8, self.SCREEN_HEIGHT - 16, 512, 256, hudd=self.hudd)
        #self.hud_display = HeadsUp(self.SCREEN_WIDTH /2, self.SCREEN_HEIGHT / 2, 1052, 352, hudd=self.hudd)
        #self.lives_ui = UserInterface(self.SCREEN_WIDTH - 86, self.SCREEN_HEIGHT - 64, self.SCREEN_WIDTH / 8, 64, "GravityRegular5", "./assets/fonts/Fonts/GravityRegular5.ttf", "Lives: ","lives", self.hudd)
        #self.score_ui = UserInterface(128, 64, 256, 64, "GravityRegular5", "./assets/fonts/Fonts/GravityRegular5.ttf", "Score: ","score", self.hudd)
        #self.fuel_ui = UserInterface(128, self.SCREEN_HEIGHT - 64, 256, 64, "GravityRegular5", "./assets/fonts/Fonts/GravityRegular5.ttf", "Fuel: ", "fuel", self.hudd)
        #self.health_ui = UserInterface(128, self.SCREEN_HEIGHT - 128, 256, 64, "GravityRegular5", "./assets/fonts/Fonts/GravityRegular5.ttf", "Health: ", "health", self.hudd) 
        ###
        self.walls = Walls(GAME_WIDTH, GAME_HEIGHT, self.space)
        self.walls.draw_walls()
        ###
        self.asteroids = pygame.sprite.Group()
        self.shots = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.ui = pygame.sprite.Group()
        ###
        self.level = self
        ###
        self.asteroidfield = AsteroidField(self)
        self.commonenemyspawns = CommonEnemySpawns(self)
        ###
        self.player = Player(self.player_sprite, self.x, self.y, self.shots, self.updatable, self.drawable, self.space, self.canvas)

        #self.background_layer = pygame.transform.scale(self.background_layer, (GAME_WIDTH, GAME_HEIGHT))
        self.hudd["lives"] = self.player.lives
        self.hudd["score"] = self.score
        self.hudd["health"] = self.player.health    
        ###
        self.updatable.add(self.player, self.asteroidfield, self.commonenemyspawns) #self.score_ui, self.lives_ui)
        self.drawable.add(self.player)
        ###
        self.collision_manager.register(1,2, self.post_solve_p_a)
        self.collision_manager.register(2,3, self.post_solve_s_a)
        self.collision_manager.register(1,6, self.post_solve_p_e_s)
        self.collision_manager.register(6,2, self.post_solve_e_s_a)
        self.collision_manager.register(3,5, self.post_solve_s_e)
        self.collision_manager.register(1,4, self.begin_p_p, phase="begin")
        self.collision_manager.register(1,5, self.post_solve_p_e)
        self.collision_manager.register(5,2, self.post_solve_e_a)
        self.collision_manager.register(7,2, self.post_solve_r_a)
        self.collision_manager.register(7,5, self.post_solve_r_e)



        #self.player_asteroid_handler = self.space.add_collision_handler(1, 2)
        #self.shot_asteroid_handler = self.space.add_collision_handler(2, 3)
        #self.player_pickup_handler = self.space.add_collision_handler(1, 4)
        #self.player_enemy_handler = self.space.add_collision_handler(1, 5)
        #self.player_enemy_shot_handler = self.space.add_collision_handler(1, 6)
        #self.enemy_shot_asteroid_handler = self.space.add_collision_handler(6, 2)
        #self.shot_enemy_handler = self.space.add_collision_handler(3, 5)
        #self.enemy_asteroid_handler = self.space.add_collision_handler(5, 2)
        #self.rocket_asteroid_handler = self.space.add_collision_handler(7, 2)
        #self.rocket_enemy_handler = self.space.add_collision_handler(7, 5)

        #need a collision handler manager class
        #self.player_asteroid_handler.post_solve = self.post_solve_p_a
        #self.shot_asteroid_handler.post_solve = self.post_solve_s_a
        #self.player_enemy_shot_handler.post_solve = self.post_solve_p_e_s
        #self.enemy_shot_asteroid_handler.post_solve = self.post_solve_e_s_a
        #self.shot_enemy_handler.post_solve = self.post_solve_s_e
        #self.player_pickup_handler.begin = self.begin_p_p
        #self.player_enemy_handler.post_solve = self.post_solve_p_e
        #self.enemy_asteroid_handler.post_solve = self.post_solve_e_a
        #self.rocket_asteroid_handler.post_solve = self.post_solve_r_a   
        #self.rocket_enemy_handler.post_solve = self.post_solve_r_e  
        self.collision_manager.install(self.space)
        ###


    #def post_solve_r_a(self, arbiter, space, data):
    #    impact_force = arbiter.total_impulse.length
        #if impact_force >= IMPACT_THRESHOLD:
        #sort out shot impact
    #    if impact_force >= 50:
     #       damage = max(min(impact_force * IMPACT_NORMALIZER * self.scaling_factor, MAX_IMPACT_DAMAGE),MIN_IMPACT_DAMAGE)
      #  else:
      #      damage = MAX_IMPACT_DAMAGE 
      #  objA, objB = arbiter.shapes
      #  if objB.game_object.shape.collision_type == 7:
      #      r_shot = objB.game_object
      #      ast_obj = objA.game_object
       # elif objA.game_object.shape.collision_type == 7:
       #     ast_obj = objB.game_object
        #    r_shot = objA.game_object
        #if arbiter.is_first_contact == True:
         #   ast_obj.damage_accumulated += damage
         #   contact = arbiter.contact_point_set.points[0]
         #   contact_point = contact.point_a
         #   if arbiter.shapes[0].collision_type != 7:
         #       impact = RocketImpact(contact_point, -arbiter.normal, ast_obj)
         #   else:
         #       impact = RocketImpact(contact_point, arbiter.normal, ast_obj)
         #   self.updatable.add(impact)
         #   self.drawable.add(impact)
         #   r_shot.kill()
            #self.hudd["score"] += 1
            #make this a standalone funciton
       #     if ast_obj.damage_accumulated >= ast_obj.split_threshold:
        #        self.score += 1
        #        contact = arbiter.contact_point_set.points[0]
         #       contact_point = contact.point_a
         #       explosion = Explosion(contact_point.x, contact_point.y, 60)
          #      self.drawable.add(explosion)
          #      self.updatable.add(explosion)
          #      self.create_drop(contact_point.x, contact_point.y, self.space, self.updatable, self.drawable)
          #      normal = arbiter.normal
          #      impulse = arbiter.total_impulse.length
          #      ast_obj.split(self.updatable, self.drawable, self.asteroids, self.space, normal, impulse, contact_point)
            #self.space.remove(r_shot.body, r_shot.shape)
        #return True
    def impact_damage_check(self, impact_force):
        if impact_force >= IMPACT_THRESHOLD:
            damage = max(min(impact_force * IMPACT_NORMALIZER * self.scaling_factor, MAX_IMPACT_DAMAGE),MIN_IMPACT_DAMAGE)
            return damage   
        else:
            damage = 0
            return damage

    def enemy_damage_check(self, enemy, damage, contact_pos, space):
        enemy.damage_accumulated += damage
        if enemy.damage_accumulated >= enemy.split_threshold:
            self.score += 1 
            if hasattr(enemy, "joints") and hasattr(enemy, "rotation_limit_list"):
                for joint in enemy.joints:
                    if joint in space.constraints:
                        self.space.remove(joint)
                for rotation in enemy.rotation_limit_list:
                    if rotation in space.constraints:
                        space.remove(rotation)
            self.commonenemyspawns.current_alien_count -= 1
            enemy.kill()
            self.create_drop(contact_pos, space, self.updatable, self.drawable)
            space.remove(enemy.body, enemy.shape)

    def asteroid_damage_check(self, asteroid, damage, impact_force, contact_pos, normal, space):
        asteroid.damage_accumulated += damage
        if asteroid.damage_accumulated >= asteroid.split_threshold:
                self.score += 1 
                explosion = Explosion(contact_pos.x, contact_pos.y, 60)
                self.drawable.add(explosion)
                self.updatable.add(explosion)
                self.create_drop(contact_pos, space, self.updatable, self.drawable)
                asteroid.split(self.updatable, self.drawable, self.asteroids, space, normal, impact_force, contact_pos)

    def player_damage_check(self, player, damage):
        if player.sheilds <= 0:
            if player.sheilds_health <= 0:
                player.health -= damage
            else:
                player.sheilds_health -= damage
                hit = SheildHit(player.body.position.x, player.body.position.y)
                self.updatable.add(hit)
                self.drawable.add(hit)


    def post_solve_r_e(self, rocket, enemy, contact_pos, impact_force, normal, arbiter, space, data):
        damage = self.impact_damage_check(impact_force)
        if arbiter.is_first_contact:
            self.enemy_damage_check(enemy, damage, contact_pos, space)
            impact = RocketImpact(contact_pos, normal, enemy)
            blood_splat = BloodSplat(contact_pos, normal)
        self.updatable.add(impact, blood_splat)
        self.drawable.add(impact, blood_splat)
        rocket.kill()
        space.remove(rocket.body, rocket.shape)
        return True 

    # def post_solve_r_e(self, arbiter, space, data):
    #     impact_force = arbiter.total_impulse.length 
    #     if impact_force >= IMPACT_THRESHOLD:
    #         damage = min(max(impact_force * IMPACT_NORMALIZER * self.scaling_factor, MAX_IMPACT_DAMAGE), MIN_IMPACT_DAMAGE)
    #     else:
    #         damage = MIN_IMPACT_DAMAGE
    #     objA, objB = arbiter.shapes
    #     if objA.game_object.shape.collision_type == 7:
    #         r_shot = objA.game_object
    #         enemy = objB.game_object
    #     elif objB.game_object.shape.collision_type == 7:
    #         enemy = objA.game_object
    #         r_shot = objB.game_object
    #     if arbiter.is_first_contact == True:
    #         enemy.damage_accumulated += damage
    #         print(enemy.damage_accumulated)
    #         contact = arbiter.contact_point_set.points[0]
    #         contact_point = contact.point_a
    #         #r_shot.kill()
    #         if arbiter.shapes[0].collision_type != 7:
    #             impact = RocketImpact(contact_point, -arbiter.normal, enemy)
    #             blood_splat = BloodSplat(contact_point, -arbiter.normal)
    #         else:
    #             impact = RocketImpact(contact_point, arbiter.normal, enemy)
    #             blood_splat = BloodSplat(contact_point,arbiter.normal)
    #         self.updatable.add(impact, blood_splat)
    #         self.drawable.add(impact, blood_splat)
    #         r_shot.kill()
    #         self.space.remove(r_shot.body, r_shot.shape)
    #         if enemy.damage_accumulated >= enemy.split_threshold:
    #             self.score += 1
    #             if hasattr(enemy, "joints") and hasattr(enemy, "rotation_limit_list"):
    #                 for joint in enemy.joints:
    #                     if joint in self.space.constraints:
    #                         self.space.remove(joint)
    #                 for rotation in enemy.rotation_limit_list:
    #                     if rotation in self.space.constraints:
    #                         self.space.remove(rotation)
    #             self.commonenemyspawns.current_alien_count -= 1
    #             #contact = arbiter.contact_point_set.points[0]
    #             #con                self.create_drop(contact_pos, space, self.updatable, self.drawable)
    #            asteroid.split(self.updatable, self.drawable, self.asteroids, space, normal, impact_force, contact_pos)
    #        space.remove(rocket.body, rocket.shape)
    #    return True

    #def post_solve_r_a(self, arbiter, space, data):
    #    impact_force = arbiter.total_impulse.length
        #if impact_force >= IMPACT_THRESHOLD:
        #sort out shot impact
    #    if impact_force >= 50:
     #       damage = max(min(impact_force * IMPACT_NORMALIZER * self.scaling_factor, MAX_IMPACT_DAMAGE),MIN_IMPACT_DAMAGE)
      #  else:
      #      damage = MAX_IMPACT_DAMAGE 
      #  objA, objB = arbiter.shapes
      #  if objB.game_object.shape.collision_type == 7:
      #      r_shot = objB.game_object
      #      ast_obj = objA.game_object
       # elif objA.game_object.shape.collision_type == 7:
       #     ast_obj = objB.game_object
        #    r_shot = objA.game_object
        #if arbiter.is_first_contact == True:
         #   ast_obj.damage_accumulated += damage
         #   contact = arbiter.contact_point_set.points[0]
         #   contact_point = contact.point_a
         #   if arbiter.shapes[0].collision_type != 7:
         #       impact = RocketImpact(contact_point, -arbiter.normal, ast_obj)
         #   else:
         #       impact = RocketImpact(contact_point, arbiter.normal, ast_obj)
         #   self.updatable.add(impact)
         #   self.drawable.add(impact)
         #   r_shot.kill()
            #self.hudd["score"] += 1
            #make this a standalone funciton
       #     if ast_obj.damage_accumulated >= ast_obj.split_threshold:
        #        self.score += 1
        #        contact = arbiter.contact_point_set.points[0]
         #       contact_point = contact.point_a
         #       explosion = Explosion(contact_point.x, contact_point.y, 60)
          #      self.drawable.add(explosion)
          #      self.updatable.add(explosion)
          #      self.create_drop(contact_point.x, contact_point.y, self.space, self.updatable, self.drawable)
          #      normal = arbiter.normal
          #      impulse = arbiter.total_impulse.length
          #      ast_obj.split(self.updatable, self.drawable, self.asteroids, self.space, normal, impulse, contact_point)
            #self.space.remove(r_shot.body, r_shot.shape)
        #return True

    def post_solve_r_a(self, rocket, asteroid, contact_pos, impact_force, normal, arbiter, space, data):
        print(impact_force)
        damage = self.impact_damage_check(impact_force)
        if arbiter.is_first_contact:
            self.asteroid_damage_check(asteroid, damage, impact_force, contact_pos, normal, space)
            impact = RocketImpact(contact_pos, normal, asteroid)
            self.updatable.add(impact)
            self.drawable.add(impact)
            rocket.kill()
            space.remove(rocket.body, rocket.shape)
        return True

    #def post_solve_r_a(self, arbiter, space, data):
    #    impact_force = arbiter.total_impulse.length
        #if impact_force >= IMPACT_THRESHOLD:
        #sort out shot impact
    #    if impact_force >= 50:
     #       damage = max(min(impact_force * IMPACT_NORMALIZER * self.scaling_factor, MAX_IMPACT_DAMAGE),MIN_IMPACT_DAMAGE)
      #  else:
      #      damage = MAX_IMPACT_DAMAGE 
      #  objA, objB = arbiter.shapes
      #  if objB.game_object.shape.collision_type == 7:
      #      r_shot = objB.game_object
      #      ast_obj = objA.game_object
       # elif objA.game_object.shape.collision_type == 7:
       #     ast_obj = objB.game_object
        #    r_shot = objA.game_object
        #if arbiter.is_first_contact == True:
         #   ast_obj.damage_accumulated += damage
         #   contact = arbiter.contact_point_set.points[0]
         #   contact_point = contact.point_a
         #   if arbiter.shapes[0].collision_type != 7:
         #       impact = RocketImpact(contact_point, -arbiter.normal, ast_obj)
         #   else:
         #       impact = RocketImpact(contact_point, arbiter.normal, ast_obj)
         #   self.updatable.add(impact)
         #   self.drawable.add(impact)
         #   r_shot.kill()
            #self.hudd["score"] += 1
            #make this a standalone funciton
       #     if ast_obj.damage_accumulated >= ast_obj.split_threshold:
        #        self.score += 1
        #        contact = arbiter.contact_point_set.points[0]
         #       contact_point = contact.point_a
         #       explosion = Explosion(contact_point.x, contact_point.y, 60)
          #      self.drawable.add(explosion)
          #      self.updatable.add(explosion)
          #      self.create_drop(contact_point.x, contact_point.y, self.space, self.updatable, self.drawable)
          #      normal = arbiter.normal
          #      impulse = arbiter.total_impulse.length
          #      ast_obj.split(self.updatable, self.drawable, self.asteroids, self.space, normal, impulse, contact_point)
            #self.space.remove(r_shot.body, r_shot.shape)
        #return True



    def post_solve_p_e_s(self, player, enemy_shot,contact_pos, impact_force, normal, arbiter, space, data):
        damage = self.impact_damage_check(impact_force)
        if arbiter.is_first_contact:
            self.player_damage_check(player, damage)
        return True 
    # def post_solve_p_e_s(self, arbiter, space, data):
    #     impact_force = arbiter.total_impulse.length
    #     if impact_force >= IMPACT_THRESHOLD:
    #         damage = max(min(impact_force * IMPACT_NORMALIZER * self.scaling_factor, MAX_IMPACT_DAMAGE),MIN_IMPACT_DAMAGE)
    #     else:
    #         damage = 0
    #     objA, objB = arbiter.shapes
    #     if objB.game_object.shape.collision_type == 1:
    #
    #         e_shot = objB.game_object
    #         player = objA.game_object
    #     elif objA.game_object.shape.collision_type == 1:
    #         e_shot = objA.game_object
    #         player = objA.game_object
    #     if arbiter.is_first_contact == True:
    #         print(damage)
    #         if player.sheilds <= 0:
    #             player.health -= damage
    #         else:
    #             player.sheilds_health -= damage
    #             hit = SheildHit(player.body.position.x, player.body.position.y)
    #             self.updatable.add(hit)
    #             self.drawable.add(hit)
    #     return True
    def post_solve_s_e(self, shot, enemy, contact_pos, impact_force, normal, arbiter, space, data):
        damage = self.impact_damage_check(impact_force)
        self.enemy_damage_check(enemy, damage, contact_pos, space)
        impact = ShotImpact(contact_pos, normal)
        blood_splat = BloodSplat(contact_pos, normal)
        self.updatable.add(impact, blood_splat)
        self.drawable.add(impact, blood_splat)
        shot.kill()
        space.remove(shot.body, shot.shape)
        return True


    # def post_solve_s_e(self, arbiter, space, data):
    #     impact_force = arbiter.total_impulse.length
    #     if impact_force >= IMPACT_THRESHOLD:
    #         damage = max(min(impact_force * IMPACT_NORMALIZER * self.scaling_factor, MAX_IMPACT_DAMAGE),MIN_IMPACT_DAMAGE)
    #     else:
    #         damage = 0
    #     objA, objB = arbiter.shapes
    #     if objA.game_object.shape.collision_type == 3:
    #         enemy = objB.game_object
    #         shot = objA.game_object
    #     elif objB.game_object.shape.collision_type == 3:
    #         enemy = objA.game_object
    #         shot = objB.game_object
    #     enemy.damage_accumulated += damage
    #     contact = arbiter.contact_point_set.points[0]
    #     contact_point = contact.point_a
    #     if arbiter.shapes[0].collision_type != 3:
    #         impact = ShotImpact(contact_point, -arbiter.normal)
    #         blood_splat = BloodSplat(contact_point, -arbiter.normal)
    #     else:
    #         impact = ShotImpact(contact_point, arbiter.normal)
    #         blood_splat = BloodSplat(contact_point, arbiter.normal)
    #     self.updatable.add(impact, blood_splat)
    #     self.drawable.add(impact, blood_splat)
    #     if enemy.damage_accumulated >= enemy.split_threshold:
    #         self.score += 1 
    #         if hasattr(enemy, "joints") and hasattr(enemy, "rotation_limit_list"):
    #             for joint in enemy.joints:
    #                 if joint in self.space.constraints:
    #                     self.space.remove(joint)
    #             for rotation in enemy.rotation_limit_list:
    #                 if rotation in self.space.constraints:
    #                     self.space.remove(rotation)
    #         self.commonenemyspawns.current_alien_count -= 1
    #         enemy.kill()
    #         self.create_drop(contact_point.x, contact_point.y, self.space, self.updatable, self.drawable)
    #         self.space.remove(enemy.body, enemy.shape)
    #     return True
    def post_solve_e_s_a(self, enemy_shot, asteroid, contact_pos, impact_force, normal, arbiter, space, data):
        damage = self.impact_damage_check(impact_force)
        if arbiter.is_first_contact:
            self.asteroid_damage_check(asteroid, damage, impact_force, contact_pos, normal, space)
            enemy_shot.kill()
            space.remove(enemy_shot.body, enemy_shot.shape)
        return True 

    # def post_solve_e_s_a(self, arbiter, space, data):
    #     impact_force = arbiter.total_impulse.length
    #     if impact_force >= IMPACT_THRESHOLD:
    #         damage = max(min(impact_force * IMPACT_NORMALIZER * self.scaling_factor, MAX_IMPACT_DAMAGE),MIN_IMPACT_DAMAGE)
    #     else:
    #         damage = 0
    #     objA, objB = arbiter.shapes
    #     if objA.game_object.shape.collision_type == 6:
    #         shot_obj = objA.game_object
    #         ast_obj = objB.game_object
    #     elif objB.game_object.shape.collision_type == 6:
    #         ast_obj = objA.game_object
    #         shot_obj = objB.game_object
    #     if arbiter.is_first_contact == True:
    #         ast_obj.damage_accumulated += damage
    #         if ast_obj.damage_accumulated >= ast_obj.split_threshold:
    #             shot_obj.kill()
    #             contact = arbiter.contact_point_set.points[0]
    #             contact_point = contact.point_a
    #             self.create_drop(contact_point.x, contact_point.y, self.space, self.updatable, self.drawable)
    #             normal = arbiter.normal
    #             impulse = arbiter.total_impulse.length
    #             ast_obj.split(self.updatable, self.drawable, self.asteroids, self.space, normal, impulse, contact_point)
    #             self.space.remove(shot_obj.body, shot_obj.shape)
    #     return True
    def post_solve_e_a(self, enemy, asteroid, contact_pos, impact_force, normal, arbiter, space, data):
        damage = self.impact_damage_check(impact_force)
        self.enemy_damage_check(enemy, damage, contact_pos, space)
        self.asteroid_damage_check(asteroid, damage, impact_force, contact_pos, normal, space)
        return True 

    # def post_solve_e_a(self, arbiter, space, data):
    #     impact_force = arbiter.total_impulse.length 
    #     impact_damage_threshold = 80.0
    #     if impact_force >= IMPACT_THRESHOLD:
    #         damage = max(min(impact_force * IMPACT_NORMALIZER * self.scaling_factor, MAX_IMPACT_DAMAGE),MIN_IMPACT_DAMAGE)
    #     else:
    #         damage = 0
    #
    #     objA, objB = arbiter.shapes
    #     if objA.game_object.shape.collision_type == 5:
    #         enemy = objA.game_object
    #         asteroid = objB.game_object
    #     elif objB.collision_type == 5:
    #         enemy = objB.game_object
    #         asteroid = objA.game_object
    #     enemy.damage_accumulated += damage
    #     asteroid.damage_accumulated += damage
    #     if asteroid.damage_accumulated >= asteroid.split_threshold:
    #         contact = arbiter.contact_point_set.points[0]
    #         contact_point = contact.point_a
    #         self.create_drop(contact_point.x, contact_point.y, self.space, self.updatable, self.drawable)
    #         normal = arbiter.normal
    #         asteroid.split(self.updatable, self.drawable, self.asteroids, self.space, normal, impact_force, contact_point)
    #     if enemy.damage_accumulated >= enemy.split_threshold:
    #         if hasattr(enemy, "joints") and hasattr(enemy, "rotation_limit_list"):
    #             for joint in enemy.joints:
    #                 if joint in self.space.constraints:
    #                     self.space.remove(joint)
    #             for rotation in enemy.rotation_limit_list:
    #                 if rotation in self.space.constraints:
    #                     self.space.remove(rotation)
    #         self.commonenemyspawns.current_alien_count -= 1
    #         contact = arbiter.contact_point_set.points[0]
    #         contact_point = contact.point_a
    #         enemy.kill()
    #         self.space.remove(enemy.body, enemy.shape)
    #         self.create_drop(contact_point.x, contact_point.y, self.space, self.updatable, self.drawable)
    #     return True

    def post_solve_p_e(self, player, enemy, contact_pos, impact_force, normal, arbiter, space, data):
        damage = self.impact_damage_check(impact_force)
        if arbiter.is_first_contact:
            self.player_damage_check(player, damage)
        return True

    # def post_solve_p_e(self, arbiter, space, data):
    #     impact_force = arbiter.total_impulse.length
    #     if impact_force >= IMPACT_THRESHOLD:
    #         damage = max(min(impact_force * IMPACT_NORMALIZER * self.scaling_factor, MAX_IMPACT_DAMAGE),MIN_IMPACT_DAMAGE)
    #     else:
    #         damage = 0
    #     objA, objB = arbiter.shapes
    #     if objA.game_object.shape.collision_type == 1:
    #         player = objA.game_object
    #     elif objB.game_object.shape.collision_type == 1:
    #         player = objB.game_object
    #     if arbiter.is_first_contact == True:
    #         if player.sheilds <= 0:
    #             player.health -= damage
    #             print(player.health)
    #         else:
    #             player.sheilds_health -= damage
    #     return True

    #pymunk collision handling functions
    
    ###
    def post_solve_s_a(self, asteroid, shot, contact_pos, impact_force, normal, arbiter, space, data):
        damage = self.impact_damage_check(impact_force)
        if arbiter.is_first_contact:
            impact = ShotSplat(contact_pos, normal)
            shot.kill()
            self.asteroid_damage_check(asteroid, damage, impact_force, contact_pos, normal, space)
            self.updatable.add(impact)
            self.drawable.add(impact)
            space.remove(shot.body, shot.shape)
        return True
    # def post_solve_s_a(self, arbiter, space, data):
    #     impact_force = arbiter.total_impulse.length
    #     #if impact_force >= IMPACT_THRESHOLD:
    #     #sort out shot impact   
    #     if impact_force >= 50:
    #         damage = max(min(impact_force * IMPACT_NORMALIZER * self.scaling_factor, MAX_IMPACT_DAMAGE),MIN_IMPACT_DAMAGE)
    #     else:
    #         damage = 0
    #     objA, objB = arbiter.shapes
    #     if objA.game_object.shape.collision_type == 2:           
    #         shot_obj = objB.game_object
    #         ast_obj = objA.game_object
    #     elif objB.game_object.shape.collision_type == 2:
    #         shot_obj = objA.game_object
    #         ast_obj = objB.game_object
    #     if arbiter.is_first_contact == True:            
    #         ast_obj.damage_accumulated += damage
    #         #self.hudd["score"] += 1
    #         #make this a standalone funciton
    #         contact = arbiter.contact_point_set.points[0]
    #         contact_point = contact.point_a
    #         if arbiter.shapes[0].collision_type != 2:
    #             impact = ShotSplat(contact_point, -arbiter.normal)
    #         else:
    #             impact = ShotSplat(contact_point, arbiter.normal)
    #         self.updatable.add(impact)
    #         self.drawable.add(impact)
    #         if ast_obj.damage_accumulated >= ast_obj.split_threshold:
    #             shot_obj.kill()
    #             self.score += 1
    #             explosion = Explosion(contact_point.x, contact_point.y, 60)
    #             self.drawable.add(explosion)
    #             self.updatable.add(explosion)
    #             self.create_drop(contact_point.x, contact_point.y, self.space, self.updatable, self.drawable)
    #             normal = arbiter.normal
    #             impulse = arbiter.total_impulse.length
    #             ast_obj.split(self.updatable, self.drawable, self.asteroids, self.space, normal, impulse, contact_point)
    #             self.space.remove(shot_obj.body, shot_obj.shape)
    #     return True

    def begin_p_p(self, player, pickup, contact_pos=None, impact_force=None, normal=None, arbiter=None, space=None, data=None):
        pickup_list = ["fuel", "bomb", "sheilds", "yamato", "rockets", "multishot"]
        for attr in pickup_list:
            if hasattr(pickup, attr):
                pickup_value = getattr(pickup, attr, 0)
                current = getattr(player, attr, 0)
                setattr(player, attr, current + pickup_value)
                #pickup.game_object.kill()
                space.remove(pickup.body, pickup.shape)
        return False

    # def begin_p_p(self, arbiter, space, data):
    #     objA, objB = arbiter.shapes
    #     if hasattr(objB.game_object, "fuel"):
    #         self.player.fuel += objB.game_object.fuel
    #         objB.game_object.kill()
    #         self.space.remove(objB.game_object.body, objB.game_object.shape)
    #     elif hasattr(objB.game_object, "bomb"):
    #         self.player.bombs += objB.game_object.bomb
    #         objB.game_object.kill()
    #         self.space.remove(objB.game_object.body, objB.game_object.shape)
    #     elif hasattr(objB.game_object, "sheilds"):
    #         self.player.sheilds += objB.game_object.sheilds
    #         objB.game_object.kill()  
    #         self.space.remove(objB.game_object.body, objB.game_object.shape)
    #     elif hasattr(objB.game_object, "yamato"):
    #         self.player.yamato += objB.game_object.yamato    
    #         objB.game_object.kill()
    #         self.space.remove(objB.game_object.body, objB.game_object.shape)
    #     elif hasattr(objB.game_object, "rockets"):
    #         self.player.rockets += objB.game_object.rockets   
    #         objB.game_object.kill()
    #         self.space.remove(objB.game_object.body, objB.game_object.shape)
    #     elif hasattr(objB.game_object, "multishot"):
    #         self.player.multishot += objB.game_object.multishot 
    #         objB.game_object.kill()
    #         self.space.remove(objB.game_object.body, objB.game_object.shape)
    #     return False
    #player - asteroid handler  
    def post_solve_p_a(self, player, asteroid, contact_pos, impact_force, normal, arbiter, space, data):
        damage = self.impact_damage_check(impact_force)
        if arbiter.is_first_contact:
            self.player_damage_check(player, damage)
        return True
    # def post_solve_p_a(self, arbiter, space, data):
    #     objA, objB = arbiter.shapes
    #     impact_force = arbiter.total_impulse.length
    #     if impact_force >= IMPACT_THRESHOLD:
    #         damage = max(min(impact_force * IMPACT_NORMALIZER * self.scaling_factor, MAX_IMPACT_DAMAGE),MIN_IMPACT_DAMAGE)
    #     else:
    #         damage = 0
    #     if objA.game_object.shape.collision_type == 1:
    #         player = objA.game_object
    #         asteroid = objB.game_object
    #     elif objB.game_object.shape.collision_type == 1:
    #         player = objB.game_object
    #         asteroid = objA.game_object
    #     if arbiter.is_first_contact == True:
    #         print(player.health)
    #         if player.sheilds <= 0:
    #         #if player.lives > 0:
    #             #if player.respawn_timer <= 0:
    #             player.health -= damage  
    #                 #player.respawn_timer = PLAYER_RESPAWN_TIMER
    #                 #self.hudd["lives"] = player.lives
    #         else:
    #             player.sheilds_health -= damage
    #             #player.animate_sheild()
    #             hit = SheildHit(player.body.position.x, player.body.position.y)
    #             #player.animate_sheild(hit)
    #             self.updatable.add(hit)
    #             self.drawable.add(hit)
    #     return True 
    # def pre_solve_p_a(self, arbiter, space, data):
        #dampen or conditionally ignore collision if sheilds or something
        #if self.player.respawn_timer > 0 and arbiter.is_first_contact == False:
        #    return False
        # return True
        #pass
    #def post_solve_p_a(self, arbiter, space, data):
        #retreive collision impulse or kenetic energy to calculate sound volume and damage amount   
        #impulse = arbiter.total_impulse
        #kenetic_loss = arbiter.total_ke
        #print(impulse)
        #pass
    # def separate(arbiter, space, data):
    #     pass
    ###
    def create_drop(self, contact_pos, space, updatable, drawable):
        drops = [FuelDrop(contact_pos.x,contact_pos.y, space), BombDrop(contact_pos.x,contact_pos.y, space), RocketDrop(contact_pos.x,contact_pos.y, space), YamatoCannon(contact_pos.x,contact_pos.y, space), SheildDrop(contact_pos.x,contact_pos.y, space), MultiShot(contact_pos.x,contact_pos.y, space)]
        new_drop = random.choice(drops)
        updatable.add(new_drop)
        drawable.add(new_drop)
        space.add(new_drop.body, new_drop.shape)
    ###
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
    ###
    def end_game(self):
        if self.player.lives <= 0:
            new_state = GameOver(self.game, self.score)
            new_state.enter_state()
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    new_state = Pause(self.game)
                    new_state.enter_state()
    
    def update(self, dt):
        super().update(dt)
        self.space.step(dt)
        self.collision_check()
        self.end_game()
        self.hudd["score"] = self.score
        self.hudd["fuel"] = int(self.player.fuel)
        self.hudd["health"] = int(self.player.health)
        self.hudd["lives"] = self.player.lives
        self.hudd["sheilds_health"] = self.player.sheilds_health
        #self.lives_ui.get_hudd(self.hudd)
        #self.score_ui.get_hudd(self.hudd)
        #self.health_ui.get_hudd(self.hudd)
        #self.fuel_ui.get_hudd(self.hudd)
        self.hud_display.get_hudd(self.hudd)
        self.updatable.update(dt)
        ###
        self.camera.update_camera(self.player)
        ###
        #gravity application might need work
        circle_shapes = [obj for obj in self.drawable if isinstance(obj, CircleShape)]
        for obj in circle_shapes:
            for obj2 in circle_shapes:
                if obj is not obj2:
                    obj.apply_gravity(obj2, dt)

        ###

    def draw(self):
        super().draw()
        self.screen.blit(self.background_layer, (-self.camera.camera_box.x * 0.4,-self.camera.camera_box.y * 0.4))
        self.screen.blit(self.background_layer_stars1, (-self.camera.camera_box.x * 0.5, -self.camera.camera_box.y * 0.5))
        self.screen.blit(self.background_layer_stars2, (-self.camera.camera_box.x * 0.6, -self.camera.camera_box.y * 0.6))
        #self.canvas.blit(self.canvas_background, (0,0))
        for obj in self.drawable:
            obj.draw()
            self.canvas.blit(obj.image, obj.rect)

        self.screen.blit(self.canvas,(0,0), self.camera.camera_box)
        #self.lives_ui.draw(self.screen)
        #self.score_ui.draw(self.screen)
        #self.fuel_ui.draw(self.screen)
        #self.health_ui.draw(self.screen)
        self.hud_display.draw(self.screen)
        
