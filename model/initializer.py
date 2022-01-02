from model.player import Player
# from model.params import parameters

## I am noticing a recurring them that initial state needs
# to be constructed with access to the parameters for the run
# i think it may make sense to make initial state constructors functions
# which take the params in, and return an instance of the statepace

def initialize(parameters):

    alice_speed = parameters['Alice Speed']
    bob_speed = parameters['Bob Speed']

    alice_accel = parameters['Alice Acceleration']
    bob_accel = parameters['Bob Acceleration']

    alice_reach = parameters['Alice Reach']
    bob_reach = parameters['Bob Reach']

    countdown = parameters['Countdown'] 

    state = {
        "Alice": Player(0,0, 0, alice_accel, countdown, alice_reach, alice_speed),
        "Bob": Player(0,0, 0, bob_accel,0, bob_reach, bob_speed), 
        "It": "Alice"
        }
    
    return state