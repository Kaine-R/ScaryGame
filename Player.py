import pygame


class Player:
    def __init__(self):
        self.img = pygame.image.load("images/playerSheet.png")
        self.rect = self.img.get_rect()
        self.frames = 4
        self.sizeofFrame = self.rect.width / self.frames
        self.vel = [0, 0]

        self.timer = 0

        # Controls
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.leftClick = False
        self.rightClick = False

        self.attackTimer = 0


    def update(self, ts):
        self.timer += 1
        # Get/Change Vel
        self.gettingVel(ts)

        # Make vel Changes
        self.rect.x += self.vel[0]
        self.rect.y += self.vel[1]

        if self.leftClick:
            if self.attackTimer <= 0

    def blit(self, screen):
        currentFrame = int(self.timer / 40)
        if currentFrame >= self.frames:
            currentFrame = 0
            self.timer = 0
        screen.blit(self.img, (self.rect.x, self.rect.y), (currentFrame*self.sizeofFrame, 0, self.sizeofFrame, self.rect.height))

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
