import pygame
import random
import math
random.seed(None)


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

        # Inventory
        self. inv = [Gun("pistol"), Gun("none")]
        self.weaponEquipped = 0

        # Controls
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.leftClick = False
        self.rightClick = False

        self.leftCD = 0
        self.rightCD = 0

    def update(self, ts):
        self.timer += 1
        self.setVelPos(ts)

    def blit(self, screen):
        currentFrame = int(self.timer / 40)
        if currentFrame >= self.frames[0]:
            currentFrame = 0
            self.timer = 0
        # pygame.draw.rect(screen, (200, 200, 200), self.rect)
        screen.blit(self.img, (self.rect.x, self.rect.y), (currentFrame*self.sizeofFrame[0], 0, self.sizeofFrame[0], self.sizeofFrame[1]))

    def setVelPos(self, ts):
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

        self.rect.x += self.vel[0]
        self.rect.y += self.vel[1]

    def melee(self, screen):
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

    def shot(self, shots, gunsounds):
        weapon = self.inv[self.weaponEquipped]
        if weapon.type != "none":
            if weapon.type == "machinegun":
                gunsounds[3].play()
            elif weapon.type != "shotgun":
                gunsounds[random.randint(0, 1)].play()
            else:
                gunsounds[2].play()

            recoilAngle = self.angle + random.randint(-weapon.spread, weapon.spread)
            if weapon.type == "shotgun":
                for i in range(6):
                    recoilAngle = self.angle + random.randint(-weapon.spread, weapon.spread)
                    bullet = Bullet(recoilAngle, self.rect.center, weapon.damage)
                    shots.append(bullet)
            else:
                bullet = Bullet(recoilAngle, self.rect.center, weapon.damage)
                shots.append(bullet)

    def rightAttack(self, ts, cd=10):
        self.rightCD -= int(ts/10) if self.rightCD > 0 else 0
        if self.rightClick and self.rightCD <= 0:
            self.setMouseAngle()
            self.rightCD = cd
            return True
        return False

    def leftAttack(self, ts, cd=10):
        self.leftCD -= int(ts/10) if self.leftCD > 0 else 0
        if self.leftClick and self.leftCD <= 0:
            self.setMouseAngle()
            self.leftCD = cd
            return True
        return False

    def setMouseAngle(self):
        mouse = pygame.mouse.get_pos()
        offset = mouse[0] - self.rect.centerx, mouse[1] - self.rect.centery
        angle = math.degrees(math.atan2(offset[1], offset[0]))
        if angle < 0:
            angle += 360
        self.angle = angle


class Gun:
    def __init__(self, gType="none"):
        self.type = gType
        if gType == "pistol":
            self.maxClip = 8
            self.maxAmmo = 60
            self.attSpeed = 15
            self.reloadSpeed = 25
            self.spread = 1
            self.damage = 2
        elif gType == "smg":
            self.maxClip = 20
            self.maxAmmo = 120
            self.attSpeed = 4
            self.reloadSpeed = 12
            self.spread = 8
            self.damage = 2
        elif gType == "ar":
            self.maxClip = 30
            self.maxAmmo = 150
            self.attSpeed = 10
            self.reloadSpeed = 25
            self.spread = 5
            self.damage = 2
        elif gType == "rifle":
            self.maxClip = 1
            self.maxAmmo = 50
            self.attSpeed = 50
            self.reloadSpeed = 10
            self.spread = 0
            self.damage = 6
        elif gType == "shotgun":
            self.maxClip = 2
            self.maxAmmo = 55
            self.attSpeed = 30
            self.reloadSpeed = 10
            self.spread = 10
            self.damage = 2
        elif gType == "machinegun":
            self.maxClip = 60
            self.maxAmmo = 480
            self.attSpeed = 2
            self.reloadSpeed = 40
            self.spread = 3
            self.damage = 2
        else:
            self.maxClip = 0
            self.maxAmmo = 0
            self.attSpeed = 0
            self.reloadSpeed = 0
            self.spread = 0
            self.damage = 0
        self.clip = self.maxClip
        self.ammo = self.maxAmmo


class Bullet:
    def __init__(self, angle, pos, damage=1):
        self.pos = pos
        self.angle = angle
        self.distance = 100
        self.damage = damage
        self.speed = random.randint(17, 27)

    def getMid(self):
        return int(self.pos[0] + math.cos(math.radians(self.angle)) * 14), int(self.pos[1] + math.sin(math.radians(self.angle)) * 12)

    def getSecondPoint(self):
        return int(self.pos[0] + math.cos(math.radians(self.angle)) * 25), int(self.pos[1] + math.sin(math.radians(self.angle)) * 25)


    def update(self):
        self.pos = int(self.pos[0] + math.cos(math.radians(self.angle)) * self.speed), int(self.pos[1] + math.sin(math.radians(self.angle)) * self.speed)