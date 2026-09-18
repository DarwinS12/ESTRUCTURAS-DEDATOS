import hashlib


def calcular_hash(texto):
    """Devuelve el SHA-256 de un texto."""
    return hashlib.sha256(texto.encode()).hexdigest()


def construir_arbol(transacciones):
    """Construye el arbol de Merkle nivel por nivel.
    Nivel 0 = hash de cada transaccion (hojas).
    Cada nivel siguiente = hash de cada par de hijos del nivel anterior."""
    nivel_actual = [calcular_hash(t) for t in transacciones]
    niveles_del_arbol = [nivel_actual]
    while len(nivel_actual) > 1:
        if len(nivel_actual) % 2 != 0:
            nivel_actual = nivel_actual + [nivel_actual[-1]]  # cantidad impar: duplicar el ultimo
        # cada nodo padre = hash de sus dos hijos concatenados
        nivel_actual = [calcular_hash(nivel_actual[i] + nivel_actual[i + 1])
                         for i in range(0, len(nivel_actual), 2)]
        niveles_del_arbol.append(nivel_actual)
    return niveles_del_arbol


def generar_prueba_inclusion(niveles_del_arbol, indice_hoja):
    """Genera la prueba de inclusion: el hash 'hermano' en cada nivel,
    necesario para reconstruir la raiz a partir de una hoja."""
    prueba_inclusion = []
    for nivel in niveles_del_arbol[:-1]:
        if len(nivel) % 2 != 0:
            nivel = nivel + [nivel[-1]]
        if indice_hoja % 2 == 0:
            prueba_inclusion.append((nivel[indice_hoja + 1], False))  # el hermano esta a la derecha
        else:
            prueba_inclusion.append((nivel[indice_hoja - 1], True))   # el hermano esta a la izquierda
        indice_hoja //= 2  # subir al indice del nodo padre, para el siguiente nivel
    return prueba_inclusion


def verificar_prueba_inclusion(transaccion, prueba_inclusion, raiz_esperada):
    """Recalcula la raiz combinando la transaccion con cada hash hermano
    de la prueba, y comprueba si coincide con la raiz esperada."""
    hash_actual = calcular_hash(transaccion)
    for hash_hermano, hermano_es_izquierdo in prueba_inclusion:
        if hermano_es_izquierdo:
            hash_actual = calcular_hash(hash_hermano + hash_actual)
        else:
            hash_actual = calcular_hash(hash_actual + hash_hermano)
    return hash_actual == raiz_esperada


if __name__ == "__main__":
    transacciones = ["Tx1", "Tx2", "Tx3", "Tx4", "Tx5"]

    niveles_del_arbol = construir_arbol(transacciones)
    raiz = niveles_del_arbol[-1][0]
    print("Merkle Raiz:", raiz)

    # Modificar una transaccion y comprobar que la raiz cambia
    transacciones_modificadas = transacciones.copy()
    transacciones_modificadas[1] = "Tx2-modificada"
    nueva_raiz = construir_arbol(transacciones_modificadas)[-1][0]
    print("Nueva Root tras modificar Tx2:", nueva_raiz)

    # Prueba de inclusion de la transaccion 3 (indice 2) y su verificacion
    indice_tx3 = 2
    prueba_tx3 = generar_prueba_inclusion(niveles_del_arbol, indice_tx3)
    print("Verificacion Tx3 (dato correcto):",
          verificar_prueba_inclusion(transacciones[indice_tx3], prueba_tx3, raiz))
    print("Verificacion con dato falso:",
          verificar_prueba_inclusion("dato falso", prueba_tx3, raiz))
