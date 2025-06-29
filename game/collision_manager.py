class CollisionManager:
    def __init__(self):
        self.__handlers: dict[tuple[int,int], callable] = {
            "begin": {},
            "pre_solve": {},
            "post_solve": {},
            "separate": {},
        }

    def register(self, type_a: int, type_b: int, fn: callable, phase: str ="post_solve"):
        def wrapped(arbiter, space, data):
            a_shape, b_shape = arbiter.shapes   

            if a_shape.game_object.shape.collision_type == type_a:
                obj_a, obj_b = a_shape.game_object, b_shape.game_object 
                pt_a, pt_b = arbiter.contact_point_set.points[0].point_a, arbiter.contact_point_set.points[0].point_b
                normal = arbiter.normal
            else:
                obj_a, obj_b = b_shape.game_object, a_shape.game_object
                pt_a, pt_b = arbiter.contact_point_set.points[0].point_b, arbiter.contact_point_set.points[0].point_a
                normal = -arbiter.normal    
                #getting the contact point by dividing the two instead of using the point on one object
            contact_pos = (pt_a + pt_b) * .5
            impact_force = arbiter.total_impulse.length
            return fn(obj_a, obj_b, contact_pos, impact_force, normal, arbiter, space, data)
        
        self.__handlers[phase][(type_a, type_b)] = wrapped
        self.__handlers[phase][(type_b, type_a)] = wrapped


    def install(self, space):
        handler = space.add_default_collision_handler()
        handler.begin = self.__dispatch("begin")
        handler.pre_solve = self.__dispatch("pre_solve")
        handler.post_solve = self.__dispatch("post_solve")
        handler.separate = self.__dispatch("separate")

    def __dispatch(self, phase):
        def dispatcher(arbiter, space, data):
            a_shape, b_shape = arbiter.shapes   
            pair = (a_shape.collision_type, b_shape.collision_type)
            fn = self.__handlers[phase].get(pair)
            if fn:
                return fn(arbiter, space, data)
            return True 
        return dispatcher


