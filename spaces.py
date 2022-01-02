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
            else:
                value = init(args)

            setattr(self, key, value)
            
            # if not(arg_dict==None):
            #     if not(arg_dict[key]==None):
            #         dim_arg_dict = arg_dict[key]

            # value = dim_init(**dim_arg_dict)
            # setattr(self, key, value)

            # if type(dim_arg_dict) == dict:
            #     value = initiator(**dim_arg_dict)
            #     setattr(self, key, value)
            # else:
            #     value = initiator(init_dict[key])
            #     setattr(self, key, value)

# class Trajectory:

class Metric:

    def __init__(self, space, func, name = "mymetric"):
        self.name = name
        self.func = func
        self.space = space

