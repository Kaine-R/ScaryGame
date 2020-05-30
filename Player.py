import pygame
import math


class Player:
    def __init__(self):
        self.img = pygame.image.load("images/playerSheet.png")
        self.img.set_alpha(50)
        self.frames = 4, 1
        self.sizeofFrame = self.img.get_width() / self.frames[0], self.img.get_height() / self.frames[1]
        self.rect = pygame.Rect((0, 0), self.sizeofFrame)
        self.vel = [0, 0]
        self.angle = 0

        self.timer = 0

        # Controls
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.leftClick = False
        self.rightClick = False

        self.attackCD = 0


    def update(self, ts):
        self.timer += 1
        # Get/Change Vel
        self.gettingVel(ts)

        # Make vel Changes
        self.rect.x += self.vel[0]
        self.rect.y += self.vel[1]

        self.attackCD -= int(ts/10)
        if self.leftClick:
            if self.attackCD <= 0:
                self.attackCD = 10

    def blit(self, screen):
        currentFrame = int(self.timer / 40)
        if currentFrame >= self.frames[0]:
            currentFrame = 0
            self.timer = 0
        # pygame.draw.rect(screen, (200, 200, 200), self.rect)
        screen.blit(self.img, (self.rect.x, self.rect.y), (currentFrame*self.sizeofFrame[0], 0, self.sizeofFrame[0], self.sizeofFrame[1]))

    def gettingVel(self, ts):
        # limit speed
        topSpeed = int(4 * (ts/10))
        speed = 2.2 * int(ts/10)

        if self.vel[0] > topSpeed:
            self.vel[0] = topSpeed
        elif self.vel[0] < -topSpeed:
            self.vel[0] = -topSpeed
        if self.vel[1] > topSpeed:
            self.vel[1] = topSpeed
        elif self.vel[1] < -topSpeed:
            self.vel[1] = -topSpeed

        # slow down
        if abs(self.vel[0]) > 2:
            if self.vel[0] > 0:
                self.vel[0] -= 1
            else:
                self.vel[0] += 1
        else:
            self.vel[0] = 0
        if abs(self.vel[1]) > 2:
            if self.vel[1] > 0:
                self.vel[1] -= 1
            else:
                self.vel[1] += 1
        else:
            self.vel[1] = 0

        if self.up:
            self.vel[1] -= speed
        if self.down:
            self.vel[1] += speed
        if self.left:
            self.vel[0] -= speed
        if self.right:
            self.vel[0] += speed

    def attack(self, screen):
        leftAngle = self.angle - 30
        if leftAngle < 0:
            leftAngle += 360
        elif leftAngle > 360:
            leftAngle -= 360
        rightAngle = self.angle + 30
        if rightAngle < 0:
            rightAngle += 360
        elif rightAngle > 360:
            rightAngle -= 360
        point1 = math.cos(math.radians(leftAngle)) * 5 + self.rect.centerx, math.sin(math.radians(leftAngle)) * 5 + self.rect.centery
        point2 = math.cos(math.radians(leftAngle)) * 30 + self.rect.centerx, math.sin(math.radians(leftAngle)) * 30 + self.rect.centery
        point3 = math.cos(math.radians(rightAngle)) * 30 + self.rect.centerx, math.sin(math.radians(rightAngle)) * 30 + self.rect.centery
        point4 = math.cos(math.radians(rightAngle)) * 5 + self.rect.centerx, math.sin(math.radians(rightAngle)) * 5 + self.rect.centery

        attackbox = [point1, point2, point3, point4]
        pygame.draw.polygon(screen, (75, 150, 75), attackbox)
