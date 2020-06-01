import pygame
import random
import GameFunctions as gf
import MapGen
from Font import TextBox, GameOver, Pause, MainMenu, HUD
from Settings import Settings
from Player import Player
from Enemy import Enemy
from Pickup import Pickup
from Blood import Blood

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
    # Pygame init()-----------------------------------
    pygame.init()
    pygame.mixer.init(44100, -16, 2, 2048)
    pygame.mixer.set_num_channels(12)
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
    pygame.display.set_caption("Scary Game")
    titleFont = pygame.font.SysFont("arial", 50)
    smallFont = pygame.font.SysFont("arial", 15)

    # Main Vars --------------------------------------
    mainMenu = [True]
    gameover = [False]
    pause = [False]
    player = Player()
    hud = HUD(screen, titleFont, 0)
    offSet = [0, 0, 0, 0]
    music = pygame.mixer.music.load("sounds/music.wav")
    pygame.mixer.music.set_volume(.4)
    pygame.mixer.music.play(-1)
    gunSound = pygame.mixer.Sound("sounds/gunsound1.wav"), \
               pygame.mixer.Sound("sounds/gunsound2.wav"), \
               pygame.mixer.Sound("sounds/shotgunsound.wav"), \
               pygame.mixer.Sound("sounds/machinegunsound.wav")
    hurt = pygame.mixer.Sound("sounds/collide.wav")
    hit = pygame.mixer.Sound("sounds/hit1.wav"), pygame.mixer.Sound("sounds/hit2.wav")
    hit[0].set_volume(.5)
    hit[1].set_volume(.5)
    gunSound[0].set_volume(settings.gunShotVolume)
    gunSound[1].set_volume(settings.gunShotVolume)
    gunSound[2].set_volume(settings.gunShotVolume)
    gunSound[3].set_volume(settings.gunShotVolume)

    # lists and gamespace ------------------------------

    gameoverScreen = GameOver()
    pauseScreen = Pause()
    mainMenuScreen = MainMenu()
    removeList = []
    enemies = []
    shots = []
    textBoxes = [hud]
    particles = []
    walls = []
    MapGen.generateWalls(walls)
    pickups = [
        Pickup((100, 600), "smg"),
        Pickup((1800, 400), "shotgun")]
    gameMap = []
    zombiesKilled = 0
    mapSize = MapGen.generateMap(gameMap)
    gameSpace = (1920, 1080 - hud.getHeight())
    timer = -20
    totalTimer = 115

    # FPS STUFF CAN BE REMOVEDs
    avgFPS = []
    count = 0
    while True:
        if mainMenu[0]:
            pause[0] = False
            gameover[0] = False
            gf.mainMenu(mainMenuScreen, mainMenu)
            mainMenuScreen.blit(screen)
            pygame.display.flip()
            screen.fill(colors["BLACK"])
        elif pause[0]:
            mainMenu[0] = False
            gameover[0] = False
            choice = gf.pauseMenu(pauseScreen, pause)
            if choice == 2:
                mainMenu[0] = [True]
                gameover[0] = [False]
                pause[0] = [False]
                mapSize = MapGen.generateMap(gameMap)
                offSet = [0, 0, 0, 0]
                player.resetAll()
                removeList.clear()
                enemies.clear()
                shots.clear()
                particles.clear()
                walls.clear()
                MapGen.generateWalls(walls)
                pickups = [
                    Pickup((100, 600), "smg"),
                    Pickup((1800, 400), "shotgun")]
                zombiesKilled = 0
                timer = -20
                totalTimer = 130
            pauseScreen.blit(screen)
            pygame.display.flip()
            screen.fill(colors["BLACK"])
        elif gameover[0]:
            mainMenu[0] = False
            pause[0] = False
            choice = gf.gameOver(gameoverScreen)
            if choice == 1:
                mainMenu[0] = [False]
                gameover[0] = [False]
                pause[0] = [False]
                mapSize = MapGen.generateMap(gameMap)
                offSet = [0, 0, 0, 0]
                player.resetAll()
                removeList.clear()
                enemies.clear()
                shots.clear()
                particles.clear()
                walls.clear()
                MapGen.generateWalls(walls)
                pickups = [
                    Pickup((100, 600), "smg"),
                    Pickup((1800, 400), "shotgun")]
                zombiesKilled = 0
                timer = -20
                totalTimer = 130
            gameoverScreen.blit(screen)
            pygame.display.flip()
            screen.fill(colors["BLACK"])
        else:
            timer += 1
            tickSpeed = clock.tick(80)

            count += 1
            if count > 160:
                count = 0
                gf.getAvgFPS(clock.get_fps(), avgFPS)
            # print(tickSpeed)

            gf.updateEvents(player, pickups, pause)
            gf.checkCollision(player, walls)
            gf.getMapOffset(player, offSet, gameSpace, mapSize)
            gf.setMapOffset(player, enemies, offSet, gameMap, pickups, walls, particles)

            for particle in particles:
                particle.blit(screen)

            # Update and Blit Map ---------------------------------------------------------------------
            for block in gameMap:
                if block.type == "wall":
                    gf.checkCollision(player, block)
                block.blit(screen)

            if MapGen.spawningEnemies(timer, totalTimer, enemies):
                timer = 0

            for i, enemy in enumerate(enemies, 0):
                if pygame.Rect.colliderect(enemy.rect, player):
                    hurt.play()
                    player.hp -= 1
                    enemies.pop(i)

            # Player Update and mouse clicks ------------------------------------------------------------
            player.update(tickSpeed)
            # player.melee(screen)
            if player.rightAttack(tickSpeed, player.inv[player.weaponEquipped].attSpeed):
                if player.inv[player.weaponEquipped].ammo > 0:
                    player.inv[player.weaponEquipped].ammo -= 1
                    player.shot(shots, gunSound)
                else:
                    player.createPistol()
            player.leftAttack(tickSpeed)

            # pickup blit ----------------------------------
            for item in pickups:
                item.blit(screen)

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
                            hit[random.randint(0, 1)].play()
                            enemy.hp -= bullet.damage
                            shots.pop(j)
                            break

                if enemy.hp > 0:
                    enemy.update(player, tickSpeed)
                    enemy.blit(screen, player)
                else:
                    zombiesKilled += 1
                    if random.randint(1, 50) <= 2:
                        item = Pickup(enemy.rect.center, gf.getRandomDrop(random.randint(0, 5)))
                        pickups.append(item)
                    removeList.append(i)
            gf.cleanList(removeList, enemies)

            # Player Blit -----------------------------------------------------------------------------
            player.resetMovement()
            player.blit(screen)

            # Text updates and Blit ---------------------------------------------------------------------
            hud.update(titleFont, zombiesKilled)
            for i, text in enumerate(textBoxes, 0):
                if text.life != 999:
                    text.life -= int(tickSpeed/10)
                if text.life < 0:
                    removeList.append(i)
                else:
                    text.blit(screen)
            gf.cleanList(removeList, textBoxes)

            gf.drawInv(screen, player)
            gf.drawHP(screen, player)

            # ------------------------------------delete-------------------------------------------------------------------------------
            # for wall in walls:
            #     wall.blit(screen)

            if player.hp <= 0:
                gameover[0] = True

            pygame.display.flip()
            screen.fill(colors["BLACK"])


print("Program Start.")
main()
