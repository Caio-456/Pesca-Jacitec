import pygame
import math
import random
from sys import exit
from systems import colisoes
from systems.game_state import GameState

# Pygame:
pygame.init()
screen = pygame.display.set_mode((1000, 625))
pygame.display.set_caption("Pesca Predatória - JACITEC")
clock = pygame.time.Clock()


# Player:
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        global xPlayer
        global yPlayer

        frames = [
            pygame.image.load(f"graficos/canoa/canoa{i}.png").convert_alpha()
            for i in range(1, 9)
        ]

        self.playerIndex = 0
        # A lista tem repetidos para certos frames terem velocidades diferentes
        self.playerAnimacao = [
            frames[0],
            frames[0],
            frames[1],
            frames[2],
            frames[2],
            frames[2],
            frames[2],
            frames[3],
            frames[4],
            frames[4],
            frames[5],
            frames[6],
            frames[6],
            frames[6],
            frames[6],
            frames[7],
        ]

        self.imageOriginal = self.playerAnimacao[self.playerIndex]
        self.image = self.imageOriginal
        self.anguloHistorico = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.rect = self.image.get_rect(center=(500, 150))
        xPlayer = self.rect.centerx
        yPlayer = self.rect.centery

    def rotacionar(self):
        global angulo
        anguloRAD = math.atan2(
            self.rect.centery - cursor_y, self.rect.centerx - cursor_x
        )
        angulo = int(math.degrees(anguloRAD)) - 90
        self.anguloHistorico.append(angulo)
        if len(self.anguloHistorico) > 10:
            self.anguloHistorico.pop(0)
        if abs((self.anguloHistorico[-1] - self.anguloHistorico[-8])) > 5:
            self.image = pygame.transform.rotate(self.imageOriginal, -angulo)
            self.rect = self.image.get_rect(center=self.rect.center)

    def animacao(self):
        global angulo
        self.playerIndex += 0.3
        if self.playerIndex > len(self.playerAnimacao):
            self.playerIndex = 0
        self.imageOriginal = self.playerAnimacao[int(self.playerIndex)]
        angulo = -(self.anguloHistorico[-1])
        self.image = pygame.transform.rotate(self.imageOriginal, angulo)
        self.rect = self.image.get_rect(center=self.rect.center)

    def mover(self):
        if game_state.impedir_jogador_de_mover is False:
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
            if not rede:
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
        self.rect = self.image.get_rect(center=(500, 900))
        self.timer = (tamanho * 30) + 1
        self.mover = True

    def novaVelocidade(self):
        return random.uniform(
            self.velocidadeBase * 0.5, self.velocidadeBase * 1.2
        )  # Uniform também arredonda para inteiro.

    def rotacionar(self):
        anguloRAD = math.atan2(
            self.rect.centery - self.ypos, self.rect.centerx - self.xpos
        )
        angulo = int(math.degrees(anguloRAD)) - 90
        self.image = pygame.transform.rotate(self.imagemSemRotacao, -angulo)
        self.rect = self.image.get_rect(center=self.rect.center)

    def movimento(self):
        if self.mover:
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

    def atordoar(self):
        self.timer -= 1
        if self.timer < (self.tamanho * 100 // 5):
            self.mover = False

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
    {"sprite": 2, "velocidade": 2, "tamanhos": range(10, 16)},
    {"sprite": 3, "velocidade": 3, "tamanhos": range(16, 22)},
    {"sprite": 4, "velocidade": 4, "tamanhos": range(22, 27)},
    {"sprite": 5, "velocidade": 4, "tamanhos": [27]},
]


# Particulas
class Particula(pygame.sprite.Sprite):
    def __init__(self, posicao):
        super().__init__()
        self.image = pygame.Surface(
            (3, 2), pygame.SRCALPHA
        )  # SRCALPHA significa que os pixels terão um canal alpha(transparência)
        pygame.draw.circle(self.image, (143, 211, 255), (2, 2), 3)  # cor, centro, raio
        self.rect = self.image.get_rect(center=posicao)
        self.moverX = random.uniform(-1, 3)  # uniform é quando aceita float
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


fonte = pygame.font.Font("graficos/DeterminationMono.ttf", 18)
transicao = False
fala = 1
dialogoSistema = Dialogo()
dialogo1 = "Parabéééénsss!!! Você está a um passo de se tornar o novo CEO da Phishing  Good & Cheap Enterprise©!"
dialogo2 = "Começaremos nossas operações em Gatuma, uma pequena cidade pesqueira entre Miausília e Peixótina! Uma chance perfeita pra subir na carreira!"
dialogo3 = "Hoje é dia 9 de janeiro... ou seja, ainda estamos no período de defeso!"
dialogo4 = (
    "Nessa época, os pescadores locais tiram férias... e o preço dos peixes dis-para!"
)
dialogo5 = "Nossa meta é simples: arrecadar 20 mil miauletas até o fim do período!"
dialogo6 = "Mostre seu instinto felino e controle as operações!"
dialogo7 = "Ah, só tem um pequeno detalhe..."
dialogo8 = "Talvez estejamos sem verba, por causa de uns “probleminhas” legais..."
dialogo9 = "Mas não se preocupe! Como sou inteligente, proativo e resiliente, já penseiem tudo!"
dialogo10 = "Pesque alguns peixes e compre melhorias ali à esquerda!"
dialogo11 = "Boa-sorte-você-consegue-e-tudo-mais-tchau!"
dialogo12 = "Ué, cadê os peixes? Missão cumprida?"

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
    0: ("NULL", 12),
}

# Background:
background = pygame.image.load("graficos/background.png").convert_alpha()

# Gatosário:
gatosario = pygame.image.load("graficos/gatosario.png").convert_alpha()
triangulo = pygame.image.load("graficos/triangulo.png").convert_alpha()
trianguloX = 900


# Botões:
class Botao(pygame.sprite.Sprite):
    def __init__(self, cod):
        global botoesInsuficientes
        global botoesComprados
        global botoesSuficientes
        global botaoFechado
        super().__init__()
        self.cod = cod
        self.comprado = False
        self.image = botaoFechado
        self.rect = self.image.get_rect(topleft=(7, (90 + (59 * cod))))
        self.liberado = False
        match cod:
            case 0:
                self.image = botoesInsuficientes[0]
                self.liberado = True
                self.preco = 50
            case 1:
                self.preco = 100
            case 2:
                self.preco = 200
            case 3:
                self.preco = 400
            case 4:
                self.preco = 800
            case 5:
                self.preco = 1600
            case 6:
                self.preco = 3200
            case 7:
                self.preco = 6400
            case 8:
                self.preco = 12800

    def cor(self):
        if self.liberado:
            if self.comprado is False:
                if game_state.dinheiro >= self.preco:
                    self.image = botoesSuficientes[self.cod]
                else:
                    self.image = botoesInsuficientes[self.cod]

    def comprar(self):  # Checado apenas quando mouse está sobre o botão
        if self.comprado is False:
            if self.liberado:
                if game_state.dinheiro >= self.preco:
                    game_state.melhoria_atual += 1
                    game_state.dinheiro -= self.preco
                    self.image = botoesComprados[self.cod]
                    self.comprado = True

    def update(self):
        if game_state.melhoria_atual >= self.cod:
            self.liberado = True
        self.cor()


botoesInsuficientes = [
    pygame.image.load(f"graficos/botoes/botao{i}-insuficiente.png").convert_alpha()
    for i in range(1, 10)
]
botoesSuficientes = [
    pygame.image.load(f"graficos/botoes/botao{i}-suficiente.png").convert_alpha()
    for i in range(1, 10)
]
botoesComprados = [
    pygame.image.load(f"graficos/botoes/botao{i}-comprado.png").convert_alpha()
    for i in range(1, 10)
]
botaoFechado = pygame.image.load("graficos/botoes/botao-fechado.png").convert_alpha()
botoes = pygame.sprite.Group()

for i in range(9):
    botoes.add(Botao(i))


# Isca:
class Isca(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        global xPlayer, yPlayer
        self.image = pygame.image.load("graficos/isca.png").convert_alpha()
        self.rect = self.image.get_rect(center=(game_state.click_x, game_state.click_y))

    def puxar(self):
        global puxarIsca
        global colisaoIsca
        global peixeCapturado
        if puxarIsca:
            if xPlayer < self.rect.x:
                self.rect.x -= 1
            if xPlayer > self.rect.x:
                self.rect.x += 1
            if yPlayer < self.rect.y:
                self.rect.y -= 1
            if yPlayer > self.rect.y:
                self.rect.y += 1
            if xPlayer == self.rect.x and yPlayer == self.rect.y:
                colisaoIsca = True
                puxarIsca = False
                dinheiroReceber(peixeCapturado.tamanho // 3)
                self.kill()

    def update(self):
        self.puxar()
        if abs(game_state.click_x - xPlayer) > 100 or abs(game_state.click_y - yPlayer) > 100:
            self.kill()


puxarIsca = False
colisaoIsca = True
isca = pygame.sprite.GroupSingle()
transparenteSurface = pygame.Surface((1000, 625), pygame.SRCALPHA)


# Rede:
class Rede(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        global xPlayer, yPlayer
        global angulo
        self.imageOriginal = pygame.image.load("graficos/rede.png").convert_alpha()
        self.image = pygame.transform.rotate(self.imageOriginal, -angulo)
        self.rect = self.image.get_rect(center=(game_state.click_x, game_state.click_y))
        self.mask = pygame.mask.from_surface(self.image)
        self.timer = 100
        game_state.impedir_jogador_de_mover = True

    def cantosRotacionados(self):
        redeLargura, redeAltura = self.imageOriginal.get_size()
        centroX, centroY = self.rect.center

        # Cálculo dos cantos em relação ao centro
        cantos = [
            (-redeLargura / 2, redeAltura / 2),  # bottomleft
            (redeLargura / 2, redeAltura / 2),  # bottomright
        ]

        # Converter o ângulo para radianos
        rad = math.radians(angulo)
        cos = math.cos(rad)
        sin = math.sin(rad)

        # Rotacionando com fórmula matemática
        rotacionado = []
        for x, y in cantos:
            rx = centroX + (x * cos - y * sin)
            ry = centroY + (x * sin + y * cos)
            rotacionado.append((rx, ry))
        return rotacionado

    def puxar(self):
        global puxarRede, rotacionar, xPlayer, yPlayer

        if puxarRede:
            centroX, centroY = self.rect.center
            dx = xPlayer - centroX
            dy = yPlayer - centroY
            distancia = math.hypot(dx, dy)

            if distancia > 2:
                centroX += (dx / distancia) * 1
                centroY += (dy / distancia) * 1
                self.rect.center = (centroX, centroY)
            else:
                puxarRede = False
                game_state.impedir_jogador_de_mover = False
                rotacionar = True
                self.kill()

    def colide_com(self, peixe):
        if not hasattr(peixe, "mask"):
            peixe.mask = pygame.mask.from_surface(peixe.image)

        offset = (peixe.rect.x - self.rect.x, peixe.rect.y - self.rect.y)
        return self.mask.overlap(peixe.mask, offset) is not None

    def update(self):
        global puxarRede
        self.puxar()
        self.timer -= 1
        if self.timer == 0:
            puxarRede = True
        if abs(game_state.click_x - xPlayer) > 300 or abs(game_state.click_y - yPlayer) > 200:
            self.kill()


puxarRede = False
rede = pygame.sprite.GroupSingle()


# Explosivo:
class Explosivo(pygame.sprite.Sprite):
    def __init__(self):
        global xPlayer, yPlayer
        super().__init__()
        self.image = pygame.image.load("graficos/explosivo.png").convert_alpha()
        self.rect = self.image.get_rect(center=(xPlayer, yPlayer))

        self.estado = "movendo"
        self.raio = 0
        self.raio_maximo = 220
        self.alpha = 255
        self.explodiu = False

    def mover(self):
        centroX, centroY = self.rect.center
        dx = game_state.click_x - centroX
        dy = game_state.click_y - centroY
        distancia = math.hypot(dx, dy)

        if distancia > 4:
            centroX += (dx / distancia) * 4
            centroY += (dy / distancia) * 4
            self.rect.center = (centroX, centroY)
        else:
            self.estado = "explodindo"

    def update(self):
        if self.estado == "movendo":
            self.mover()
        elif self.estado == "explodindo":
            self.raio += 5
            self.alpha -= 8
            if self.alpha < 0:
                self.alpha = 0
            if self.raio >= self.raio_maximo:
                self.explodiu = True
                self.kill()
        centro_ex = pygame.math.Vector2(self.rect.center)
        for peixe in peixes.sprites():
            centro_peixe = pygame.math.Vector2(peixe.rect.center)
            distancia = centro_ex.distance_to(centro_peixe)
            # definir "raio do peixe" aproximado (meio da largura/altura)
            raio_peixe = max(peixe.rect.width, peixe.rect.height) * 0.5
            if distancia <= self.raio + raio_peixe:
                dinheiroReceber(peixe.tamanho * 15)
                peixe.kill()


explosivos = pygame.sprite.Group()


def desenharExplosao(screen, explosivo):
    if explosivo.estado == "explodindo" and not explosivo.explodiu:
        surf = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        pygame.draw.circle(
            surf, (213, 224, 75, explosivo.alpha), explosivo.rect.center, explosivo.raio
        )
        screen.blit(surf, (0, 0))


# Armadilha:
class Armadilha(pygame.sprite.Sprite):
    def __init__(self, cod):
        super().__init__()
        self.cod = cod
        self.image = pygame.image.load("graficos/armadilha1.png").convert_alpha()
        self.rect = self.image.get_rect(
            center=(random.randrange(134, 1000), random.randrange(80, 625))
        )

    def update(self):
        if game_state.melhoria_atual > 4:
            self.image = pygame.image.load("graficos/armadilha2.png").convert_alpha()


armadilhas = pygame.sprite.Group()


# Cianeto:
class Cianeto(pygame.sprite.Sprite):
    def __init__(self, cod):
        super().__init__()
        self.cod = cod
        self.image = pygame.image.load("graficos/cianeto.png").convert_alpha()
        self.rect = self.image.get_rect(
            center=(random.randrange(134, 1000), random.randrange(80, 625))
        )


cianetos = pygame.sprite.Group()


def colisoesIsca():
    global puxarIsca
    global colisaoIsca
    if not isca.sprite:  # Se não tiver isca lançada.
        return False

    if colisaoIsca is True:
        global peixeCapturado
        peixeCapturado = pygame.sprite.spritecollideany(isca.sprite, peixes)
        if (
            pygame.sprite.spritecollide(isca.sprite, peixes, True)
            and puxarIsca is False
        ):  # Remove o peixe colidido.
            puxarIsca = True
            colisaoIsca = False


def colisoesRede():
    global puxarRede
    global rotacionar
    if not rede.sprite:
        return False

    global peixeCapturado
    peixeCapturado = pygame.sprite.spritecollideany(rede.sprite, peixes)
    if peixeCapturado:
        if game_state.melhoria_atual > 6:
            if rede.sprite.colide_com(peixeCapturado):
                puxarRede = True
                dinheiroReceber(peixeCapturado.tamanho * 15)
                peixeCapturado.kill()
        if game_state.melhoria_atual > 5:
            if peixeCapturado.tamanho in range(16, 28):
                if rede.sprite.colide_com(peixeCapturado):
                    puxarRede = True
                    dinheiroReceber(peixeCapturado.tamanho * 3)
                    peixeCapturado.kill()
        if game_state.melhoria_atual <= 5:
            if peixeCapturado.tamanho in range(22, 28):
                if rede.sprite.colide_com(peixeCapturado):
                    puxarRede = True
                    dinheiroReceber(peixeCapturado.tamanho * 2)
                    peixeCapturado.kill()


def colisaoArmadilhas():
    global peixeArmadilhado
    peixeArmadilhado = pygame.sprite.groupcollide(armadilhas, peixes, False, False)

    if peixeArmadilhado:  # dict_values([[<Peixe Sprite(in 1 groups)>]])
        for listaPeixes in peixeArmadilhado.values():
            for peixe in listaPeixes:
                if game_state.melhoria_atual > 4:
                    if peixe.tamanho in range(1, 22):
                        peixe.kill()
                        dinheiroReceber(peixe.tamanho)
                else:
                    if peixe.tamanho in range(10, 22):
                        peixe.kill()
                        dinheiroReceber(peixe.tamanho // 4)


def colisaoCianeto():
    global peixeAtordoado

    peixeAtordoado = pygame.sprite.groupcollide(cianetos, peixes, False, False)

    if peixeAtordoado:  # dict_values([[<Peixe Sprite(in 1 groups)>]])
        for listaPeixes in peixeAtordoado.values():
            for peixe in listaPeixes:
                peixe.atordoar()


def colisoes():
    colisaoArmadilhas()
    if game_state.melhoria_atual > 3:
        colisoesRede()
    else:
        colisoesIsca()
    if game_state.melhoria_atual > 7:
        colisaoCianeto()


peixeCapturado = None
peixeArmadilhado = None


# Dinheiro:
def dinheiroConsultaImpressao():
    dinherioSurface = pygame.transform.scale_by(
        fonte.render(f"{game_state.dinheiro:05d}", False, (250, 250, 250)), 2
    )
    dinheiroRect = dinherioSurface.get_rect(center=(80, 23))
    screen.blit(dinherioSurface, dinheiroRect)
    return game_state.dinheiro


def dinheiroReceber(quanto):
    if game_state.melhoria_atual > 2:
        quanto = quanto * 2
    game_state.dinheiro += quanto

game_state = GameState()
dinheiroMeta = 20000
barraLargura = 113
barraAltura = 19
reflexoBarra = pygame.image.load("graficos/reflexo.png").convert_alpha()
reflexoBarra.set_alpha(190)


# Eventos pygame:
def processarEventos():
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

            game_state.click_x,  game_state.click_y = pygame.mouse.get_pos()
            if cursor_x >= 134 and cursor_y >= 80:
                rotacionar = True
                if event.button == 1:
                    if game_state.impedir_jogador_de_mover is False:
                        if xPlayer < game_state.click_x:
                            moverx = -velocidade
                        if xPlayer > game_state.click_x:
                            moverx = velocidade
                        if yPlayer < game_state.click_y:
                            movery = -velocidade
                        if yPlayer > game_state.click_y:
                            movery = velocidade
                elif event.button == 3:
                    if game_state.melhoria_atual > 8:
                        explosivos.add(Explosivo())
                    if 8 >= game_state.melhoria_atual > 3:
                        if not puxarRede and len(rede) == 0:
                            rede.add(Rede())
                            game_state.impedir_jogador_de_mover = True
                    if game_state.melhoria_atual <= 3:
                        isca.add(Isca())

            for botao in botoes:
                if botao.rect.collidepoint((cursor_x, cursor_y)):
                    if pygame.MOUSEBUTTONDOWN:
                        botao.comprar()


while True:
    processarEventos()
    cursor_x, cursor_y = pygame.mouse.get_pos()
    if cursor_x < 134 or cursor_y < 80:
        pygame.mouse.set_cursor(*pygame.cursors.arrow)
    else:
        pygame.mouse.set_cursor(*pygame.cursors.broken_x)

    if len(rede) == 0:
        puxarRede = False

    if movendo:
        if len(rede) == 1:
            for i in rede:
                i.kill()
        if abs(xPlayer - game_state.click_x) < 10:
            moverx = 0
        if abs(yPlayer - game_state.click_y) < 10:
            movery = 0

    colisoes()

    if game_state.melhoria_atual > 0:
        if len(armadilhas) < 3:
            for i in range(3):
                armadilhas.add(Armadilha(i))
    if game_state.melhoria_atual > 1:
        if len(armadilhas) < 9:
            for i in range(3):
                armadilhas.add(Armadilha(i))
    if game_state.melhoria_atual > 7:
        if len(cianetos) < 30:
            for i in range(3):
                cianetos.add(Cianeto(i))

    # Updates:
    player.update()
    particulas.update()
    peixes.update()
    isca.update()
    rede.update()
    botoes.update()
    armadilhas.update()
    if game_state.melhoria_atual > 8:
        explosivos.update()

    if fala in dialogos:
        dialogo, proxFala = dialogos[fala]
        if proxFala != 12:
            dialogoSistema.ateOndeEscrever(dialogo, proxFala)
        elif proxFala == 12:
            game_state.impedir_jogador_de_mover = False
            if len(peixes) == 0:
                dialogoSistema.ateOndeEscrever(dialogo12, 12)

    # Peixes:
    if random.randint(1, 3) == 3:
        if len(peixes) < (304 - (game_state.melhoria_atual * 38)):
            peixes.add(Peixe(random.randint(1, 27)))

    # Blits e draws:
    transparenteSurface.fill((0, 0, 0, 0))  # Limpa transparenteSurface

    # Barra de progresso:
    progresso = game_state.dinheiro / dinheiroMeta
    larguraAtual = int(barraLargura * progresso)
    pygame.draw.rect(
        transparenteSurface, (145, 219, 105), (12, 51, larguraAtual, barraAltura)
    )
    screen.blit(background, (0, 0))

    peixes.draw(screen)

    cianetos.draw(screen)

    armadilhas.draw(screen)

    explosivos.draw(screen)
    for explosivo in explosivos:
        desenharExplosao(screen, explosivo)

    if game_state.melhoria_atual > 8:
        pygame.draw.circle(
            transparenteSurface, (250, 250, 250, 80), (xPlayer, yPlayer), 500, 2
        )
    if 8 >= game_state.melhoria_atual > 3:
        if rede.sprite:
            bottomleft, bottomright = rede.sprite.cantosRotacionados()
            pygame.draw.line(screen, (250, 250, 250), (xPlayer, yPlayer), bottomleft)
            pygame.draw.line(screen, (250, 250, 250), (xPlayer, yPlayer), bottomright)
        rede.draw(screen)
        pygame.draw.circle(
            transparenteSurface, (250, 250, 250, 80), (xPlayer, yPlayer), 200, 2
        )
    if game_state.melhoria_atual <= 3:
        if isca.sprite:
            pygame.draw.line(
                screen, (250, 250, 250), (xPlayer, yPlayer), isca.sprite.rect.center
            )
        isca.draw(screen)
        pygame.draw.circle(
            transparenteSurface, (250, 250, 250, 80), (xPlayer, yPlayer), 100, 2
        )

    screen.blit(transparenteSurface, (0, 0))

    screen.blit(reflexoBarra, (11, 50))

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

    botoes.draw(screen)

    particulas.draw(screen)

    player.draw(screen)

    dinheiroConsultaImpressao()

    pygame.display.update()
    clock.tick(60)
