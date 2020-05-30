import pygame
import GameFunctions as gf
from Player import Player
from Enemy import Enemy
from Block import Block

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
    pygame.display.set_caption("Scary Game")
    pause = False
    player = Player()
    enemy = Enemy()
    enemy.rect.x = 100

    enemies = [enemy]
    particles = []
    map = []

    for i in range(10):
        block = Block("roof", (i*50, 25))
        map.append(block)
    for i in range(10):
        block = Block("wall", (i*50, 50))
        map.append(block)
    for i in range(10):
        block = Block("tile", (i*50, 100))
        map.append(block)

    # FPS STUFF CAN BE REMOVED
    avgFPS = []
    count = 0

    while not pause:
        tickSpeed = clock.tick(80)

        count += 1
        if count > 80:
            count = 0
            gf.getAvgFPS(clock.get_fps(), avgFPS)
        # print(tickSpeed)

        gf.updateEvents(player)

        for block in map:
            block.update()
            if block.type == "wall":
                gf.checkCollision(player, block)
            block.blit(screen)

        player.update(tickSpeed)
        player.attack(screen)

        for enemy in enemies:
            enemy.update(player)
            enemy.blit(screen)

        player.blit(screen)

        pygame.display.flip()
        screen.fill(BLACK)


print("Program Start.")
main()
