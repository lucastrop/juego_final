from class_personaje import *
from pygame.locals import *
from constantes import *
from configuracion import *
from botin import *
import pygame
from disparo import *

class Personaje_ppal(Personaje):
    def __init__(self, x, y, vidas, animaciones, estado):
        super().__init__(x, y, vidas, animaciones, estado)
        self.contador_pasos = 0
        self.animacion_actual = animaciones[estado]
        self.imagen = animaciones[estado][self.contador_pasos]
        self.rect = self.imagen.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.saltando = False
        self.velocidad = 10
        self.velocidad_y = 0
        self.gravedad = 3
        self.mov_izq = False
        self.mov_der = False
        self.atacando =False
        self.muriendo = False
        self.puntaje = 0
        self.llave = False
        self.proyectiles = []
    def saltar(self):
        if not self.saltando:
            self.velocidad_y = -20
            self.saltando = True
    def mover_der(self):
        nueva_x = self.rect.x + self.velocidad
        if(nueva_x > 0 and nueva_x < ANCHO_VENTANA-70):
            self.rect.x = nueva_x
    def mover_izq(self):
        nueva_x = self.rect.x - self.velocidad
        if(nueva_x > 0 and nueva_x < ANCHO_VENTANA-70):
            self.rect.x = nueva_x

    def aplicar_gravedad(self,lista_plataformas):
        self.velocidad_y += self.gravedad
        self.rect.y += self.velocidad_y

        for plataforma in lista_plataformas:
            if self.rect.colliderect(plataforma["rectangulo"]):
                self.saltando = False
                self.velocidad_y = 0
                self.rect.bottom = plataforma["rectangulo"].top
                break

    def movimiento_y(self):
        if self.saltando:
            self.rect.y += self.velocidad_y

    def animar(self):
        if self.mov_izq:
            if(self.contador_pasos < len(self.animacion_actual)-1): #es mas chico que la cantidad que tengo en la animnacion
                self.contador_pasos += 1
                self.imagen = pygame.transform.flip(self.animacion_actual[self.contador_pasos],-1,False)
            else:
                self.atacando = False
                self.contador_pasos = 0
                self.imagen = pygame.transform.flip(self.animacion_actual[self.contador_pasos],-1,False)
        else:
            if(self.contador_pasos < len(self.animacion_actual)-1):
                self.contador_pasos += 1
                self.imagen = self.animacion_actual[self.contador_pasos]
            else:
                self.atacando = False
                self.contador_pasos = 0
                self.imagen = self.animacion_actual[self.contador_pasos]

    def update(self, pantalla, lista_plataformas, lista_enemigos):
        match self.estado:
            case "caminar":
                if not self.saltando and self.esta_vivo():
                    self.animacion_actual = self.animaciones["caminar"]
                elif self.saltando and self.esta_vivo():
                    self.animacion_actual = self.animaciones["saltando"]
                self.animar()
            case "quieto":
                if not self.saltando and self.esta_vivo():
                    self.animacion_actual = self.animaciones["quieto"]
                    self.animar()
            case "saltando":
                    if self.esta_vivo():
                        self.animacion_actual = self.animaciones["saltando"]
                        self.animar()
            case "atacando":
                 if self.esta_vivo():
                    if self.atacando == True:
                        self.animacion_actual = self.animaciones["atacando"]
                    else:
                        self.estado = "quieto"
                    self.animar()
            case "auch":
                if self.esta_vivo():
                    self.animacion_actual = self.animaciones["auch"]
                    self.animar()
            case "muriendo":
                self.animacion_actual = self.animaciones["muriendo"]
                self.animar()
        
        self.actualizar_proyectiles(pantalla, lista_enemigos)          
        self.aplicar_gravedad(lista_plataformas)
        for plataforma in lista_plataformas:
            pantalla.blit(plataforma["superficie"], plataforma["rectangulo"])
        pantalla.blit(self.imagen, self.rect)

    def verificar_colision_enemigo(self, lista_enemigos):
        if self.vidas > 0:
            for enemigo in lista_enemigos:
                if self.rect.colliderect(enemigo.rect) and enemigo.esta_vivo():
                    self.estado = "auch"
                    self.vidas -= 1
                    nueva_x = self.rect.x -100
                    if nueva_x > 0:
                        self.rect.x -= 100
                    self.rect.y -= 50

    def vivir_o_morir(self): #verifica si sigue vivo y de ser que no entra en estado muriendo
        if not self.esta_vivo():
            self.estado = "muriendo"

    def verificar_colision_objeto(self,lista_objetos):
        if self.vidas > 0:
            for objeto in lista_objetos:
                if self.rect.colliderect(objeto.rect):
                        if objeto.tipo == "coin":
                            self.puntaje += 10
                            lista_objetos.remove(objeto)
                        if objeto.tipo == "llave":
                            lista_objetos.remove(objeto)
                            self.llave = True

    def abrir_puerta(self,puerta):
        if self.llave:
            if self.rect.colliderect(puerta.rect):
                return True

    def disparar(self):
        x = None
        y = self.rect.centery + 10
        if self.mov_der:
            direccion = "derecha"
            x = self.rect.right
        elif self.mov_izq:
            x = self.rect.left -20
            direccion = "izquierda"
        if x is not None:
            self.proyectiles.append(Disparo(x,y,direccion))
        

    def actualizar_proyectiles(self,pantalla,lista_enemigos): #verifica colision con enemigos y elimina el disparo si colisiona/llega al borde de la pantalla
        i = 0
        while i < len(self.proyectiles):
            proyectil = self.proyectiles[i]
            proyectil.update(pantalla)
            if proyectil.rect.centerx < 0 or proyectil.rect.centerx > ANCHO_VENTANA:
                self.proyectiles.pop(i)
                i -= 1
            for enemigo in lista_enemigos:    
                if proyectil.rect.colliderect(enemigo.rect) and enemigo.vidas > 0:
                    enemigo.vidas -= 1
                    if enemigo.vidas == 0:
                        self.puntaje += 20
                        enemigo.muriendo = True
                        enemigo.estado = "muriendo"
                    self.proyectiles.pop(i)
                    i -=1
            i += 1