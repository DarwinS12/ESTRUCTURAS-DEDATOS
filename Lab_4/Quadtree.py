import math

LIMITE_PUNTOS = 16  # si un cuadrante pasa de esto, se divide en 4


def distancia(punto_a, punto_b):
    return math.hypot(punto_a[0] - punto_b[0], punto_a[1] - punto_b[1])


class Quadtree:
    def __init__(self, izquierda, abajo, derecha, arriba):
        self.izquierda, self.abajo = izquierda, abajo
        self.derecha, self.arriba = derecha, arriba
        self.centro_x = (izquierda + derecha) / 2
        self.centro_y = (abajo + arriba) / 2
        self.puntos = []
        self.hijos = []  # si está vacío, este cuadrante es una hoja

    def agregar(self, punto):
        if self.hijos:
            self.hijo_donde_cae(punto).agregar(punto)
            return
        self.puntos.append(punto)
        if len(self.puntos) > LIMITE_PUNTOS:
            self.dividir()

    def dividir(self):
        self.hijos = [
            Quadtree(self.izquierda, self.abajo, self.centro_x, self.centro_y),   # abajo-izquierda
            Quadtree(self.centro_x, self.abajo, self.derecha, self.centro_y),     # abajo-derecha
            Quadtree(self.izquierda, self.centro_y, self.centro_x, self.arriba),  # arriba-izquierda
            Quadtree(self.centro_x, self.centro_y, self.derecha, self.arriba),    # arriba-derecha
        ]
        # los puntos que tenía pasan a los hijos
        for punto in self.puntos:
            self.hijo_donde_cae(punto).agregar(punto)
        self.puntos = []

    def hijo_donde_cae(self, punto):
        posicion = 0
        if punto[0] >= self.centro_x:
            posicion += 1
        if punto[1] >= self.centro_y:
            posicion += 2
        return self.hijos[posicion]

    def distancia_al_cuadrante(self, punto):
        # qué tan lejos está el punto del cuadrante (0 si está dentro)
        dx = max(self.izquierda - punto[0], 0, punto[0] - self.derecha)
        dy = max(self.abajo - punto[1], 0, punto[1] - self.arriba)
        return math.hypot(dx, dy)

    def buscar_en_radio(self, centro, radio):
        # si el cuadrante queda fuera del círculo, ni lo revisamos
        if self.distancia_al_cuadrante(centro) > radio:
            return []
        puntos_en_radio = [p for p in self.puntos if distancia(p, centro) <= radio]
        for subcuadrante in self.hijos:
            puntos_en_radio += subcuadrante.buscar_en_radio(centro, radio)
        return puntos_en_radio

    def mas_cercanos(self, punto, cuantos=1, cercanos=None):
        # lista de (distancia, punto) con los más cercanos que llevamos
        if cercanos is None:
            cercanos = []
        if len(cercanos) == cuantos and self.distancia_al_cuadrante(punto) > cercanos[-1][0]:
            return cercanos
        for p in self.puntos:
            cercanos.append((distancia(p, punto), p))
        cercanos.sort()
        del cercanos[cuantos:]
        # miramos primero los hijos más cercanos para poder descartar rápido los demás
        for subcuadrante in sorted(self.hijos, key=lambda sub: sub.distancia_al_cuadrante(punto)):
            subcuadrante.mas_cercanos(punto, cuantos, cercanos)
        return cercanos


def armar_quadtree(puntos):
    coordenadas_x = [p[0] for p in puntos]
    coordenadas_y = [p[1] for p in puntos]
    arbol = Quadtree(min(coordenadas_x), min(coordenadas_y), max(coordenadas_x), max(coordenadas_y))
    for punto in puntos:
        arbol.agregar(punto)
    return arbol


def radio_fuerza_bruta(puntos, centro, radio):
    return [p for p in puntos if distancia(p, centro) <= radio]


def cercanos_fuerza_bruta(puntos, punto, cuantos=1):
    ordenados = sorted((distancia(p, punto), p) for p in puntos)
    return ordenados[:cuantos]
