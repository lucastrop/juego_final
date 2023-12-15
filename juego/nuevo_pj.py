from class_personaje import *
from pygame.locals import *
from constantes import *
import pygame
def girar_imagenes(lista_original, flip_x, flip_y):
    lista_girada = []

    for imagen in lista_original:
        lista_girada.append(pygame.transform.flip(imagen, flip_x, flip_y))
def obtener_animaciones():
    diccionario_animaciones ={}
    diccionario_animaciones["quieto"] = obtener_sup_sprite(r"Recursos\fantasmita_quieto.png",1,1)
    diccionario_animaciones["caminarizq"] = obtener_sup_sprite(r"Recursos\fantasmita_caminarizq.png",1,6)
    diccionario_animaciones["caminarder"] = obtener_sup_sprite(r"Recursos\fantasmita_caminarder.png",1,6)
    diccionario_animaciones["saltando"] = obtener_sup_sprite(r"Recursos\fantasmita_saltando.png",1,1)
    diccionario_animaciones["cayendo"] = obtener_sup_sprite(r"Recursos\fantasmita_cayendo.png",1,1)
    diccionario_animaciones["atacando"] = obtener_sup_sprite(r"Recursos\fantasmita_atacando.png",1,5)
    diccionario_animaciones["escudo"] = obtener_sup_sprite(r"Recursos\fantasmita_escudo.png",1,5)
    return diccionario_animaciones

def obtener_sup_sprite(path,filas, columnas):
    lista = []
    superficie_imagen = pygame.image.load(path).convert_alpha()
    fotograma_ancho = int(superficie_imagen.get_width()/columnas)
    fotograma_alto = int(superficie_imagen.get_height()/filas)
    for columna in range(columnas):
        for fila in range(filas):
            x = columna * fotograma_ancho
            y = fila * fotograma_alto
            superficie_fotograma = superficie_imagen.subsurface(x,y,fotograma_ancho, fotograma_alto) #toma un pedazo de la superficie)
            lista.append(superficie_fotograma)
    return lista


class Nuevo(Personaje):
    def __init__(self, x, vidas, y, animaciones, estado):
        super().__init__(x, vidas)
        self.animaciones = animaciones
        self.estado = estado
        self.contador_pasos = 0
        self.animacion_actual = animaciones[estado]
        self.imagen = animaciones[estado][self.contador_pasos]
        largo = self.imagen.get_height
        print(largo)
        self.rect = self.imagen.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.saltando = False
        self.velocidad = 10
        self.limite_salto = 10
        self.velocidad_y = 0
        self.gravedad = 2
        self.mov_izq = False
    def saltar(self):
        if not self.saltando:
            self.velocidad_y = -15
            self.saltando = True
    def mover_der(self):
        nueva_x = self.rect.x + self.velocidad
        if(nueva_x > 0 and nueva_x < ANCHO_VENTANA-70):
            self.rect.x = nueva_x
    def mover_izq(self):
        nueva_x = self.rect.x - self.velocidad
        if(nueva_x > 0 and nueva_x < ANCHO_VENTANA-70):
            self.rect.x = nueva_x
    def aplicar_gravedad(self):
        self.velocidad_y += self.gravedad
        self.rect.y += self.velocidad_y
        if self.rect.y > ALTO_VENTANA - 70: #para que no se salga de la pantalla
                self.rect.y = ALTO_VENTANA - 70
                self.saltando = False
                self.velocidad_y = 0

    def movimiento_y(self):
        if self.saltando:
            self.rect.y += self.velocidad_y

    def animar(self):
        if self.mov_izq:
            if(self.contador_pasos < len(self.animacion_actual)-1): #es mas chico que la cantidad que tengo en la animnacion
                    self.contador_pasos += 1
                    self.imagen = pygame.transform.flip(self.animacion_actual[self.contador_pasos],-1,False)
            else:
                self.contador_pasos = 0
                self.imagen = pygame.transform.flip(self.animacion_actual[self.contador_pasos],-1,False)
        else:
            if(self.contador_pasos < len(self.animacion_actual)-1): 
                self.contador_pasos += 1
                self.imagen = self.animacion_actual[self.contador_pasos]
            else:
                self.contador_pasos = 0
                self.imagen = self.animacion_actual[self.contador_pasos]

    def update(self, pantalla):
        match self.estado:
            case "caminarder":
                if not self.saltando:
                    self.animacion_actual = self.animaciones["caminarder"]
                elif self.saltando:
                    self.animacion_actual = self.animaciones["saltando"]
                self.animar()
            case "caminarizq":
                if not self.saltando:
                    self.animacion_actual = self.animaciones["caminarder"]
                elif self.saltando:
                    self.animacion_actual = self.animaciones["saltando"]
                self.animar()
            case "quieto":
                if not self.saltando:
                    self.animacion_actual = self.animaciones["quieto"]
                    self.animar()
            case "saltando":
                    self.saltando = True
                    self.animacion_actual = self.animaciones["saltando"]
                    self.animar()
            # case "cayendo":
            #     if not self.saltando:
            #         self.esta_saltando = True
            #         # self.desplazamiento_y = self.potencia_salto
            #         self.animacion_actual = self.animaciones["saltando"]
            #         self.animar()
        pantalla.blit(self.imagen, self.rect)