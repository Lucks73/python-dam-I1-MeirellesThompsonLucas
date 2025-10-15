def pedir_notas():
    while True:
        # Solicita al usuario una cadena con notas separadas por comas
        entrada = input("Introduce las notas separadas por comas (ej: 5,7.5,9,10): ").strip()
        try:
            # Convierte cada elemento separado por coma en float, ignorando espacios vacíos
            notas = [float(n) for n in entrada.split(",") if n.strip()]
            # Verifica que todas las notas estén entre 0 y 10
            if not notas or not all(0 <= n <= 10 for n in notas):
                raise ValueError
            return notas  # Si todo es válido, devuelve la lista y rompe el bucle
        except ValueError:
            # Mensaje de error si la conversión falla o hay números fuera de rango
            print("❌ Error: introduce solo números entre 0 y 10.")

def resumen_boletin(notas):
    # Verifica que se hayan introducido notas válidas
    if not notas:
        print("No se introdujeron notas válidas.")
        return

    total = len(notas)
    # Calcula la media con dos decimales
    media = round(sum(notas) / total, 2)
    minima, maxima = min(notas), max(notas)
    # Contadores de aprobados y sobresalientes
    aprobados = sum(1 for n in notas if n >= 5)
    sobresalientes = sum(1 for n in notas if n >= 9)

    # Cálculo de la nota más repetida (moda) de manera simple
    notas_redondeadas = [round(n, 2) for n in notas]
    mas_repetidas = []
    max_frec = 0
    for n in set(notas_redondeadas):
        freq = notas_redondeadas.count(n)
        if freq > max_frec:
            max_frec = freq # Nueva frecuencia máxima
            mas_repetidas = [n] # Reinicia la lista con la nueva moda
        elif freq == max_frec:
            mas_repetidas.append(n) # Añade a la lista

    # Determina el nivel según la media
    if media >= 8:
        nivel = "Nivel excelente"
    elif media >= 5:
        nivel = "Nivel medio"
    else:
        nivel = "Necesita refuerzo"

    # Muestra el resumen completo en formato bonito
    print(f"""
📊 --- BOLETÍN ESTADÍSTICO ---
Total de notas: {total}
Media: {media:.2f}
Mínima: {minima}
Máxima: {maxima}
Aprobados: {(aprobados / total) * 100:.2f}%
Sobresalientes: {(sobresalientes / total) * 100:.2f}%
Nota(s) más repetida(s): {', '.join(str(n) for n in mas_repetidas)}
➡️ {nivel}
""")


if __name__ == "__main__":
    notas = pedir_notas()  # Llama a la función para pedir notas
    resumen_boletin(notas) # Genera el resumen estadístico
