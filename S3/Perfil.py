from datetime import *

# Manejo de excepciones
try:
    #Pedir el nombre y el año de nacimiento al usuario.
    print("Dame tu nombre:")
    nombre = input()
    print("Introducir el año en que has nacido:")
    anyo = input()

    # Obtener la edad del usuario.
    edad = date.today().year - int(anyo)

    # Mostrar el resultado.
    print(f"Tu nombre es {nombre} y tienes {edad} años.")

    if edad < 18 and edad >= 0:
        print("Eres menor de edad.")
    elif edad >= 18 and 65 > edad:
        print("Eres mayor de edad.")
    elif edad >= 65 and edad <= 120:
        print("Eres un anciano.")
    elif edad < 0:
        print("Aún no has nacido.")
    elif edad > 120:
        print("Edad no válida.")
        
except ValueError:
    # Controlar el error si el usuario no introduce un número.
    print("El valor introducido no es correcto.")