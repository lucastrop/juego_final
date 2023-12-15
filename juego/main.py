import re
import json
import pygame
from pygame.locals import *
from class_personaje import *
from constantes import *
from class_personaje_ppal import *
from class_enemigo1 import *
from class_enemigo2 import *
from configuracion import *
from configuracion import *
from class_jefe import *

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
    
def guardar_puntaje(nombre_jugador, puntaje): #intenta abrir el archivo, si no existe crea la lista de puntajes y luego con w+ crea y abre el archivo.
    try:
        with open('puntajes.json', 'r') as archivo:
            puntajes = json.load(archivo)
    except FileNotFoundError:
        puntajes = []

    jugador_existente = False
    for jugador in puntajes:
        if jugador["nombre"] == nombre_jugador:
            jugador_existente = True
            # Si el jugador ya existe, se actualiza su puntaje si el nuevo es mayor
            if puntaje > jugador["puntaje"]:
                jugador["puntaje"] = puntaje
            break

    if not jugador_existente:
        puntajes.append({"nombre": nombre_jugador, "puntaje": puntaje})

    with open('puntajes.json', 'w') as archivo:
        json.dump(puntajes, archivo)

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

pygame.display.set_caption("Fantasmita")

#INPUT DE NOMBRE
font = pygame.font.Font(None, 50)
input_box = pygame.Rect(360, 110, 300, 50)
active = False
texto = ""


#player
animaciones_ppal = obtener_animaciones()
animaciones_calabaza = obtener_animaciones_calabaza()
animaciones_fantasma = obtener_animaciones_fantasma()
animaciones_jefe = obtener_animaciones_jefe()
player = Personaje_ppal(70, 670, 3, animaciones_ppal, "quieto")

lista_enemigos = []

#NIVEL 1
#enemigos
calabaza = Enemigo_1(1000,110,1,animaciones_calabaza,"caminar","calabaza")
lista_enemigos1 = [calabaza]
#Objetos nivel 1
coin1 = Objeto(250,350,"coin", r"Recursos\coin.png",50,50)
coin2 = Objeto(0,150,"coin", r"Recursos\coin.png",50,50)
coin3 = Objeto(946,410,"coin", r"Recursos\coin.png",50,50)
coin4 = Objeto(62,400,"coin", r"Recursos\coin.png",50,50)
puerta1 = Objeto(50,100,"puerta",r"Recursos\puerta.png",100,100)
llave1 = Objeto(1200,140,"llave",r"Recursos\llave.png",100,50)
lista_objetos1 = [coin1,coin2,coin3,coin4,puerta1,llave1]
#plataformas nivel 1
piso1 = crear_plataforma((ANCHO_VENTANA,30), (0,670),"Recursos\piso.png")
plataforma1 = crear_plataforma((130,30),(0, 450), "Recursos\plataforma.png")
plataforma2 = crear_plataforma((130,30),(400, 450), "Recursos\plataforma.png")
plataforma3 = crear_plataforma((130,30),(550, 550), "Recursos\plataforma.png")
plataforma4 = crear_plataforma((130,30),(1200,500), "Recursos\plataforma.png") #CAMBIAR A 200
plataforma5 = crear_plataforma((130,30),(560, 315), "Recursos\plataforma.png")
plataforma6 = crear_plataforma((130,30),(210, 400), "Recursos\plataforma.png")
plataforma_larga1 = crear_plataforma((500,30),(800, 200), "Recursos\plataforma.png")
plataforma_larga2 = crear_plataforma((500,30),(0, 200), "Recursos\plataforma.png")
lista_plataformas1 = [piso1,plataforma1, plataforma2, plataforma3, plataforma4,plataforma_larga1, plataforma_larga2, plataforma5,plataforma6]

#NIVEL 2
#plataformas
piso2 = crear_plataforma((ANCHO_VENTANA,30), (0,670),"Recursos\piso_pasto_largo.png")
plat1 = crear_plataforma((130,30),(0, 450), "Recursos\plat1.png")
plat2 = crear_plataforma((130,30),(610, 520), "Recursos\plat1.png")
plat3 = crear_plataforma((130,30),(420, 400), "Recursos\plat1.png")
plat4 = crear_plataforma((130,30),(240, 320), "Recursos\plat1.png")
plat5 = crear_plataforma((130,30),(90, 250), "Recursos\plat1.png")
plat6 = crear_plataforma((130,30),(530, 220), "Recursos\plat1.png")
plat7 = crear_plataforma((130,30),(0, 450), "Recursos\plat1.png")
plat_larga1 = crear_plataforma((500,30),(800, 200), "Recursos\plataforma2.png")
plat_larga2 = crear_plataforma((500,30),(800, 400), "Recursos\plataforma2.png")
lista_plataformas2 = [piso2,plat1,plat2, plat3, plat4, plat5,plat6, plat7, plat_larga1,plat_larga2]
#objetos 2
llave2 = Objeto(120,200,"llave",r"Recursos\llave.png",100,50)
puerta2 = Objeto(1200,300,"puerta",r"Recursos\puerta.png",100,100)
coin5 = Objeto(1230,140,"coin", r"Recursos\coin.png",50,50)
coin6 = Objeto(1220,610,"coin", r"Recursos\coin.png",50,50)
coin7 = Objeto(580,160,"coin", r"Recursos\coin.png",50,50)
coin8 = Objeto(62,390,"coin", r"Recursos\coin.png",50,50)
lista_objetos2 = [llave2,puerta2, coin5,coin6,coin7,coin8]
#enemigos 2
calabaza2 = Enemigo_1(1000,310,1,animaciones_calabaza,"caminar","calabaza")
fantasma = Enemigo_2(700,650,1,animaciones_fantasma,"caminar", "fantasma")
fantasma2 = Enemigo_2(1000,650,1,animaciones_fantasma,"caminar", "fantasma")
lista_enemigos2 = [fantasma,calabaza2, fantasma2]

#NIVEL 3
#plataformas
piso3 = crear_plataforma((ANCHO_VENTANA,30), (0,670),"Recursos\piso.png")
plat8 = crear_plataforma((130,30),(0, 500), "Recursos\plataforma.png")
plat9 = crear_plataforma((130,30),(1170, 500), "Recursos\plataforma.png")
plat10 = crear_plataforma((130,30),(580, 200), "Recursos\plataforma.png")
plataforma_larga4 = crear_plataforma((550,30),(150, 400), "Recursos\plataforma.png")
plataforma_larga5 = crear_plataforma((550,30),(610, 400), "Recursos\plataforma.png")
lista_plataformas3 = [plat8, piso3, plat9, plat10, plataforma_larga4,plataforma_larga5]
#enemigos
jefe = Jefe(700,225, 50, animaciones_jefe,"caminar", "jefe")
fantasma3 = Enemigo_2(400,200,1, animaciones_fantasma, "caminar", "fantasma")
fantasma4 = Enemigo_2(1000,600,1,animaciones_fantasma, "caminar", "fantasma")
fantasma5 = Enemigo_2(700,100,1,animaciones_fantasma,"caminar","fantasma")
lista_enemigos3 = [jefe, fantasma3,fantasma4, fantasma5]
#objetos
llave3 = Objeto(630,330,"llave",r"Recursos\llave.png",100,50)
puerta3 = Objeto(600,100,"puerta",r"Recursos\puerta.png",100,100)
lista_objetos3 = [puerta3]

def sumar_segundos_puntaje(player,segundos):
        player.puntaje += int(segundos)

def reset_enemigos(enemigos:list):
    for enemigo in enemigos:
        if enemigo.nombre == "fantasma" or enemigo.nombre == "calabaza":
            enemigo.vidas = 1
        elif enemigo.nombre == "jefe":
            enemigo.vidas = 50
        enemigo.estado = "caminar"
def reset_player(player):
        player.estado = "quieto"
        player.puntaje = 0
        player.rect.x = 70
        player.rect.y = 670
        player.vidas = 3

def crear_lista_puntajes():
    try:
        with open('puntajes.json', 'r') as archivo:
            puntajes = json.load(archivo)
    except FileNotFoundError:
        puntajes = []
    puntajes_ordenados = ordenar_puntajes(puntajes)
    lista_textos = []
    for puntaje in puntajes_ordenados[:5]:
        texto = f"{puntaje['nombre']} - {puntaje['puntaje']}"
        lista_textos.append(texto)
    return lista_textos
def verificar_5_puntajes(lista_textos):
    if len(lista_textos) == 5:
        return True
    else:
        return False
def obtener_textos_mejores(lista_textos):
        texto1 = f"1° {lista_textos[0]}"
        texto2 = f"2° {lista_textos[1]}"
        texto3 = f"3° {lista_textos[2]}"
        texto4 = f"4° {lista_textos[3]}"
        texto5 = f"5° {lista_textos[4]}"
        return texto1,texto2,texto3,texto4,texto5


enemigos = [calabaza,calabaza2,fantasma,fantasma2,fantasma3,fantasma4,fantasma5,jefe]
nombre_jugador = ""
menu_principal = True
correr_nivel1 = False
correr_nivel2 = False
correr_nivel3 = False
reset_timer = True
bandera_disparo = False
game_over = False
ver_llave = False
mostrar_mejores = False
ingresar_nombre_activo = False
mejores_5 = False
musica = True

pygame.mixer.init()
pygame.mixer.music.load(r"C:\Users\usuario\Downloads\juego\vampire_valtz.mp3")
pygame.mixer.music.play()
pausar_musica = False
pygame.mixer.music.play()
bandera_play = True
while bandera_play:
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
            if evento.key == pygame.K_m and game_over or mostrar_mejores:
                game_over = False
                mostrar_mejores = False
                menu_principal = True
            if evento.key == pygame.K_s and menu_principal:
                if pausar_musica:
                    pygame.mixer.music.unpause()  # Reanudar la música si está pausada
                    pausar_musica = False
                else:
                    pygame.mixer.music.pause()  # Pausar la música si está sonando
                    pausar_musica = True
            if evento.key == pygame.K_q and menu_principal:
                bandera_play = False
            if ingresar_nombre_activo:
                if evento.key == pygame.K_RETURN:
                    nombre_jugador = texto
                    ingresar_nombre_activo = False
                    menu_principal = False
                    correr_nivel1 = True
                    texto = ''
                elif evento.key == pygame.K_BACKSPACE:
                    texto = texto[:-1]
                else:
                    texto += evento.unicode
                width = max(200, font.size(texto)[0]+10)
                input_box.w = width
            if evento.key == pygame.K_h and menu_principal:
                menu_principal = False
                mostrar_mejores = True
            if evento.key == pygame.K_a:
                if player.esta_vivo():
                    player.estado = "atacando"
                    player.atacando = True
                    player.disparar()
        if evento.type == MOUSEBUTTONDOWN:
            if input_box.collidepoint(evento.pos):
                ingresar_nombre_activo = True
            else:
                ingresar_nombre_activo = False
    teclas_presionadas = pygame.key.get_pressed()
    if player.esta_vivo():
        if teclas_presionadas[pygame.K_LEFT]:
            player.estado = "caminar"
            player.mov_der = False
            player.mov_izq = True
            player.mover_izq()
        if teclas_presionadas[pygame.K_RIGHT]:
            player.estado = "caminar"
            player.mov_izq = False
            player.mov_der = True
            player.mover_der()
        if teclas_presionadas[pygame.K_UP]:
            player.estado = "saltando"
            player.saltar()
            player.movimiento_y()
    if menu_principal:
        fondo = pygame.image.load(r"recursos\fondo_principal.jpg").convert()
        fondo = pygame.transform.scale(fondo,(ANCHO_VENTANA,ALTO_VENTANA))
        lista_objetos= []
        lista_plataformas = []
    if mostrar_mejores:
        fondo = pygame.image.load(r"recursos\fondo_puntajes.jpg").convert()
        fondo = pygame.transform.scale(fondo,(ANCHO_VENTANA,ALTO_VENTANA))
        lista_mejores = crear_lista_puntajes()
        if verificar_5_puntajes(lista_mejores):
            cadena1,cadena2,cadena3,cadena4,cadena5 = obtener_textos_mejores(lista_mejores)
            texto_puntaje1 = fuente.render(cadena1, True, BLANCO)
            texto_puntaje2 = fuente.render(cadena2, True, BLANCO)
            texto_puntaje3 = fuente.render(cadena3, True, BLANCO)
            texto_puntaje4 = fuente.render(cadena4, True, BLANCO)
            texto_puntaje5 = fuente.render(cadena5, True, BLANCO)
            mejores_5 = True
        else:
            cadena_error = "Se necesitan al menos 5 puntajes para mostrar los mejores 5"
            texto_error = fuente.render(cadena_error, True, BLANCO) 

    if correr_nivel1:
        if reset_timer == True:
            segundos = "120"
            reset_player(player)
            lista_objetos1 = [coin1,coin2,coin3,coin4,puerta1,llave1]
            lista_objetos2 = [llave2,puerta2, coin5,coin6,coin7,coin8]
            reset_enemigos(enemigos)
            reset_timer = False
        fondo = pygame.image.load(r"recursos\fondo_bosque_ojitos.jpg").convert()
        fondo = pygame.transform.scale(fondo,(ANCHO_VENTANA,ALTO_VENTANA))
        lista_plataformas = lista_plataformas1
        lista_enemigos = lista_enemigos1
        lista_objetos = lista_objetos1
        if player.abrir_puerta(puerta1):
            sumar_segundos_puntaje(player,segundos)
            player.llave = False
            correr_nivel1 = False
            reset_timer = True
            correr_nivel2 = True
        if player.vidas == 0 or segundos == "Tiempo":
            correr_nivel1 = False
            game_over = True
            puntaje_final = player.puntaje

    if correr_nivel2:
        piso2 = crear_plataforma((ANCHO_VENTANA,30), (0,670),"Recursos\piso_pasto.png")
        lista_plataformas = lista_plataformas2
        lista_enemigos = lista_enemigos2
        lista_objetos = lista_objetos2
        if reset_timer == True:
            segundos = "120"
            player.rect.x = 70
            player.rect.y = 670
            reset_timer = False
        fondo = pygame.image.load(r"recursos\fondo_bosque2.jpg").convert()
        fondo = pygame.transform.scale(fondo,(ANCHO_VENTANA,ALTO_VENTANA))
        if player.abrir_puerta(puerta2):
            sumar_segundos_puntaje(player,segundos)
            player.llave = False
            correr_nivel2 = False
            reset_timer = True
            correr_nivel3 = True
        if player.vidas == 0 or segundos == "Tiempo":
            correr_nivel2 = False
            game_over = True
            puntaje_final = player.puntaje
    if correr_nivel3:
        lista_plataformas = lista_plataformas3
        lista_enemigos = lista_enemigos3
        lista_objetos = lista_objetos3
        if reset_timer == True:
            segundos = "120"
            player.rect.x = 70
            player.rect.y = 670
            reset_timer = False
        fondo = pygame.image.load(r"recursos\fondo_violeta.jpg").convert()
        fondo = pygame.transform.scale(fondo,(ANCHO_VENTANA,ALTO_VENTANA))
        if jefe.vidas == 0 and not ver_llave:
            lista_objetos3.append(llave3)
            ver_llave = True
        if player.abrir_puerta(puerta3):
            sumar_segundos_puntaje(player,segundos)
            player.llave = False
            correr_nivel3 = False
            reset_timer = True
            game_over = True
            puntaje_final = player.puntaje 
        if player.vidas == 0 or segundos == "Tiempo":
            correr_nivel3 = False
            game_over = True
            puntaje_final = player.puntaje
    if game_over:
        guardar = True
        if guardar:
            guardar_puntaje(nombre_jugador, puntaje_final)
            guardar = False
        fondo = pygame.image.load(r"recursos\fondo_final.jpg").convert()
        fondo = pygame.transform.scale(fondo,(ANCHO_VENTANA,ALTO_VENTANA))
        reset_timer = True
        lista_objetos= []
        lista_plataformas = []

    if player.vidas  > 0:
        vidas = imagen_vida(player)

    ventana_1.blit(fondo, (0,0))
    if menu_principal:
        pygame.draw.rect(ventana_1, BLANCO, input_box, 2)
        texto_superficie = font.render(texto, True, (255, 255, 255))
        ventana_1.blit(texto_superficie, (input_box.x+5, input_box.y+5))
    if mostrar_mejores:
        if mejores_5:
            ventana_1.blit(texto_puntaje1, (200,200))
            ventana_1.blit(texto_puntaje2, (200,300))
            ventana_1.blit(texto_puntaje3, (200,400))
            ventana_1.blit(texto_puntaje4, (200,500))
            ventana_1.blit(texto_puntaje5, (200,600))
        else:
            ventana_1.blit(texto_error, (200,400))
    puntaje_string = f"Score: {str(player.puntaje)}"
    vidas_jefe = f"{str(jefe.vidas)}/50"
    segundos_texto = fuente.render(str(segundos), True, BLANCO)
    puntaje_texto = fuente.render(puntaje_string, True, BLANCO)
    puntaje_final_texto = fuente.render(str(puntaje_string), True, BLANCO)
    vidas_jefe_texto = fuente.render(vidas_jefe, True, BLANCO)
    if game_over:
        ventana_1.blit(puntaje_final_texto, (500,500))
    if game_over == False and menu_principal == False and mostrar_mejores == False:
        ventana_1.blit(segundos_texto, POS_TIMER)
        ventana_1.blit(puntaje_texto, POS_PUNTAJE)
        ventana_1.blit(vidas, POS_VIDAS)
        actualizar_objetos(lista_objetos,ventana_1)
        player.verificar_colision_enemigo(lista_enemigos)
        player.verificar_colision_objeto(lista_objetos)
        player.vivir_o_morir()
        player.update(ventana_1, lista_plataformas, lista_enemigos)
        for enemigo in lista_enemigos:
            if enemigo.muriendo or enemigo.vidas > 0:
                enemigo.update(ventana_1)
                if correr_nivel3:
                    ventana_1.blit(vidas_jefe_texto, POS_VIDAS_JEFE)
                    corazon_negro = pygame.image.load(r"recursos\corazon_negro.png").convert_alpha()
                    corazon_negro = pygame.transform.scale(corazon_negro,(66,50))
                    ventana_1.blit(corazon_negro, POS_CORAZON_NEGRO)
    if obtener_modo():
        for plataforma in lista_plataformas:
            pygame.draw.rect(ventana_1, "red", plataforma["rectangulo"],3)
        pygame.draw.rect(ventana_1,"green", player.rect, 3)
        pygame.draw.rect(ventana_1,"blue", calabaza.rect, 3)
        pygame.draw.rect(ventana_1,"blue", coin1.rect, 3)
    RELOJ.tick(FPS)
    pygame.display.update()
pygame.quit()
