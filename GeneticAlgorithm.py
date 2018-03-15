import copy
import random


class GeneticAlgorithm:
    def __init__(self, number):
        self.population = []
        for i in range(number):
            circle = generateCircle()
            while circle.isOverlappingList(obstacles):
                circle = generateCircle()
            self.population.append(circle)
        self.generation = 0
        self.bestScore = 0.0
        self.bestCircle = None
        self.totalScore = 0.0
        self.obstacles = obstacles

    def computeScore(self, circle):
        if circle.isOverlappingList(self.obstacles):
            return 0.0
        if circle.x < circle.radius or circle.y < circle.radius or circle.x + circle.radius > param.SCREEN_SIZE or circle.y + circle.radius > param.SCREEN_SIZE:
            return 0.0
        return circle.radius

    def mutate(self, circle):
        # print("Mutate of " + str(circle)
        newCircle = Circle(0, 0, 0)
        newCircle.x = circle.x * random.uniform(.99, 1.01)
        newCircle.y = circle.y * random.uniform(.99, 1.01)
        newCircle.radius = circle.radius * random.uniform(1.0, 1.01)
        # print("Result : " + str(newCircle)
        return newCircle

    def crossover(self, circle1, circle2):
        # print("Crossover of " + str(circle1) + " and " + str(circle2)
        # if dad and mum are the same, no need for crossover
        if circle1.equals(circle2):
            print("Crossover : No change")
            return circle1, circle2
        baby1 = copy.copy(circle1)
        baby2 = copy.copy(circle2)
        if random.random() > .5:
            baby1.x = circle2.x
            baby2.x = circle1.x
        if random.random() > .5:
            baby1.y = circle2.y
            baby2.y = circle1.y
        if random.random() > .5:
            baby1.radius = circle2.radius
            baby2.radius = circle1.radius
        # print("Result : " + str(baby1) + " , " + str(baby2)
        return baby1, baby2

    def select(self, value, scores):
        # print("Select " + str(value)
        current = 0
        for circle in self.population:
            if scores[circle] > 0:
                current += scores[circle]
                if current > value:
                    # print("Selected ",str(circle), " : ", scores[circle]
                    return circle
        print("Select ERROR " + str(value))

    def epoch(self):
        # create empty new population
        newPopulation = []

        # compute fitness scores
        scores = {}
        self.totalScore = 0
        self.bestScore = 0
        for circle in self.population:
            score = self.computeScore(circle)
            if score > self.bestScore:
                self.bestScore = score
                self.bestCircle = circle
            scores[circle] = score
            self.totalScore += score
        # self.printPopulation(scores)
        # print("Total score : "+str(self.totalScore)
        # print("Best score : "+str(self.bestScore)

        # crossover
        # print("CROSSOVER"
        while len(newPopulation) < param.POPULATION_SIZE:
            # select 2 members of the population, base on roulette wheel selection
            dad = self.select(random.uniform(0.0, self.totalScore), scores)
            mum = self.select(random.uniform(0.0, self.totalScore), scores)

            if scores[dad] == 0 or scores[mum] == 0:
                print("error, parent at score 0")
            baby1, baby2 = self.crossover(dad, mum)
            newPopulation.append(baby1)
            newPopulation.append(baby2)

        # mutate
        # print("MUTATE"
        newPopulation2 = []
        for best in self.getNBestCircles(10):
            newPopulation2.append(best[0])
        newPopulation2.append(self.bestCircle)

        for circle in newPopulation:
            newPopulation2.append(self.mutate(circle))

        # print("New population size " + str(len(newPopulation2))
        # replace the old population with the new one
        self.population = newPopulation2
        self.generation += 1

    def printPopulation(self, scores):
        print("Epoch " + str(self.generation))
        for circle in self.population:
            print(circle, " : ", scores[circle])

    def getNBestCircles(self, n):
        scores = {}
        for circle in self.population:
            scores[circle] = self.computeScore(circle)

        result = sorted(scores.items(), key=lambda x: x[1])
        return result[:n]
