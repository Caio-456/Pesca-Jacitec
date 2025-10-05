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

        frames = [ pygame.image.load(f"graficos/canoa/canoa{i}.png").convert_alpha() for i in range(1, 9) ]

        self.playerIndex = 0
        # A lista tem repetidos para certos frames terem velocidades diferentes
        self.playerAnimacao = [
            frames[0], frames[0], 
            frames[1], 
            frames[2], frames[2], frames[2], frames[2], 
            frames[3], 
            frames[4], frames[4], 
            frames[5], 
            frames[6], frames[6], frames[6], frames[6], 
            frames[7]]
        
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
        if travar is False:
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
rotacionar = False
travar = True

# Peixes:
class Peixe(pygame.sprite.Sprite):
    global confPeixes
    global peixesPortes

    def __init__(self, tamanho):
        super().__init__()
        self.tamanho = tamanho
        for configuracoes in confPeixes:
            if tamanho in configuracoes["tamanhos"]:
                self.image = peixesPortes[configuracoes["sprite"]]
                self.imagemSemRotacao = self.image
                self.velocidadeBase = configuracoes["velocidade"]

        self.velocidade = self.novaVelocidade()
        self.xpos = random.randrange(134, 1000)
        self.ypos = random.randrange(80 + ((self.tamanho * 3)), 625)
        self.rect = self.image.get_rect(center = (500, 900))

    def novaVelocidade(self):
        return random.uniform(self.velocidadeBase * 0.5, self.velocidadeBase * 1.2) # Uniform também arredonda para inteiro.
    
    def rotacionar(self):
        anguloRAD = math.atan2(self.rect.centery - self.ypos, self.rect.centerx - self.xpos)
        angulo = (int(math.degrees(anguloRAD)) - 90)
        self.image = pygame.transform.rotate(self.imagemSemRotacao, -angulo)
        self.rect = self.image.get_rect(center = self.rect.center)

    def movimento(self):
        if self.rect.x < self.xpos:
            self.rect.x += self.velocidade
        if self.rect.x > self.xpos:
            self.rect.x -= self.velocidade
        if self.rect.y < self.ypos:
            self.rect.y += self.velocidade
        if self.rect.y > self.ypos:
            self.rect.y -= self.velocidade
            
        if abs(self.rect.y - self.ypos) < 10 and abs(self.rect.x - self.xpos) < 10:
            self.velocidade = self.novaVelocidade()
            self.xpos = random.randrange(134, 1000)
            self.ypos = random.randrange(80 + ((self.tamanho * 3)), 625)


    def update(self):
        self.movimento()
        self.rotacionar()

peixes = pygame.sprite.Group()

peixesPortes = {
    1: pygame.image.load("graficos/peixes/peixe1.png").convert_alpha(),
    2: pygame.image.load("graficos/peixes/peixe2.png").convert_alpha(),
    3: pygame.image.load("graficos/peixes/peixe3.png").convert_alpha(),
    4: pygame.image.load("graficos/peixes/peixe4.png").convert_alpha(),
    5: pygame.image.load("graficos/peixes/peixe5.png").convert_alpha(),
}

confPeixes = [
    {"sprite": 1, "velocidade": 1, "tamanhos": range(1, 10)},
    {"sprite": 2, "velocidade": 2, "tamanhos": range(10, 17)},
    {"sprite": 3, "velocidade": 3, "tamanhos": range(16, 22)},
    {"sprite": 4, "velocidade": 4, "tamanhos": range(22, 27)},
    {"sprite": 5, "velocidade": 4, "tamanhos": [27]},
]


# Particulas
class Particula(pygame.sprite.Sprite):
    def __init__(self, posicao):
        super().__init__()
        self.image = pygame.Surface((3, 2), pygame.SRCALPHA) # SRCALPHA significa que os pixels terão um canal alpha(transparência)
        pygame.draw.circle(self.image, (143, 211, 255), (2, 2), 3) # cor, centro, raio
        self.rect = self.image.get_rect(center = posicao)
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

# Diálogo:
class Dialogo:
    def __init__(self):
        global transicao
        global fala
        self.texto = []
        self.posicaoMaxima = 0
        self.posicao = 0
        self.separacao = 0
        self.avancar = False

    def ateOndeEscrever(self, dialogo, proxFala):
        global transicao
        global fala

        if transicao is True:
            self.posicaoMaxima = 0
            self.posicao = 0
            self.separacao = 0
            self.texto = []
            transicao = False

        
        if self.posicaoMaxima <= len(dialogo):
            self.posicaoMaxima += 1
        
        if self.posicao <= self.posicaoMaxima:
            texto_surface = fonte.render(dialogo[self.posicao], False, (250, 253, 255))
            self.texto.append(texto_surface)

        self.posicao += 1
        if self.posicao == len(dialogo):
            fala = proxFala + 0.1

    def escrever(self):
        for i in range(self.posicao):
            if i < 75:
                screen.blit(self.texto[i], ((220 + (self.separacao)), 15))
            else:
                screen.blit(self.texto[i], ((220 + (self.separacao) - 675), 30))
            self.separacao += 9
        self.separacao = 0
    
fonte = pygame.font.Font('graficos/DeterminationMono.ttf', 18)
transicao = False
fala = 1
dialogoSistema = Dialogo()
dialogo1 = 'Parabénnnsss!!!Você está a um passo de ser o novo CEO da Phising good & cheap Enterprise©!'
dialogo2 = 'Começaremos nossas operações em Gatuma,uma pequena cidade pesqueira entre aMiasília e Peixótina.Uma oportunidade perfeita para subir na sua carreira!'
dialogo3 = 'Hoje é 9 de Janeiro,ou seja,ainda estamos no período de defeso!!'
dialogo4 = 'Essa é época onde os pescadores locais tiram férias, e os preços dos peixesaumenta!'
dialogo5 = 'Nossa meta é arrecadar 200 mil peixes até o fim do período.'
dialogo6 = 'Controle as operações e mostre teu espirito felino!'
dialogo7 = 'Ah, só tem um detalhezinho...'
dialogo8 = 'Talvez estejamos sem verba,por alguns "probleminhas" legais.'
dialogo9 = 'Mas não se preocupe!Como sou grande,magnífico,inteligente,proativo e resiliente,chamei meu sobrinho pra cuidar disso!'
dialogo10 = 'Tem uma canoa ali,você pode usa-la para pagar as operações!'
dialogo11 = 'Boa-sorte-você-consegue-e-tudo-mais-tchau!'

dialogos = {
    1: (dialogo1, 2),
    2: (dialogo2, 3),
    3: (dialogo3, 4),
    4: (dialogo4, 5),
    5: (dialogo5, 6),
    6: (dialogo6, 7),
    7: (dialogo7, 8),
    8: (dialogo8, 9),
    9: (dialogo9, 10),
    10: (dialogo10, 11),
    11: (dialogo11, 0),
    0: ('NULL', 12)
}

# Background:
background = pygame.image.load('graficos/background.png').convert()

# Gatosário:
gatosario = pygame.image.load('graficos/gatosario.png').convert()
triangulo = pygame.image.load('graficos/triangulo.png').convert()
trianguloX = 900

# Eventos pygame:
def processarEventos():
    global click_x, click_y
    global rotacionar
    global moverx, movery
    global fala
    global transicao
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            
            if round((fala % 1), 2) == 0.1:
                fala = int(fala)
                transicao = True

            click_x, click_y = pygame.mouse.get_pos()
            if cursor_x >= 134 and cursor_y >= 80:
                rotacionar = True
                if event.button == 1:
                    if travar is False:
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
    peixes.update()
    
    if fala in dialogos:
        dialogo, proxFala = dialogos[fala]
        if proxFala != 12:
            dialogoSistema.ateOndeEscrever(dialogo, proxFala)
        elif proxFala == 12:
            travar = False

    # Blits e draws: 
    screen.blit(background, (0,0))
    
    if proxFala != 12:
        screen.blit(gatosario, (153, 8))
        if trianguloX == 900:
            vem = True
        if trianguloX == 890:
            vem = False
        
        if vem:
            trianguloX -= 0.25
        else:
            trianguloX += 0.25
        
        screen.blit(triangulo, (trianguloX, 45))
        dialogoSistema.escrever()

    print(len(peixes))
    if random.randint(1, 5) == 5:
        if len(peixes) < 300:
            peixes.add(Peixe(random.randint(1, 27)))
    peixes.draw(screen)
    particulas.draw(screen)
    player.draw(screen)

    pygame.display.update()
    clock.tick(60)