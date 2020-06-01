import pygame
import random

class Enemy:
    def __init__(self):
        self.img = [pygame.image.load("images/enemy1.png").convert(),
                    pygame.image.load("images/enemy2.png").convert(),
                    pygame.image.load("images/enemy3.png").convert()]
        self.img[0].set_colorkey((255, 255, 255))
        self.img[1].set_colorkey((255, 255, 255))
        self.img[2].set_colorkey((255, 255, 255))
        self.frames = 3
        self.rect = self.img[0].get_rect()
        self.timer = 0
        self.speed = random.randint(0, 2)

        self.hp = 3

        self.sightLines = 9999
        self.away = False
        self.towards = True

    def update(self, player, ts):
        self.timer += 1
        gap = 10
        distoObj = 0

        if distoObj < self.sightLines:
            if self.away:
                if self.rect.centerx < player.rect.centerx - gap:
                    self.rect.x -= self.speed + int(ts/10)
                elif self.rect.centerx > player.rect.centerx + gap:
                    self.rect.x += self.speed + int(ts/10)
                if self.rect.centery < player.rect.centery - gap:
                    self.rect.y -= self.speed + int(ts/10)
                elif self.rect.centery > player.rect.centery + gap:
                    self.rect.y += self.speed + int(ts/10)
            elif self.towards:
                if self.rect.centerx < player.rect.centerx - gap:
                    self.rect.x += self.speed + int(ts/10)
                elif self.rect.centerx > player.rect.centerx + gap:
                    self.rect.x -= self.speed + int(ts/10)
                if self.rect.centery < player.rect.centery - gap:
                    self.rect.y += self.speed + int(ts/10)
                elif self.rect.centery > player.rect.centery + gap:
                    self.rect.y -= self.speed + int(ts/10)

    def blit(self, screen, player):
        currentFrame = int(self.timer / 40)
        if currentFrame >= self.frames:
            currentFrame = 0
            self.timer = 0
        # pygame.draw.rect(screen, (200, 200, 200), self.rect)
        pygame.draw.circle(screen, (255, 20, 20), self.rect.center, 12)
        screen.blit(pygame.transform.rotate(self.img[currentFrame], -player.angle), (self.rect.x, self.rect.y))
