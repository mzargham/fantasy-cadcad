#import os

#os.chdir("..")

from model.initializer import initialize
from model.params import parameters

sim_config = {
    "max_timesteps":1000, 
    "initial_state":initialize(parameters), 
    "parameters": parameters,
    "dynamics":"model/dynamics.py",
    ### optional 
    "seed": 82361,
    "exit_criteria": "model/exit.py"
    }