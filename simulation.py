# this first import will be eliminated for a model running against an actual cadCAD engine
from model.dynamics import runstep
from model.exit import criterion

import runpy
import numpy.random as rng

class Simulation:

    def __init__(self, sim_config = {"max_timesteps":10, "initial_state":{}, "parameters":{},"dynamics":"path/to/my/model/dynamics.py" }):
        self.config = sim_config

        self.seedInt = None 
        self.results = []


    ### setters
    def set_config(self, sim_config):
        self.config = sim_config

    def set_initial_state(self, state):
        self.config['initial_state']=state

    def set_parameters(self, sim_params):
        self.config['parameters']=sim_params

    def set_max_timesteps(self, max_timesteps):
        self.config['max_timesteps']=max_timesteps

    def set_dynamics(self, sim_dynamics):
        self.config['dynamics'] = sim_dynamics

    ### executor
    def run(self):
        T = self.config["max_timesteps"]

        # Placeholder/Reminder that we'll need
        # to get the "dynamics" characterized  by a
        # runstep function or equivalent
        # built from our PSUBs
        runpy.run_path(self.config["dynamics"])
        #placeholder for going to get this
        runpy.run_path(self.config["exit_criteria"])

        # initial condition
        self.results.append([self.config["initial_state"]])

        # loop
        ## i am tracking the seed i use for the run
        ## in order to make it reproducable
        try:
            self.seedInt = self.config["seed"]
        except:
            self.seedInt = rng.randint(0,2**18)
        
        rng.seed(self.seedInt)
        for _ in range(T):
            data = runstep(self)
            self.results.append(data)
            if criterion(data[-1]):
                break

    def results2df(self, dropIntermediates=False):
        import pandas as pd
        results = self.results

        data = []
        T = len(results)
        for t in range(T):
            r = results[t]
            K = len(r)

            if not(dropIntermediates):
                for k in range(K):
                    datum= results[t][k]
                    datum["timestep"]=t
                    datum["subset"]=k+int(t>0)
                    data.append(datum)
            elif dropIntermediates:
                k=K-1
                datum= results[t][k]
                datum["timestep"]=t
                datum["subset"]=k+int(t>0)
                data.append(datum)


        df = pd.DataFrame(data)

        return df

