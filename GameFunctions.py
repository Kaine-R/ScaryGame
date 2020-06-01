import pygame
import math
import sys
from Font import TextBox

def pauseMenu(pauseScreen, pause):
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_0:
                print("Program End.")
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_ESCAPE:
                pause[0] = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                mousePos = pygame.mouse.get_pos()
                if pygame.Rect.collidepoint(pauseScreen.resumeRect, mousePos[0], mousePos[1]):
                    pause[0] = False
                    return 1
                if pygame.Rect.collidepoint(pauseScreen.mainMenuRect, mousePos[0], mousePos[1]):
                    return 2
    return 0

def gameOver(gameoverScreen):
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_0:
                print("Program End.")
                pygame.quit()
                sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                mousePos = pygame.mouse.get_pos()
                if pygame.Rect.collidepoint(gameoverScreen.replayRect, mousePos[0], mousePos[1]):
                    return 1
                if pygame.Rect.collidepoint(gameoverScreen.quitRect, mousePos[0], mousePos[1]):
                    print("Program End.")
                    pygame.quit()
                    sys.exit()
    return 0

def mainMenu(mainMenuScreen, mainMenu):
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_0:
                print("Program End.")
                pygame.quit()
                sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                mousePos = pygame.mouse.get_pos()
                if pygame.Rect.collidepoint(mainMenuScreen.playRect, mousePos[0], mousePos[1]):
                    mainMenu[0] = False
                    return 1
                if pygame.Rect.collidepoint(mainMenuScreen.quitRect, mousePos[0], mousePos[1]):
                    print("Program End.")
                    pygame.quit()
                    sys.exit()
    return 0


def getAvgFPS(fps, avgFPS):
    if len(avgFPS) > 10:
        avgFPS.pop()
    avgFPS.append(fps)
    if len(avgFPS) > 0:
        avg = 0
        for i in avgFPS:
            avg += i
        print(round(avg/len(avgFPS), 2))


def pickupItems(player, pickups):
    for i, item in enumerate(pickups, 0):
        if getDistance(player.rect.center, item.rect.center) < 70:
            return i
    return -1


def getMapOffset(player, offset, gameSpace, mapSize):
    if player.rect.centerx > gameSpace[0]/2 +2 and not player.stopRight:
        if offset[2] < mapSize[0] - gameSpace[0] - 2:
            offset[0] += player.rect.centerx - gameSpace[0]/2
            offset[2] += offset[0]
    elif player.rect.centerx < gameSpace[0]/2 -2 and not player.stopLeft:
        if offset[2] > 2:
            offset[0] += player.rect.centerx - gameSpace[0]/2
            offset[2] += offset[0]

    if player.rect.centery > gameSpace[1]/2 +2 and not player.stopUp:
        if offset[3] < mapSize[1] - gameSpace[1] - 2:
            offset[1] += player.rect.centery - gameSpace[1]/2
            offset[3] += offset[1]
    elif player.rect.centery < gameSpace[1]/2 -2 and not player.stopDown:
        if offset[3] > 2:
            offset[1] += player.rect.centery - gameSpace[1]/2
            offset[3] += offset[1]


def setMapOffset(player, enemies, offset, gameMap, pickups, walls, particles):
    player.rect.x -= offset[0]
    player.rect.y -= offset[1]
    for part in particles:
        part.rect.x -= offset[0]
        part.rect.y -= offset[1]
    for wall in walls:
        wall.rect.x -= offset[0]
        wall.rect.y -= offset[1]
    for item in pickups:
        item.rect.x -= offset[0]
        item.rect.y -= offset[1]
    for enemy in enemies:
        enemy.rect.x -= offset[0]
        enemy.rect.y -= offset[1]
    for block in gameMap:
        block.rect.x -= offset[0]
        block.rect.y -= offset[1]
    offset[0], offset[1] = 0, 0


def updateEvents(player, pickups, pause):
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
            elif event.key == pygame.K_TAB:
                player.weaponEquipped = 1 if player.weaponEquipped == 0 else 0
                print(player.weaponEquipped)
            elif event.key == pygame.K_e:
                closeItem = pickupItems(player, pickups)
                if closeItem != -1:
                    player.grabbingItem(pickups[closeItem])
                    pickups.pop(closeItem)
            elif event.key == pygame.K_ESCAPE:
                pause[0] = True
            elif event.key == pygame.K_0:
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

def drawInv(screen, player, ):
    screenSize = screen.get_size()
    player.inv[0].rect.x, player.inv[0].rect.y = 50, screenSize[1] - player.inv[0].rect.height - 20
    player.inv[0].update()
    player.inv[0].ammoRect.x, player.inv[0].ammoRect.y = player.inv[0].rect.x + 5, player.inv[0].rect.y + player.inv[0].rect.height - 20
    if player.weaponEquipped == 0:
        player.inv[0].blit(screen, True)
    else:
        player.inv[0].blit(screen)

    player.inv[1].rect.x, player.inv[1].rect.y = 100 + player.inv[0].rect.width, screenSize[1] - player.inv[1].rect.height - 20
    player.inv[1].update()
    player.inv[1].ammoRect.x, player.inv[1].ammoRect.y = player.inv[1].rect.x + 5, player.inv[1].rect.y + player.inv[1].rect.height - 20
    if player.weaponEquipped == 1:
        player.inv[1].blit(screen, True)
    else:
        player.inv[1].blit(screen)

def drawHP(screen, player):
    screenSize = screen.get_size()
    imgSize = player.hpImg.get_size()
    pos = [screenSize[0] - 200, screenSize[1] - imgSize[1] - 10]
    if player.hp >= 3:
        screen.blit(player.hpImg, pos)
    else:
        screen.blit(player.ehpImg, pos)
    pos[0] = pos[0] + imgSize[0] + 10
    if player.hp >= 2:
        screen.blit(player.hpImg, pos)
    else:
        screen.blit(player.ehpImg, pos)
    pos[0] += imgSize[0] + 10
    if player.hp >= 1:
        screen.blit(player.hpImg, pos)
    else:
        screen.blit(player.ehpImg, pos)


def getRandomDrop(rand):
    if rand == 0:
        return "smg"
    elif rand == 1:
        return "ar"
    elif rand == 2:
        return "shotgun"
    elif rand == 3:
        return "rifle"
    elif rand == 4:
        return "machinegun"
    elif rand == 5:
        return "health"
    else:
        return "none"


def checkCollision(player, walls):
    for wall in walls:
        if pygame.sprite.collide_rect(player, wall):
            if wall.stopRight:
                player.vel[0] -= 1
                player.stopRight = True
            elif wall.stopLeft:
                player.vel[0] += 1
                player.stopLeft = True
            elif wall.stopUp:
                player.vel[1] += 3
                player.stopUp = True
            elif wall.stopDown:
                player.vel[1] -= 3
                player.stopDown = True

def getDistance(p1, p2):
    return math.sqrt(((p1[0] - p2[0]) ** 2)+((p1[1] - p2[1]) ** 2))


def cleanList(removeList, list1):
    removeList.sort(reverse=True)
    for i in removeList:
        try:
            list1.pop(i)
        except:
            print("List size: " + str(len(removeList)))
            print(removeList)
    removeList.clear()
