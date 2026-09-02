# Laboratorio 1 - Estructura de Datos

**Estudiante:** DARWIN ESTEBAN SALAZAR GARCIA

## Objetivo

Escribir una matriz de 100.000 x 100.000 en disco duro y mostrar su
contenido, sin agotar la memoria RAM y sin desperdiciar espacio en disco.

## Archivos

- `Darwin_Salazar_Lab_Creacion_Matriz.py`: código del laboratorio. Al ejecutarlo crea `Darwin_Salazar_Lab_Matriz.bin` y
  muestra su contenido.
- `Darwin_Salazar_Lab_Matriz.bin`: el archivo generado (no se sube al repo por su tamaño;
  se genera corriendo `Darwin_Salazar_Lab_Creacion_Matriz.py`). Pesa 1.1642 GiB.

Para correrlo:

```bash
python3 Darwin_Salazar_Lab_Creacion_Matriz.py
```

## El problema y cómo se resuelve

La matriz tiene 10.000 millones de celdas. Armarla completa en RAM ocuparía varios gigas y
podría colgar el computador, entonces `crear_matriz()` la escribe en disco
de a bloques de 5.000 filas, usando solo unos pocos MB de RAM a la vez. Cada
bloque se arma de una vez con NumPy y se guarda con una sola escritura, en
vez de escribir un byte a la vez muchas veces.

Como cada celda solo vale 0 o 1 (es una matriz identidad), se guardan 8
celdas por byte (1 bit por celda) en vez de un byte completo por celda.
Eso hace que el archivo pese 8 veces menos: 1.1642 GiB en vez de 9.31 GB.

Además, el archivo empieza con un encabezado que dice cuántas filas y
columnas tiene. Con ese dato se puede calcular en qué byte empieza
cualquier fila, así que es una matriz de verdad y no una simple fila de
bytes pegados.

## Cómo verificar que el archivo quedó bien

Al terminar de ejecutarse, el script imprime dos cosas para comprobar que
todo salió correcto:

1. El tamaño real del archivo contra el tamaño que debería tener según el
   encabezado (filas, columnas y bits por celda). Si coinciden, el archivo
   tiene exactamente el tamaño de una matriz de 100.000 x 100.000
   empaquetada en bits.
2. El valor de tres celdas puntuales: `M[0][0]` y `M[99999][99999]` deben
   dar 1 porque están en la diagonal de la matriz identidad, y `M[0][1]`
   debe dar 0 porque está fuera de la diagonal.

Esta es la salida real al correr el script:

```
Matriz 100000x100000 | archivo: 1.1642 GiB (esperado 1.1642 GiB)
M[0][0] = 1  M[0][1] = 0  M[99999][99999] = 1
```