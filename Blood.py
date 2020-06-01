import pygame
import random


class Blood:
    def __init__(self, pos, angle):
        if random.randint(0, 1) == 0:
            self.img = pygame.image.load("images/blood1.png").convert()
            self.img = pygame.transform.rotate(self.img, angle)
            self.img.set_colorkey((255, 255, 255))
            self.rect = pygame.Rect(pos, (10, 10))

    def blit(self, screen):
        screen.blit(self.img, self.rect)
