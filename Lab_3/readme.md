# Laboratorio 3 — Sistema de Búsqueda de Estudiantes

## 1. Problema y objetivo
Administrar registros de estudiantes (`id`, `nombre`, `edad`, `promedio`) con tres operaciones: **buscar por ID**, **insertar** y **listar en orden ascendente de ID**.

**Objetivo:** medir cómo cambia el tiempo de tres estructuras (Lista, Árbol Binario de Búsqueda y Árbol B+) cuando crece el número de estudiantes N, el número de búsquedas M y el orden de inserción (IDs aleatorios vs. ordenados), y compararlo con la teoría.

## 2. Contenido
```
Lab_3.py
mediciones.csv     # datos crudos (una fila por ejecución, tiempos en segundos)
graficas          
readme.md 
```

## 3. Estructuras
| Estructura | Insertar | Buscar | Idea |
|---|---|---|---|
| **Lista** | O(1) | O(N) | Se agrega al final y se busca uno por uno. Para listar se ordena. |
| **ABB** | O(log N), **O(N) si se desbalancea** | O(log N), **O(N) si se desbalancea** | Menores a la izquierda, mayores a la derecha. Listar = recorrido en orden. |
| **B+** | O(log N) | O(log N) | Nodos con hasta 64 claves; los datos están en hojas enlazadas. Siempre balanceado. |

El código verifica en cada ejecución que el listado salga ordenado por ID.

## 4. Diseño experimental
| Aspecto | Descripción |
|---|---|
| **Hardware** | Computador personal: Windows 11, AMD Ryzen 5 5600G, 32 GB de RAM DDR4 (2 × 16 GB), disco SSD CT2000P3310SSD8. |
| **Software** | Python 3.11.9, `pandas`, `numpy`, `matplotlib` |
| **Tamaños N** | 10, 30, 100, 300, 1.000, 3.000, 10.000 (N pequeños para ver costos fijos; el máximo es 10.000 porque el ABB con IDs ordenados es muy lento en Python) |
| **Búsquedas M** | M = 1.000 al variar N. Al variar M: 100, 1.000 y 10.000 con N = 10.000 |
| **Repeticiones** | 15 por configuración, más 1 de calentamiento que se descarta |
| **Datos** | IDs únicos al azar. *Aleatorio*: se insertan así. *Ordenado*: se insertan de menor a mayor. Mismos datos para las tres estructuras (semilla fija) |
| **Búsquedas** | M IDs elegidos al azar entre los insertados (todas exitosas) |
| **Medición** | `time.perf_counter()`. Se mide el **tiempo total en segundos** de cada operación: insertar los N estudiantes, hacer las M búsquedas, listar los N estudiantes |
| **Valores atípicos** | Se descarta la primera repetición (calentamiento). No se elimina ningún otro dato; la desviación estándar muestra cuánta variación hubo |
| **Estadísticas** | Número de ejecuciones (15), promedio y desviación estándar |

## 5. Cómo repetir el experimento
1. Instalar las librerías (`pip install pandas numpy matplotlib`).
2. Ejecutar `python Lab_3.py`. Genera `mediciones.csv` y `graficas/`.


## 6. Resultados
Tiempos en **segundos**, **promedio ± desviación estándar** de 15 ejecuciones (0,001 s = 1 milisegundo). Las gráficas usan escala logarítmica para que quepan tiempos muy distintos.

### Búsqueda: tiempo de 1.000 búsquedas
| Escenario | Estructura | N=10 | N=100 | N=1.000 | N=10.000 |
|---|---|---|---|---|---|
| aleatorio | Lista | 0,000226 ± 0,000019 | 0,001299 ± 0,000091 | 0,0117 ± 0,0003 | 0,1497 ± 0,0059 |
| aleatorio | ABB | 0,000240 ± 0,000025 | 0,000539 ± 0,000081 | 0,000756 ± 0,000030 | 0,001213 ± 0,000044 |
| aleatorio | B+ | 0,000204 ± 0,000020 | 0,000320 ± 0,000040 | 0,000324 ± 0,000003 | 0,000455 ± 0,000005 |
| ordenado | Lista | 0,000216 ± 0,000022 | 0,001196 ± 0,000084 | 0,0106 ± 0,0003 | 0,1457 ± 0,0043 |
| ordenado | ABB | 0,000358 ± 0,000038 | 0,002800 ± 0,000090 | 0,0289 ± 0,0006 | 0,3648 ± 0,0135 |
| ordenado | B+ | 0,000204 ± 0,000021 | 0,000278 ± 0,000002 | 0,000327 ± 0,000009 | 0,000472 ± 0,000010 |

![Búsqueda](graficas/buscar_s_vs_N.png)

**Cuánto crece el tiempo de búsqueda al multiplicar N por 100 (de N = 100 a N = 10.000).** Si es O(N) debería crecer ≈ 100 veces; si es O(log N), solo ≈ 2 veces.

| Estructura | IDs aleatorios | IDs ordenados |
|---|---|---|
| Lista | 115,3× | 121,9× |
| ABB | 2,3× | 130,3× |
| B+ | 1,4× | 1,7× |

### Inserción: tiempo de insertar N estudiantes
| Escenario | Estructura | N=100 | N=1.000 | N=10.000 |
|---|---|---|---|---|
| aleatorio | Lista | 0,000010 ± 0,000002 | 0,000072 ± 0,000009 | 0,000789 ± 0,000213 |
| aleatorio | ABB | 0,000073 ± 0,000010 | 0,001009 ± 0,000045 | 0,0151 ± 0,0005 |
| aleatorio | B+ | 0,000052 ± 0,000006 | 0,000500 ± 0,000028 | 0,005882 ± 0,000206 |
| ordenado | Lista | 0,000011 ± 0,000001 | 0,000078 ± 0,000015 | 0,000824 ± 0,000147 |
| ordenado | ABB | 0,000426 ± 0,000106 | 0,0368 ± 0,0007 | 4,51 ± 0,06 |
| ordenado | B+ | 0,000043 ± 0,000002 | 0,000439 ± 0,000007 | 0,004872 ± 0,000198 |

![Inserción](graficas/insertar_s_vs_N.png)

Insertar N estudiantes cuesta más cuanto mayor es N. Al multiplicar N por 100 (de 100 a 10.000), el ABB con IDs ordenados crece ≈ 10.600 veces (cada inserción cuesta O(N), así que el total es O(N²), que daría ≈ 10.000). Todas las demás crecen entre 76 y 207 veces, o sea casi en proporción a N (≈ 100 si cada inserción cuesta lo mismo, ≈ 200 si cuesta O(log N)).

### Altura del ABB y relación con el tiempo
| Escenario | N=10 | N=100 | N=1.000 | N=10.000 |
|---|---|---|---|---|
| ABB aleatorio | 5 | 13 | 21 | 30 |
| ABB ordenado | 10 | 100 | 1000 | 10000 |
| log2(N) (ideal) | 3 | 7 | 10 | 13 |

![Altura](graficas/altura_vs_N.png)
![Tiempo vs altura](graficas/tiempo_vs_altura.png)

Cada punto de la segunda gráfica es una ejecución del ABB con 1.000 búsquedas: a más altura, más tiempo (altura 30: 0,0012 s; altura 1.000: 0,029 s; altura 10.000: 0,36 s).

### Efecto de M (N = 10.000, IDs aleatorios): tiempo de las M búsquedas
| Estructura | M=100 | M=1.000 | M=10.000 |
|---|---|---|---|
| Lista | 0,0152 ± 0,0009 | 0,1497 ± 0,0059 | 1,53 ± 0,02 |
| ABB | 0,000128 ± 0,000012 | 0,001213 ± 0,000044 | 0,0120 ± 0,0004 |
| B+ | 0,000051 ± 0,000008 | 0,000455 ± 0,000005 | 0,004451 ± 0,000144 |

![Tiempo vs M](graficas/tiempo_vs_M.png)

### Listado de N estudiantes
![Listado](graficas/listar_s_vs_N.png)

Con N = 10.000: B+ ≈ 0,0001 s; ABB ≈ 0,0011 a 0,0025 s; Lista ≈ 0,0024 s (IDs aleatorios) y 0,0002 s (IDs ordenados).

## 7. Interpretación

- **¿Coincide con la teoría?** Sí. Al multiplicar N por 100 (de 100 a 10.000), la lista crece ≈ 115 y ≈ 122 veces (O(N) daría ≈ 100); el B+ casi no crece (1,4 y 1,7 veces) y el ABB aleatorio crece 2,3 veces (O(log N) daría ≈ 2); y el ABB ordenado crece ≈ 130 veces (O(N)).
- **¿Cuándo deja el ABB de ser O(log N)?** Cuando los IDs se insertan en orden: el árbol queda como una cadena y su altura es N (10, 100, 1.000, 10.000). Con IDs aleatorios la altura es ≈ 30 para N = 10.000 (log₂ N = 13).
- **Altura y tiempo:** el tiempo de búsqueda crece junto con la altura.
- **Datos ordenados:** solo afectan al ABB. Con N = 10.000, 1.000 búsquedas tardan 0,36 s frente a 0,0012 s con IDs aleatorios (≈ 301 veces más) e insertar tarda 4,5 s frente a 0,015 s (≈ 299 veces más). La lista y el B+ casi no cambian.
- **¿Desde qué N se ven las diferencias?** Con N = 10 las tres tardan casi lo mismo (≈ 0,0002 s). Desde N ≈ 100 la lista ya es ≈ 2 veces más lenta que el ABB y ≈ 4 veces más lenta que el B+, y la brecha crece.
- **Costos constantes:** con N pequeño, el costo fijo de llamar la función y recorrer pesa más que la complejidad; por eso la lista (O(N)) empata con los árboles en N = 10. Insertando, la lista es la más rápida siempre (solo agrega al final).
- **Efecto de M:** el tiempo total crece en proporción a M: con 10 veces más búsquedas, ≈ 10 veces más tiempo (lista: de 0,015 a 0,15 a 1,5 s). El orden entre las estructuras no cambia.

## 8. Principales hallazgos
1. Con pocos datos (≈ 10) las tres estructuras son equivalentes; desde ≈ 100 las diferencias son claras.
2. El B+ es el más estable: menos de 0,001 s para 1.000 búsquedas con N = 10.000, sin importar el orden.
3. El ABB es muy bueno con IDs aleatorios, pero con IDs ordenados es el peor, incluso peor que la lista (0,36 s vs 0,15 s con N = 10.000).
4. La altura explica el rendimiento del ABB.


## Nota
El código y el readme fueron hechos con ayuda de inteligencia artificial   
