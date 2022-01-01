from model.player import Player

from model.params import parameters

alice_speed = parameters['Alice Speed']
bob_speed = parameters['Bob Speed']

state = {"Alice": Player(0,0, alice_speed), "Bob": Player(10,20, bob_speed), "It": "Alice" }