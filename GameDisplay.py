import sys
import pygame

from Parameters import *


class GameDisplay:
    def __init__(self, gameModel, player):
        pygame.init()

        # screen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.area = pygame.Rect(-BORDER_SIZE, -BORDER_SIZE, SCREEN_WIDTH + 2 * BORDER_SIZE, SCREEN_HEIGHT + 2 * BORDER_SIZE)

        # text
        self.myFont30 = pygame.font.SysFont(None, 30)
        self.myFont200 = pygame.font.SysFont(None, 200)
        self.myFont100 = pygame.font.SysFont(None, 100)
        pygame.display.set_caption("Asteroids")

        self.mouseSprite = pygame.sprite.Sprite()

        self.gameModel = gameModel
        self.player = player

    def startThread(self):
        while not self.gameModel.isOver:
            self.update(10)

    def update(self):

        # clear screen
        self.screen.fill((0, 0, 0))

        # render text
        asteroidsDestroyedLabel = self.myFont30.render("Asteroids destroyed: " + str(self.gameModel.score), 1, (255, 255, 255))
        self.screen.blit(asteroidsDestroyedLabel, (0, 0))

        timeLabel = self.myFont30.render("Time: " + str(self.gameModel.age), 1, (255, 255, 255))
        self.screen.blit(timeLabel, (0, 35))

        if self.gameModel.isOver:
            label = self.myFont200.render("GAME OVER", 1, (255, 255, 255))
            self.screen.blit(label, ((SCREEN_WIDTH - label.get_width()) / 2, (SCREEN_HEIGHT - label.get_height()) / 2))
            label2 = self.myFont100.render("Press Enter to restart, Echap to quit", 1, (255, 255, 255))
            self.screen.blit(label2, ((SCREEN_WIDTH - label2.get_width()) / 2, 100 + (SCREEN_HEIGHT - label2.get_height()) / 2))
            pygame.display.quit()
            pygame.quit()
            return

        else:

            # draw gameModel
            self.gameModel.asteroidsGroup.draw(self.screen)
            self.gameModel.shipGroup.draw(self.screen)
            self.gameModel.bulletsGroup.draw(self.screen)

            # show quadrant lines#
            #        nbQuadrants = 8
            #        for i in range(nbQuadrants):
            #            angle = gameModel.ship.theta + (i+0.5)*2*math.pi/nbQuadrants
            #            delta = np.array((2000*math.cos(angle), 2000*math.sin(angle)))
            #            pygame.draw.aaline(screen, (100,100,100), gameModel.ship.pos, gameModel.ship.pos+delta)

            timeLabel = self.myFont30.render("Input: " + str(self.player.inputVector), 1, (255, 255, 255))
            self.screen.blit(timeLabel, (0, 70))
            timeLabel = self.myFont30.render("Output: " + str(self.player.commands), 1, (255, 255, 255))
            self.screen.blit(timeLabel, (0, 100))

        pygame.display.flip()
