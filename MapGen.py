import pygame
import random

from Enemy import Enemy
from Walls import Wall

def generateMap(gameMap):
    offset = [0, 0]
    road = bigPic("images/roadBackground.png")
    road.rect.x, road.rect.y = offset[0], offset[1]
    house = bigPic("images/houseBackground.png")
    house.rect.x, house.rect.y = offset[0] + road.rect.width, offset[1]
    gameMap.append(road)
    gameMap.append(house)

    return road.rect.width + house.rect.width, house.rect.height



def generateWalls(walls):
    # print("i")
    newWall = Wall((70, 1400), (0, 0))
    newWall.stopLeft = True
    walls.append(newWall)
    newWall = Wall((2800, 50), (0, 0))
    newWall.stopUp = True
    walls.append(newWall)
    newWall = Wall((70, 1400), (2750, 0))
    newWall.stopRight = True
    walls.append(newWall)
    newWall = Wall((2800, 50), (0, 1400))
    newWall.stopDown = True
    walls.append(newWall)


def spawningEnemies(timer, totalTimer, enemies):
    rand = random.randint(0, 10)
    pos = pickSpawn(rand)

    if timer >= totalTimer:
        if random.randint(0, 2) == 0:
            totalTimer -= 1
        if len(enemies) < 400:
            for i in range(random.randint(2, 4)):
                rand = random.randint(0, 10)
                pos = pickSpawn(rand)
                newZom = Enemy()
                newZom.rect.x, newZom.rect.y = pos
                newZom.speed += int(totalTimer/10000)
                enemies.append(newZom)
        return True
    return False


def pickSpawn(rand):
    if rand == 0:
        pos = -100, -150
    elif rand == 1:
        pos = -200, -400
    elif rand == 2:
        pos = 1200, -10
    elif rand == 3:
        pos = 1200, -300
    elif rand == 4:
        pos = 1200, -700
    elif rand == 5:
        pos = 1800, -200
    elif rand == 6:
        pos = 200, 2000
    elif rand == 7:
        pos = 600, 2000
    else:
        pos = 600, -100
    return pos


class bigPic:
    def __init__(self, loc):
        self.img = pygame.image.load(loc).convert()
        self.rect = self.img.get_rect()
        self.type = "bigPic"

    def blit(self, screen):
        screen.blit(self.img, (self.rect.x, self.rect.y))


class Block:
    def __init__(self, type, pos):
        self.type = type
        if type == "tile":
            self.img = pygame.image.load("images/Tile.png").convert()
        elif type == "wall":
            self.img = pygame.image.load("images/wall.png").convert()
        elif type == "roof":
            self.img = pygame.image.load("images/roof.png").convert()
        else:
            self.img = pygame.image.load("images/default.png").convert()
        self.rect = pygame.Rect(pos, (50, 50))
        self.picNum = random.randint(0, 3)

    def blit(self, screen):
        size = 50
        if self.type == "tile" or self.type == "roof":
            size = 25
        screen.blit(self.img, (self.rect.x, self.rect.y), (self.picNum*50, 0, 50, size))

