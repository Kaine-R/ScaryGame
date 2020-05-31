import pygame
import GameFunctions as gf
import MapGen
from Font import TextBox, HUD
from Settings import Settings
from Player import Player
from Enemy import Enemy
from Block import Block

# from Bullet import Bullet

# REMOVE escape close program feature
colors = {
    "RED": (200, 100, 100),
    "YELLOW": (175, 175, 70),
    "GREEN": (100, 200, 100),
    "LBLUE": (70, 175, 175),
    "BLUE": (100, 100, 200),
    "PURPLE": (175, 70, 175),
    "WHITE": (220, 220, 220),
    "GRAY": (150, 150, 150),
    "BLACK": (50, 50, 50)}

settings = Settings()


def main():
    # Pygame init()---------------
    pygame.init()
    pygame.mixer.init(44100, -16, 2, 2048)
    pygame.mixer.set_num_channels(12)
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((1600, 900))
    pygame.display.set_caption("Scary Game")

    # Main Vars ---------------
    pause = False
    player = Player()
    titleFont = pygame.font.SysFont("arial", 50)
    smallFont = pygame.font.SysFont("arial", 15)
    gunSound = pygame.mixer.Sound("sounds/gunsound1.wav"), \
               pygame.mixer.Sound("sounds/gunsound2.wav"), \
               pygame.mixer.Sound("sounds/shotgunsound.wav"), \
               pygame.mixer.Sound("sounds/machinegunsound.wav")
    gunSound[0].set_volume(settings.gunShotVolume)
    gunSound[1].set_volume(settings.gunShotVolume)
    gunSound[2].set_volume(settings.gunShotVolume)
    gunSound[3].set_volume(settings.gunShotVolume)

    enemy = Enemy()
    enemy.rect.x, enemy.rect.y = 200, 300
    removeList = []
    enemies = [enemy]
    shots = []
    hud = HUD(screen)
    textBoxes = [hud]
    particles = []
    # text = [1, 2] ----delete maybe
    gameMap = []
    MapGen.generateMap(gameMap)

    # FPS STUFF CAN BE REMOVEDs
    avgFPS = []
    count = 0
    txt = TextBox(titleFont, "hello", (600, 500))
    textBoxes.append(txt)

    while not pause:
        tickSpeed = clock.tick(80)

        count += 1
        if count > 160:
            count = 0
            gf.getAvgFPS(clock.get_fps(), avgFPS)
        # print(tickSpeed)

        gf.updateEvents(player)

        # screen = pygame.display.set_mode((1920, 1080))
        # Update and Blit Map ---------------------------------------------------------------------
        for block in gameMap:
            block.update()
            if block.type == "wall":
                gf.checkCollision(player, block)
            block.blit(screen)

        # Player Update and mouse clicks ------------------------------------------------------------
        player.update(tickSpeed)
        player.melee(screen)
        if player.rightAttack(tickSpeed, player.inv[player.weaponEquipped].attSpeed):
            player.shot(shots, gunSound)
        player.leftAttack(tickSpeed)

        # Bullet update and blit --------------------------------------------------------------------
        for i, bullet in enumerate(shots, 0):
            if bullet.distance > 0:
                bullet.distance -= int(tickSpeed / 10 + bullet.speed / 10)
                bullet.update()
                pygame.draw.line(screen, colors["YELLOW"], bullet.pos, bullet.getSecondPoint(), 2)
            else:
                removeList.append(i)
        gf.cleanList(removeList, shots)

        # Enemy Update and Blit ---------------------------------------------------------------------
        for i, enemy in enumerate(enemies, 0):
            for j, bullet in enumerate(shots, 0):
                if gf.getDistance(bullet.getMid(), enemy.rect.center) < 20:
                    point2 = bullet.getSecondPoint()
                    if pygame.Rect.collidepoint(enemy.rect, bullet.pos[0], bullet.pos[1]) or pygame.Rect.collidepoint(enemy.rect, point2[0], point2[1]):
                        enemy.hp -= bullet.damage
                        print("enemy hit! Current HP is : {}".format(enemy.hp))
                        removeList.append(j)
            gf.cleanList(removeList, shots)

            if enemy.hp > 0:
                enemy.update(player)
                enemy.blit(screen)
            else:
                removeList.append(i)
        gf.cleanList(removeList, enemies)

        # Player Blit -----------------------------------------------------------------------------
        player.blit(screen)

        # Text updates and Blit ---------------------------------------------------------------------
        for i, text in enumerate(textBoxes, 0):
            if text.life != 999:
                text.life -= int(tickSpeed/10)
            if text.life < 0:
                removeList.append(i)
            else:
                text.blit(screen)
        gf.cleanList(removeList, textBoxes)

        pygame.display.flip()
        screen.fill(colors["BLACK"])


print("Program Start.")
main()
