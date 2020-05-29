import pygame
import GameFunctions as gf
from Player import Player

# REMOVE escape close program feature

RED = (200, 100, 100)
YELLOW = (175, 175, 70)
GREEN = (100, 200, 100)
LBLUE = (70, 175, 175)
BLUE = (100, 100, 200)
PURPLE = (175, 70, 175)
WHITE = (220, 220, 220)
GRAY = (150, 150, 150)
BLACK = (50, 50, 50)


def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((1600, 900))
    pause = False
    player = Player()

    while not pause:
        tickSpeed = clock.tick(80)
        print(tickSpeed)
        gf.updateEvents(player)

        player.update(tickSpeed)

        player.blit(screen)

        pygame.display.flip()
        screen.fill(BLACK)


print("Program Start.")
main()
