import numpy as np


class NeuralNetwork:
    def __init__(self, nbInputs, hiddenLayersSizes, nbOutputs, activationFunction):
        self.nbInputs = nbInputs
        self.nbOutputs = nbOutputs
        layers = [NNLayer(nbInputs, hiddenLayersSizes[0], activationFunction)]
        for layerNb, neuronsNb in enumerate(hiddenLayersSizes):
            hiddenLayer = NNLayer(layers[layerNb-1].neuronsNb, neuronsNb, activationFunction)
            layers.append(hiddenLayer)
        layers.append(NNLayer(layers[-1].neuronsNb, nbOutputs, activationFunction))

    def compute(self, inputVector):
        if inputVector.shape != (1, self.nbInputs):
            raise ValueError("Incorrect inputVector size")
        result = inputVector
        for layer in self.layers:
            result = layer.compute(result)
        return result


class NNLayer:
    def __init__(self, inputNb, neuronsNb, activationFunction):
        self.inputNb = inputNb
        self.neuronsNb = neuronsNb
        self.activationFunction = activationFunction
        self.weights = np.zeros((inputNb, neuronsNb))

    def compute(self, inputVector):
        if inputVector.shape != (1, self.inputNb):
            raise ValueError("Incorrect inputVector size")
        b = np.matmul(inputVector, self.weights)

        outputVector = self.activationFunction(b)
        return outputVector