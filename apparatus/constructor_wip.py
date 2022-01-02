## This dictionary works like the legacy cadCAD params object to produce a bunch 
# of individual params dictionaries (used cartesian product rule)

# its pretty clear creating constructors is challenging
# instinctively, i think we should be looking at making
# these constructors their own class

sweeper = {
    "Alice Speed": [1], 
    "Bob Speed": [.9, 1, 1] , 
    "Alice Start Positions":[(0,0), (2,0)], 
    "Bob Start Positions":[(10,10), (10,20), (10,-20), (-10,15)] 
    }

from functools import reduce
from operator import mul

counts = [len(v) for v in sweeper.values()]  
count = reduce(mul, counts, 1)

import os
os.chdir('..')
from model.player import Player
#

alice_speed = sweeper['Alice Speed']
bob_speed = sweeper['Bob Speed']

def initial_state_contructor():

    state = {
    "Alice": [Player(0,0, va) for va in alice_speed], 
    "Bob": [Player(10,20, vb) for vb in bob_speed], 
    "It": ["Alice", "Bob"] 
    }
    return state

def dynamics_constructor():

    dynamics_path = "/model/dynamics.py"

    return dynamics_path

def max_timesteps_constructor():

    return 25

def sim_configs_constructor():

    sim_configs = []
    for i in items:
        params = params_constructor()
        initial_state = initial_state_constructor()
        dynamics = dynamics_constructor()
        max_timesteps = max_timesteps_constructor()

        sim_config = {"max_timesteps":max_timesteps, "initial_state":initial_state, "parameters":params,"dynamics":dynamics}

        sim_configs.append(sim_config)

    return sim_configs