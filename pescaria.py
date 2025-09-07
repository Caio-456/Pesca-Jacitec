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
        index = 0
        playerAnimacao = [canoa1, canoa2, canoa3, canoa4, canoa5, canoa6, canoa7, canoa8]
        self.imageOriginal = playerAnimacao[index]        
        self.image = self.imageOriginal
        self.anguloHistorico = [0,0,0,0,0,0,0,0,0,0]
        self.rect = self.image.get_rect(center = (500,150))
        self.rodando = True
        self.i = 0

    def rotacionar(self):
        cursor_x, cursor_y = pygame.mouse.get_pos()
        anguloRAD = math.atan2(self.rect.centery - cursor_y, self.rect.centerx - cursor_x)
        angulo = (int(math.degrees(anguloRAD)) - 90)
        self.anguloHistorico.append(angulo)
        if len(self.anguloHistorico) > 10:
            self.anguloHistorico.pop(0)

        if abs((self.anguloHistorico[-1] - self.anguloHistorico[-8])) > 5:
            #print(self.anguloHistorico)
            #print(angulo)
            self.image = pygame.transform.rotate(self.imageOriginal, -angulo)
            self.rect = self.image.get_rect(center = self.rect.center)
            
    def update(self):
        self.rotacionar()

# Player:
player = pygame.sprite.GroupSingle()
player.add(Player())

# Background:
background = pygame.image.load('graficos/background.png').convert()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    player.update()
    screen.blit(background, (0,0))
    player.draw(screen)

    pygame.display.flip()
    pygame.display.update()
    clock.tick(60)