import random
import unittest
import matplotlib.pyplot as plt
from Quadtree import armar_quadtree, radio_fuerza_bruta, cercanos_fuerza_bruta

TAMANO_CIUDAD = 10000  # metros (10 km x 10 km)
RADIO = 500            # metros

random.seed(42)


def punto_al_azar():
    return (random.uniform(0, TAMANO_CIUDAD), random.uniform(0, TAMANO_CIUDAD))


entregas = [punto_al_azar() for _ in range(10000)]
arbol = armar_quadtree(entregas)


class PruebasQuadtree(unittest.TestCase):
    def test_radio_igual_a_fuerza_bruta(self):
        for _ in range(100):
            centro = punto_al_azar()
            esperado = sorted(radio_fuerza_bruta(entregas, centro, RADIO))
            obtenido = sorted(arbol.buscar_en_radio(centro, RADIO))
            self.assertEqual(esperado, obtenido)

    def test_cercanos_igual_a_fuerza_bruta(self):
        for _ in range(100):
            ubicacion = punto_al_azar()
            self.assertEqual(cercanos_fuerza_bruta(entregas, ubicacion, 5),
                             arbol.mas_cercanos(ubicacion, 5))

    def test_radio_sin_puntos(self):
        self.assertEqual(arbol.buscar_en_radio((-50000, -50000), RADIO), [])


def grafica_radio():
    centro = (5000, 5000)
    dentro = arbol.buscar_en_radio(centro, RADIO)
    plt.figure(figsize=(7, 7))
    plt.scatter(*zip(*entregas), s=2, color="lightgray", label="Puntos de entrega")
    plt.scatter(*zip(*dentro), s=12, color="red", label=f"Dentro del radio ({len(dentro)})")
    plt.gca().add_patch(plt.Circle(centro, RADIO, fill=False, color="blue"))
    plt.scatter(*centro, color="blue", marker="x", s=80, label="Centro")
    plt.title(f"Búsqueda por radio de {RADIO} m")
    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    plt.axis("equal")
    plt.legend()
    plt.savefig("radio.png", dpi=120)
    plt.close()


def grafica_cercanos():
    ubicacion = (3000, 7000)
    cercanos = [p for _, p in arbol.mas_cercanos(ubicacion, 5)]
    plt.figure(figsize=(7, 7))
    plt.scatter(*zip(*entregas), s=2, color="lightgray", label="Puntos de entrega")
    plt.scatter(*zip(*cercanos), s=40, color="green", label="5 más cercanos")
    for p in cercanos:
        plt.plot([ubicacion[0], p[0]], [ubicacion[1], p[1]], color="green", linewidth=0.8)
    plt.scatter(*ubicacion, color="blue", marker="x", s=80, label="Ubicación dada")
    plt.title("Puntos más cercanos")
    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    plt.xlim(2700, 3300)  # zoom para que se vean mejor
    plt.ylim(6700, 7300)
    plt.legend()
    plt.savefig("vecinos.png", dpi=120)
    plt.close()


if __name__ == "__main__":
    grafica_radio()
    grafica_cercanos()
    unittest.main()
