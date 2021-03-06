import numpy as np
import pandas as pd

def relu(x):
    return max(0.0, x)


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


class NeuralNetwork:
    def __init__(self, nbInputs, hiddenLayersSizes, nbOutputs):
        self.nbInputs = nbInputs
        self.nbOutputs = nbOutputs

        # input layer
        self.layers = [NNLayer(nbInputs, nbInputs, np.arctan)]

        # hidden layers
        for neuronsNb in hiddenLayersSizes:
            hiddenLayer = NNLayer(self.layers[-1].neuronsNb, neuronsNb, np.arctan)
            self.layers.append(hiddenLayer)

        # output layer
        self.layers.append(NNLayer(self.layers[-1].neuronsNb, nbOutputs, np.arctan))

    def compute(self, inputVector):
        if len(inputVector) != self.nbInputs:
            raise ValueError("Incorrect inputVector size")
        result = inputVector
        # print("Input :", result)
        for i, layer in enumerate(self.layers):
            result = layer.compute(result)
            # print("After layer", i, ":", result)
        return result

    def DNA(self):
        return np.concatenate([l.weights.flatten() for l in self.layers])

    def setFromDNA(self, dna: np.array):
        # check DNA has enough values
        if len(dna) != sum(l.weights.size for l in self.layers):
            print("Incorrect DNA size, is ", len(dna), ",should be", sum(l.weights.size for l in self.layers))
        for layer in self.layers:
            layerWeights = dna[:layer.weights.size]
            dna = dna[layer.weights.size:]
            layer.weights = layerWeights.reshape(layer.weights.shape)

    def __str__(self):
        s = ""
        for il, layer in enumerate(self.layers):
            s += "Layer " + str(il) + " (" + str(layer.inputNb+1) + "," + str(layer.neuronsNb) + "):\n"
            df = pd.DataFrame(layer.weights)
            s += df.to_string(header=False, index=False) + "\n\n"
        return s

    def structStr(self):
        s = ""
        for layer in self.layers:
            s += str(len(layer.weights)) + ","
        s += str(self.nbOutputs)
        return s


class NNLayer:
    def __init__(self, inputNb, neuronsNb, activationFunction):
        self.inputNb = inputNb
        self.neuronsNb = neuronsNb
        self.activationFunction = activationFunction

        # generate random weights, including an additional one for bias
        self.weights = np.random.uniform(-1.0, 1.0, (inputNb + 1, neuronsNb))

    def compute(self, inputVector):
        if len(inputVector) != self.inputNb:
            raise ValueError("Incorrect inputVector size")

        # add bias as additional input value -1from
        inputVector = np.insert(inputVector, 0, -1)

        h = np.matmul(inputVector, self.weights)

        outputVector = self.activationFunction(h)
        return outputVector
