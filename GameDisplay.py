import pygame

from Parameters import *


class GameDisplay:
    def __init__(self):
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

        self.player = None
        self.generation = -1

    def setPlayer(self, player, generation):
        self.player = player
        self.generation = generation

    def update(self):
        if not self.player.gameModel.isOver:
            # clear screen
            self.screen.fill((0, 0, 0))

            # render text
            playerInfoLabel = self.myFont30.render(
                "Generation: " + str(self.generation) + "    Name:" + self.player.name, 1, (255, 255, 255))
            self.screen.blit(playerInfoLabel, (5, 5))

            timeLabel = self.myFont30.render(
                "Time: " + str(self.player.gameModel.age) + "    Asteroids destroyed: " + str(
                    self.player.gameModel.score), 1, (255, 255, 255))
            self.screen.blit(timeLabel, (300, 5))

            inputOutputLabel = self.myFont30.render(
                "Input: " + str(self.player.inputVector) + "    Output: " + str(self.player.commands), 1,
                (255, 255, 255))
            self.screen.blit(inputOutputLabel, (5, 35))

            # draw gameModel
            self.player.gameModel.asteroidsGroup.draw(self.screen)
            self.player.gameModel.shipGroup.draw(self.screen)
            self.player.gameModel.bulletsGroup.draw(self.screen)

            pygame.display.flip()
        else:
            label = self.myFont200.render("GAME OVER", 1, (255, 255, 255))
            self.screen.blit(label, ((SCREEN_WIDTH - label.get_width()) / 2, (SCREEN_HEIGHT - label.get_height()) / 2))
            label2 = self.myFont100.render("Press Enter to restart, Echap to quit", 1, (255, 255, 255))
            self.screen.blit(label2,
                             ((SCREEN_WIDTH - label2.get_width()) / 2, 100 + (SCREEN_HEIGHT - label2.get_height()) / 2))
