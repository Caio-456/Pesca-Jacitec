import pygame


class Botao(pygame.sprite.Sprite):
    global game_state

    def __init__(self, cod):
        super().__init__()
        self.cod = cod
        self.comprado = False
        self.image = botaoFechado.convert_alpha()
        self.rect = self.image.get_rect(topleft=(7, (90 + (59 * cod))))
        self.liberado = False
        match cod:
            case 0:
                self.image = botoesInsuficientes[0].convert_alpha()
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

    def cor(self, game_state):
        if self.liberado:
            if self.comprado is False:
                if game_state.dinheiro >= self.preco:
                    self.image = botoesSuficientes[self.cod].convert_alpha()
                else:
                    self.image = botoesInsuficientes[self.cod].convert_alpha()

    def comprar(self, game_state):  # Checado apenas quando mouse está sobre o botão
        if self.comprado is False:
            if self.liberado:
                if game_state.dinheiro >= self.preco:
                    game_state.melhoria_atual += 1
                    game_state.dinheiro -= self.preco
                    self.image = botoesComprados[self.cod].convert_alpha()
                    self.comprado = True

    def update(self, game_state):
        if game_state.melhoria_atual >= self.cod:
            self.liberado = True
        self.cor(game_state)


botoesInsuficientes = [
    pygame.image.load(f"graficos/botoes/botao{i}-insuficiente.png")
    for i in range(1, 10)
]
botoesSuficientes = [
    pygame.image.load(f"graficos/botoes/botao{i}-suficiente.png") for i in range(1, 10)
]
botoesComprados = [
    pygame.image.load(f"graficos/botoes/botao{i}-comprado.png") for i in range(1, 10)
]
botaoFechado = pygame.image.load("graficos/botoes/botao-fechado.png")
