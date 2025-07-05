from game.state import State 
from game.userinterface import UserInterface
from entities.player import Player
from entities.shot import Shot   
from entities.asteroid import Asteroid 
from effects.explosions.explosion_animate import Explosion 
#from .asteroidfield import AsteroidField
from entities.enemies.scourge import Scourge
from entities.enemies.flyingsaucer import FlyingSaucer
#from entities.enemies.centipedespawner import CentipedeSpawn
from .spawner import Spawner    
from menus.pause import Pause
from menus.game_over import GameOver  
from entities.circleshape import CircleShape
from effects.explosions.rocket_impact_explosion import RocketImpact
from effects.explosions.shot_impact import ShotImpact
from effects.explosions.shot_splat import ShotSplat
from effects.explosions.blood_splat import BloodSplat
from effects.explosions.sheild_hit import SheildHit
from entities.walls import Walls
#from .commonenemyspawns import * 
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
        #self.background_layer_stars1 = pygame.transform.scale(self.background_layer_stars1, (GAME_HEIGHT, GAME_WIDTH))
        #self.background_layer_stars2 = pygame.transform.scale(self.background_layer_stars2, (GAME_HEIGHT, GAME_WIDTH))
        #self.background_layer_stars2 = pygame.transform.rotate(self.background_layer_stars2, 180)
        #self.background_layer = pygame.transform.scale(self.background_layer, (GAME_HEIGHT, GAME_WIDTH))

        self.background_layer_stars1 = pygame.transform.scale(self.background_layer_stars1, (GAME_WIDTH, GAME_HEIGHT))
        self.background_layer_stars2 = pygame.transform.scale(self.background_layer_stars2, (GAME_WIDTH, GAME_HEIGHT))
        self.background_layer_stars2 = pygame.transform.rotate(self.background_layer_stars2, 90)
        self.background_layer = pygame.transform.scale(self.background_layer, (GAME_WIDTH, GAME_HEIGHT))
        #self.canvas_background = pygame.image.load('./assets/images/layer2.png').convert_alpha()$
        #self.canvas_background = pygame.transform.scale_by(self.canvas_background, 3)
       # self.hud_display = HeadsUp()
        ###
        self.hudd = {"score": 0, "lives": 99, "fuel": 100,"health": 100, "sheilds_health": 100}
        self.hud_display = HeadsUp(256 + 8, self.SCREEN_HEIGHT - 16, 512, 256, hudd=self.hudd)
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
        #self.asteroidfield = AsteroidField(self)
        self.alien_types = [Scourge, FlyingSaucer]
        self.commonenemyspawns = Spawner(self, self.alien_types, self.aliens, self.scaling_factor, self.asteroid_spawn_rate, self.current_alien_count, self.alien_max_count, ALIEN_MAX_RADIUS, ALIEN_MIN_RADIUS, GAME_HEIGHT, GAME_WIDTH, ALIEN_KINDS)
        self.asteroidfield = Spawner(self, Asteroid, self.asteroids, self.scaling_factor, self.asteroid_spawn_rate, self.current_asteroid_count, self.max_asteroids, ASTEROID_MAX_RADIUS, ASTEROID_MIN_RADIUS, GAME_HEIGHT, GAME_WIDTH, ASTEROID_KINDS )
        ###
        self.player = Player(self.player_sprite, self.x, self.y, self.shots, self.updatable, self.drawable, self.space, self.canvas)

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
        self.collision_manager.install(self.space)
        ###



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
        if player.sheilds > 0:
            if player.sheilds_health > 0:
                player.sheilds_health -= damage
                hit = SheildHit(player.body.position.x, player.body.position.y)
                self.updatable.add(hit)
                self.drawable.add(hit)
            else:
                player.health -= damage
        if player.sheilds <= 0:
            if player.sheilds_health > 0:
                player.sheilds_health -= damage
                hit = SheildHit(player.body.position.x, player.body.position.y)
                self.updatable.add(hit)
                self.drawable.add(hit)
            else:
                player.health -= damage


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


    def post_solve_p_e_s(self, player, enemy_shot,contact_pos, impact_force, normal, arbiter, space, data):
        damage = self.impact_damage_check(impact_force)
        if arbiter.is_first_contact:
            self.player_damage_check(player, damage)
        return True 

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

    def post_solve_e_s_a(self, enemy_shot, asteroid, contact_pos, impact_force, normal, arbiter, space, data):
        damage = self.impact_damage_check(impact_force)
        if arbiter.is_first_contact:
            self.asteroid_damage_check(asteroid, damage, impact_force, contact_pos, normal, space)
            enemy_shot.kill()
            space.remove(enemy_shot.body, enemy_shot.shape)
        return True 

    def post_solve_e_a(self, enemy, asteroid, contact_pos, impact_force, normal, arbiter, space, data):
        damage = self.impact_damage_check(impact_force)
        self.enemy_damage_check(enemy, damage, contact_pos, space)
        self.asteroid_damage_check(asteroid, damage, impact_force, contact_pos, normal, space)
        return True 


    def post_solve_p_e(self, player, enemy, contact_pos, impact_force, normal, arbiter, space, data):
        damage = self.impact_damage_check(impact_force)
        if arbiter.is_first_contact:
            self.player_damage_check(player, damage)
        return True


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
    ##TODO fix this wrapper not handling begin functions 
    def begin_p_p(self, player, pickup, contact_pos, impact_force, normal, arbiter, space, data):
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
        self.hud_display.get_hudd(self.hudd)
        self.updatable.update(dt)
        ###
        self.camera.update_camera(self.player)
        ###
        #gravity application need implmentation
        circle_shapes = [obj for obj in self.updatable if isinstance(obj, CircleShape)]
        for obj in circle_shapes:
            for obj2 in circle_shapes:
                if obj is not obj2:
                    obj.apply_gravity(obj2, dt)

        #

    def draw(self):
        super().draw()
        self.screen.blit(self.background_layer, (-self.camera.camera_box.x * 0.4,-self.camera.camera_box.y * 0.4))
        self.screen.blit(self.background_layer_stars1, (-self.camera.camera_box.x * 0.5, -self.camera.camera_box.y * 0.5))
        self.screen.blit(self.background_layer_stars2, (-self.camera.camera_box.x * 0.6, -self.camera.camera_box.y * 0.6))
        for obj in self.drawable:
            obj.draw()
            self.canvas.blit(obj.image, obj.rect)

        self.screen.blit(self.canvas,(0,0), self.camera.camera_box)
        self.hud_display.draw(self.screen)
        
