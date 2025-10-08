# Programa que pide una lista de números, calcula suma, media, máximo y detecta duplicados
# con control de errores y verificación de valores numéricos

while True:
    try:
        # Pedir la lista de números separados por comas
        entrada = input("Introduce una lista de números separados por comas: ")

        # Verificar que el usuario no haya dejado la entrada vacía
        if not entrada.strip():
            raise ValueError("La lista no puede estar vacía.")

        # Convertir la cadena en una lista de floats
        numeros_str = [x.strip() for x in entrada.split(",")]
        
        numeros = []
        for x in numeros_str:
            try:
                numeros.append(float(x))
            except ValueError:
                raise ValueError(f"'{x}' no es un número válido.")

        # Verificar que la lista tenga al menos un número válido
        if len(numeros) == 0:
            raise ValueError("No se detectaron números válidos.")

        # Si todo está correcto, salir del bucle
        break

    except ValueError as e:
        print(f"Error: {e}. Por favor, inténtalo de nuevo.\n")

# Calcular suma, media y máximo
suma = sum(numeros)
media = suma / len(numeros)
maximo = max(numeros)

# Detectar duplicados
duplicados = set([x for x in numeros if numeros.count(x) > 1])

# Mostrar resultados
print("\nResultados:")
print(f"Suma: {suma}")
print(f"Media: {media}")
print(f"Máximo: {maximo}")
if duplicados:
    print(f"Números duplicados: {sorted(duplicados)}")
else:
    print("No hay números duplicados.")
