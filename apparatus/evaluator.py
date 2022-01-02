from model.player import distance

def evaluate_sim(sim):
    
    scores = {}
    scores['sim_length'] = get_sim_len(sim)
    scores['mean_distance'] = get_mean_distance(sim)
    scores['alice_it_fraction'] = get_alice_it_frac(sim)

    return scores

def get_sim_len(sim):
    print("sim len")
    print(len(sim.results))
    return len(sim.results)

def get_mean_distance(sim):
    print("mean distance")
    T = get_sim_len(sim)
    distances = []
    for r in sim.results:
        alice = r[-1]['Alice']
        bob = r[-1]['Bob']
        dist = distance(alice, bob)
        distances.append(dist)
    
    mean = sum(distances)/T
    return mean

def get_alice_it_frac(sim):
    print("alice it fraction")
    T = get_sim_len(sim)
    counter = 0
    for r in sim.results:
        it = r[-1]["It"]
        if it=="Alice":
            counter +=1
            
    frac = counter/T
    return frac

