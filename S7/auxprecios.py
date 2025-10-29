# --- auxprecios.py ---
# Funciones para trabajar con listas de precios, ahora con manejo de errores.

def mostrar_precios(precios):
    """Muestra todos los precios de la lista."""
    try:
        if not precios:
            raise ValueError("La lista de precios está vacía.")
        print("Lista de precios:")
        for p in precios:
            print(f"- ${p:.2f}")
    except ValueError as e:
        print(f"Error: {e}")
    finally:
        print("Fin de la función mostrar_precios().")


def calcular_suma(precios):
    """Devuelve la suma total de los precios."""
    try:
        return sum(precios)
    except TypeError:
        print("Error: La lista contiene elementos no numéricos.")
        return 0


def calcular_promedio(precios):
    """Devuelve el precio promedio."""
    try:
        if len(precios) == 0:
            raise ValueError("No se puede calcular el promedio de una lista vacía.")
    except ValueError as e:
        print(f"Error: {e}")
        return 0
    else:
        return sum(precios) / len(precios)
    finally:
        print("Fin del cálculo de promedio.")


def precio_maximo(precios):
    """Devuelve el precio más alto."""
    try:
        return max(precios)
    except ValueError:
        print("Error: la lista está vacía.")
        return None
