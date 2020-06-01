import pygame


class Wall:
    def __init__(self, size, pos):
        self.rect = pygame.Rect(pos, size)
        self.stopLeft = False
        self.stopRight = False
        self.stopUp = False
        self.stopDown = False

    def blit(self, screen):
        pygame.draw.rect(screen, (250, 250, 250), self.rect)
