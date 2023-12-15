import pygame
from pygame.locals import *
from class_personaje import *
from constantes import *
from class_personaje_ppal import *
from class_enemigo1 import *


DEBUG = False #para ver hitboxs

def cambiar_modo():
    global DEBUG
    DEBUG = not DEBUG  

def obtener_modo():
    return DEBUG

nivel_1 = False
nivel_2 = False
nivel_3 = False

def imagen_vida(player):
    if player.vidas == 3:
        imagen = pygame.image.load(r"Recursos\3corazon.png").convert_alpha()
        imagen= pygame.transform.scale(imagen,(200,50))
    elif player.vidas == 2:
        imagen = pygame.image.load(r"Recursos\2corazon.png").convert_alpha()
        imagen= pygame.transform.scale(imagen,(133,50))
    elif player.vidas == 1:
        imagen = pygame.image.load(r"Recursos\1corazon.png").convert_alpha()
        imagen= pygame.transform.scale(imagen,(66,50))
    return imagen

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

def obtener_animaciones():
    diccionario_animaciones ={}
    diccionario_animaciones["quieto"] = obtener_sup_sprite(r"Recursos\fantasmita_quieto.png",1,1)
    diccionario_animaciones["caminar"] = obtener_sup_sprite(r"Recursos\fantasmita_caminarder.png",1,6)
    diccionario_animaciones["saltando"] = obtener_sup_sprite(r"Recursos\fantasmita_saltando.png",1,1)
    diccionario_animaciones["auch"] = obtener_sup_sprite(r"Recursos\fantasmita_cayendo.png",1,1)
    diccionario_animaciones["atacando"] = obtener_sup_sprite(r"Recursos\fantasmita_atacando.png",1,5)
    diccionario_animaciones["escudo"] = obtener_sup_sprite(r"Recursos\fantasmita_escudo.png",1,5)
    diccionario_animaciones["muriendo"] = obtener_sup_sprite(r"Recursos\fantasmita_muriendo.png",1,5)
    return diccionario_animaciones

def obtener_animaciones_calabaza():
    diccionario_animaciones ={}
    diccionario_animaciones["caminar"] = obtener_sup_sprite(r"Recursos\calabaza.png",1,6)
    diccionario_animaciones["muriendo"] = obtener_sup_sprite(r"Recursos\calabaza_muriendo.png",1,4)
    return diccionario_animaciones

def obtener_animaciones_fantasma():
    diccionario_animaciones ={}
    diccionario_animaciones["caminar"] = obtener_sup_sprite(r"Recursos\fantasma.png",1,6)
    diccionario_animaciones["auch"] = obtener_sup_sprite(r"Recursos\fantasma_auch.png",1,1)
    diccionario_animaciones["muriendo"] = obtener_sup_sprite(r"Recursos\fantasma_muriendo.png",1,6)
    return diccionario_animaciones

def obtener_animaciones_jefe():
    diccionario_animaciones ={}
    diccionario_animaciones["caminar"] = obtener_sup_sprite(r"Recursos\jefe_caminarg.png",1,4)
    diccionario_animaciones["quieto"] = obtener_sup_sprite(r"Recursos\jefe_quieto.png",1,6)
    diccionario_animaciones["muriendo"] = obtener_sup_sprite(r"Recursos\jefe_muriendo.png",1,8)
    return diccionario_animaciones

def crear_plataforma(tamanio, posicion, path_imagen=""):
    plataforma ={}
    plataforma["superficie"] = pygame.image.load(path_imagen)
    plataforma["superficie"] = pygame.transform.scale(plataforma["superficie"], tamanio)
    plataforma["rectangulo"] = plataforma["superficie"].get_rect()
    x, y = posicion
    plataforma["rectangulo"].x = x
    plataforma["rectangulo"].y = y
    plataforma["posicion"] = posicion
    return plataforma

def ordenar_puntajes(puntajes): #metodo burbujeo
    n = len(puntajes)

    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if puntajes[j]["puntaje"] < puntajes[j + 1]["puntaje"]:
                puntajes[j], puntajes[j + 1] = puntajes[j + 1], puntajes[j]

    return puntajes