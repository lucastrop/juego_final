import re
import pygame
from pygame.locals import *
from class_personaje import *
from constantes import *
from class_personaje_ppal import *
from class_enemigo1 import *
from configuracion import *

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
    
#PLATAFORMAS

#nivel 1
piso = crear_plataforma((ANCHO_VENTANA,30), (0,670),"Recursos\piso.png")
plataforma1 = crear_plataforma((130,30),(0, 450), "Recursos\plataforma.png")
plataforma2 = crear_plataforma((130,30),(400, 450), "Recursos\plataforma.png")
plataforma3 = crear_plataforma((130,30),(550, 550), "Recursos\plataforma.png")
plataforma4 = crear_plataforma((130,30),(1200, 400), "Recursos\plataforma.png")
plataforma5 = crear_plataforma((130,30),(560, 315), "Recursos\plataforma.png")
plataforma6 = crear_plataforma((130,30),(1200, 450), "Recursos\plataforma.png")
plataforma_larga1 = crear_plataforma((500,30),(800, 200), "Recursos\plataforma.png")
plataforma_larga2 = crear_plataforma((500,30),(0, 200), "Recursos\plataforma.png")
lista_plataformas1 = [piso,plataforma1, plataforma2, plataforma3, plataforma4,plataforma_larga1, plataforma_larga2, plataforma5,plataforma6]

segundos = "120"
fin_tiempo = False

pygame.init()

#TIMER
timer_segundos = pygame.USEREVENT
pygame.time.set_timer(timer_segundos,1000)
fuente = pygame.font.SysFont("Arial", 40)
RELOJ = pygame.time.Clock()

# PANTALLA
ventana_1 = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))

#nivel 1
fondo = pygame.image.load(r"recursos\fondo_bosque_ojitos.jpg").convert()
fondo = pygame.transform.scale(fondo,(ANCHO_VENTANA,ALTO_VENTANA))

pygame.display.set_caption("Fantasmita")

#player
animaciones_ppal = obtener_animaciones()
animaciones_calabaza = obtener_animaciones_calabaza()
player = Personaje_ppal(70, 670, 3, animaciones_ppal, "quieto")

#enemigos
calabaza = Enemigo_1(1000,110,1,animaciones_calabaza,"caminar","calabaza")
lista_enemigos = []
lista_enemigos1 = [calabaza]

#Objetos nivel 1
coin1 = Objeto(250,300,"coin", r"Recursos\coin.png",50,50)
coin2 = Objeto(0,150,"coin", r"Recursos\coin.png",50,50)
coin3 = Objeto(946,430,"coin", r"Recursos\coin.png",50,50)
coin4 = Objeto(62,400,"coin", r"Recursos\coin.png",50,50)
puerta = Objeto(50,100,"puerta",r"Recursos\puerta.png",100,100)
llave = Objeto(1200,140,"llave",r"Recursos\llave.png",100,50)
lista_objetos1 = [coin1,coin2,coin3,coin4,puerta,llave]

correr_nivel1 = True
def sumar_segundos_puntaje(player,segundos):
        player.puntaje += segundos

def funcion_principal(player):
    teclas_presionadas = pygame.key.get_pressed()
    if player.esta_vivo():
        if teclas_presionadas[pygame.K_LEFT]:
            player.estado = "caminar"
            player.mov_izq = True
            player.mover_izq()
        if teclas_presionadas[pygame.K_RIGHT]:
            player.estado = "caminar"
            player.mov_izq = False
            player.mover_der()
        if teclas_presionadas[pygame.K_UP]:
            player.estado = "saltando"
            player.saltar()
            player.movimiento_y()

bandera_play = True
while bandera_play:
    funcion_principal(player)
    lista_eventos = pygame.event.get()
    for evento in lista_eventos:
        if evento.type == pygame.QUIT:
            bandera_play = False
        if evento.type == pygame.USEREVENT:
            if evento.type == timer_segundos:
                if fin_tiempo == False:
                    segundos = int(segundos)- 1
                    if int(segundos) == 0:
                        fin_tiempo = True
                        segundos = "Tiempo"
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                if player.esta_vivo():
                    player.estado = "quieto"
            if evento.key == pygame.K_a and player.atacando == False:
                if player.esta_vivo():
                    player.estado = "quieto"
        if evento.type == pygame.KEYDOWN: 
            if evento.key == pygame.K_TAB:
                cambiar_modo()
            if evento.key == pygame.K_a:
                if player.esta_vivo():
                    player.estado = "atacando"
                    player.atacando = True
                        
        if evento.type == MOUSEBUTTONDOWN:
            print(evento.pos)


    lista_plataformas = lista_plataformas1
    lista_enemigos = lista_enemigos1
    lista_objetos = lista_objetos1

    ventana_1.blit(fondo, (0,0))
    segundos_texto = fuente.render(str(segundos), True, BLANCO)
    ventana_1.blit(segundos_texto, POS_TIMER)
    actualizar_objetos(lista_objetos,ventana_1)
    player.verificar_colision_enemigo(lista_enemigos)
    player.verificar_colision_objeto(lista_objetos,correr_nivel1)
    player.vivir_o_morir()
    if player.abrir_puerta(puerta):
        sumar_segundos_puntaje(player,segundos)
        break
    player.update(ventana_1, lista_plataformas)
    calabaza.moverse()
    calabaza.update(ventana_1)
    print(player.puntaje)
    if obtener_modo():
        for plataforma in lista_plataformas:
            pygame.draw.rect(ventana_1, "red", plataforma["rectangulo"],3)
        pygame.draw.rect(ventana_1,"green", player.rect, 3)
        pygame.draw.rect(ventana_1,"blue", calabaza.rect, 3)
        pygame.draw.rect(ventana_1,"blue", coin1.rect, 3)
    RELOJ.tick(FPS)
    pygame.display.update()
pygame.quit()
