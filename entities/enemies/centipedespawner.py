
from .centipedehead import CentipedeHead    
from .centipedebody import CentipedeBody    
import math
import pymunk
class CentipedeSpawn(position_x, position_y, updatable, drawable, space, canvas):
    def __init__(self):
        #self.radius = radius 
        self.position_x = position_x
        self.position_y = position_y
        self.space = space
        self.canvas = canvas
        self.updatable = updatable
        self.drawable = drawable

        ##Hardcode to Constants later or use .random
        self.body_count = 6

    def spawn(self, radius, position, velocity):
        segments = []
        joints = []
        rotation_limit_list = []
        length = self.body_count
        for i in range(length):
            if i == 0:
                segment = CentipedeHead(position.x + (1 * 2 * radius), position.y, radius, self.space, self.canvas)
            else:
                segment = CentipedeBody(position.x + ((i + 1) * 2 * radius), position.y, radius, self.space)
            segments.append(segment)
            self.space.add(segment.body, segment.shape)
            self.updatable.add(segment)
            self.drawable.add(segment)
        for i in range(length - 1):
            body_a = segments[i].body   
            body_b = segments[i + 1].body   
            joint = pc.PinJoint(body_a, body_b, (0,0))
            joint.collide_bodies = False    
            joint.stiffness = 1000.0
            joints.append(joint)    
            self.space.add(joint)
            rotation_limit = pc.RotaryLimitJoint(body_a, body_b, math.pi / 6, -math.pi / 6)
            rotation_limit_list.append(rotation_limit)
            self.space.add(rotation_limit)
            segments[i].joints.append(joint)
            segments[i + 1].joints.append(joint)
            segments[i].rotation_limit_list.append(rotation_limit)
            segments[i + 1].rotation_limit_list.append(rotation_limit)
        segments[0].body.velocity = velocity
