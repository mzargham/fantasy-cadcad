# we need change this so that constructor path is what tells the engine
# where it needs to go to get the constructor for the sim configs
from apparatus.simple_constructor import sim_configs_constructor
from apparatus.evaluator import evaluate_sim

from simulation import Simulation
# import runpy
import pandas as pd

class Experiment:

    def __init__(self, exp_config = {"Name": "Name This Experiment", "Description":"Explain the purpose of this Experiment" ,"Constructor":"path/to/constructor", 'Trials':1 }):
        
        self.config = exp_config
        
        # use the iterator to append unique simulation configs to sim_configs
        # self.sim_configs = [] #sim_config objects
        self.simcount = 0
        self.configcount = 0
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
        #runpy.run_path(self.config["Constructor"])
        
        sim_configs = sim_configs_constructor()
        #running the iterator script must result in a list of
        #valid sim_configs 

        return sim_configs

    def generate(self):

        sim_configs = self.construct_sim_configs()

        monte_carlo_number = self.config['Trials']
            
        for sim_config in sim_configs:
        
            for n in range(monte_carlo_number):
                #simId = self.simcount
                #print(simId)
                sim = Simulation(sim_config=sim_config)
                self.simulations.append({"Simulation Id": self.simcount, "Config Id":self.configcount, "Simulation":sim, "Trial":n,"Complete":False })
                self.simcount +=1
            
            self.configcount +=1

    def execute(self):

        for simRecord in self.simulations:
            if not(simRecord["Complete"]):
                sim = simRecord["Simulation"]
                sim.run()
                simRecord["Complete"] = True

    def evaluate(self):

        for simRecord in self.simulations:
            if simRecord["Complete"]:
                sim = simRecord['Simulation']
                evals = evaluate_sim(sim)
                print("evals")
                print(evals)
                print("")
                simRecord["Evaluations"] = {}
                for k in evals.keys():
                    print(k)
                    simRecord["Evaluations"][k] = evals[k]

    def get_records(self, as_df=True):
        #Export!
        records = []
        for simRecord in self.simulations:
            if simRecord["Complete"]:
                records.append(simRecord)
        if as_df:
            return pd.DataFrame(records)
        else:
            return records

    def export_results_df(self, dropIntermediates=True):
        dataframes = []
        for simRecord in self.simulations:
            if simRecord["Complete"]:
                dataframe = simRecord['Simulation'].results2df(dropIntermediates=dropIntermediates)
                dataframe['Simulation Id'] = simRecord['Simulation Id']
                dataframes.append(dataframe)

        return pd.concat(dataframes, axis=0)

    # def export_evals_df(self):
    #     evals = []
    #     for simRecord in self.simulations:
    #         if simRecord["Complete"]:
    #             #sim = simRecord['Simulation']
    #             eval = {}
    #             eval['Simulation Id'] = simRecord['Simulation Id']
    #             for k in simRecord["Evaluations"].keys():
    #                 simRecord["Evaluations"][k] = evals[k]
                
    #             evals.append(eval)

    #     #print(evals)

    #     return pd.DataFrame(evals) 

    # def export_configs_df(self):
    #     configs = []
    #     for simRecord in self.simulations:
    #         if simRecord["Complete"]:
    #             simId = simRecord['Simulation Id']
    #             config = simRecord['Simulation'].config
    #             config['Simulation Id'] = simId
    #             #print(simRecord['Simulation Id'])
    #             configs.append(config)

    #     #print(configs)

    #     return pd.DataFrame(configs)

    def run(self):

        self.generate()
        self.execute()

        try:
            self.config["Evaluator"]
            self.evaluate()
        except:
            print(self.config)

        return self.get_records(as_df=False)

        


