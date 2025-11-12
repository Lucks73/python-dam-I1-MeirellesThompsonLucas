def pedir_numero(prompt):
    """
    Solicita al usuario un número entero con validación.
    min_val y max_val son opcionales para restringir el rango.
    """
    while True:
        try:
            valor = int(input(prompt))
            if (valor < 0) or ( valor > 10):
                print("Introduce un número entre 0 y 10.")
                continue
            return valor
        except ValueError:
            print("Entrada no válida. Debes introducir un número entero.")

def pedir_notas(cantidad):
    """
    Solicita una lista de notas al usuario.
    Cada nota debe estar entre 0 y 10.
    """
    notas = []
    for i in range(cantidad):
        nota = pedir_numero(f"Nota del alumno {i+1}: ")
        notas.append(nota)
    return notas

def calcular_media(notas):
    """
    Calcula la media de las notas, evitando división por cero.
    """
    if len(notas) == 0:
        return 0 
    return sum(notas) / len(notas)

def mostrar_resultados(notas):
    """
    Muestra la media y los aprobados.
    """
    media = calcular_media(notas)
    print(f"Media: {media:.2f}")
    print("Aprobados:")
    for nota in notas:
        if nota >= 5:
            print(nota)

def programa():
    n = pedir_numero("¿Cuántos alumnos? ")
    notas = pedir_notas(n)
    mostrar_resultados(notas)

programa()
