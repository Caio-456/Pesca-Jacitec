class GameState:
    def __init__(self):
        self.dinheiro = 0
        self.melhoria_atual = 0
        self.impedir_jogador_de_mover = True
        self.jogador_pode_rotacionar = False
        self.metodo_de_pesca = "vara"
        self.angulo_jogador = 0
        self.puxar_isca = False
        self.x_player = 0
        self.y_player = 0
        self.click_x = 0
        self.click_y = 0
        self.click_x_alvo = 0
        self.click_y_alvo = 0
