import copy

class Space:

    def __init__(self, schema = {}, metrics = {}, name = "myspace"):
        """
        schema must contain the names of the dimensions in the space as keys
        furthermore, we need type_checkers, and class instantiators for each dimension
        it should suffice form the values to be dtype objects
        """
        self.name = name
        self.dimensions = list(schema.keys())
        for key in self.dimensions:
            setattr(self, key, schema[key])

        self.metrics = list(metrics.keys())
        for key in self.metrics:
            setattr(self, key, metrics[key])

    def point(self, arg_dict):
            return Point(self,arg_dict)

    def set_name(self, name):
        self.name = name

    def append_dimension(self, key, dtype):

        if key in self.dimensions:
            Warning(key+" dimension already in this space")
        else:
            self.dimensions.append(key)
            setattr(self, key, dtype)

    def append_metric(self, key, metric):

        if key in self.metrics:
            Warning(key+" metric already in this space")
        else:
            self.metrics.append(key)
            setattr(self, key, metric)


def space_from_point(point):

    return copy.deepcopy(point.space)



class Point:

    def __init__(self, space, arg_dict):
        self.space = space

        for key in space.dimensions:
            initiator = getattr(space,key)
            value = initiator(arg_dict[key])
            setattr(self, key, value)

# class Trajectory:

class Metric:

    def __init__(self, space, func, name = "mymetric"):
        self.name = name
        self.func = func
        self.space = space

