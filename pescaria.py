import pygame
import math
import random
from sys import exit

# Pygame:
pygame.init()
screen = pygame.display.set_mode((1000,625))
pygame.display.set_caption('Pesca')
clock = pygame.time.Clock()

# Player:
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
        # A lista tem repetidos para certos frames terem velocidades diferentes
        self.playerAnimacao = [
            canoa1, canoa1, 
            canoa2, 
            canoa3, canoa3, canoa3, canoa3, 
            canoa4, 
            canoa5, canoa5, 
            canoa6, 
            canoa7, canoa7, canoa7, canoa7, 
            canoa8]
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
        self.playerIndex += 0.3
        if self.playerIndex > len(self.playerAnimacao):
            self.playerIndex = 0
        self.imageOriginal = self.playerAnimacao[int(self.playerIndex)]
        self.image = pygame.transform.rotate(self.imageOriginal, -(self.anguloHistorico[-1]))
        self.rect = self.image.get_rect(center = self.rect.center)

    def mover(self):
        global moverx
        global xPlayer
        global movery
        global yPlayer
        global movendo
        global rotacionar
        xPlayer = self.rect.centerx
        yPlayer = self.rect.centery
        movendo = True
        rotacionar = False
        self.rect.centerx = self.rect.centerx - moverx
        self.rect.centery = self.rect.centery - movery
        if self.rect.centerx == xPlayer and self.rect.centery == yPlayer:
            movendo = False
            rotacionar = True

    def gerar_particulas(self, particulas):
        for _ in range(2):
            particulas.add(Particula(self.rect.center))


    def update(self):
        if cursor_x >= 134 and cursor_y >= 80 and rotacionar is True:
            self.rotacionar()
        self.mover()
        if movendo:
            self.animacao()
            player.sprite.gerar_particulas(particulas)

player = pygame.sprite.GroupSingle()
moverx = 0
movery = 0
movendo = False
velocidade = 3
player.add(Player())
rotacionar = True

# Particulas
class Particula(pygame.sprite.Sprite):
    def __init__(self, posicaoMaxima):
        super().__init__()
        self.image = pygame.Surface((3, 2), pygame.SRCALPHA) # SRCALPHA significa que os pixels terão um canal alpha(transparência)
        pygame.draw.circle(self.image, (143, 211, 255), (2, 2), 3) # cor, centro, raio
        self.rect = self.image.get_rect(center = posicaoMaxima)
        self.moverX = random.uniform(-1, 3) # uniform é quando aceita float
        self.moverY = random.uniform(1, 3)
        self.timer = 30

    def update(self):
        self.rect.x += self.moverX
        self.rect.y += self.moverY
        self.timer -= 1
        opacidade = self.timer / 40
        self.image.set_alpha(abs(int(255 * opacidade)))
        if self.timer <= 0:
            self.kill()

particulas = pygame.sprite.Group()

# Background:
background = pygame.image.load('graficos/background.png').convert()

# Gatosário:
gatosario = pygame.image.load('graficos/gatosario.png').convert()
fonte = pygame.font.Font('graficos/pixel-operator.ttf', 18)
fonte2 = pygame.font.Font('graficos/pixeltype.ttf', 18)
fonte3 = pygame.font.Font('graficos/monobit.ttf', 18)
fonte4 = pygame.font.Font('graficos/Jersey10-Regular.ttf', 18)

dialogo1 = 'Parabénnnsss!!!Você está a um passo de ser o novo CEO da Phising good & cheap Enterprise©!'
dialogo2 = 'Começaremos nossas operações em Gatuma,uma pequena cidade pesqueira entre a Miasília e Peixótina.Uma oportunidade perfeita para subir na sua carreira!'
dialogo3 = 'Hoje é 9 de Janeiro,ou seja,ainda estamos no período de defeso!!'
dialogo4 = 'Essa é época onde os pescadores locais tiram férias, e os preços dos peixes aumenta!'
dialogo5 = 'Nossa meta é arrecadar 200 mil peixes até o fim do período.'
dialogo6 = 'Controle as operações e mostre teu espirito felino!'
dialogo7 = 'Ah, só tem um detalhezinho...'
dialogo8 = 'Talvez estejamos sem verba,por alguns "probleminhas" legais.'
dialogo9 = 'Mas não se preocupe!Como sou grande,magnífico,inteligente,proativo e resiliente,chamei meu sobrinho pra cuidar disso!'
dialogo10 = 'Tem uma canoa ali,você pode usa-la para pagar as operações!'
dialogo11 = 'Boa-sorte-você-consegue-e-tudo-mais-tchau!'
dialogo = 'Null'

texto = []
fala = 1
posicaoMaxima = 0
posicao = 0
separacao = 0
avancar = False

def escrever():
        global separacao
        for i in range(posicao):
            if dialogo[i] in ['c', 'n', 's', 'd']:
                separacao -= 1
                screen.blit(texto[i], ((220 + (separacao)), 15))
            elif dialogo[i - 1] in ['j', 'l']:
                separacao -= 4
                screen.blit(texto[i], ((220 + (separacao)), 15))
            elif dialogo[i - 1] in ['m']:
                separacao += 3
                screen.blit(texto[i], ((220 + (separacao)), 15))
            else:
                screen.blit(texto[i], ((220 + (separacao)), 15))
            separacao += 9
        separacao = 0

# Eventos pygame:
def processarEventos():
    global click_x, click_y
    global rotacionar
    global moverx, movery
    global fala
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if fala % 1 != 0:
                fala -= 0.1
            print(fala)
            click_x, click_y = pygame.mouse.get_pos()
            if cursor_x >= 134 and cursor_y >= 80:
                rotacionar = True
                if event.button == 1:
                    if xPlayer < click_x:
                        moverx = -velocidade
                    if xPlayer > click_x:
                        moverx = velocidade
                    if yPlayer < click_y:
                        movery = -velocidade
                    if yPlayer > click_y:
                        movery = velocidade
                elif event.button == 3:
                    print("Botão direito!")

while True:
    processarEventos()

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

    # Updates:
    player.update()
    particulas.update()


    screen.blit(background, (0,0))
    screen.blit(gatosario, (153, 8))

    if fala == 1:
        dialogo = dialogo1

        if posicaoMaxima <= len(dialogo):
            posicaoMaxima += 1
        
        if posicao <= posicaoMaxima:
            texto_surface = fonte4.render(dialogo[posicao], False, (250, 253, 255))
            texto.append(texto_surface)
            print(dialogo[posicao])
        posicao += 1
        if posicao == len(dialogo):
            fala = 2.1
            transicao = True

    if fala == 2:
        if transicao is True:
            posicaoMaxima = 0
            posicao = 0
            separacao = 0
            texto = []
            transicao = False

        dialogo = dialogo2

        if posicaoMaxima <= len(dialogo):
            posicaoMaxima += 1
        
        if posicao <= posicaoMaxima:
            texto_surface = fonte4.render(dialogo[posicao], False, (250, 253, 255))
            texto.append(texto_surface)
            print(dialogo[posicao])
        posicao += 1
        if posicao == len(dialogo):
            fala = 3
    
    escrever()



    particulas.draw(screen)
    player.draw(screen)
    pygame.display.update()
    clock.tick(60)