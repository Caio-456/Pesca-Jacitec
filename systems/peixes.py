import pygame
import random
import math


class Peixe(pygame.sprite.Sprite):
    def __init__(self, tamanho):
        super().__init__()
        if tamanho == 27:
            self.tamanho = 12
        self.tamanho = tamanho
        for configuracoes in conf_peixes:
            if tamanho in configuracoes["tamanhos"]:
                self.image = peixes_portes[configuracoes["sprite"]].convert_alpha()
                self.imagem_sem_rotacao = self.image
                self.velocidade_base = configuracoes["velocidade"]

        self.velocidade = self.novaVelocidade()
        self.xpos = random.randrange(134, 1000)
        self.ypos = random.randrange(80 + ((self.tamanho * 3)), 625)
        self.rect = self.image.get_rect(center=(500, 900))
        self.timer = (tamanho * 30) + 1
        self.mover = True
        self.arrastado = False

    def novaVelocidade(self):
        return int(random.uniform(self.velocidade_base, self.velocidade_base * 2))

    def rotacionar(self):
        anguloRAD = math.atan2(
            self.rect.centery - self.ypos, self.rect.centerx - self.xpos
        )
        angulo = int(math.degrees(anguloRAD)) - 90
        self.image = pygame.transform.rotate(self.imagem_sem_rotacao, -angulo)
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

    def arrastar(self, game_state):
        self.mover = False
        centro_x, centro_y = self.rect.center
        dx = game_state.x_player - centro_x
        dy = game_state.y_player - centro_y
        distancia = math.hypot(dx, dy)
        if distancia > 30:
            centro_x += (dx / distancia) * 1
            centro_y += (dy / distancia) * 1
            self.rect.center = (centro_x, centro_y)  # type: ignore
        else:
            game_state.dinheiro += (35 - self.tamanho) * 40
            self.kill()

    def atordoar(self):
        self.timer -= 1
        if self.timer < (self.tamanho * 100 // 5):
            self.mover = False

    def update(self, game_state):
        if self.arrastado: 
            self.arrastar(game_state)
        self.movimento()
        self.rotacionar()


peixes_portes = {
    1: pygame.image.load("graficos/peixes/peixe1.png"),
    2: pygame.image.load("graficos/peixes/peixe2.png"),
    3: pygame.image.load("graficos/peixes/peixe3.png"),
    4: pygame.image.load("graficos/peixes/peixe4.png"),
    5: pygame.image.load("graficos/peixes/peixe5.png"),
}

conf_peixes = [
    {"sprite": 1, "velocidade": 1, "tamanhos": range(1, 11)},
    {"sprite": 2, "velocidade": 1, "tamanhos": range(11, 19)},
    {"sprite": 3, "velocidade": 3, "tamanhos": range(19, 25)},
    {"sprite": 4, "velocidade": 2, "tamanhos": range(25, 27)},
    {"sprite": 5, "velocidade": 2, "tamanhos": [27]},
]
