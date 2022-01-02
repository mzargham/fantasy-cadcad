# we need change this so that constructor path is what tells the engine
# where it needs to go to get the constructor for the sim configs
from apparatus.constructor import sim_configs_constructor

from simulation import Simulation
import runpy
import pandas as pd

class Experiment:

    def __init__(self, exp_config = {"Name": "Name This Experiment", "Description":"Explain the purpose of this Experiment" ,"Constructor":"path/to/constructor", 'Repetitions':1 }):
        
        self.config = exp_config
        
        # use the iterator to append unique simulation configs to sim_configs
        # self.sim_configs = [] #sim_config objects
        self.size = 0
        self.simulations = []
        # use the generate to append unique Simulation objects to simulations
        # for sim_config in self.sim_configs:
        #     simId = self.size
        #     sim = Simulation(sim_config=sim_config)
        #     self.simulations.append({"Simulation Id": simId, "Simulation":sim, "Complete":False })
        #     self.size +=1
    
    def set_config(self, exp_config):
        
        self.config = exp_config

    
    def construct_sim_configs(self):
        
        # Placeholder/Reminder that we'll need
        # to get the "dynamics" characterized  by a
        # runstep function or equivalent
        # built from our PSUBs
        runpy.run_path(self.config["Constructor"])
        
        sim_configs = sim_configs_constructor()
        #running the iterator script must result in a list of
        #valid sim_configs 

        return sim_configs

    def generate(self):

        sim_configs = self.construct_sim_configs()
        monte_carlo_number = self.config['Reptitions']
            
        for sim_config in sim_configs:
            for _ in range(monte_carlo_number):
                simId = self.size
                sim = Simulation(sim_config=sim_config)
                self.simulations.append({"Simulation Id": simId, "Simulation":sim, "Complete":False })
                self.size +=1

    def execute(self):

        for simRecord in self.simulations:
            if not(simRecord["Complete"]):
                sim = simRecord["Simulation"]
                sim.run()
                simRecord["Complete"] = True

    def get_results(self):
        #Export!
        results = []
        for simRecord in self.simulations:
            if simRecord["Complete"]:
                results.append(simRecord)

        return results

    def export_results_df(self):
        dataframes = []
        for simRecord in self.simulations:
            if simRecord["Complete"]:
                dataframe = simRecord['Simulation'].results2df()
                dataframe['Simulation Id'] = simRecord['Simulation Id']
                dataframes.append(dataframe)

        return pd.concat(dataframes, axis=1)


    def export_configs_df(self):
        configs = []
        for simRecord in self.simulations:
            if simRecord["Complete"]:
                config = simRecord['Simulation'].config
                config['Simulation Id'] = simRecord['Simulation Id']
                configs.append(config)

        return pd.DataFrame(configs) 

    def run(self):

        self.generate()
        self.execute()

        return self.get_results()

        


