import random
import time
import matplotlib.pyplot as plt
from Quadtree import armar_quadtree, radio_fuerza_bruta, cercanos_fuerza_bruta

TAMANO_CIUDAD = 10000
RADIO = 500
NUM_CONSULTAS = 200
CANTIDADES = [10, 20, 30, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000]

random.seed(1)


def punto_al_azar():
    return (random.uniform(0, TAMANO_CIUDAD), random.uniform(0, TAMANO_CIUDAD))


def tiempo_promedio(funcion, consultas):
    inicio = time.perf_counter()
    for consulta in consultas:
        funcion(consulta)
    return (time.perf_counter() - inicio) * 1000 / len(consultas)  # en ms


t_armado = []
t_radio_arbol, t_radio_fb = [], []
t_cercano_arbol, t_cercano_fb = [], []

for n in CANTIDADES:
    entregas = [punto_al_azar() for _ in range(n)]
    consultas = [punto_al_azar() for _ in range(NUM_CONSULTAS)]

    inicio = time.perf_counter()
    arbol = armar_quadtree(entregas)
    t_armado.append((time.perf_counter() - inicio) * 1000)  # en ms

    t_radio_arbol.append(tiempo_promedio(lambda c: arbol.buscar_en_radio(c, RADIO), consultas))
    t_radio_fb.append(tiempo_promedio(lambda c: radio_fuerza_bruta(entregas, c, RADIO), consultas))
    t_cercano_arbol.append(tiempo_promedio(lambda c: arbol.mas_cercanos(c, 1), consultas))
    t_cercano_fb.append(tiempo_promedio(lambda c: cercanos_fuerza_bruta(entregas, c, 1), consultas))

    print(f"n={n:6d} | radio: árbol {t_radio_arbol[-1]:8.3f} ms, fb {t_radio_fb[-1]:8.3f} ms"
          f" | cercano: árbol {t_cercano_arbol[-1]:8.3f} ms, fb {t_cercano_fb[-1]:8.3f} ms"
          f" | armado {t_armado[-1]:7.1f} ms")


def desde_que_n_gana(t_arbol, t_fb):
    # primer n a partir del cual el árbol gana en todos los tamaños siguientes
    for i in range(len(CANTIDADES)):
        if all(a < f for a, f in zip(t_arbol[i:], t_fb[i:])):
            return CANTIDADES[i]


n_radio = desde_que_n_gana(t_radio_arbol, t_radio_fb)
n_cercano = desde_que_n_gana(t_cercano_arbol, t_cercano_fb)
print(f"\nEl Quadtree le gana a fuerza bruta en radio desde n = {n_radio}")
print(f"El Quadtree le gana a fuerza bruta en más cercano desde n = {n_cercano}")

plt.figure(figsize=(8, 5))
plt.plot(CANTIDADES, t_radio_arbol, "o-", label="Radio - Quadtree")
plt.plot(CANTIDADES, t_radio_fb, "o-", label="Radio - Fuerza bruta")
plt.plot(CANTIDADES, t_cercano_arbol, "s--", label="Más cercano - Quadtree")
plt.plot(CANTIDADES, t_cercano_fb, "s--", label="Más cercano - Fuerza bruta")
plt.xscale("log")
plt.yscale("log")
plt.xlabel("Cantidad de puntos (n)")
plt.ylabel("Tiempo por consulta (ms)")
plt.title("Quadtree vs fuerza bruta")
plt.legend()
plt.grid(True, which="both", alpha=0.3)
plt.savefig("comparacion_tiempos.png", dpi=120)
plt.close()

plt.figure(figsize=(8, 5))
plt.plot(CANTIDADES, t_armado, "o-", color="purple")
plt.xlabel("Cantidad de puntos (n)")
plt.ylabel("Tiempo de armado (ms)")
plt.title("Tiempo de armado del Quadtree")
plt.grid(True, alpha=0.3)
plt.savefig("armado.png", dpi=120)
plt.close()

i = CANTIDADES.index(10000)
veces_radio = t_radio_fb[i] / t_radio_arbol[i]
veces_cercano = t_cercano_fb[i] / t_cercano_arbol[i]

print(f"""
DISCUSIÓN
El Quadtree le empieza a ganar a fuerza bruta desde {n_cercano} puntos en el más cercano y
{n_radio} en radio. Antes de eso casi no hay diferencia, porque el árbol pierde tiempo en las
llamadas repetidas y con tan pocos puntos no alcanza a descartar nada.

Después la diferencia crece rápido. Fuerza bruta revisa todos los puntos en cada consulta,
así que su tiempo sube con n, mientras que el árbol solo mira los cuadrantes que están cerca.
Con 10.000 puntos el Quadtree fue como {veces_radio:.0f} veces más rápido en radio y
{veces_cercano:.0f} veces más rápido en el más cercano.

Armar el árbol demora unos {t_armado[i]:.0f} ms con 10.000 puntos, pero como los datos no
cambian, solo hay que hacerlo una sola vez y ese tiempo se recupera con pocas consultas.
""")
