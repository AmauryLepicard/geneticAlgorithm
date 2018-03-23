from NeuralNetwork import NeuralNetwork

class AIPlayer:
    def __init__(self):
        self.nn = NeuralNetwork(12, (6, 6), 3)

    def DNA(self):
        return self.nn.DNA()

    def getData(self):
