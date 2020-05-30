import pygame
import random

class Block:
    def __init__(self, type, pos):
        self.type = type
        if type == "tile":
            self.img = pygame.image.load("images/Tile.png")
        elif type == "wall":
            self.img = pygame.image.load("images/wall.png")
        elif type == "roof":
            self.img = pygame.image.load("images/roof.png")
        else:
            self.img = pygame.image.load("images/default.png")
        self.rect = pygame.Rect(pos, (50, 50))
        self.picNum = random.randint(0, 3)

    def update(self):
        if False:
            print("")

    def blit(self, screen):
        size = 50
        if self.type == "tile" or self.type == "roof":
            size = 25
        screen.blit(self.img, (self.rect.x, self.rect.y), (self.picNum*50, 0, 50, size))

