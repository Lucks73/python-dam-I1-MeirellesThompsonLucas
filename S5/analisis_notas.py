def pedir_notas():
    entrada = input("Introduce las notas separadas por comas (ej: 5,7.5,9,10): ").strip()
    try:
        notas = [float(n) for n in entrada.split(",") if n.strip()]
        if not all(0 <= n <= 10 for n in notas):
            raise ValueError
        return notas
    except ValueError:
        print("❌ Error: introduce solo números entre 0 y 10.")
        return []


def resumen_boletin(notas):
    if not notas:
        print("No se introdujeron notas válidas.")
        return

    total = len(notas)
    media = round(sum(notas) / total, 2)
    minima, maxima = min(notas), max(notas)
    aprobados = sum(1 for n in notas if n >= 5)
    sobresalientes = sum(1 for n in notas if n >= 9)

    # Nota más repetida (modo) de manera sencilla
    notas_redondeadas = [round(n, 1) for n in notas]
    mas_repetidas = []
    max_frec = 0
    for n in set(notas_redondeadas):
        freq = notas_redondeadas.count(n)
        if freq > max_frec:
            max_frec = freq
            mas_repetidas = [n]
        elif freq == max_frec:
            mas_repetidas.append(n)

    # Nivel según media
    if media >= 8:
        nivel = "Nivel excelente"
    elif media >= 5:
        nivel = "Nivel medio"
    else:
        nivel = "Necesita refuerzo"

    print(f"""
📊 --- BOLETÍN ESTADÍSTICO ---
Total de notas: {total}
Media: {media:.2f}
Mínima: {minima}
Máxima: {maxima}
Aprobados: {(aprobados / total) * 100:.1f}%
Sobresalientes: {(sobresalientes / total) * 100:.1f}%
Nota(s) más repetida(s): {', '.join(str(n) for n in mas_repetidas)}
➡️ {nivel}
""")


if __name__ == "__main__":
    notas = pedir_notas()
    resumen_boletin(notas)
