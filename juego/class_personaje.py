import pygame


class Personaje:
    tipo = "Personaje"
    def __init__(self, x, y, vidas, animaciones, estado):
        self.estado = estado
        self.animaciones = animaciones
        self.x = x
        self.y = y
        self.vidas = vidas
    def esta_vivo(self):
        return self.vidas > 0


