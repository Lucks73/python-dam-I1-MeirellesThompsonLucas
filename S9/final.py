import random
from datetime import datetime
# Lista de personajes predeterminados
personajes = [
    {"Nombre": "Aria", "Fuerza": 7, "Agilidad": 8, "Inteligencia": 6, "Creacion": "2025-01-01 10:00:00"},
    {"Nombre": "Brax", "Fuerza": 9, "Agilidad": 5, "Inteligencia": 4, "Creacion": "2025-01-02 15:30:00"},
    {"Nombre": "Luna", "Fuerza": 4, "Agilidad": 9, "Inteligencia": 8, "Creacion": "2025-01-03 20:45:00"}
]

# Función 1: Pedir el nombre del personaje
def pedir_nombre():
    while True:
        try:
            nombre = input("Ingresa el nombre de tu personaje: ").strip()
            if not nombre:
                raise ValueError("El nombre no puede estar vacío.")
            return nombre
        except ValueError as e:
            print(f"Error: {e}")

# Función 2: Generar atributos del personaje
def generar_atributos():
    atributos = {
        "Fuerza": random.randint(1, 10),
        "Agilidad": random.randint(1, 10),
        "Inteligencia": random.randint(1, 10)
    }
    return atributos

# Función 3: Crear un nuevo personaje
def crear_personaje(listaPersonajes):
    nombre = pedir_nombre()
    atributos = generar_atributos()
    creacion = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    personaje = {"Nombre": nombre, **atributos, "Creacion": creacion}
    personajes.append(personaje)
    print(f"\nPersonaje '{nombre}' creado exitosamente!\n")

# Función 4: Mostrar todos los personajes
def mostrar_personajes(listaPersonajes):
    if not personajes:
        print("\nNo hay personajes para mostrar.\n")
        return
    print("\n--- LISTA DE PERSONAJES ---")
    for i, p in enumerate(personajes):
        print(f"\nPersonaje {i + 1}:")
        for clave, valor in p.items():
            print(f"{clave}: {valor}")
    print("\n")

# Función principal con menú
def main():
    while True:
        print("=== GENERADOR DE PERSONAJES ===")
        print("1. Crear nuevo personaje")
        print("2. Ver personajes existentes")
        print("3. Salir")
        
        try:
            opcion = int(input("Elige una opción (1-3): "))
            if opcion == 1:
                crear_personaje(personajes)
            elif opcion == 2:
                mostrar_personajes(personajes)
            elif opcion == 3:
                print("Saliendo del programa...")
                break
            else:
                print("Opción inválida. Elige entre 1 y 3.\n")
        except ValueError:
            print("Error: Debes ingresar un número.\n")

if __name__ == "__main__":
    main()
