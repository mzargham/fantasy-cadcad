from model.sim_config import sim_config

seeds = range(10)

def sim_configs_constructor():

    sim_configs = []
    for s in seeds:
        config = sim_config.copy()

        config['seed'] = s
        sim_configs.append(config)

    return sim_configs