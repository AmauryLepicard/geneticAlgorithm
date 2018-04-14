import multiprocessing

import matplotlib.pyplot as plt
import numpy as np

from Parameters import *
from Population import Population


class GeneticAlgorithm:
    def __init__(self, populationSize, generations):
        # empty the dna file
        open("dna.txt", 'w').close()
        with open("dna.txt", 'a') as f_handle:
            self.averageFitness = []
            self.maxFitness = []
            self.population = Population(populationSize)
            for i in range(generations):
                self.population.generationNumber = i
                avgF, maxF = self.testGeneration(f_handle)
                self.averageFitness.append(avgF)
                self.maxFitness.append(maxF)
                print("Generation", i, "Best fitness", maxF, "Average fitness", avgF)

        f_handle.close()
        plt.plot(range(generations), self.averageFitness)
        plt.plot(range(generations), self.maxFitness)
        plt.show()

    def testGeneration(self, f_handle):
        self.population.computeAllFitness(verbose=False, useMultiProcess=GA_USE_PROCESSES, nbRuns=GA_NUMBER_RUNS)
        bestFitness = max(self.population.fitnessDict.values())
        averageFitness = np.average(list(self.population.fitnessDict.values()))
        bestPlayer = max(self.population.fitnessDict, key=self.population.fitnessDict.get)
        dna = bestPlayer.DNA().reshape(1, -1)
        # print("Best player DNA:", dna.shape, dna)
        np.savetxt(f_handle, dna, fmt='%.5f', delimiter=",", newline="")
        f_handle.write("\n")
        if GA_SHOW_BESTPLAYER_GAME:
            if GA_USE_PROCESSES:
                displayProcess = multiprocessing.Process(target=self.population.showGame, kwargs={'player': bestPlayer})
                displayProcess.start()
            else:
                self.population.showGame(bestPlayer)
                self.population.generateNewPopulation()
        return averageFitness, bestFitness
