def es_primo(num):
    if num < 2:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True

def verificar_numero():
    while True:
        try:
            numero = int(input("Introduce un número entero: "))
            break
        except ValueError:
            print("Error: debes introducir un número entero válido. Intenta de nuevo.")

    if es_primo(numero):
        print(f"{numero} es un número primo.")
    else:
        print(f"{numero} no es un número primo.")

verificar_numero()
