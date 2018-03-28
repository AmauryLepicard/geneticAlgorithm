from NeuralNetwork import NeuralNetwork

def relu(x):
    return max(0.0, x)

class AIPlayer:
    def __init__(self):
        self.nn = NeuralNetwork(12, (6, 6), 3, relu)

    def DNA(self):
        return self.nn.DNA()

    def getData(self):
        pass
