# --- precios.py ---
# Programa que usa el módulo auxprecios con manejo de errores

import auxprecios

# Caso 1: lista correcta
print("\n=== Caso 1: Lista válida ===")
lista_precios = [10.5, 20.0, 15.75, 30.2, 25.0]
auxprecios.mostrar_precios(lista_precios)
print(f"Suma total: {auxprecios.calcular_suma(lista_precios)}")
print(f"Promedio: {auxprecios.calcular_promedio(lista_precios):.2f}")
print(f"Precio máximo: {auxprecios.precio_maximo(lista_precios)}")

# Caso 2: lista vacía (provoca ValueError controlado)
print("\n=== Caso 2: Lista vacía ===")
lista_vacia = []
auxprecios.mostrar_precios(lista_vacia)
auxprecios.calcular_promedio(lista_vacia)
auxprecios.precio_maximo(lista_vacia)

# Caso 3: lista con error de tipo (provoca TypeError controlado)
print("\n=== Caso 3: Lista con datos no numéricos ===")
lista_erronea = [10, "veinte", 30]
auxprecios.mostrar_precios(lista_erronea)
auxprecios.calcular_suma(lista_erronea)
