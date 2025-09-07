import pygame
import math
from sys import exit

# Pygame:
pygame.init()
screen = pygame.display.set_mode((1000,625))
pygame.display.set_caption('Pesca')
clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        canoa1 = pygame.image.load('graficos/canoa/canoa1.png').convert_alpha()
        canoa2 = pygame.image.load('graficos/canoa/canoa2.png').convert_alpha()
        canoa3 = pygame.image.load('graficos/canoa/canoa3.png').convert_alpha()
        canoa4 = pygame.image.load('graficos/canoa/canoa4.png').convert_alpha()
        canoa5 = pygame.image.load('graficos/canoa/canoa5.png').convert_alpha()
        canoa6 = pygame.image.load('graficos/canoa/canoa6.png').convert_alpha()
        canoa7 = pygame.image.load('graficos/canoa/canoa7.png').convert_alpha()
        canoa8 = pygame.image.load('graficos/canoa/canoa8.png').convert_alpha()
        self.playerIndex = 0
        self.playerAnimacao = [canoa1, canoa2, canoa3, canoa4, canoa5, canoa6, canoa7, canoa8]
        self.imageOriginal = self.playerAnimacao[self.playerIndex]        
        self.image = self.imageOriginal
        self.anguloHistorico = [0,0,0,0,0,0,0,0,0,0]
        self.rect = self.image.get_rect(center = (500,150))

    def rotacionar(self):
        anguloRAD = math.atan2(self.rect.centery - cursor_y, self.rect.centerx - cursor_x)
        angulo = (int(math.degrees(anguloRAD)) - 90)
        self.anguloHistorico.append(angulo)
        if len(self.anguloHistorico) > 10:
            self.anguloHistorico.pop(0)
        if abs((self.anguloHistorico[-1] - self.anguloHistorico[-8])) > 5:
            self.image = pygame.transform.rotate(self.imageOriginal, -angulo)
            self.rect = self.image.get_rect(center = self.rect.center)

    def animacao(self):
        if movendo is True:
            self.playerIndex += 0.5
            if self.playerIndex > 7:
                self.playerIndex = 0
            print(self.playerIndex)
            self.imageOriginal = self.playerAnimacao[int(self.playerIndex)]

    def mover(self):
        global moverx
        global xPlayer
        global movery
        global yPlayer
        xPlayer = self.rect.centerx
        yPlayer = self.rect.centery
        self.rect.centerx = self.rect.centerx - moverx
        self.rect.centery = self.rect.centery - movery
        
    def update(self):
        if cursor_x >= 134 and cursor_y >= 80:
            self.rotacionar()
        self.mover()
        if moverx != 0 and movery != 0:
            self.animacao()

# Player:
player = pygame.sprite.GroupSingle()
moverx = 0
movery = 0
movendo = False
velocidade = 2
player.add(Player())

# Background:
background = pygame.image.load('graficos/background.png').convert()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_x, click_y = pygame.mouse.get_pos()
                if cursor_x >= 134 and cursor_y >= 80:
                    if event.button == 1:
                        print("Left click detected!")
                        movendo = True
                        if xPlayer < click_x:
                            moverx = -velocidade
                        if xPlayer > click_x:
                            moverx = velocidade
                        if yPlayer < click_y:
                            movery = -velocidade
                        if yPlayer > click_y:
                            movery = velocidade
                    elif event.button == 3:
                        print("Right click detected!")
                    print(click_x, click_y)

    cursor_x, cursor_y = pygame.mouse.get_pos()
    if cursor_x < 134 or cursor_y < 80:
        pygame.mouse.set_cursor(*pygame.cursors.arrow)
    else:
        pygame.mouse.set_cursor(*pygame.cursors.broken_x)

    if movendo:
        if abs(xPlayer - click_x) < 10:
            moverx = 0 
        if abs(yPlayer - click_y) < 10:
            movery = 0 

    player.update()
    screen.blit(background, (0,0))
    player.draw(screen)

    pygame.display.flip()
    pygame.display.update()
    clock.tick(60)