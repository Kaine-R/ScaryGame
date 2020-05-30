import pygame
import math
import sys


def getAvgFPS(fps, avgFPS):
    if len(avgFPS) > 10:
        avgFPS.pop()
    avgFPS.append(fps)
    if len(avgFPS) > 0:
        avg = 0
        for i in avgFPS:
            avg += i
        print(round(avg/len(avgFPS), 2))


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
            mouse = pygame.mouse.get_pos()
            offset = mouse[0] - player.rect.centerx, mouse[1] - player.rect.centery
            angle = math.degrees(math.atan2(offset[1], offset[0]))
            if angle < 0:
                angle += 360
            player.angle = angle
            # print(angle)
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

def checkCollision(player, obj):
    if pygame.sprite.collide_rect(player, obj):
        print("hit wall")