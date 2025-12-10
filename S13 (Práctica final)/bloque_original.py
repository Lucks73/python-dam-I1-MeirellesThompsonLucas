# Bloque original de minijuegos (extraído de EmojiCipherOriginal.py)
# Versión con comentarios pedagógicos extendidos.
# Este archivo contiene únicamente los bloques de datos y funciones
# que implementan los minijuegos originales antes de ser adaptados
# a una interfaz más rica. Está pensado como material didáctico:
# cada variable y función incluye explicación de su propósito,
# entradas, salidas y notas sobre el comportamiento.

# ==================================================================
# --- Datos estáticos: contenido y formato
# ==================================================================
# `frases_emoji` y `peliculas_emoji` son diccionarios simples que
# funcionan como *bancos de preguntas*. Las claves son las respuestas
# esperadas en texto (por ejemplo "te quiero" o "titanic"). Los valores
# son la representación en emojis que se muestra al jugador.
# Notas importantes:
# - Las claves están escritas en minúsculas y con espacios cuando
#   corresponda; la función `normalize_text` (definida en el programa
#   principal) se encarga de igualar acentos y mayúsculas al comparar.
# - Al añadir nuevas entradas, mantener el formato: clave → valor emoji.

frases_emoji = {
    "te quiero": "❤️👉👤",
    "buenos días": "☀️👋",
    "vamos a comer": "👉🍽️",
    "hace calor": "🔥🌞",
    "estoy cansado": "😩🛌",
    "buenas noches": "🌙✨",
    "tengo hambre": "🤤🍔",
    "tengo sueño": "😴💤",
    "muchas gracias": "🙏💖",
    "hasta luego": "👋➡️",
    "vamos a estudiar": "📚🧠",
    "estoy feliz": "😄✨",
    "me duele la cabeza": "🤕🧠",
    "vamos a jugar": "🎮🔥",
    "no entiendo nada": "🤯❓",
}

# El diccionario de películas cumple la misma función que `frases_emoji`:
# las claves son el título en texto (forma sencilla y normalizada) y los
# valores son los emojis que evocan la película.
peliculas_emoji = {
    "titanic": "🚢🌊💔",
    "el rey leon": "🦁👑🌅",
    "avatar": "🌌👽💙",
    "it": "🤡🎈",
    "jurassic park": "🦖🚙🌴",
    "harry potter": "🧙‍♂️✨🪄",
    "star wars": "🌌⚔️🛸",
    "toy story": "🤠🧸🚀",
    "buscando a nemo": "🐠🔍🌊",
    "spider man": "🕷️🕸️🧑‍🦱",
    "frozen": "❄️👭⛄",
    "piratas del caribe": "🏴‍☠️⚓🌊",
    "la bella y la bestia": "🌹👸🐻",
    "shrek": "🧅👹🐴",
    "up": "🎈🏠👴",
}

# Lista de emojis que se usan para el minijuego de identificar el emoji.
# Es una lista simple; en el juego se elige uno al azar con `random.choice`.
lista_emojis_identificar = [
    "😀", "😂", "🤣", "😍", "😎", "🤯", "🥶", "🤖", "👻", "🐱", "🐶", "🦊", "🐼",
    "🌧️", "⚡", "🔥", "🌈", "⭐", "🌙", "🍎", "🍔", "🍕", "🥐", "⚽", "🏀", "🚗",
    "✈️", "🚀", "📱", "💡", "🎲", "🎧", "🎮", "🎁", "👑", "📚", "💀"
]

# Variables auxiliares que guardan el último elemento mostrado en cada
# minijuego (se usan para evitar que la misma pregunta salga dos veces
# seguidas). Son `None` al inicio y se actualizan cuando se lanza un juego.
ultima_frase = None
ultima_peli = None


# ==================================================================
# --- Funciones auxiliares (explicadas)
# ==================================================================

def elegir_item_sin_repetir(diccionario: dict, ultimo):
    """
    Selecciona una clave y su valor asociado de `diccionario` de forma
    aleatoria, procurando no devolver la misma clave que `ultimo`.

    Entradas:
        diccionario: dict - mapa clave→valor del que extraer un ítem.
        ultimo: el valor de la clave que se mostró la última vez en este
               tipo de juego (puede ser `None`).

    Salida:
        (clave, valor) si hay éxito, o (None, None) si ocurre un error.

    Comportamiento:
    - Convierte las claves a una lista para poder usar `random.choice`.
    - Si el diccionario tiene 0 o 1 elementos, devuelve el primero (caso
      trivial). Si tiene más, elige aleatoriamente y repite la elección
      si coincide con `ultimo` (evita repeticiones inmediatas).
    - En producción es posible mejorar la lógica para evitar bucles
      infinitos (por ejemplo, usando una copia filtrada), pero aquí la
      versión es suficiente y clara para aprendizaje.
    """
    try:
        claves = list(diccionario.keys())
        if len(claves) <= 1:
            # Si solo hay una opción, la devolvemos tal cual.
            return claves[0], diccionario[claves[0]]

        elegido = random.choice(claves)
        # Repetimos la elección mientras coincida con el último mostrado.
        while elegido == ultimo:
            elegido = random.choice(claves)
        return elegido, diccionario[elegido]
    except Exception:
        # Si ocurre cualquier error, devolvemos un par nulo. El llamador
        # debe manejar este caso (por ejemplo, no iniciar el juego).
        return None, None


def generar_pista(respuesta: str) -> str:
    """
    Genera una pista muy simple y didáctica a partir de la respuesta.

    - Separa la respuesta en palabras, toma la primera letra de cada una
      y devuelve una cadena con esas iniciales y el número de palabras.

    Por ejemplo: "hola mundo" → "Pista: iniciales h m — 2 palabra(s)."
    Esto es útil porque muestra información pero no revela la respuesta.
    """
    partes = respuesta.split()
    iniciales = " ".join(p[0] for p in partes)
    return f"Pista: iniciales {iniciales} — {len(partes)} palabra(s)."


def pedir_respuesta(titulo, mensaje):
    """
    Abre una ventana modal sencilla que pide al usuario una cadena de texto.

    Parámetros:
        titulo: texto que se usa en la barra de la ventana modal.
        mensaje: cuerpo del mensaje que explica lo que hay que escribir.

    Retorna:
        La cadena ingresada por el usuario (str), o `None` si se cierra
        la ventana sin responder.

    Detalles de implementación:
    - Se crea un `Toplevel` como ventana hija de `ventana` (ventana principal)
      para que el usuario pueda escribir de forma cómoda.
    - `ventana_resp.grab_set()` evita que el usuario interactúe con la
      ventana principal hasta cerrar la modal.
    - Se retorna el contenido del Entry cuando se pulsa "Enviar".
    """
    ventana_resp = tk.Toplevel(ventana)
    ventana_resp.title(titulo)
    ventana_resp.geometry("420x230")

    tk.Label(ventana_resp, text=mensaje, font=("Consolas", 13)).pack(pady=20)

    entrada = tk.Entry(ventana_resp, font=("Consolas", 12))
    entrada.pack(pady=10, fill="x")

    resultado = {"respuesta": None}

    def enviar():
        # Guardamos la respuesta en el diccionario `resultado` que
        # permanece accesible desde el contexto exterior y cerramos.
        resultado["respuesta"] = entrada.get()
        ventana_resp.destroy()

    tk.Button(ventana_resp, text="Enviar", command=enviar).pack(pady=10)
    entrada.bind("<Return>", lambda e: enviar())

    ventana_resp.transient(ventana)
    ventana_resp.grab_set()
    ventana.wait_window(ventana_resp)

    return resultado["respuesta"]


# ==================================================================
# --- Minijuegos (versión original)
# ==================================================================

def jugar_frase_emoji():
    """
    Juego por texto: se muestra una cadena de emojis y el jugador debe
    escribir la frase correspondiente.

    Lógica resumida:
    - Se elige una frase distinta a la última mostrada con
      `elegir_item_sin_repetir`.
    - El jugador tiene 2 intentos (variable `intentos`).
    - Se solicita la respuesta mediante `pedir_respuesta`.
    - Si falla en el primer intento, se muestra una pista; si falla
      también en el segundo, se revela la respuesta final.
    """
    global ultima_frase
    try:
        frase, em = elegir_item_sin_repetir(frases_emoji, ultima_frase)
        if not frase:
            # No hay frase válida (posible error en el diccionario)
            return

        ultima_frase = frase
        intentos = 2

        while intentos > 0:
            mensaje = f"Traduce esta frase:\n\n{em}\n\nIntentos restantes: {intentos}"
            respuesta = pedir_respuesta("Adivina la frase", mensaje)

            # `normalize_text` compara sin acentos ni mayúsculas
            if normalize_text(respuesta) == normalize_text(frase):
                messagebox.showinfo("Correcto", "¡Has acertado! 🎉")
                return

            intentos -= 1

            if intentos == 1:
                # Si le queda un intento, damos una pista que no revela
                # la respuesta completa pero orienta al jugador.
                messagebox.showinfo("Pista", generar_pista(frase))
            else:
                # Si ya no quedan intentos, mostramos la respuesta.
                messagebox.showerror("Fin del juego", f"La frase era:\n\n{frase}")
                return

    except Exception:
        # En caso de excepción mostramos un error genérico. En un
        # entorno de aprendizaje esto ayuda a no bloquear la app.
        messagebox.showerror("Error", "Hubo un fallo en el minijuego")


def jugar_pelicula_emoji():
    """
    Juego por texto: se muestran emojis que representan una película y el
    jugador debe escribir el título.

    Notas:
    - Igual que en `jugar_frase_emoji` se usa `elegir_item_sin_repetir`.
    - Se usan 2 intentos y se muestra una pista al llegar al último.
    """
    global ultima_peli
    try:
        peli, em = elegir_item_sin_repetir(peliculas_emoji, ultima_peli)
        if not peli:
            return

        ultima_peli = peli
        intentos = 2

        while intentos > 0:
            mensaje = f"Adivina la película:\n\n{em}\n\nIntentos restantes: {intentos}"
            respuesta = pedir_respuesta("Adivina la película", mensaje)

            if normalize_text(respuesta) == normalize_text(peli):
                messagebox.showinfo("Correcto", "¡Has acertado! 🎉")
                return

            intentos -= 1
            if intentos == 1:
                messagebox.showinfo("Pista", generar_pista(peli))
            else:
                messagebox.showerror("Fin del juego", f"La película era:\n\n{peli}")
                return

    except Exception:
        messagebox.showerror("Error", "Hubo un fallo en el minijuego")


def jugar_identifica_emoji():
    """
    Juego estilo "ahorcado" simplificado: se elige un emoji y el jugador
    debe escribir su nombre. Por cada fallo se revela aleatoriamente una
    letra del nombre.

    Detalles de implementación:
    - `emoji.demojize` convierte el emoji a su nombre textual, por ejemplo
      'dog' o 'perro', dependiendo de la librería y el idioma.
    - `normalize_text` normaliza la cadena (quita acentos y pasa a
      minúsculas) para comparar entradas del usuario correctamente.
    - `progreso` es una lista de caracteres que contiene '_' en las
      posiciones ocultas y el carácter real donde ya se ha revelado.
    - `revelar_letra` elige una posición oculta al azar y la muestra.
    - El juego termina cuando el usuario acierta (mensaje de éxito) o
      cuando ya no quedan letras ocultas (se revela la respuesta).
    """
    try:
        em = random.choice(lista_emojis_identificar)
        nombre = emoji.demojize(em, language='es').strip(":")
        nombre = normalize_text(nombre)

        ventana_juego = tk.Toplevel(ventana)
        ventana_juego.title("Identifica el emoji")
        ventana_juego.geometry("480x350")

        tk.Label(ventana_juego, text=f"Adivina el nombre del emoji:\n\n{em}",
                 font=("Consolas", 22)).pack(pady=20)

        # Inicialmente ocultamos letras alfanuméricas con '_' pero dejamos
        # visibles signos y separadores (si existieran).
        progreso = ["_" if c.isalnum() else c for c in nombre]
        lbl_progreso = tk.Label(ventana_juego, text=" ".join(progreso), font=("Consolas", 18))
        lbl_progreso.pack(pady=10)

        entrada = tk.Entry(ventana_juego, font=("Consolas", 14))
        entrada.pack(pady=10)

        def actualizar_progreso():
            lbl_progreso.config(text=" ".join(progreso))

        def revelar_letra():
            # Calcula los índices que aún están ocultos y revela uno al azar.
            indices = [i for i, c in enumerate(progreso) if c == "_"]
            if indices:
                idx = random.choice(indices)
                progreso[idx] = nombre[idx]
                actualizar_progreso()

        def enviar():
            intento = normalize_text(entrada.get())
            entrada.delete(0, tk.END)

            if intento == nombre:
                messagebox.showinfo("Correcto", "¡Has acertado! 🎉")
                ventana_juego.destroy()
            else:
                # En esta versión original vamos mostrando letras hasta
                # que se complete el nombre; no hay "vidas" numeradas.
                revelar_letra()
                if "_" not in progreso:
                    # Todas las letras reveladas: el jugador no ha acertado
                    # por sí mismo y mostramos la respuesta final.
                    messagebox.showerror("Perdiste", f"La palabra era:\n{nombre}")
                    ventana_juego.destroy()

        tk.Button(ventana_juego, text="Enviar", command=enviar,
                  font=("Arial", 12, "bold")).pack(pady=10)

        entrada.bind("<Return>", lambda e: enviar())

        ventana_juego.transient(ventana)
        ventana_juego.grab_set()
        ventana.wait_window(ventana_juego)

    except Exception:
        messagebox.showerror("Error", "Hubo un fallo en el minijuego Identifica Emoji")
