import pygame

class Enemy:
    def __init__(self):
        self.img = pygame.image.load("images/enemyWalking.png")
        self.frames = 4, 1
        self.sizeofFrame = self.img.get_width() / self.frames[0], self.img.get_height() / self.frames[1]
        self.rect = pygame.Rect((0, 0), self.sizeofFrame)
        self.timer = 0


        self.sightLines = 9999
        self.away = True
        self.towards = True

    def update(self, player):
        self.timer += 1
        gap = 20
        distoObj = 0

        if distoObj < self.sightLines:
            if self.away:
                if self.rect.centerx < player.rect.centerx - gap:
                    self.rect.x -= 1
                elif self.rect.centerx > player.rect.centerx + gap:
                    self.rect.x += 1
                if self.rect.centery < player.rect.centery - gap:
                    self.rect.y -= 1
                elif self.rect.centery > player.rect.centery + gap:
                    self.rect.y += 1
            elif self.towards:
                if self.rect.centerx < player.rect.centerx - gap:
                    self.rect.x += 1
                elif self.rect.centerx < player.rect.centerx + gap:
                    self.rect.x -= 1
                if self.rect.centery < player.rect.centery - gap:
                    self.rect.y += 1
                elif self.rect.centery > player.rect.centery + gap:
                    self.rect.y -= 1

    def blit(self, screen):
        currentFrame = int(self.timer / 40)
        if currentFrame >= self.frames[0]:
            currentFrame = 0
            self.timer = 0
        # pygame.draw.rect(screen, (200, 200, 200), self.rect)
        screen.blit(self.img, (self.rect.x, self.rect.y),
                    (currentFrame * self.sizeofFrame[0], 0, self.sizeofFrame[0], self.sizeofFrame[1]))