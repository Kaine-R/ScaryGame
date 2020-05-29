import pygame
import sys


def updateEvents(player):
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player.up = True
            elif event.key == pygame.K_a:
                player.left = True
            elif event.key == pygame.K_s:
                player.down = True
            elif event.key == pygame.K_d:
                player.right = True
            elif event.key == pygame.K_ESCAPE:
                print("Program End.")
                pygame.quit()
                sys.exit()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                player.up = False
            elif event.key == pygame.K_a:
                player.left = False
            elif event.key == pygame.K_s:
                player.down = False
            elif event.key == pygame.K_d:
                player.right = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                player.leftClick = True
            elif event.button == pygame.BUTTON_RIGHT:
                player.rightClick = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == pygame.BUTTON_LEFT:
                player.leftClick = False
            elif event.button == pygame.BUTTON_RIGHT:
                player.rightClick = False
        elif event.type == pygame.QUIT:
            print("Program End.")
            pygame.quit()
            sys.exit()
