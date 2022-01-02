### we will put the psubs here
### for now i am writing a simple script
### so I can focus on defining APIs

# its pretty clear creating dynamics is crux of any cadCAD model
# instinctively, i think we should be looking at making
# these dynamics objects their own class
# the dynamics class would have their PSUB structure as an attribute
# they would also be best to look at how to make mechanism, policies
# and more into classes to improve the composition UX, 
# will look at that next

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
    it = new_state['It']

    if it == 'Alice':
        reach = alice.r
    elif it == 'Bob':
        reach = bob.r

    ### substep 2: input layer
    dist = distance(alice,bob)

    ### substep 2: state update layer

    if dist < reach:
        flipIt(new_state)
        it = new_state['It']
        if it == "Alice":
            alice.c = parameters["Countdown"]-1
        elif it == "Bob":
            bob.c = parameters["Countdown"]-1
    
    return new_state


### this is a hack to get the model running without
# a real cadCAD engine; this is a mocked model
# for working on the UI
def runstep(simuation):

    trajectory = simuation.results

    last_state = trajectory[-1][-1]
    print(last_state)

    next_state = runsubstep1(last_state)

    new_state = runsubstep2(next_state)

    return [next_state, new_state]
