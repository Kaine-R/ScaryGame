import pygame


class TextBox:
    def __init__(self, msg, pos, font, life=999):
        self.img = font.render(msg, 1, (150, 10, 150))
        self.rect = self.img.get_rect()
        self.rect.x, self.rect.y = pos[0], pos[1]
        self.life = life

    def blit(self, screen):
        screen.blit(self.img, (self.rect.x, self.rect.y))

class Pause:
    def __init__(self):
        font = pygame.font.SysFont("arial", 100)
        self.img = font.render("Pause", 1, (50, 40, 40))

        self.resume = font.render("Resume", 1, (120, 120, 120))
        self.resumeRect = self.resume.get_rect()

        self.mainMenu = font.render("Main Menu", 1, (120, 120, 120))
        self.mainMenuRect = self.mainMenu.get_rect()

    def blit(self, screen):
        screenSize = screen.get_size()
        screen.blit(self.img, (screenSize[0] / 2, screenSize[1] / 2))
        self.resumeRect.x, self.resumeRect.y = screenSize[0] / 2, screenSize[1] / 2 +150
        screen.blit(self.resume, (self.resumeRect.x, self.resumeRect.y))
        self.mainMenuRect.x, self.mainMenuRect.y = screenSize[0] / 2, screenSize[1] / 2 +250
        screen.blit(self.mainMenu, (self.mainMenuRect.x, self.mainMenuRect.y))


class MainMenu:
    def __init__(self):
        font = pygame.font.SysFont("arial", 100)
        sfont = pygame.font.SysFont("arial", 40)
        self.img = font.render("Main Menu", 1, (150, 140, 140))

        self.play = font.render("Play", 1, (120, 120, 120))
        self.playRect = self.play.get_rect()

        self.quit = font.render("Quit", 1, (120, 120, 120))
        self.quitRect = self.quit.get_rect()

        self.title = font.render("\"Game Name\"", 1, (220, 220, 120))

        self.summary = [sfont.render("Controls:", 1, (120, 120, 120)),
                        sfont.render("\"right click\" to shot weapon", 1, (120, 120, 120)),
                        sfont.render("\"wasd\" to move", 1, (120, 120, 120)),
                        sfont.render("\"Tab\" to switch weapons:", 1, (120, 120, 120)),
                        sfont.render("\"Zero (0)\" for fast quit:", 1, (120, 120, 120)),
                        sfont.render("\"e\" to pick up close weapons and medpacks", 1, (120, 120, 120)),
                        sfont.render("\"escape\" to pause", 1, (120, 120, 120)),
                        sfont.render("\"There's no settings, or volume control and it's barely a game", 1, (120, 120, 120)),
                        sfont.render("Try and kill 120 zombies", 1, (250, 250, 40)),
                        sfont.render("Credits:", 1, (120, 120, 120)),
                        sfont.render("Team: Multi-Purpose", 1, (120, 120, 120)),
                        sfont.render("Members: just me (@Kandy Kaine)", 1, (120, 120, 120)),
                        sfont.render("Used Python(pygame)", 1, (120, 120, 120)),
                        sfont.render("Used rfxgen for sounds", 1, (120, 120, 120))]


    def blit(self, screen):
        screenSize = screen.get_size()
        screen.blit(self.img, (screenSize[0] / 2, screenSize[1] / 2))
        self.playRect.x, self.playRect.y = screenSize[0] / 2, screenSize[1] / 2 +150
        screen.blit(self.play, (self.playRect.x, self.playRect.y))
        self.quitRect.x, self.quitRect.y = screenSize[0] / 2, screenSize[1] / 2 +250
        screen.blit(self.quit, (self.quitRect.x, self.quitRect.y))
        screen.blit(self.title, (1250, 200))
        for i, msg in enumerate(self.summary, 0):
            if i >= 9:
                screen.blit(msg, (100, 450 + 40 * i))
            else:
                screen.blit(msg, (100, 50 + 40 * i))


class GameOver:
    def __init__(self):
        font = pygame.font.SysFont("arial", 100)
        self.img = font.render("GAME OVER", 1, (255, 40, 40))

        self.replay = font.render("Replay", 1, (120, 120, 120))
        self.replayRect = self.replay.get_rect()

        self.quit = font.render("Quit", 1, (120, 120, 120))
        self.quitRect = self.quit.get_rect()

    def blit(self, screen):
        screenSize = screen.get_size()
        screen.blit(self.img, (screenSize[0] / 2, screenSize[1] / 2))
        self.replayRect.x, self.replayRect.y = screenSize[0] / 2, screenSize[1] / 2 + 150
        screen.blit(self.replay, (self.replayRect.x, self.replayRect.y))
        self.quitRect.x, self.quitRect.y = screenSize[0] / 2, screenSize[1] / 2 + 250
        screen.blit(self.quit, (self.quitRect.x, self.quitRect.y))


class HUD:
    def __init__(self, screen, font, kc):
        self.screenSize = screen.get_size()
        self.life = 999
        self.backbar = pygame.image.load("images/backbar.png")
        self.HUDGrouping = []
        self.killCount = font.render("Zombies Killed: " + str(kc), 1, (0, 0, 0))

    def getHeight(self):
        size = self.backbar.get_rect()
        return size.height

    def update(self, font, kc):
        self.killCount = font.render("Zombies Killed: " + str(kc), 1, (0, 0, 0))

    def blit(self, screen):
        screenSize = screen.get_size()
        size = self.backbar.get_size()
        screen.blit(self.backbar, (0, int(self.screenSize[1] - size[1])))
        screen.blit(self.killCount, (screenSize[0] / 2 - 40, screenSize[1] - 70))
        for text in self.HUDGrouping:
            text.blit(screen)
