import copy

class Space:

    def __init__(self, schema = {}, name = "myspace"):
        """
        schema must contain the names of the dimensions in the space as keys
        furthermore, we need type_checkers, and class instantiators for each dimension
        it should suffice form the values to be dtype objects
        """
        self.name = name
        self.dimensions = []
        self.metrics = []
        # self.dimensions = list(schema.keys())
        for key in schema.keys():
            try:
                dtype = schema[key]
                dim = Dimension(key, dtype, lambda arg: dtype(arg) )
                setattr(self, key, dim)
                self.append_dimensions.append(key)
            except:
                Warning("One or more dimensions in schema underspecified")

        # self.metrics = list(metrics.keys())
        # for key in self.metrics:
        #     setattr(self, key, metrics[key])

    def point(self, args):
            return Point(self,args)

    def set_name(self, name):
        self.name = name

    def append_dimension(self, key, dtype, init=None):
        if init==None:
            init=dtype

        if key in self.dimensions:
            Warning(key+" dimension already in this space")
        else:
            self.dimensions.append(key)
            dim = Dimension(key,dtype,init)
            setattr(self, key, dim)

    def append_metric(self, key, metric):

        if key in self.metrics:
            Warning(key+" metric already in this space")
        else:
            self.metrics.append(key)
            setattr(self, key, metric)


def space_from_point(point):

    return copy.deepcopy(point.space)

class Dimension:

    def __init__(self, name, dtype, init):
        self.name = name
        self.dtype = dtype
        self.init = init

class Point:

    def __init__(self, space, args_dict):
        self.space = space

        for key in space.dimensions:
            dim = getattr(space,key)
            init = dim.init
            args = args_dict[key]

            if type(args)==dict:
                value = init(**args)
            elif type(args)==tuple:
                #print(*args)
                value = init(*args)
            else:
                value = init(args)

            setattr(self, key, value)
    
    def set_space(self, space):
        self.space= space

    def copy(self):

        #first make a clean deep copy
        point = copy.deepcopy(self)
        #then make sure to set the space back to same parent space
        point.set_space(self.space)

        return point
        

class Trajectory:

    def __init__(self, point):
        """
        A Trajectory is an ordered sequence of points in a space
        input point must be of class Point
        """
        self.space = point.space
        self.points= [point]
        self.dynamics = Dynamics(self.space)
        self.length = 1

    def append_point(self,point):
        if point.space == self.space:
            self.points.append(point)
            self.length +=1
        else:
            Warning("input point not in the right space")

    def append_points(self,points):
        
        for point in points:
            self.append_point(point)
    
    def set_dynamics(self, dynamics):
        self.dynamics = dynamics
    
    def apply_dynamics(self, iterations=1):
        step = self.dynamics.step
        for _ in range(iterations):
            p = self.points[-1].copy()
            point = step(p)
            self.append_point(point)

class Dynamics:
    """
    Dynamics is a map from a space to itself
    initized as an identity map
    """
    def __init__(self, space, step = lambda p: p ):
        self.space = space
        self.step = step
    
    def set_step(self, func):
        self.step = func


class Metric:

    def __init__(self, space, func, name = "mymetric"):
        self.name = name
        self.func = func
        self.space = space

