import pygame

class Objeto:
    def __init__(self, x, y, tipo, imagen, ancho,alto):
        self.imagen = pygame.image.load(imagen).convert_alpha()
        self.imagen = pygame.transform.scale(self.imagen,(ancho,alto))
        self.rect = self.imagen.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.tipo = tipo
        self.mostrar = True
    def update(self,pantalla):
        if self.mostrar:
            pantalla.blit(self.imagen, self.rect)
    def get_tipo(self):
        return self.tipo

def actualizar_objetos(lista_objetos,pantalla):
    for objeto in lista_objetos:
       objeto.update(pantalla)