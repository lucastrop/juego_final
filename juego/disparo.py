import pygame

class Disparo:
    def __init__(self, x, y, direccion):
        self.superficie = pygame.image.load(r"Recursos\disparo.png")
        self.superficie = pygame.transform.scale(self.superficie, (40,20))
        self.rect = self.superficie.get_rect()
        self.rect.x = x
        self.rect.centery = y
        self.direccion = direccion
    def update(self,pantalla):
        if self.direccion == "derecha":
            self.rect.x += 10
            self.superficie = pygame.image.load(r"Recursos\disparo.png")
        elif self.direccion == "izquierda":
            self.superficie = pygame.image.load(r"Recursos\disparo_izq.png")
            self.rect.x -= 10
        pantalla.blit(self.superficie, self.rect)

