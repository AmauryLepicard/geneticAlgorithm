import random

import numpy as np
import pygame

from AIPlayer import AIPlayer
from GameDisplay import GameDisplay


class GeneticAlgorithm:
    def __init__(self, populationSize, generations, gameModel):
        population = Population(populationSize, gameModel)
        for i in range(generations):
            population.testAll()
            print("Generation", i, "Best fitness", max(population.fitnessDict.values()))
            population.generateNewPopulation(i)


class Population:
    def __init__(self, nbPlayers, gameModel):
        self.fitnessDict = {}
        self.gameModel = gameModel
        for i in range(nbPlayers):
            player = AIPlayer(self.gameModel, "p0"+str(i))
            self.add(player)
        self.generationNumber = 0

    def add(self, player):
        self.fitnessDict[player] = -1.0

    def testPlayer(self, player, showGame=True):
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
                display.update(False)

        self.fitnessDict[player] = player.gameModel.age

    def testAll(self):
        for i, player in enumerate(self.fitnessDict):
            print("Testing player", player.name, "... ", end="")
            self.testPlayer(player, False)
            print("done, score=", self.fitnessDict[player])

    def selectBestPlayers(self, percentBest=0.1,
                          allowMultiSelect=False):  # By default, the 10% best of the population are chosen, and each player can only be chosen once
        numberToSelect = int(len(self.fitnessDict) * percentBest)
        print("Select", numberToSelect, "best players")

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
                    print("   Selecting", player.name, "with", fitness)
                    bestPlayers.append(player)
                    if ~allowMultiSelect:
                        del tempDict[player]
                    break

        return bestPlayers

    def crossover(self, father, mother, name, useCrossover=True):
        print("Crossing ", father.name, "with", mother.name)
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
        return child

    def mutate(self, player, mutationRate=0.02,
               mutationAmplitude=0.5):  # defaut mutation rate is 2%, mutation amplitude is 5%
        newDNA = player.DNA()
        for i in range(newDNA.size):
            if random.random() < mutationRate:
                newDNA[i] *= random.uniform(1.0 - mutationAmplitude, 1.0 + mutationAmplitude)
        player.setFromDNA(newDNA)
        return player

    def generateNewPopulation(self, generationNumber):
        newPopulation = {}

        self.generationNumber += 1

        print("Elitism")
        # elitism, keep the best players without changing them
        bestPlayers = self.selectBestPlayers()
        for p in bestPlayers:
            newPopulation[p] = -1.0
            print("Kept", p.name)

        print("Crossover")
        # crossover, create new childs
        for i in range(len(self.fitnessDict) - len(bestPlayers)):
            father = random.choice(list(self.fitnessDict.keys()))
            mother = random.choice(list(self.fitnessDict.keys()))
            child = self.crossover(father, mother, "p"+str(self.generationNumber)+str(i))

            # mutate the child
            child = self.mutate(child)

            newPopulation[child] = -1
            print("   Child:", child.name)

        self.fitnessDict = newPopulation
