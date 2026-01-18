import random 
import pymunk
import pygame
import weakref  
class Spawner(pygame.sprite.Sprite):
    def __init__(self, level, entity_cls, group_type, scaling_factor, spawn_rate, current_count, max_count, max_radius, min_radius, height, width, kind, assets, vectors=[(1,0),(-1,0),(0,1),(0,-1)]):
        super().__init__()
        self.level = weakref.proxy(level)
        #self.level = level 
        self.assets = assets    
        self.entity_cls = entity_cls
        self.group_type = group_type
        self.updatable = level.updatable
        self.drawable = level.drawable
        self.space = level.space
        self.spawn_rate = spawn_rate
        self.max_count = max_count
        self.min_radius = min_radius
        self.max_radius = max_radius
        self.scaling_factor = scaling_factor
        self.height = height    
        self.width = width
        self.vectors = vectors
        self.kind = kind    
        self.spawn_timer = 0
        self.current_count = current_count


        self.edges = [
            [pymunk.Vec2d(*self.vectors[0]), lambda y: pymunk.Vec2d(-self.max_radius, y * self.height)],
            [pymunk.Vec2d(*self.vectors[1]), lambda y: pymunk.Vec2d(self.width + self.max_radius, y * self.height)],
            [pymunk.Vec2d(*self.vectors[2]), lambda x: pymunk.Vec2d(x * self.width, -self.max_radius)],
            [pymunk.Vec2d(*self.vectors[3]), lambda x: pymunk.Vec2d(x * self.width, self.height + self.max_radius)],
        ]
    def __spawn_wrapper(self, spawn_fn, entity_cls, *args):
        #help(entity_cls)
        #print(getattr(self, entity_cls))
        if isinstance(entity_cls, list):
            choice = random.choice(entity_cls)
            #find another way
            self.edges = [
                [pymunk.Vec2d(*self.vectors[0]), lambda y: pymunk.Vec2d(self.max_radius, y * self.height)],
                [pymunk.Vec2d(*self.vectors[1]), lambda y: pymunk.Vec2d(self.width - self.max_radius, y * self.height)],
                [pymunk.Vec2d(*self.vectors[2]), lambda x: pymunk.Vec2d(x * self.width, self.max_radius)],
                [pymunk.Vec2d(*self.vectors[3]), lambda x: pymunk.Vec2d(x * self.width, self.height - self.max_radius)],
        ]
            #print(choice)
        else:
            choice = entity_cls
            #centralize the counts to a dict or something
            self.current_count = self.level.current_alien_count
        override = getattr(entity_cls, "spawn", None)
        if callable(override):
            return override(*args)
        return spawn_fn(choice, *args )
        
    
    def setup_spawn(self, entity_cls, radius, position, velocity, kind, assets):
        
        entity = entity_cls(position.x, position.y, radius, self.space, self.level, kind, assets)
        entity.body.velocity = velocity 
        self.group_type.add(entity)
        self.updatable.add(entity)
        self.drawable.add(entity)
        self.space.add(entity.body, entity.shape)

    def spawn(self, *args):
        return self.__spawn_wrapper(self.setup_spawn, self.entity_cls, *args)

    def update(self, dt):

        self.spawn_timer += dt 
        if self.spawn_timer > self.spawn_rate and self.current_count <= self.max_count:
            self.spawn_timer = 0
            self.current_count += 1
            edge = random.choice(self.edges)
            #TODO set in constants
            speed = random.randint(40, 100) * self.scaling_factor
            velocity = edge[0] * speed  
            velocity = velocity.rotated(random.randint(-30, 30))
            position = edge[1](random.uniform(0,1))
            kind = random.randint(1, self.kind)
            #TODO cant move forward till we figure out how to wrap in the centipede thingy 
            self.spawn(self.min_radius * kind, position, velocity, kind, self.assets)




    
 

