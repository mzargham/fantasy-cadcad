### we will put the psubs here
### for now i am writing a simple script
### so I can focus on defining APIs

import copy
from model.player import distance
from model.params import parameters

def flipIt(state):  
    it = state["It"]
    if it == "Alice":
        state["It"] = "Bob"
    elif it == "Bob":
        state["It"] = "Alice"

def runsubstep1(state):

    new_state = copy.deepcopy(state)

    ### step 1: input layer
    it = new_state['It']

    ### step 1: state update leyer
    alice = new_state['Alice']
    bob = new_state['Bob']

    if it=="Alice":
        bob.evade(alice)
        alice.chase(bob)

    elif it =="Bob":
        alice.evade(bob)
        bob.chase(alice)
    
    else:
        alice.evade(bob)
        bob.evade(alice)

    return new_state

def runsubstep2(state):

    new_state = copy.deepcopy(state)
    alice = new_state['Alice']
    bob = new_state['Bob']

    ### substep 2: input layer
    dist = distance(alice,bob)

    ### substep 2: state update layer

    if dist < parameters["reach"]:
        flipIt(new_state)
        it = new_state['It']
        if it == "Alice":
            alice.c = 3
        elif it == "Bob":
            bob.c = 3 
    
    return new_state

def runstep(simuation):

    trajectory = simuation.results

    last_state = trajectory[-1][-1]
    print(last_state)

    next_state = runsubstep1(last_state)

    new_state = runsubstep2(next_state)

    return [next_state, new_state]
