def convertir_temperatura():
    while True:
        try:
            temp = float(input("Introduce la temperatura en grados Celsius: "))
            break
        except ValueError:
            print("Error: debes introducir un número válido. Intenta de nuevo.")

    while True:
        opcion = input("Convertir a (K)elvin o (F)ahrenheit? ").strip().upper()
        if opcion == "K":
            resultado = temp + 273.15
            print(f"{temp}°C son {resultado} K")
            break
        elif opcion == "F":
            resultado = (temp * 9/5) + 32
            print(f"{temp}°C son {resultado} °F")
            break
        else:
            print("Opción inválida. Escribe 'K' para Kelvin o 'F' para Fahrenheit.")   
convertir_temperatura()