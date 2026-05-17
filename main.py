import pygame
import math
import random
from sys import exit
from systems.peixes import Peixe
from systems.botoes import Botao
from systems.particulas import Particula
from systems.game_state import GameState

# Pygame:
pygame.init()
screen = pygame.display.set_mode((1000, 625))
pygame.display.set_caption("Pesca Predatória - JACITEC")
clock = pygame.time.Clock()

game_state = GameState()
limite_y = 106
limite_x = 145

# Player:
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

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

        self.imagem_sem_rotacao = self.playerAnimacao[self.playerIndex]
        self.image = self.imagem_sem_rotacao
        self.anguloHistorico = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.rect = self.image.get_rect(center=(560, 250))
        game_state.x_player = self.rect.centerx
        game_state.y_player = self.rect.centery

    def rotacionar(self):
        anguloRAD = math.atan2(
            self.rect.centery - cursor_y, self.rect.centerx - cursor_x
        )
        game_state.angulo_jogador = int(math.degrees(anguloRAD)) - 90
        self.anguloHistorico.append(game_state.angulo_jogador)
        if len(self.anguloHistorico) > 10:
            self.anguloHistorico.pop(0)
        if abs((self.anguloHistorico[-1] - self.anguloHistorico[-8])) > 5:
            self.image = pygame.transform.rotate(
                self.imagem_sem_rotacao, -game_state.angulo_jogador
            )
            self.rect = self.image.get_rect(center=self.rect.center)

    def animacao(self):
        self.playerIndex += 0.3
        if self.playerIndex > len(self.playerAnimacao):
            self.playerIndex = 0
        self.imagem_sem_rotacao = self.playerAnimacao[int(self.playerIndex)]
        game_state.angulo_jogador = -(self.anguloHistorico[-1])
        self.image = pygame.transform.rotate(
            self.imagem_sem_rotacao, game_state.angulo_jogador
        )
        self.rect = self.image.get_rect(center=self.rect.center)

    def mover(self):
        if game_state.impedir_jogador_de_mover is False:
            global mover_x
            global mover_y
            global jogador_esta_se_movendo
            game_state.x_player = self.rect.centerx
            game_state.y_player = self.rect.centery
            jogador_esta_se_movendo = True
            self.rect.centerx = self.rect.centerx - mover_x
            self.rect.centery = self.rect.centery - mover_y

            if (
                self.rect.centerx == game_state.x_player
                and self.rect.centery == game_state.y_player
            ):
                jogador_esta_se_movendo = False
                game_state.jogador_pode_rotacionar = True

    def gerar_particulas(self, particulas):
        for _ in range(2):
            particulas.add(Particula(self.rect.center))

    def update(self):
        if (
            cursor_x >= limite_x
            and cursor_y >= limite_y
            and game_state.jogador_pode_rotacionar is True
        ):
            self.rotacionar()
        self.mover()
        if jogador_esta_se_movendo:
            game_state.jogador_pode_rotacionar = False
            self.animacao()
            player.sprite.gerar_particulas(particulas)


player = pygame.sprite.GroupSingle()
mover_x = 0
mover_y = 0
jogador_esta_se_movendo = False
velocidade = 3
player.add(Player())


# Peixes:
peixes = pygame.sprite.Group()

# Particulas
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
            texto_surface = fonte_dialogo.render(
                dialogo[self.posicao], False, (250, 253, 255)
            )
            self.texto.append(texto_surface)

        self.posicao += 1
        if self.posicao == len(dialogo):
            fala = proxFala + 0.1

    def escrever(self):
        for i in range(self.posicao):
            if i < 58:
                screen.blit(self.texto[i], ((285 + (self.separacao)), 35))
            else:
                screen.blit(self.texto[i], ((285 + (self.separacao) - 696), 53))
            self.separacao += 12
        self.separacao = 0


fonte = pygame.font.Font("graficos/DeterminationMono.ttf", 18)
fonte_dialogo = pygame.font.Font("graficos/DeterminationMono.ttf", 24)
transicao = False
fala = 1
dialogoSistema = Dialogo()
dialogo1 = 'Parabéééénsss!!! Você está a um passo de se tornar o novo CEO da "Phishing Good & Cheap Enterprise©"!'
dialogo2 = "Começaremos nossas operações em Gatuma,uma pequena cidade pesqueira entre Miausília e Peixótina!"
dialogo3 = "Hoje é dia 9 de janeiro...ou seja,ainda estamos no períodode defeso!"
dialogo4 = (
    "Nessa época,os pescadores locais tiram férias...e o preço dos peixes dispara!"
)
dialogo5 = "Nossa meta é simples:arrecadar 20 mil miauletas até o fim do período!"
dialogo6 = "Mostre seu instinto felino e controle as operações!"
dialogo7 = "Ah,só tem um pequeno detalhe..."
dialogo8 = "Talvez estejamos sem verba,por causa de uns probleminhas  legais..."
dialogo9 = "Mas não se preocupe! Como sou inteligente,proativo e      resiliente,já penseiem tudo!"
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
background = pygame.transform.scale2x(background)
menu = pygame.image.load("graficos/fundo_menu.png").convert_alpha()

# Gatosário:
gatosario = pygame.image.load("graficos/gatosario.png").convert_alpha()
gatosario = pygame.transform.scale_by(gatosario, 2)
triangulo = pygame.image.load("graficos/triangulo.png").convert_alpha()
triangulo = pygame.transform.scale_by(triangulo, 2)
trianguloX = 950


# Botões:
botoes = pygame.sprite.Group()

for i in range(9):
    botoes.add(Botao(i))


# Isca:
class Isca(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("graficos/isca.png").convert_alpha()
        self.rect = self.image.get_rect(center=(game_state.click_x, game_state.click_y))

    def puxar(self):
        global colisao_isca
        global peixeCapturado
        if game_state.puxar_isca:
            self.image = peixeCapturado.imagem_sem_rotacao  # type: ignore
            self.image = pygame.transform.rotate(
                self.image, game_state.angulo_jogador + 180
            )
            self.rect = self.image.get_rect(center=self.rect.center)
            if game_state.x_player < self.rect.x:
                self.rect.x -= 1
            if game_state.x_player > self.rect.x:
                self.rect.x += 1
            if game_state.y_player < self.rect.y:
                self.rect.y -= 1
            if game_state.y_player > self.rect.y:
                self.rect.y += 1
            if (
                game_state.x_player == self.rect.x
                and game_state.y_player == self.rect.y
            ):
                colisao_isca = True
                game_state.puxar_isca = False
                dinheiroReceber(peixeCapturado.tamanho // 3)  # type: ignore
                self.kill()

    def update(self):
        self.puxar()
        game_state.jogador_pode_rotacionar = False
        if (
            abs(game_state.click_x - game_state.x_player) > 100
            or abs(game_state.click_y - game_state.y_player) > 100
        ):
            self.kill()


colisao_isca = True
isca = pygame.sprite.GroupSingle()
transparenteSurface = pygame.Surface((1000, 625), pygame.SRCALPHA)


# Rede:
class Rede(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.imagem_sem_rotacao = pygame.image.load("graficos/rede.png").convert_alpha()
        self.image = pygame.transform.rotate(
            self.imagem_sem_rotacao, -game_state.angulo_jogador
        )
        self.rect = self.image.get_rect(center=(game_state.click_x, game_state.click_y))
        self.mask = pygame.mask.from_surface(self.image)
        self.timer = 100
        game_state.impedir_jogador_de_mover = True

    def cantosRotacionados(self):
        redeLargura, redeAltura = self.imagem_sem_rotacao.get_size()
        centro_x, centro_y = self.rect.center

        # Cálculo dos cantos em relação ao centro
        cantos = [
            (-redeLargura / 2, redeAltura / 2),  # bottomleft
            (redeLargura / 2, redeAltura / 2),  # bottomright
        ]

        # Converter o ângulo para radianos
        rad = math.radians(game_state.angulo_jogador)
        cos = math.cos(rad)
        sin = math.sin(rad)

        # Rotacionando com fórmula matemática
        rotacionado = []
        for x, y in cantos:
            rx = centro_x + (x * cos - y * sin)
            ry = centro_y + (x * sin + y * cos)
            rotacionado.append((rx, ry))
        return rotacionado

    def puxar(self):
        global puxarRede

        if puxarRede:
            centro_x, centro_y = self.rect.center
            dx = game_state.x_player - centro_x
            dy = game_state.y_player - centro_y
            distancia = math.hypot(dx, dy)

            if distancia > 2:
                centro_x += (dx / distancia) * 1
                centro_y += (dy / distancia) * 1
                self.rect.center = (centro_x, centro_y)  # type: ignore
            else:
                puxarRede = False
                game_state.impedir_jogador_de_mover = False
                game_state.jogador_pode_rotacionar = True
                self.kill()

    def colide_com(self, peixe):
        if not hasattr(peixe, "mask"):
            peixe.mask = pygame.mask.from_surface(peixe.image)

        offset = (peixe.rect.x - self.rect.x, peixe.rect.y - self.rect.y)
        return self.mask.overlap(peixe.mask, offset) is not None

    def update(self):
        global puxarRede
        game_state.jogador_pode_rotacionar = False
        self.puxar()
        self.timer -= 1
        if self.timer == 0:
            puxarRede = True
        if (
            abs(game_state.click_x - game_state.x_player) > 300
            or abs(game_state.click_y - game_state.y_player) > 200
        ):
            self.kill()


puxarRede = False
rede = pygame.sprite.GroupSingle()


# Explosivo:
class Explosivo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("graficos/explosivo.png").convert_alpha()
        self.rect = self.image.get_rect(
            center=(game_state.x_player, game_state.y_player)
        )

        self.estado = "movendo"
        self.raio = 0
        self.raio_maximo = 140
        self.alpha = 255
        self.explodiu = False
        self.alvo_x = game_state.click_x
        self.alvo_y = game_state.click_y

    def mover(self):
        centro_x, centro_y = self.rect.center
        dx = self.alvo_x - centro_x
        dy = self.alvo_y - centro_y
        distancia = math.hypot(dx, dy)

        if distancia > 4:
            centro_x += (dx / distancia) * 4
            centro_y += (dy / distancia) * 4
            self.rect.center = (centro_x, centro_y)  # type: ignore
        else:
            self.estado = "explodindo"

    def update(self):
        if self.estado == "movendo":
            self.mover()
        elif self.estado == "explodindo":
            self.raio += 6
            self.alpha -= 10
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
            surf, (213, 224, 75, explosivo.alpha), explosivo.rect.center, explosivo.raio + 20
        )
        screen.blit(surf, (0, 0))


# Armadilha:
class Armadilha(pygame.sprite.Sprite):
    def __init__(self, cod):
        super().__init__()
        self.cod = cod
        self.image = pygame.image.load("graficos/armadilha1.png").convert_alpha()
        self.rect = self.image.get_rect(
            center=(random.randrange(limite_x, 1000), random.randrange(limite_y + 50, 625))
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
            center=(random.randrange(limite_x, 1000), random.randrange(limite_y, 625))
        )


cianetos = pygame.sprite.Group()


def colisoesIsca():
    global colisao_isca
    if not isca.sprite:  # Se não tiver isca lançada.
        return False

    if colisao_isca is True:
        global peixeCapturado
        peixeCapturado = pygame.sprite.spritecollideany(isca.sprite, peixes)
        if (
            pygame.sprite.spritecollide(isca.sprite, peixes, True)
            and game_state.puxar_isca is False
        ):  # Remove o peixe colidido.
            game_state.puxar_isca = True
            colisao_isca = False


def colisoesRede():
    global puxarRede
    if not rede.sprite:
        return False
    puxarRede = True
    global peixeCapturado
    peixeCapturado = pygame.sprite.spritecollideany(rede.sprite, peixes)
    if peixeCapturado:
        if game_state.melhoria_atual > 6:
            if rede.sprite.colide_com(peixeCapturado):
                peixeCapturado.arrastado = True
        if game_state.melhoria_atual > 5:
            if peixeCapturado.tamanho in range(10, 28):
                if rede.sprite.colide_com(peixeCapturado):
                    peixeCapturado.arrastado = True
        if game_state.melhoria_atual <= 5:
            if peixeCapturado.tamanho in range(22, 28):
                if rede.sprite.colide_com(peixeCapturado):
                    peixeCapturado.arrastado = True

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


def peixe():
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


dinheiroMeta = 20000
barraLargura = 113
barraAltura = 19
reflexoBarra = pygame.image.load("graficos/reflexo.png").convert_alpha()
reflexoBarra.set_alpha(190)


# Eventos pygame:
def processarEventos():
    global mover_x, mover_y
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

            game_state.click_x, game_state.click_y = pygame.mouse.get_pos()
            if cursor_x >= limite_x and cursor_y >= limite_y:
                if event.button == 1:
                    if game_state.impedir_jogador_de_mover is False:
                        if game_state.x_player < game_state.click_x:
                            mover_x = -velocidade
                        if game_state.x_player > game_state.click_x:
                            mover_x = velocidade
                        if game_state.y_player < game_state.click_y:
                            mover_y = -velocidade
                        if game_state.y_player > game_state.click_y:
                            mover_y = velocidade
                elif event.button == 3:
                    if game_state.melhoria_atual > 8:
                        explosivos.add(Explosivo())
                    if 8 >= game_state.melhoria_atual > 3:
                        if not puxarRede and len(rede) == 0:
                            rede.add(Rede())
                            game_state.impedir_jogador_de_mover = True
                    if game_state.melhoria_atual <= 3:
                        isca.add(Isca())
            else:
                game_state.jogador_pode_rotacionar = False

            for botao in botoes:
                if botao.rect.collidepoint((cursor_x, cursor_y)):
                    if pygame.MOUSEBUTTONDOWN:
                        botao.comprar(game_state)


while True:
    processarEventos()
    cursor_x, cursor_y = pygame.mouse.get_pos()
    if cursor_x < limite_x or cursor_y < limite_y:
        pygame.mouse.set_cursor(*pygame.cursors.arrow)
    else:
        pygame.mouse.set_cursor(*pygame.cursors.broken_x)

    if len(rede) == 0:
        puxarRede = False

    if jogador_esta_se_movendo:
        if len(rede) == 1:
            for i in rede:
                i.kill()
        if abs(game_state.x_player - game_state.click_x) < 10:
            mover_x = 0
        if abs(game_state.y_player - game_state.click_y) < 10:
            mover_y = 0

    peixe()

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
    peixes.update(game_state)
    isca.update()
    rede.update()
    botoes.update(game_state)
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
        if len(peixes) < (320 - (game_state.melhoria_atual * 40)):
            tamanho = random.randint(1, 27)
            if tamanho == 27:
                tamanho = random.randint(20, 27)
            peixes.add(Peixe(tamanho))

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
            transparenteSurface,
            (250, 250, 250, 80),
            (game_state.x_player, game_state.y_player),
            500,
            2,
        )
    if 8 >= game_state.melhoria_atual > 3:
        if rede.sprite:
            bottomleft, bottomright = rede.sprite.cantosRotacionados()
            pygame.draw.line(
                screen,
                (250, 250, 250),
                (game_state.x_player, game_state.y_player),
                bottomleft,
            )
            pygame.draw.line(
                screen,
                (250, 250, 250),
                (game_state.x_player, game_state.y_player),
                bottomright,
            )
        rede.draw(screen)
        pygame.draw.circle(
            transparenteSurface,
            (250, 250, 250, 80),
            (game_state.x_player, game_state.y_player),
            200,
            2,
        )
    if game_state.melhoria_atual <= 3:
        if isca.sprite:
            pygame.draw.line(
                screen,
                (250, 250, 250),
                (game_state.x_player, game_state.y_player),
                isca.sprite.rect.center,
            )
        isca.draw(screen)
        pygame.draw.circle(
            transparenteSurface,
            (250, 250, 250, 80),
            (game_state.x_player, game_state.y_player),
            100,
            2,
        )

    screen.blit(transparenteSurface, (0, 0))

    screen.blit(menu, (0, 0))

    screen.blit(reflexoBarra, (11, 50))

    if proxFala != 12:
        screen.blit(gatosario, (153, 8))
        if trianguloX == 950:
            vem = True
        if trianguloX == 940:
            vem = False

        if vem:
            trianguloX -= 0.25
        else:
            trianguloX += 0.25

        screen.blit(triangulo, (trianguloX, 85))
        dialogoSistema.escrever()

    botoes.draw(screen)

    particulas.draw(screen)

    player.draw(screen)

    dinheiroConsultaImpressao()

    pygame.display.update()
    clock.tick(60)