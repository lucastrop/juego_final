from class_personaje import *
from class_personaje_ppal import *
from configuracion import *
import pygame

class Enemigo_1(Personaje):
    def __init__(self, x, y, vidas, animaciones, estado, nombre):
        super().__init__(x, y, vidas,animaciones, estado) #indica que se comporta como Personaje y le paso lo que necesita como variable, es la herencia)
        self.frame = 0
        self.mov_der = False
        self.animacion_actual = animaciones[estado]
        self.imagen = animaciones[estado][self.frame]
        self.rect = self.imagen.get_rect()
        self.nombre = nombre
        self.rect.x = x
        self.rect.y = y
        self.muriendo = False

    def moverse_izq(self):
        self.rect.x = self.rect.x - 10
    def moverse_der(self):
        self.rect.x = self.rect.x + 10
    def moverse(self):
        if self.esta_vivo():
            if self.mov_der == False:
                self.moverse_izq()
                if self.rect.x == 800:
                    self.mov_der = True
            if self.mov_der:
                self.moverse_der()
                if self.rect.x == 1200:
                    self.mov_der = False


    def update(self, pantalla):
        match self.estado:
            case "caminar":
                self.animacion_actual = self.animaciones["caminar"]
                self.moverse()
                self.animar_enemigo()
                pantalla.blit(self.imagen, self.rect)
            case "muriendo":
                if self.muriendo:
                    self.animacion_actual = self.animaciones["muriendo"]
                    self.animar_enemigo()
                    pantalla.blit(self.imagen, self.rect)


        
    def animar_enemigo(self):
        if self.mov_der:
            if(self.frame < len(self.animacion_actual)-1): #es mas chico que la cantidad que tengo en la animnacion
                self.frame += 1
                self.imagen = pygame.transform.flip(self.animacion_actual[self.frame],-1,False)
            else:
                self.muriendo= False
                self.frame = 0
                self.imagen = pygame.transform.flip(self.animacion_actual[self.frame],-1,False)
        else:
            if(self.frame < len(self.animacion_actual)-1):
                self.frame += 1
                self.imagen = self.animacion_actual[self.frame]
            else:
                self.muriendo = False
                self.frame = 0
                self.imagen = self.animacion_actual[self.frame]
    