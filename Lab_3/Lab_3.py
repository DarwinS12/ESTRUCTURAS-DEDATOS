import gc, os, random, time
from bisect import bisect_left, bisect_right
from collections import namedtuple
import numpy as np, pandas as pd, matplotlib.pyplot as plt

Estudiante = namedtuple("Estudiante", "id nombre edad promedio") # namedtuple permite crear tuplas con campos nombrados para acceder fácilmente a cada dato.

TAMANOS_N = [10, 30, 100, 300, 1000, 3000, 10000]    # estudiantes insertados
BUSQUEDAS_M_FIJO = 1000                              # M usado al variar N
TAMANOS_M = [100, 1000, 10000]                       # M usado al variar M (con N = 10000)
REPETICIONES = 15                                    # repeticiones medidas (+1 de calentamiento descartada)
ESCENARIOS = ["aleatorio", "ordenado"]
CONFIGURACIONES = [(n, BUSQUEDAS_M_FIJO) for n in TAMANOS_N] + [(10000, m) for m in TAMANOS_M if m != BUSQUEDAS_M_FIJO]


# ---------------- Estructura 1: Lista desordenada ----------------
class ListaEstudiantes:
    def __init__(self):
        self.estudiantes = []

    def insertar(self, estudiante):
        self.estudiantes.append(estudiante)

    def buscar(self, id_buscado):
        for estudiante in self.estudiantes:
            if estudiante.id == id_buscado:
                return estudiante

    def listar(self):
        return sorted(self.estudiantes)


# ---------------- Estructura 2: Árbol binario de búsqueda ----------------
class ArbolBinarioBusqueda:
    def __init__(self):
        self.raiz = None   # nodo = [estudiante, hijo_izquierdo, hijo_derecho]
        self.altura = 0

    def insertar(self, estudiante):
        nuevo_nodo, profundidad, nodo = [estudiante, None, None], 1, self.raiz
        if nodo is None:
            self.raiz = nuevo_nodo
        while nodo is not None:
            profundidad += 1
            lado = 1 if estudiante.id < nodo[0].id else 2
            if nodo[lado] is None:
                nodo[lado] = nuevo_nodo
                break
            nodo = nodo[lado]
        self.altura = max(self.altura, profundidad)

    def buscar(self, id_buscado):
        nodo = self.raiz
        while nodo is not None and nodo[0].id != id_buscado:
            nodo = nodo[1] if id_buscado < nodo[0].id else nodo[2]
        return nodo[0] if nodo else None

    def listar(self):   # recorrido en orden sin recursión
        resultado, pila, nodo = [], [], self.raiz
        while pila or nodo:
            while nodo:
                pila.append(nodo)
                nodo = nodo[1]
            nodo = pila.pop()
            resultado.append(nodo[0])
            nodo = nodo[2]
        return resultado


# ---------------- Estructura 3: Árbol B+ ----------------
class NodoBMas:
    def __init__(self, es_hoja):
        self.es_hoja, self.claves, self.hijos, self.siguiente = es_hoja, [], [], None


class ArbolBMas:
    def __init__(self, maximo_claves=64):
        self.maximo_claves = maximo_claves
        self.raiz = NodoBMas(es_hoja=True)

    def _buscar_hoja(self, id_buscado, camino=None):
        nodo = self.raiz
        while not nodo.es_hoja:
            if camino is not None:
                camino.append(nodo)
            nodo = nodo.hijos[bisect_right(nodo.claves, id_buscado)]
        return nodo

    def buscar(self, id_buscado):
        hoja = self._buscar_hoja(id_buscado)
        posicion = bisect_left(hoja.claves, id_buscado) # bisect_left encuentra la posición a la izquierda donde debería estar el ID en la lista ordenada de claves
        if posicion < len(hoja.claves) and hoja.claves[posicion] == id_buscado:
            return hoja.hijos[posicion]

    def insertar(self, estudiante):
        camino = []
        nodo = self._buscar_hoja(estudiante.id, camino)
        posicion = bisect_left(nodo.claves, estudiante.id)
        nodo.claves.insert(posicion, estudiante.id)
        nodo.hijos.insert(posicion, estudiante)
        while len(nodo.claves) > self.maximo_claves:   # dividir el nodo desbordado
            medio = len(nodo.claves) // 2
            hermano = NodoBMas(nodo.es_hoja)
            if nodo.es_hoja:
                hermano.claves, hermano.hijos = nodo.claves[medio:], nodo.hijos[medio:]
                nodo.claves, nodo.hijos = nodo.claves[:medio], nodo.hijos[:medio]
                hermano.siguiente, nodo.siguiente = nodo.siguiente, hermano
                clave_subida = hermano.claves[0]
            else:
                clave_subida = nodo.claves[medio]
                hermano.claves, hermano.hijos = nodo.claves[medio + 1:], nodo.hijos[medio + 1:]
                nodo.claves, nodo.hijos = nodo.claves[:medio], nodo.hijos[:medio + 1]
            if not camino:
                self.raiz = NodoBMas(es_hoja=False)
                self.raiz.claves, self.raiz.hijos = [clave_subida], [nodo, hermano]
                return
            padre = camino.pop()
            posicion = bisect_right(padre.claves, clave_subida)
            padre.claves.insert(posicion, clave_subida)
            padre.hijos.insert(posicion + 1, hermano)
            nodo = padre

    def listar(self):   # recorre las hojas enlazadas desde la más a la izquierda
        hoja, resultado = self.raiz, []
        while not hoja.es_hoja:
            hoja = hoja.hijos[0]
        while hoja:
            resultado.extend(hoja.hijos)
            hoja = hoja.siguiente
        return resultado


ESTRUCTURAS = {"Lista": ListaEstudiantes, "ABB": ArbolBinarioBusqueda, "B+": ArbolBMas}


# ---------------- Experimentos ----------------
def medir(funcion):
    inicio = time.perf_counter()
    resultado = funcion()
    return time.perf_counter() - inicio, resultado


def ejecutar_experimentos():
    filas = []
    gc.disable()   # evita pausas del recolector de basura dentro de las mediciones
    for n, m in CONFIGURACIONES:
        for escenario in ESCENARIOS:
            for repeticion in range(REPETICIONES + 1):   # la repetición 0 es calentamiento y se descarta
                random.seed(repeticion)
                ids = random.sample(range(10 * n), n)
                if escenario == "ordenado":
                    ids.sort()
                estudiantes = [Estudiante(i, f"Estudiante {i}", random.randint(17, 30), round(random.uniform(0, 5), 2)) for i in ids]
                ids_buscados = random.choices(ids, k=m)
                for nombre, clase in ESTRUCTURAS.items():
                    estructura = clase()
                    t_insertar, _ = medir(lambda: [estructura.insertar(e) for e in estudiantes])
                    t_buscar, _ = medir(lambda: [estructura.buscar(i) for i in ids_buscados])
                    t_listar, listado = medir(estructura.listar)
                    assert [e.id for e in listado] == sorted(ids)   # verifica que el listado sea correcto
                    if repeticion > 0:
                        filas.append(dict(N=n, M=m, escenario=escenario, estructura=nombre, repeticion=repeticion,
                                          insertar_s=t_insertar,   # segundos para insertar los N estudiantes
                                          buscar_s=t_buscar,       # segundos para hacer las M búsquedas
                                          listar_s=t_listar,       # segundos para listar los N estudiantes
                                          altura=getattr(estructura, "altura", np.nan)))
                print(f"N={n} M={m} {escenario} repetición {repeticion}/{REPETICIONES}")
    gc.enable()
    return pd.DataFrame(filas)


def resumir(mediciones):
    resumen = mediciones.groupby(["N", "M", "escenario", "estructura"])[["insertar_s", "buscar_s", "listar_s", "altura"]].agg(["count", "mean", "std"])
    resumen.columns = [f"{columna}_{estadistico}" for columna, estadistico in resumen.columns]
    return resumen.reset_index()


# ---------------- Gráficas ----------------
def grafica_tiempo_vs_n(resumen, columna, titulo):
    datos = resumen[resumen.M == BUSQUEDAS_M_FIJO]
    figura, ejes = plt.subplots(1, 2, figsize=(12, 4.5), sharey=True)
    for eje, escenario in zip(ejes, ESCENARIOS):
        for estructura in ESTRUCTURAS:
            d = datos[(datos.escenario == escenario) & (datos.estructura == estructura)]
            eje.errorbar(d.N, d[columna + "_mean"], yerr=d[columna + "_std"], marker="o", capsize=3, label=estructura)
        eje.set(xscale="log", yscale="log", xlabel="Tamaño de entrada N (estudiantes)", ylabel=f"{titulo} (segundos)",
                title=f"IDs {escenario}s")
        eje.grid(True, which="both", alpha=0.3)
        eje.legend(title="Estructura")
    figura.suptitle(f"{titulo} vs N (promedio ± desviación estándar, {REPETICIONES} repeticiones, M={BUSQUEDAS_M_FIJO})")
    figura.tight_layout()
    figura.savefig(f"graficas/{columna}_vs_N.png", dpi=150)


def grafica_altura_vs_n(resumen):
    plt.figure(figsize=(7, 4.5))
    for escenario in ESCENARIOS:
        d = resumen[(resumen.M == BUSQUEDAS_M_FIJO) & (resumen.escenario == escenario) & (resumen.estructura == "ABB")]
        plt.errorbar(d.N, d.altura_mean, yerr=d.altura_std, marker="o", capsize=3, label=f"ABB con IDs {escenario}s")
    plt.plot(TAMANOS_N, np.log2(TAMANOS_N), "k--", label="log2(N) (altura ideal)")
    plt.xscale("log"), plt.yscale("log"), plt.grid(True, which="both", alpha=0.3), plt.legend()
    plt.xlabel("Tamaño de entrada N (estudiantes)"), plt.ylabel("Altura del ABB (niveles)")
    plt.title("Altura del ABB vs N (promedio ± desviación estándar)")
    plt.tight_layout(), plt.savefig("graficas/altura_vs_N.png", dpi=150)


def grafica_tiempo_vs_altura(mediciones):
    plt.figure(figsize=(7, 4.5))
    for escenario in ESCENARIOS:
        d = mediciones[(mediciones.estructura == "ABB") & (mediciones.escenario == escenario) & (mediciones.M == BUSQUEDAS_M_FIJO)]
        plt.scatter(d.altura, d.buscar_s, label=f"ABB con IDs {escenario}s")
    plt.xscale("log"), plt.yscale("log"), plt.grid(True, which="both", alpha=0.3), plt.legend()
    plt.xlabel("Altura del ABB (niveles)"), plt.ylabel(f"Tiempo de {BUSQUEDAS_M_FIJO} búsquedas (segundos)")
    plt.title("Tiempo de búsqueda vs altura del ABB (cada punto es una ejecución)")
    plt.tight_layout(), plt.savefig("graficas/tiempo_vs_altura.png", dpi=150)


def grafica_tiempo_vs_m(resumen):
    plt.figure(figsize=(7, 4.5))
    for estructura in ESTRUCTURAS:
        d = resumen[(resumen.N == 10000) & (resumen.escenario == "aleatorio") & (resumen.estructura == estructura)]
        plt.errorbar(d.M, d.buscar_s_mean, yerr=d.buscar_s_std, marker="o", capsize=3, label=estructura)
    plt.xscale("log"), plt.yscale("log"), plt.grid(True, which="both", alpha=0.3), plt.legend(title="Estructura")
    plt.xlabel("Número de búsquedas M"), plt.ylabel("Tiempo de las M búsquedas (segundos)")
    plt.title("Tiempo de búsqueda vs M (N=10000, IDs aleatorios)")
    plt.tight_layout(), plt.savefig("graficas/tiempo_vs_M.png", dpi=150)


if __name__ == "__main__":
    os.makedirs("graficas", exist_ok=True)
    mediciones = ejecutar_experimentos()
    mediciones.to_csv("mediciones.csv", index=False)   # una fila por ejecución
    resumen = resumir(mediciones)
    grafica_tiempo_vs_n(resumen, "buscar_s", "Tiempo de las M búsquedas")
    grafica_tiempo_vs_n(resumen, "insertar_s", "Tiempo de insertar N estudiantes")
    grafica_tiempo_vs_n(resumen, "listar_s", "Tiempo de listar N estudiantes")
    grafica_altura_vs_n(resumen)
    grafica_tiempo_vs_altura(mediciones)
    grafica_tiempo_vs_m(resumen)