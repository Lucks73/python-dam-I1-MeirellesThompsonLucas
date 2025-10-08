def analizar_cadena():
    while True:
        texto = input("Introduce una cadena de texto: ")
        if texto.strip() == "":
            print("Error: la cadena no puede estar vacía. Intenta de nuevo.")
        else:
            break

    vocales = "aeiouAEIOU"
    num_vocales = sum(1 for c in texto if c in vocales)
    num_consonantes = sum(1 for c in texto if c.isalpha() and c not in vocales)
    num_mayusculas = sum(1 for c in texto if c.isupper())
    num_caracteres = len(texto)

    print(f"Vocales: {num_vocales}")
    print(f"Consonantes: {num_consonantes}")
    print(f"Mayúsculas: {num_mayusculas}")
    print(f"Total de caracteres: {num_caracteres}")

analizar_cadena()
