import numpy as np
import pandas as pd

class NeuralNetwork:
    def __init__(self, nbInputs, hiddenLayersSizes, nbOutputs, activationFunction):
        self.nbInputs = nbInputs
        self.nbOutputs = nbOutputs
        self.activationFunction = np.vectorize(activationFunction)

        #input layer
        self.layers = [NNLayer(nbInputs, nbInputs, self.activationFunction)]

        #hidden layers
        for neuronsNb in hiddenLayersSizes:
            hiddenLayer = NNLayer(self.layers[-1].neuronsNb, neuronsNb, self.activationFunction)
            self.layers.append(hiddenLayer)

        # output layer
        self.layers.append(NNLayer(self.layers[-1].neuronsNb, nbOutputs, self.activationFunction))

    def compute(self, inputVector):
        if len(inputVector) != self.nbInputs:
            raise ValueError("Incorrect inputVector size")
        result = inputVector
        #print("Input :", result)
        for i,layer in enumerate(self.layers):
            result = layer.compute(result)
            #print("After layer", i, ":", result)
        return result

    def DNA(self):
        return np.concatenate([l.weights.flatten() for l in self.layers])

    def __str__(self):
        s = ""
        for il, layer in enumerate(self.layers):
            s += "Layer " + str(il) + " (" + str(layer.inputNb) + "," + str(layer.neuronsNb) + "):\n"
            df = pd.DataFrame(layer.weights)
            s += df.to_string(header=False, index=False) + "\n\n"
        return s

class NNLayer:
    def __init__(self, inputNb, neuronsNb, activationFunction):
        self.inputNb = inputNb
        self.neuronsNb = neuronsNb
        self.activationFunction = activationFunction
        self.weights = np.random.rand(inputNb, neuronsNb)

    def compute(self, inputVector):
        if len(inputVector) != self.inputNb:
            raise ValueError("Incorrect inputVector size")
        b = np.matmul(inputVector, self.weights)

        outputVector = self.activationFunction(b)
        return outputVector

