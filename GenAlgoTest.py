import pygame

from GameModel import GameModel
from GeneticAlgorithm import GeneticAlgorithm
from Parameters import *

area = pygame.Rect(-BORDER_SIZE, -BORDER_SIZE, SCREEN_WIDTH + 2 * BORDER_SIZE, SCREEN_HEIGHT + 2 * BORDER_SIZE)
game = GameModel(area, asteroidsNumber=ASTEROID_NUMBER)
ga = GeneticAlgorithm(20, 5)
