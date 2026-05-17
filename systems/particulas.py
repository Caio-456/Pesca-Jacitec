import pygame
import random


class Particula(pygame.sprite.Sprite):
    def __init__(self, posicao):
        super().__init__()
        self.image = pygame.Surface(
            (3, 2), pygame.SRCALPHA
        )  # SRCALPHA significa que os pixels terão um canal alpha(transparência)
        pygame.draw.circle(self.image, (143, 211, 255), (2, 2), 3)  # cor, centro, raio
        self.rect = self.image.get_rect(center=posicao)
        self.mover_particula_x = random.uniform(-1, 3)
        self.mover_particula_y = random.uniform(1, 3)
        self.timer = 30

    def update(self):
        self.rect.x += self.mover_particula_x  # type: ignore
        self.rect.y += self.mover_particula_y  # type: ignore
        self.timer -= 1
        opacidade = self.timer / 40
        self.image.set_alpha(abs(int(255 * opacidade)))
        if self.timer <= 0:
            self.kill()
