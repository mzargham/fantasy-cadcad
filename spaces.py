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
                self.dimensions.append(key)
            except:
                print(Warning("One or more dimensions in schema underspecified"))

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

        if type(metric)==Metric:
            metric.set_space(self)
        else:
            metric = Metric(metric, self, description="autogenerated metric object")

        if key in self.metrics:
            Warning(key+" metric already in this space")
        else:
            self.metrics.append(key)
            setattr(self, key, metric)

def cartersian(space1,space2):
    dims1 = space1.dimensions
    dims2 = space2.dimensions
    #dims = dims1+dims2
    #print(dims)

    name1 = space1.name
    name2 = space2.name
    name = name1+str(" X ")+name2

    metrics1 = space1.metrics
    metrics2 = space2.metrics
    #metrics = metrics1 + metrics2
    #print(metrics)

    space = Space(name=name)

    for dim in dims1:
        d = getattr(space1,dim)
        space.append_dimension(dim,d.dtype,d.init)

    for met in metrics1:
        m = getattr(space1,met)
        space.append_metric(met,m)
    
    for dim in dims2:
        d = getattr(space2,dim)
        space.append_dimension(dim,d.dtype,d.init)

    for met in metrics2:
        m = getattr(space2,met)
        space.append_metric(met,m)

    return space

def spacewise_cartesian(spaces):
    
    base = Space(name="cartesian produce of spaces "+str(spaces))
    for space in spaces:
        base = cartersian(base, space)
    
    return base

def pointwise_cartesian(points):

    #combine spaces of points then make a new point in the new space
    spaces = [p.space for p in points]
    space = spacewise_cartesian(spaces)

    spaces = []
    args = {}
    for p in points:
        spaces.append(p.space)
        for d in p.state.dimensions:
            args[d] = getattr(p,d)

    space = spacewise_cartesian(spaces)
    point = Point(space,args)

    return point
    

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

    def __init__(self, point, dynamics = None, params = None):
        """
        A Trajectory is an ordered sequence of points in a space
        input point must be of class Point
        """
        self.space = point.space
        self.points= [point]
        self.params = params

        if dynamics == None:
            self.dynamics = Dynamics(self.space, Block(self.space, self.space, lambda point: point))
        else:
            self.dynamics = dynamics

        self.length = 1
    
    def set_params(self, params):
        self.params=params

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
            if self.params ==None:
                point = step(p)
            else:
                point = step(p,self.params)
            self.append_point(point)

class Dynamics:
    """
    Dynamics is a map from a space to itself
    initized as an identity map
    """
    def __init__(self, space, block=None):

        if block == None:
            block = Block(space, space, lambda point: point)
            block.set_description('This Block encodes dynamics for statespace '+str(space))

        self.block = block
        self.space = space
        self.step = self.block.map
    
    def set_step(self, func):
        self.block.set_func(func)
        self.step = self.block.map


class Metric:

    def __init__(self, func, space=None ,description = "my metric"):
        self.description = description
        self.eval = func
        self.space = space
    
    def set_func(self, func):
        self.eval = func
    
    def set_space(self, space):
        self.space = space

    def set_description(self, description):
        self.description = description

class Block:
    """
    the point of these Blocks is to take an input
    in the domain and map it to an output in the codomain
    usage:
    
    point_in_codomain = block.map(point_in_domain)
    """
    def __init__(self,domain,codomain, func, paramspace = Space(), description=None):
        
        self.paramspace = paramspace
        self.params = paramspace.point({})
        self.description = description

        if type(domain)==Space:
            self.domain = domain
        else:
            Warning("domain must be a Space")
        
        if type(codomain)==Space:
            self.codomain = codomain
        else:
            Warning("codomain must be a Space")
        
        self.map = func

    def set_params(self, point, override = False):
        
        if override:
            self.paramspace = point.space
            self.params = point
        else:
            if self.paramspace == point.space:
                self.params = point
            else:
                args = {}
                for d in self.paramspace.dimensions:
                    args[d] = getattr(point, d)
                
                self.params = self.paramspace.point(args)

    def set_domain(self,space):
        if type(space)==Space:
            self.domain = space
        else:
            Warning("domain must be a Space")

    def set_codomain(self,space):
        if type(space)==Space:
            self.codomain = space
        else:
            Warning("codomain must be a Space")

    def set_func(self, func):

        self.map = func

    def set_description(self, description):
        self.description= description

    def compose(self, block):
        """
        pt_in_codomain_of_self = self.map(block.map(pt_in_domain_of_block))
        """
        func = lambda point: self.map(block.map(point))

        description = "made by composition; collapsed space is called '"+str(self.domain.name)+"'"

        return Block(block.domain, self.codomain, func, description=description )

    def copy(self):
        
        domain = self.domain
        codomain = self.codomain
        func = self.map
        description = "copy of block: "+str(self)

        return Block(domain,codomain,func, description=description)

def parallel(blocks):
    #    | ->[ ] -->|
    # -->| ->[ ] -->| x | -->   
    #    | ->[ ] -->|

    N = len(blocks)

    check = 1
    for n in range(N-1):
        check *= int(blocks[n].domain==blocks[n+1].domain)

    if check:
        domain = blocks[0].domain
        codomain = spacewise_cartesian([b.codomain for b in blocks])

        def func(point):
            # assumes point in domain
            points = []
            for b in blocks:
                output = b.map(point)
                points.append(output)

            return pointwise_cartesian(points)

        block = Block(domain,codomain, func)

        return block

    else:
        print(Warning("domains of parallel blocks do not match"))


def chain(blocks):
    # runs left to right
    # domain->[  ] -> [ ] -> [ ]->codomain
    # domain = blocks[0].domain
    # codomain = blocks[-1].codomain

    # revese the order of the list since composition works in the opposite direction
    N = len(blocks)
    block = blocks[N-1]
    
    for n in range(N-2,-1,-1):

        new = blocks[n]

        # getting the compositions to chain in reverse
        # was a huge pain, edit with care
        #print(n)
        #print(new.codomain == block.domain)
        #print("")

        block = block.compose(new)

    description = "chain compose of "+str(blocks)
    
    block.set_description(description)

    return block

#class Stage:

### work in progress below
# systems will be composed of multistage dynamics
# from here we can work out way back to
# simulations
# and eventually
# experiments

class System():

    def __init__(self, statespace, paramspace):
        """
        this is a generalized dynamical system
        statespace is a space
        paramspace is a space
        stages is a list of dynamics
        if you have a system you can more easily make
        instances of dynamics by composing policies and mechanism
        """
        self.statespace = statespace
        self.paramspace = paramspace

        self.stages = []

    def set_statespace(self,space):
        self.statespace = space

    def set_paramspace(self,space):
        self.paramspace = space

    def append_stage(self,dynamics):
        self.stages.append(dynamics)

    def insert_stage(self, dynamics, index):
        self.stages.insert(index, dynamics)

    ### plan to have Systems generate "trajectories of trajectories"
    ### where the inner lists loops through substeps or stages (each of which are dynamics)
    ### where the outer list contains the ordering of timesteps
    ### stages seems like a better term than substep
    

class Stage(Dynamics):

    def __init__(self, system, policies=[], mechanisms=[], block=None):
        self.policies = policies
        self.mechanisms = mechanisms
        self.inputSpace = spacewise_cartesian([m.domain for m in mechanisms])
        
        super().__init__(system.statespace, block=block)

    def update_inputSpace(self):

        self.inputSpace = spacewise_cartesian([m.domain for m in self.mechanisms])
    
    def append_policy(self, policy):   

        self.update_inputSpace()

        policy.set_codomain(self.inputSpace)
        policy.set_domain(self.system.statespace)

        for obs in policy.observables:
            if obs in self.system.statespace:
                pass
            else:
                print(Warning('observable not in system statespace'))

        self.polices.append(policy)
    
    def append_mechanism(self, mechanism):
        
        mechanism.set_codomain(self.system.statespace)

        if mechanism.dimension in self.system.statesoace:
            pass
        else:
            print(Warning('output dimension not in system statespace'))

        self.mechanisms.append(mechanism)
        self.update_inputSpace()

    def update_step(self, updateDescription=False):

        inputMap = parallel(self.policies)
        
        
        # inputMap.codomain == self.inputSpace
        stateUpdateMap = parallel(self.mechanisms)

        stateUpdateMap.set_domain(inputMap.codomain)

        

        if updateDescription:
            inputs = [d for d in inputMap.codomain.dimensions]
            states_updated = [d for d in stateUpdateMap.codomain.dimensions]
            stateUpdateMap.set_description("inputs = "+str(inputs)+" and states updated = "+str(states_updated))

        block = stateUpdateMap.compose(inputMap)
        # combine policies
        # combine mechanisms
        # combines policies with mechanisms
        # results in a statespace->statespace map
        ###

        self.set_step(block)


        

class Mechanism(Block):

    def __init__(self, domain, codomain, dimension, func, description=None):
        super().__init__(domain, codomain, func, description=description)

        self.dimension = dimension

class Policy(Block):

    def __init__(self, domain, codomain, func, description=None, observables =[]):
        super().__init__(domain, codomain, func, description=description)

        self.observables = observables

    def set_observables(self, observables):
        #observables should be a subset of keys of the domain
        self.observables = observables

