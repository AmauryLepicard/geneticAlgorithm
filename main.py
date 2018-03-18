import pygame

import Game
import Parameters

pygame.init()
screen = pygame.display.set_mode((Parameters.SCREEN_WIDTH, Parameters.SCREEN_HEIGHT))
area = pygame.Rect(0, 0, Parameters.SCREEN_WIDTH, Parameters.SCREEN_HEIGHT)
myFont = pygame.font.SysFont(None, 15)
mouseSprite = pygame.sprite.Sprite()

game = Game.Game(screen, area, asteroidsNumber=10)

game.mainLoop()
