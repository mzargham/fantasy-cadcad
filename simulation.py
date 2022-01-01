from model.dynamics import runstep
import runpy

class Simulation:

    def __init__(self, sim_config = {"max_timesteps":10, "initial_state":{}, "parameters":{},"dynamics":"path/to/my/model" }):
        self.config = sim_config
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
        runpy.run_path(self.config["dynamics"])

        # initial condition
        self.results.append([self.config["initial_state"]])

        # loop
        for t in range(T):
            data = runstep(self)
            self.results.append(data)

    def results2df(self):
        import pandas as pd
        results = self.results

        data = []
        T = len(results)
        for t in range(T):
            r = results[t]
            K = len(r)
            for k in range(K):
                datum= results[t][k]
                datum["timestep"]=t
                datum["subset"]=k+int(t>0)
                data.append(datum)

        df = pd.DataFrame(data)

        return df

