# Pedir 3 números al usuario
num1 = float(input("Ingrese el primer número: "))
num2 = float(input("Ingrese el segundo número: "))
num3 = float(input("Ingrese el tercer número: "))

# Calcular suma
suma = num1 + num2 + num3

# Calcular media
media = suma / 3

# Encontrar el número mayor
mayor = max(num1, num2, num3)

# Mostrar resultados
print(f"\nLa suma de los números es: {suma}")
print(f"La media de los números es: {media}")
print(f"El número mayor es: {mayor}")
