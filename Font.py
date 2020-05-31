import pygame


class TextBox:
    def __init__(self, font, msg, pos, life=999):
        self.img = font.render(msg, 1, (150, 10, 150))
        self.rect = self.img.get_rect()
        self.rect.x, self.rect.y = pos[0], pos[1]
        self.life = life

    def blit(self, screen):
        screen.blit(self.img, (self.rect.x, self.rect.y))


class HUD:
    def __init__(self, screen):
        self.screenSize = screen.get_size()
        self.life = 999
        self.backbar = pygame.image.load("images/backbar.png")
        self.weaponBorder = pygame.image.load("images/weaponborder.png")
        self.wBorderRect1 = self.weaponBorder.get_rect()
        self.wBorderRect1.x, self.wBorderRect1.y = self.screenSize[0] - 200, self.screenSize[1] - 70
        self.weaponBorder2 = pygame.image.load("images/weaponborder.png")
        self.HUDGrouping = []


    def blit(self, screen):
        size = self.backbar.get_size()
        screen.blit(self.backbar, (0, int(self.screenSize[1] - size[1])))
        screen.blit(self.weaponBorder, (self.wBorderRect1.x, self.wBorderRect1.y))
        for text in self.HUDGrouping:
            text.blit(screen)