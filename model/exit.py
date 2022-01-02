from model.player import distance

def criterion(state):
    alice = state["Alice"]
    bob = state["Bob"]

    dist = distance(alice, bob)

    return dist > 10