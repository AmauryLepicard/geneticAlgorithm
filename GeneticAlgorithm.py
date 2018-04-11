import multiprocessing
import random

import numpy as np
import pygame

from AIPlayer import AIPlayer
from GameDisplay import GameDisplay
from GameModel import GameModel
from Parameters import *


class GeneticAlgorithm:
    def __init__(self, populationSize, generations):
        # empty the dna file
        open("dna.txt", 'w').close()
        with open("dna.txt", 'a') as f_handle:
            population = Population(populationSize)
            for i in range(generations):
                population.computeAllFitness(verbose=False, useMultiProcess=GA_USE_PROCESSES)
                print("Generation", i, "Best fitness", max(population.fitnessDict.values()), "Average fitness",
                      np.average(list(population.fitnessDict.values())))
                bestPlayer = max(population.fitnessDict, key=population.fitnessDict.get)
                # print("Best player DNA:", bestPlayer.DNA().shape, bestPlayer.DNA())
                np.savetxt(f_handle, bestPlayer.DNA(), fmt='%.5f', delimiter=",", newline=",")
                f_handle.write("\n")
                if GA_USE_PROCESSES:
                    displayProcess = multiprocessing.Process(target=population.showGame, kwargs={'player': bestPlayer})
                    displayProcess.start()
                else:
                    population.showGame(bestPlayer)
                population.generateNewPopulation()
        f_handle.close()


class Population:
    def __init__(self, nbPlayers):
        self.fitnessDict = {}
        for i in range(nbPlayers):
            area = pygame.Rect(-BORDER_SIZE, -BORDER_SIZE, SCREEN_WIDTH + 2 * BORDER_SIZE,
                               SCREEN_HEIGHT + 2 * BORDER_SIZE)
            gameModel = GameModel(area, asteroidsNumber=ASTEROID_NUMBER)
            player = AIPlayer(gameModel, "g0p" + str(i))
            self.add(player)
        self.generationNumber = 0
        self.display = GameDisplay()
        self.currentGenerationNumber = 0

    def add(self, player):
        self.fitnessDict[player] = -1.0

    def showGame(self, player):
        player.gameModel.restart()
        clock = pygame.time.Clock()

        self.display.setPlayer(player, self.currentGenerationNumber)
        while not player.gameModel.isOver:
            delta = clock.tick(60)
            player.gameModel.update(delta, False)
            player.update()
            self.display.update()

    # @functionTimer
    def computePlayerFitness(self, player, verbose=False):
        player.gameModel.restart()

        delta = 10
        while not player.gameModel.isOver:
            # update gameModel and player
            player.gameModel.update(delta, False)
            player.update()
        self.fitnessDict[player] = player.gameModel.score
        if verbose:
            print(player.name, "=>", self.fitnessDict[player])  # , ",", end="", flush=True)

    # @functionTimer
    def computeAllFitness(self, useMultiProcess=GA_USE_PROCESSES, verbose=False):
        print("Testing generation", self.generationNumber, ":")
        if useMultiProcess:
            processes = {}
            for player in self.fitnessDict:
                processes[player] = multiprocessing.Process(target=self.computePlayerFitness,
                                                            name="Process-" + player.name,
                                                            kwargs={'player': player, 'verbose': verbose})
                processes[player].start()
            for player in self.fitnessDict:
                processes[player].join()
                if verbose:
                    print("join", player.name, "=>", self.fitnessDict[player])  # , ",", end="", flush=True)
        else:
            for i, player in enumerate(self.fitnessDict):
                self.computePlayerFitness(player, verbose)
                if verbose:
                    print(player.name, "=>", self.fitnessDict[player], ",", end="", flush=True)
        if verbose:
            print()

    def selectBestPlayers(self, percentBest=GA_BEST_RATIO, useRouletteWheel=GA_USE_ROULETTE_WHEEL,
                          allowMultiSelect=GA_ALLOW_MULTISELECT):  # By default, the 10% best of the population are chosen, and each player can only be chosen once
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
                        if not allowMultiSelect:
                            del tempDict[player]
                        break
            return bestPlayers
        else:
            tempDict = sorted(self.fitnessDict, key=self.fitnessDict.get, reverse=True)[:numberToSelect]
            for p in tempDict:
                print(p.name, "(", self.fitnessDict[p], "), ", end="")

            return tempDict

    def crossover(self, father, mother, name, useCrossover=True):
        # print("Crossing ", father.name, "with", mother.name, end="")
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
        area = pygame.Rect(-BORDER_SIZE, -BORDER_SIZE, SCREEN_WIDTH + 2 * BORDER_SIZE, SCREEN_HEIGHT + 2 * BORDER_SIZE)
        gameModel = GameModel(area, asteroidsNumber=ASTEROID_NUMBER)

        child = AIPlayer(gameModel, name)
        child.setFromDNA(newDNA)
        # print("=> child:", child.name)
        return child

    def mutate(self, player, mutationRate=GA_MUTATION_CHANCE,
               mutationAmplitude=GA_MUTATION_AMPLITUDE):  # defaut mutation rate is 2%, mutation amplitude is 5%
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
        self.currentGenerationNumber += 1
