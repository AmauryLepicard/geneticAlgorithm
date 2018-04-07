from AIPlayer import AIPlayer

class Population
    def __init__(self, nbPlayers, game):
        self.fitnessDict = {}
        for i in range(nbPLayers):
            self.add(AIPlayer(game))

    def add(self, player):
        self.fitnessDict[player] = -1.0



