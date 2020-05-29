import pygame


class Creature:
    def __init__(self):
        self.rect = pygame.Rect((50, 50), (20, 20))

    def blit(self, screen):
        try:
            screen.blit(self.img, (self.rect.x, self.rect.y))
        except:
            print("No img assigned to Creature.")