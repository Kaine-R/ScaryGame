import pygame
import random
import math
from Font import TextBox
random.seed(None)


class Player:
    def __init__(self):
        self.img = [pygame.image.load("images/player1.png").convert(),
                    pygame.image.load("images/player2.png").convert(),
                    pygame.image.load("images/player3.png").convert()]
        self.img[0].set_colorkey((255, 255, 255))
        self.img[1].set_colorkey((255, 255, 255))
        self.img[2].set_colorkey((255, 255, 255))
        self.rect = pygame.Rect((960, 490), self.img[0].get_size())
        self.frames = 3

        # Stats
        self.vel = [0, 0]
        self.angle = 0
        self.hp = 3
        self.timer = 0
        self.hpImg = pygame.image.load("images/hpBar.png").convert()
        self.hpImg.set_colorkey((255, 255, 255))
        self.ehpImg = pygame.image.load("images/ehpBar.png").convert()
        self.hpImg.set_colorkey((255, 255, 255))


        # Inventory
        self. inv = [Gun("pistol"), Gun("smg")]
        self.weaponEquipped = 0

        # Controls
        self.action = Action()
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.leftClick = False
        self.rightClick = False

        self.stopLeft = False
        self.stopRight= False
        self.stopUp = False
        self.stopDown = False

        self.leftCD = 0
        self.rightCD = 0

    def resetAll(self):
        self.rect.x, self.rect.y = (960, 490)
        self.vel = [0, 0]
        self.angle = 0
        self.hp = 3
        self.timer = 0

        # Inventory
        self. inv = [Gun("pistol"), Gun("smg")]
        self.weaponEquipped = 0

        # Controls
        self.action = Action()
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.leftClick = False
        self.rightClick = False

        self.stopLeft = False
        self.stopRight = False
        self.stopUp = False
        self.stopDown = False

        self.leftCD = 0
        self.rightCD = 0

    def update(self, ts):
        self.timer += 1
        self.setVelPos(ts)

    def resetMovement(self):
        self.stopLeft = False
        self.stopRight = False
        self.stopUp = False
        self.stopDown = False

    def blit(self, screen):
        currentFrame = int(self.timer / 40)
        if currentFrame >= self.frames:
            currentFrame = 0
            self.timer = 0
        # pygame.draw.rect(screen, (200, 200, 200), self.rect)
        screen.blit(pygame.transform.rotate(self.img[currentFrame], -self.angle), (self.rect.x, self.rect.y))

    def resetAction(self):
        self.action.type = "none"
        self.action.index = -1

    def setVelPos(self, ts):
        # limit speed
        topSpeed = int(4 * (ts/10))
        speed = 2.2 * int(ts/10)

        if self.stopLeft:
            self.rect.x += 2
            self.vel[0] = 3 * int(ts/10)
        if self.stopRight:
            self.rect.x -= 2
            self.vel[0] = -3 * int(ts/10)
        if self.stopUp:
            self.rect.y += 2
            self.vel[1] = 3 * int(ts/10)
        if self.stopDown:
            self.rect.y -= 2
            self.vel[1] = -3 * int(ts/10)

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
            elif weapon.type != "shotgun" and weapon.type != "rifle":
                gunsounds[random.randint(0, 1)].play()
            else:
                gunsounds[2].play()

            recoilAngle = self.angle + random.randint(-weapon.spread, weapon.spread)
            if weapon.type == "shotgun":
                for i in range(8):
                    recoilAngle = self.angle + random.randint(-weapon.spread, weapon.spread)
                    bullet = Bullet(recoilAngle, self.rect.center, weapon.damage)
                    bullet.distance = weapon.distance
                    shots.append(bullet)
            else:
                bullet = Bullet(recoilAngle, self.rect.center, weapon.damage)
                bullet.distance = weapon.distance
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

    def grabbingItem(self, item):
        if item.type == "health":
            self.hp = 3
        elif item.type == "none":
            print("Error, picked up none.")
        else:
            self.inv[self.weaponEquipped] = Gun(item.type)

    def createPistol(self):
        self.inv[self.weaponEquipped] = Gun("pistol")

class Action:
    def __init__(self):
        self.type = "none"
        self.index = -1

class Gun:
    def __init__(self, gType="none"):
        self.type = gType
        if gType == "pistol":
            self.img = pygame.image.load("images/pistol.png").convert()
            self.maxAmmo = 666
            self.attSpeed = 12
            self.spread = 1
            self.damage = 2
            self.distance = 80
        elif gType == "smg":
            self.img = pygame.image.load("images/smg.png").convert()
            self.maxAmmo = 120
            self.attSpeed = 3
            self.spread = 8
            self.damage = 2
            self.distance = 100
        elif gType == "ar":
            self.img = pygame.image.load("images/ar.png").convert()
            self.maxAmmo = 150
            self.attSpeed = 7
            self.spread = 5
            self.damage = 2
            self.distance = 170
        elif gType == "rifle":
            self.img = pygame.image.load("images/rifle.png").convert()
            self.maxAmmo = 50
            self.attSpeed = 30
            self.spread = 0
            self.damage = 6
            self.distance = 300
        elif gType == "shotgun":
            self.img = pygame.image.load("images/shotgun.png").convert()
            self.maxAmmo = 66
            self.attSpeed = 30
            self.spread = 8
            self.damage = 2
            self.distance = 50
        elif gType == "machinegun":
            self.img = pygame.image.load("images/machinegun.png").convert()
            self.maxAmmo = 220
            self.attSpeed = 2
            self.spread = 3
            self.damage = 2
            self.distance = 140
        else:
            self.img = pygame.image.load("images/default.png").convert()
            self.maxAmmo = 0
            self.attSpeed = 0
            self.spread = 0
            self.distance = 0
            self.damage = 0
        self.font = pygame.font.SysFont("arial", 15)
        self.name = self.font.render(gType.upper(), 1, (0, 0, 0))
        self.rect = self.img.get_rect()
        self.ammo = self.maxAmmo
        self.ammoText = self.font.render(str(self.ammo) + " / " + str(self.maxAmmo), 1, (0, 0, 0))
        self.ammoRect = self.ammoText.get_rect()

    def update(self):
        self.ammoText = self.font.render(str(self.ammo) + " / " + str(self.maxAmmo), 1, (0, 0, 0))

    def blit(self, screen, selected=False):
        pygame.draw.rect(screen, (250, 250, 250), self.rect)
        screen.blit(self.img, self.rect)
        screen.blit(self.name, self.rect)
        screen.blit(self.ammoText, self.ammoRect)
        if selected:
            pygame.draw.rect(screen, (200, 30, 200), self.rect, 3)



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