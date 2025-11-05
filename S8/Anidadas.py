# --- GESTOR INTERACTIVO DE PELÍCULAS Y SERIES ---

catalogo = []  # Lista de diccionarios

def añadir_registro():
    """Añadir un nuevo registro."""
    titulo = input("Título: ").strip()
    tipo = input("Tipo (película/serie): ").strip()
    try:
        calificacion = float(input("Calificación (0-10): "))
    except ValueError:
        print("Error: la calificación debe ser numérica.")
        return

    if not titulo or not tipo:
        print("Error: no se permiten campos vacíos.")
        return
    if any(r["titulo"].lower() == titulo.lower() for r in catalogo):
        print("Error: ese título ya existe.")
        return
    if not (0 <= calificacion <= 10):
        print("Error: la calificación debe estar entre 0 y 10.")
        return

    registro = {"titulo": titulo, "tipo": tipo, "calificacion": calificacion}
    catalogo.append(registro)
    print(f"'{titulo}' añadido correctamente.")


def buscar_por_titulo():
    """Buscar registro por título."""
    titulo = input("Introduce el título a buscar: ").strip()
    for r in catalogo:
        if r["titulo"].lower() == titulo.lower():
            print(f"Encontrado: {r}")
            return
    print("No se encontró ese título.")


def calificacion_media():
    """Calcular la calificación media."""
    if not catalogo:
        print("No hay datos en el catálogo.")
        return
    media = sum(r["calificacion"] for r in catalogo) / len(catalogo)
    print(f"Calificación media: {media:.2f}")


def mostrar_catalogo():
    """Mostrar todos los registros."""
    if not catalogo:
        print("Catálogo vacío.")
        return
    for r in catalogo:
        print(f"- {r['titulo']} ({r['tipo']}) → {r['calificacion']}")


def menu():
    """Menú interactivo."""
    while True:
        print("\n--- MENÚ ---")
        print("1. Añadir registro")
        print("2. Buscar por título")
        print("3. Calcular calificación media")
        print("4. Mostrar catálogo completo")
        print("5. Salir")

        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            añadir_registro()
        elif opcion == "2":
            buscar_por_titulo()
        elif opcion == "3":
            calificacion_media()
        elif opcion == "4":
            mostrar_catalogo()
        elif opcion == "5":
            
            # --- CATÁLOGO CON DICCIONARIO DE LISTAS ---

            catalogo_inverso = {
                "titulo": ["Breaking Bad", "Inception", "Friends"],
                "tipo": ["serie", "película", "serie"],
                "calificacion": [9.8, 9.0, 8.5]
            }

            # Mostrar todos los títulos
            print("Títulos:", catalogo_inverso["titulo"])

            # Calcular la media de las calificaciones
            media = sum(catalogo_inverso["calificacion"]) / len(catalogo_inverso["calificacion"])
            print(f"Calificación media: {media:.2f}")

            # Mostrar el primer registro completo
            i = 0
            print(f"\nPrimer registro:")
            print(f"- {catalogo_inverso['titulo'][i]} ({catalogo_inverso['tipo'][i]}) → {catalogo_inverso['calificacion'][i]}")

            
            print("Hasta luego.")
            break
        else:
            print("Opción no válida.")


# --- INICIO DEL PROGRAMA ---
if __name__ == "__main__":
    menu()
