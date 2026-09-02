import struct, os
import numpy as np

N = 100000                  # filas = columnas
H = 8                        # header: 2 x uint32 (filas, columnas)
BLOQUE = 5000                # filas por bloque (RAM baja)
ARCHIVO = os.path.join(os.path.expanduser("~/Desktop"), "Darwin_Salazar_Lab_Matriz.bin")


def crear_matriz(archivo=ARCHIVO, n=N, bloque=BLOQUE):
    """Escribe la matriz identidad n x n en disco, 1 bit por celda,
    por bloques de filas (nunca carga la matriz completa en RAM)."""
    with open(archivo, "wb") as f:
        f.write(struct.pack("<II", n, n))          # header: filas, columnas
        for i0 in range(0, n, bloque):
            i1 = min(i0 + bloque, n)
            buf = np.zeros((i1 - i0, n // 8), dtype=np.uint8)  # bloque vacío ya empaquetado (8 columnas por byte)
            filas = np.arange(i0, i1)
            byte_en_fila = filas // 8                 # byte de la fila donde cae el 1 de la diagonal
            bit_en_byte = 7 - (filas % 8)              # bit dentro de ese byte (MSB primero)
            buf[np.arange(i1 - i0), byte_en_fila] |= (1 << bit_en_byte).astype(np.uint8)
            f.write(buf.tobytes())                     # una sola escritura por bloque


def leer_forma(archivo=ARCHIVO):
    """Lee solo el header (8 bytes): no carga el resto del archivo."""
    with open(archivo, "rb") as f:
        return struct.unpack("<II", f.read(H))


def leer_bit(i, j, archivo=ARCHIVO):
    """Lee la celda (i, j) usando filas/columnas del header
    (no carga el resto del archivo)."""
    _, cols = leer_forma(archivo)
    with open(archivo, "rb") as f:
        f.seek(H + i * (cols // 8) + j // 8)  # byte exacto de esa celda
        return (f.read(1)[0] >> (7 - j % 8)) & 1  # bit exacto dentro del byte


if __name__ == "__main__":
    crear_matriz()
    filas, cols = leer_forma()
    tam, esperado = os.path.getsize(ARCHIVO), H + filas * (cols // 8)  # tamaño real vs. esperado
    print(f"Matriz {filas}x{cols} | archivo: {tam/1024**3:.4f} GiB "
          f"(esperado {esperado/1024**3:.4f} GiB)")
    print("M[0][0] =", leer_bit(0, 0), " M[0][1] =", leer_bit(0, 1),
          " M[99999][99999] =", leer_bit(filas - 1, cols - 1))