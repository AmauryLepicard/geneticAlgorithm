import random
import numpy as np
import pygame
import threading

from AIPlayer import AIPlayer
from GameDisplay import GameDisplay
from Decorators import *


class GeneticAlgorithm:
    def __init__(self, populationSize, generations, gameModel):
        with open("dna.txt", 'a') as f_handle:
            population = Population(populationSize, gameModel)
            for i in range(generations):
                population.computeAllFitness()
                print("Generation", i, "Best fitness", max(population.fitnessDict.values()), "Average fitness", np.average(list(population.fitnessDict.values())))
                bestPlayer = max(population.fitnessDict, key=population.fitnessDict.get)
                np.savetxt(f_handle, bestPlayer.DNA(), fmt='%.5f', delimiter=",", newline=",")
                population.computePlayerFitness(bestPlayer, True)
                population.generateNewPopulation()
        f_handle.close()


class Population:
    def __init__(self, nbPlayers, gameModel):
        self.fitnessDict = {}
        self.gameModel = gameModel
        for i in range(nbPlayers):
            player = AIPlayer(self.gameModel, "g0p"+str(i))
            self.add(player)
        self.generationNumber = 0

    def add(self, player):
        self.fitnessDict[player] = -1.0

    # @functionTimer
    def computePlayerFitness(self, player, showGame=True):
        self.gameModel.restart()
        if showGame:
            display = GameDisplay(self.gameModel, player)

        clock = pygame.time.Clock()

        while not player.gameModel.isOver:
            # update gameModel
            if showGame:
                delta = clock.tick(60)
            else:
                delta = 10

            # update gameModel model
            player.gameModel.update(delta, False)
            player.update()
            if showGame:
                display.update()
        self.fitnessDict[player] = player.gameModel.age
        print(player.name, "=>", self.fitnessDict[player], end="", flush=True)

    # @functionTimer
    def computeAllFitness(self, useThread=False):
        print("Testing generation", self.generationNumber, ":")
        if useThread:
            threads = {}
            for p in self.fitnessDict:
                threads[p] = threading.Thread(target=self.computePlayerFitness, kwargs={'player': p, 'showGame': False})
                threads[p].start()
                # self.fitnessDict[player] = self.testPlayer(player, False)
                # print(player.name, "=>", self.fitnessDict[player] , ",", end="", flush=True)
            for p in self.fitnessDict:
                threads[p].join()
                print(p.name, "=>", self.fitnessDict[p], ",", end="", flush=True)
        else:
            for i, player in enumerate(self.fitnessDict):
                self.computePlayerFitness(player, False)
                print(player.name, "=>", self.fitnessDict[player], ",", end="", flush=True)

    def selectBestPlayers(self, percentBest=0.2, useRouletteWheel=False, allowMultiSelect=True):  # By default, the 10% best of the population are chosen, and each player can only be chosen once
        numberToSelect = int(len(self.fitnessDict) * percentBest)
        print("Select", numberToSelect, "best players: ", end="")

        if useRouletteWheel:
            # roulette wheel selection: players have a chance to be selected proportional to  their fitness
            bestPlayers = []

            # copy the players fitness dictionary (to allow removing players from the copy, not the population)
            tempDict = self.fitnessDict.copy()
            for i in range(numberToSelect):
                fitnessSum = sum(tempDict.values())
                pick = random.uniform(0, fitnessSum)
                current = 0
                for player, fitness in tempDict.items():
                    current += fitness
                    if current > pick:
                        print(player.name, "(", fitness, "), ", end="")
                        bestPlayers.append(player)
                        if ~allowMultiSelect:
                            del tempDict[player]
                        break
            return bestPlayers
        else:
            tempDict = sorted(self.fitnessDict, key=self.fitnessDict.get, reverse=True)[:numberToSelect]
            for p in tempDict:
                print(p.name, "(", self.fitnessDict[p], "), ", end="")

            return tempDict

    def crossover(self, father, mother, name, useCrossover=True):
        print("Crossing ", father.name, "with", mother.name, end="")
        fatherDNA = father.DNA()
        motherDNA = mother.DNA()

        if useCrossover:
            # generate new DNA based on random crossover point
            crossoverPoint = random.randint(0, fatherDNA.size - 1)
            newDNA = np.concatenate([fatherDNA[:crossoverPoint], motherDNA[crossoverPoint:]])
        else:
            # randomly choose DNA elements from father or mother
            newDNA = np.zeros(fatherDNA.size)
            for i in range(fatherDNA.size):
                if random.random() > 0.5:
                    newDNA[i] = fatherDNA[i]
                else:
                    newDNA[i] = motherDNA[i]

        # create a child with newDNA
        child = AIPlayer(self.gameModel, name)
        child.setFromDNA(newDNA)
        print("=> child:", child.name)
        return child

    def mutate(self, player, mutationRate=0.02,
               mutationAmplitude=0.5):  # defaut mutation rate is 2%, mutation amplitude is 5%
        newDNA = player.DNA()
        for i in range(newDNA.size):
            if random.random() < mutationRate:
                newDNA[i] *= random.uniform(1.0 - mutationAmplitude, 1.0 + mutationAmplitude)
        player.setFromDNA(newDNA)
        return player

    def generateNewPopulation(self):
        newPopulation = {}

        self.generationNumber += 1

        print("Elitism:")
        # elitism, keep the best players without changing them
        bestPlayers = self.selectBestPlayers()
        for p in bestPlayers:
            newPopulation[p] = -1.0

        print()
        print("Crossover:")
        # crossover, create new childs
        for i in range(len(self.fitnessDict) - len(bestPlayers)):
            father = random.choice(bestPlayers)
            mother = random.choice(bestPlayers)
            child = self.crossover(father, mother, "g" + str(self.generationNumber) + "p" + str(i))

            # mutate the child
            child = self.mutate(child)

            newPopulation[child] = -1

        self.fitnessDict = newPopulation
