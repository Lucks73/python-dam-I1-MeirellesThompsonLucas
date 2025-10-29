# --- Sistema interactivo de TIENDA usando diccionarios ---

tienda = {
    "manzanas": 1.5,
    "pan": 2.0,
    "leche": 1.2
}

def mostrar_productos():
    print("\n--- Productos disponibles ---")
    for producto, precio in tienda.items():
        print(f"- {producto}: ${precio:.2f}")

while True:
    print("\n--- MENÚ DE OPCIONES ---")
    print("1. Ver productos")
    print("2. Insertar producto")
    print("3. Modificar precio")
    print("4. Eliminar producto")
    print("5. Calcular métricas")
    print("6. Ver productos caros (más de $2.0)")
    print("7. Salir")

    opcion = input("Elige una opción (1-7): ")

    if opcion == "1":
        mostrar_productos()

    elif opcion == "2":
        producto = input("Nombre del nuevo producto: ").lower()
        precio = float(input("Precio: "))
        tienda[producto] = precio
        print(f"✅ '{producto}' añadido con precio ${precio:.2f}")

    elif opcion == "3":
        producto = input("Producto a modificar: ").lower()
        if producto in tienda:
            nuevo_precio = float(input("Nuevo precio: "))
            tienda[producto] = nuevo_precio
            print(f"✅ Precio de '{producto}' actualizado a ${nuevo_precio:.2f}")
        else:
            print("❌ Ese producto no existe.")

    elif opcion == "4":
        producto = input("Producto a eliminar: ").lower()
        if producto in tienda:
            del tienda[producto]
            print(f"✅ '{producto}' eliminado del inventario.")
        else:
            print("❌ Ese producto no existe.")

    elif opcion == "5":
        if tienda:
            suma = sum(tienda.values())
            promedio = suma / len(tienda)
            max_precio = max(tienda.values())
            print(f"\n📊 Métricas:")
            print(f"- Suma total: ${suma:.2f}")
            print(f"- Promedio de precios: ${promedio:.2f}")
            print(f"- Precio máximo: ${max_precio:.2f}")
        else:
            print("No hay productos para calcular métricas.")

    elif opcion == "6":
        print("\n💰 Productos con precio mayor a $2.0:")
        for producto, precio in tienda.items():
            if precio > 2.0:
                print(f"- {producto}: ${precio:.2f}")

    elif opcion == "7":
        print("Saliendo del sistema... 🖖")
        break

    else:
        print("Opción no válida. Intenta de nuevo.")
