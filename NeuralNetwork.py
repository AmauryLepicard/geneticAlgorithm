import numpy as np


class NeuralNetwork:
    def __init__(self, nbInputs, hiddenLayersSizes, nbOutputs, activationFunction):
        self.nbInputs = nbInputs
        self.nbOutputs = nbOutputs
        #input layer
        self.layers = [NNLayer(nbInputs, nbInputs, activationFunction)]

        #hidden layers
        for layerNb, neuronsNb in enumerate(hiddenLayersSizes):
            hiddenLayer = NNLayer(self.layers[layerNb].neuronsNb, neuronsNb, activationFunction)
            self.layers.append(hiddenLayer)

        #output layer
        self.layers.append(NNLayer(self.layers[-1].neuronsNb, nbOutputs, activationFunction))

    def compute(self, inputVector):
        if inputVector.shape != (1, self.nbInputs):
            raise ValueError("Incorrect inputVector size")
        result = inputVector
        for layer in self.layers:
            result = layer.compute(result)
        return result

    def DNA(self):
        return np.concatenate([l.weights.flatten() for l in self.layers])

class NNLayer:
    def __init__(self, inputNb, neuronsNb, activationFunction):
        self.inputNb = inputNb
        self.neuronsNb = neuronsNb
        self.activationFunction = activationFunction
        self.weights = np.random.rand(inputNb, neuronsNb)

    def compute(self, inputVector):
        if inputVector.shape != (1, self.inputNb):
            raise ValueError("Incorrect inputVector size")
        b = np.matmul(inputVector, self.weights)

        outputVector = self.activationFunction(b)
        return outputVector