import pygame
from Font import TextBox


class Pickup:
    def __init__(self, pos, gtype="none"):
        self.type = gtype
        if gtype == "smg":
            self.img = pygame.image.load("images/smg.png").convert()
        elif gtype == "ar":
            self.img = pygame.image.load("images/ar.png").convert()
        elif gtype == "rifle":
            self.img = pygame.image.load("images/rifle.png").convert()
        elif gtype == "shotgun":
            self.img = pygame.image.load("images/shotgun.png").convert()
        elif gtype == "machinegun":
            self.img = pygame.image.load("images/machinegun.png").convert()
        elif gtype == "health":
            self.img = pygame.image.load("images/health.png").convert()
        self.img.set_colorkey((255, 255, 255))
        self.rect = self.img.get_rect()
        self.rect.x, self.rect.y = pos[0], pos[1]
        font = pygame.font.SysFont("arial", 20)
        self.text = TextBox("Pick Up: E", (self.rect.x, self.rect.y), font)
        self.text.rect = self.rect

    def blit(self, screen):
        # pygame.draw.rect(screen, (20, 20,20), self.rect)
        screen.blit(self.text.img, (self.text.rect.x + 20, self.text.rect.y - 20))
        screen.blit(self.img, (self.rect.x, self.rect.y))
