# Bloque actualizado de minijuegos (extraído de EmojiCipherActualizado.py)
# Esta versión contiene las mismas funciones que la original pero con
# mejoras en la interfaz (ventanas centradas, corazones como vidas,
# texto en fuentes grandes). Aquí se encuentran comentarios extensos para
# explicar cada sección y los motivos de diseño.

# ==================================================================
# --- Datos: preguntas y recursos visuales
# ==================================================================
# Las estructuras `frases_emoji`, `peliculas_emoji` y
# `lista_emojis_identificar` tienen el mismo significado que en la
# versión original. Se mantienen para compatibilidad y facilidad de
# edición por parte del alumno.

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

lista_emojis_identificar = [
    "😀", "😂", "🤣", "😍", "😎", "🤯", "🥶", "🤖", "👻", "🐱", "🐶", "🦊", "🐼",
    "🌧️", "⚡", "🔥", "🌈", "⭐", "🌙", "🍎", "🍔", "🍕", "🥐", "⚽", "🏀", "🚗",
    "✈️", "🚀", "📱", "💡", "🎲", "🎧", "🎮", "🎁", "👑", "📚", "💀"
]

# Guardan el último elemento mostrado para evitar repetir inmeditamente
ultima_frase = None
ultima_peli = None


# ==================================================================
# --- Funciones de apoyo (explicadas con detalle)
# ==================================================================

def elegir_item_sin_repetir(diccionario: dict, ultimo):
    """
    Igual que en la versión original: elige aleatoriamente un par
    (clave, valor) de un diccionario, evitando el valor `ultimo`.

    Motivo didáctico: separar la lógica de selección de datos del resto
    facilita pruebas y comprensión.
    """
    try:
        claves = list(diccionario.keys())
        if len(claves) <= 1:
            return claves[0], diccionario[claves[0]]

        elegido = random.choice(claves)
        while elegido == ultimo:
            elegido = random.choice(claves)
        return elegido, diccionario[elegido]
    except Exception:
        return None, None


def generar_pista(respuesta: str) -> str:
    """Devuelve una pista simple: iniciales + número de palabras."""
    partes = respuesta.split()
    iniciales = " ".join(p[0] for p in partes)
    return f"Pista: iniciales {iniciales} — {len(partes)} palabra(s)."


def cifrar_parcial_dialogo(dialogo: str, clave: dict) -> str:
    """
    Cifra parcialmente un diálogo para usarlo como pista visual.

    Regla didáctica:
    - Dejar la primera y última letra de cada palabra sin cifrar (mejora
      la legibilidad), cifrar solo las letras intermedias según `clave`.
    - Si no hay clave, devolvemos el diálogo tal cual.

    Resultado: mezcla de letras y emojis que sugiere la frase sin ocultarla
    completamente.
    """
    if not clave:
        return dialogo

    palabras = dialogo.split()
    partes_cifradas = []

    for palabra in palabras:
        if len(palabra) <= 2:
            partes_cifradas.append(palabra)
            continue

        primera = palabra[0]
        ultima = palabra[-1]
        medio = palabra[1:-1]

        medio_cifrado = ""
        for ch in medio:
            medio_cifrado += clave.get(ch, ch)

        partes_cifradas.append(primera + medio_cifrado + ultima)

    return " ".join(partes_cifradas)


def pedir_respuesta(titulo, mensaje):
    """Modal reutilizable para pedir una respuesta al usuario.

    Igual que en la versión original pero documentado para el alumno.
    """
    ventana_resp = tk.Toplevel(ventana)
    ventana_resp.title(titulo)
    ventana_resp.geometry("420x230")

    tk.Label(ventana_resp, text=mensaje, font=("Consolas", 13)).pack(pady=20)

    entrada = tk.Entry(ventana_resp, font=("Consolas", 12))
    entrada.pack(pady=10, fill="x")

    resultado = {"respuesta": None}

    def enviar():
        resultado["respuesta"] = entrada.get()
        ventana_resp.destroy()

    tk.Button(ventana_resp, text="Enviar", command=enviar).pack(pady=10)
    entrada.bind("<Return>", lambda e: enviar())

    ventana_resp.transient(ventana)
    ventana_resp.grab_set()
    ventana.wait_window(ventana_resp)

    return resultado["respuesta"]


# ==================================================================
# --- Minijuegos (versión actualizada, con explicación de la UI)
# ==================================================================

def jugar_frase_emoji():
    """
    Versión enriquecida del minijuego de frases:

    - Ventana grande y centrada para mejorar la experiencia.
    - Emojis mostrados con fuente amplia (`Segoe UI Emoji`) para que
      sean legibles en distintas plataformas.
    - Se muestran 3 vidas representadas por corazones (visual + textual).
    - Cuando queda 1 vida, mostramos una pista destacada con color.

    El código explica exactamente qué hace cada bloque UI para que el
    estudiante pueda replicarlo o modificar estilos.
    """
    global ultima_frase
    try:
        frase, em = elegir_item_sin_repetir(frases_emoji, ultima_frase)
        if not frase:
            return

        ultima_frase = frase
        vidas = 3

        ventana_juego = tk.Toplevel(ventana)
        ventana_juego.title("Adivina la frase")

        # Intento de centrar la ventana respecto a la principal; si falla
        # (por ejemplo si la ventana principal no está mapeada), se usa
        # un fallback centrándolo en la pantalla.
        ancho, alto = 700, 420
        try:
            vx = ventana.winfo_rootx()
            vy = ventana.winfo_rooty()
            vw = ventana.winfo_width()
            vh = ventana.winfo_height()
            x = vx + (vw - ancho) // 2
            y = vy + (vh - alto) // 2
        except Exception:
            sw = ventana_juego.winfo_screenwidth()
            sh = ventana_juego.winfo_screenheight()
            x = (sw - ancho) // 2
            y = (sh - alto) // 2

        ventana_juego.geometry(f"{ancho}x{alto}+{x}+{y}")
        ventana_juego.configure(bg=BG_PRIMARY)

        # Emoji principal, tamaño grande para visibilidad
        lbl_emoji = tk.Label(ventana_juego, text=em, font=("Segoe UI Emoji", 56), bg=BG_PRIMARY, fg=TXT_PRIMARY)
        lbl_emoji.pack(pady=(18, 6))

        # Marco donde colocamos los corazones que representan las vidas.
        frame_vidas = tk.Frame(ventana_juego, bg=BG_PRIMARY)
        frame_vidas.pack()

        corazones = []
        for i in range(vidas):
            lbl = tk.Label(frame_vidas, text="❤️", font=("Arial", 28), bg=BG_PRIMARY)
            lbl.pack(side="left", padx=6)
            corazones.append(lbl)

        # Etiqueta de pista (vacía al inicio). Usamos colores suaves para
        # no distraer demasiado, pero sí aportar contraste cuando aparece.
        pista_label = tk.Label(ventana_juego, text="", font=("Consolas", 13), bg="#FFF7AE", fg="#7C2D12", wraplength=ancho - 40, justify="center")
        pista_label.pack(pady=(12, 6), padx=20, fill="x")

        entrada = tk.Entry(ventana_juego, font=("Consolas", 20))
        entrada.pack(pady=8, padx=20, fill="x")
        entrada.focus_set()

        def actualizar_corazones(n_vidas):
            # Actualiza la representación gráfica de las vidas.
            for idx, lbl in enumerate(corazones):
                if idx < n_vidas:
                    lbl.config(text="❤️")
                else:
                    lbl.config(text="🤍")

        def mostrar_pista():
            # Construye y muestra la pista de forma visible.
            pista = generar_pista(frase)
            pista_label.config(text=f"🎯 Pista: {pista}", bg="#D1FAE5", fg="#065F46")

        def enviar():
            nonlocal vidas
            respuesta = entrada.get()
            if respuesta is None or respuesta.strip() == "":
                # No hacemos nada si la entrada está vacía.
                return

            if normalize_text(respuesta) == normalize_text(frase):
                messagebox.showinfo("Correcto", "¡Has acertado! 🎉")
                ventana_juego.destroy()
                return

            # Respuesta incorrecta: restamos vida y actualizamos UI.
            vidas -= 1
            actualizar_corazones(vidas)

            # Cuando queda una vida, damos una pista y mostramos un aviso.
            if vidas == 1:
                mostrar_pista()
                messagebox.showinfo("Pista", "Te dejo una pista para ayudarte 💡")

            if vidas <= 0:
                # Si se agotan las vidas, revelamos la respuesta.
                messagebox.showerror("Fin del juego", f"La frase era:\n\n{frase}")
                ventana_juego.destroy()

        btn_enviar = tk.Button(ventana_juego, text="Enviar", command=enviar, font=("Arial", 14, "bold"), bg=BTN_MAIN, fg="white", width=12)
        btn_enviar.pack(pady=12)

        entrada.bind("<Return>", lambda e: enviar())

        ventana_juego.transient(ventana)
        ventana_juego.grab_set()
        ventana.wait_window(ventana_juego)

    except Exception:
        messagebox.showerror("Error", "Hubo un fallo en el minijuego")


def jugar_pelicula_emoji():
    """
    Juego: adivina la película a partir de emojis.

    Características añadidas en la versión actualizada:
    - Muestra un diálogo famoso cifrado parcialmente como pista visual
      (mezcla letras y emojis).
    - Muestra la clave dentro de la misma ventana (en lugar de un pop-up)
      para que el alumno pueda verla y entender la correspondencia.
    """
    global ultima_peli, clave_actual
    try:
        peli, em = elegir_item_sin_repetir(peliculas_emoji, ultima_peli)
        if not peli:
            return

        ultima_peli = peli
        vidas = 3

        # Mapa de diálogos famosos (para enriquecer la pista)
        dialogos = {
            "titanic": "I'm the king of the world!",
            "el rey leon": "Hakuna Matata",
            "avatar": "I see you",
            "it": "You'll float too",
            "jurassic park": "Welcome to Jurassic Park",
            "harry potter": "You're a wizard, Harry",
            "star wars": "May the Force be with you",
            "toy story": "To infinity and beyond",
            "buscando a nemo": "Just keep swimming",
            "spider man": "With great power comes great responsibility",
            "frozen": "Let it go",
            "piratas del caribe": "Why is the rum gone?",
            "la bella y la bestia": "Tale as old as time",
            "shrek": "Ogres are like onions",
            "up": "Adventure is out there"
        }

        dialogo = dialogos.get(peli.lower(), "Diálogo no disponible")

        # Generamos una versión cifrada (total o parcial) del diálogo. Si
        # no hay clave cargada, se muestra un mensaje informativo.
        if clave_actual:
            dialogo_cifrado = codificar(dialogo, clave_actual)
        else:
            dialogo_cifrado = "(No hay clave cargada para cifrar la frase)"

        ventana_juego = tk.Toplevel(ventana)
        ventana_juego.title("Adivina la película")

        ancho, alto = 720, 520
        try:
            vx = ventana.winfo_rootx()
            vy = ventana.winfo_rooty()
            vw = ventana.winfo_width()
            vh = ventana.winfo_height()
            x = vx + (vw - ancho) // 2
            y = vy + (vh - alto) // 2
        except Exception:
            sw = ventana_juego.winfo_screenwidth()
            sh = ventana_juego.winfo_screenheight()
            x = (sw - ancho) // 2
            y = (sh - alto) // 2

        ventana_juego.geometry(f"{ancho}x{alto}+{x}+{y}")
        ventana_juego.configure(bg=BG_PRIMARY)

        # Emoji grande
        lbl_emoji = tk.Label(ventana_juego, text=em, font=("Segoe UI Emoji", 56), bg=BG_PRIMARY, fg=TXT_PRIMARY)
        lbl_emoji.pack(pady=(18, 6))

        # Contenedor con dos columnas: izquierda (emojis + diálogo),
        # derecha (clave con scroll). Esta organización facilita ver
        # la relación entre la clave y el diálogo cifrado.
        contenido = tk.Frame(ventana_juego, bg=BG_PRIMARY)
        contenido.pack(expand=True, fill="both", padx=12, pady=6)

        col_izq = tk.Frame(contenido, bg=BG_PRIMARY)
        col_izq.pack(side="left", expand=True, fill="both")

        col_der = tk.Frame(contenido, bg=BG_PRIMARY)
        col_der.pack(side="right", fill="y", padx=(8, 0))

        # Mostramos el diálogo parcialmente cifrado (o sin cifrar si no
        # hay clave). En la versión educativa preferimos una cifra parcial
        # que siga siendo legible.
        dialogo_parcial = cifrar_parcial_dialogo(dialogo, clave_actual) if clave_actual else dialogo

        lbl_cifrado = tk.Label(col_izq, text=dialogo_parcial, font=("Consolas", 12), bg="#0b1a2b", fg="#D1FAE5", wraplength=(ancho // 2) - 40, justify="center")
        lbl_cifrado.pack(pady=(6, 12), padx=20, fill="x")

        # En la columna derecha mostramos la clave completa dentro de un
        # `ScrolledText` para que el alumno pueda consultarla como referencia.
        tk.Label(col_der, text="Clave (pista)", font=("Consolas", 11, "bold"), bg=BG_PRIMARY, fg=TXT_PRIMARY).pack(pady=(6, 4))

        clave_box = scrolledtext.ScrolledText(col_der, width=30, height=18, font=("Consolas", 10))
        clave_box.pack(padx=4, pady=4)
        if clave_actual:
            clave_box.insert(tk.END, formato_clave_legible(clave_actual))
        else:
            clave_box.insert(tk.END, "No hay clave cargada. Genera o carga una clave para ver la pista.")
        clave_box.config(state="disabled")

        # Vidas (corazones) y entrada en la columna izquierda
        frame_vidas = tk.Frame(col_izq, bg=BG_PRIMARY)
        frame_vidas.pack(pady=(6, 0))

        corazones = []
        for i in range(vidas):
            lbl = tk.Label(frame_vidas, text="❤️", font=("Arial", 28), bg=BG_PRIMARY)
            lbl.pack(side="left", padx=6)
            corazones.append(lbl)

        pista_label = tk.Label(col_izq, text="", font=("Consolas", 13), bg="#FFF7AE", fg="#7C2D12", wraplength=(ancho // 2) - 40, justify="center")
        pista_label.pack(pady=(12, 6), padx=20, fill="x")

        entrada = tk.Entry(col_izq, font=("Consolas", 20))
        entrada.pack(pady=8, padx=20, fill="x")
        entrada.focus_set()

        def actualizar_corazones(n_vidas):
            for idx, lbl in enumerate(corazones):
                if idx < n_vidas:
                    lbl.config(text="❤️")
                else:
                    lbl.config(text="🤍")

        def mostrar_pista():
            pista = generar_pista(peli)
            pista_label.config(text=f"🎬 Pista: {pista}", bg="#E0F2FE", fg="#0369A1")

        def enviar():
            nonlocal vidas
            respuesta = entrada.get()
            if respuesta is None or respuesta.strip() == "":
                return

            if normalize_text(respuesta) == normalize_text(peli):
                messagebox.showinfo("Correcto", "¡Has acertado! 🎉")
                ventana_juego.destroy()
                return

            vidas -= 1
            actualizar_corazones(vidas)

            if vidas == 1:
                mostrar_pista()
                messagebox.showinfo("Pista", "Aquí tienes una pista para ayudarte 💡")

            if vidas <= 0:
                messagebox.showerror("Fin del juego", f"La película era:\n\n{peli}")
                ventana_juego.destroy()

        btn_enviar = tk.Button(ventana_juego, text="Enviar", command=enviar, font=("Arial", 14, "bold"), bg=BTN_MAIN, fg="white", width=12)
        btn_enviar.pack(pady=12)

        entrada.bind("<Return>", lambda e: enviar())

        ventana_juego.transient(ventana)
        ventana_juego.grab_set()
        ventana.wait_window(ventana_juego)

    except Exception:
        messagebox.showerror("Error", "Hubo un fallo en el minijuego")


def jugar_identifica_emoji():
    """
    Versión enriquecida del juego "Identifica el emoji". Esta variante:
    - Trata espacios como '_' internamente para facilitar la entrada.
    - No usa un contador de vidas; en su lugar va revelando letras hasta
      completar la palabra (método pedagógico para evitar frustración).

    La función incluye comentarios que explican cada paso para que un
    estudiante pueda seguir la lógica y adaptar el comportamiento.
    """
    try:
        em = random.choice(lista_emojis_identificar)
        nombre = emoji.demojize(em, language='es').strip(":")
        nombre = normalize_text(nombre)
        # Reemplazamos espacios por '_' para que la visualización sea
        # consistente con la interfaz que muestra guiones bajos.
        nombre = nombre.replace(" ", "_")

        ventana_juego = tk.Toplevel(ventana)
        ventana_juego.title("Identifica el emoji")

        ancho, alto = 520, 420
        try:
            vx = ventana.winfo_rootx()
            vy = ventana.winfo_rooty()
            vw = ventana.winfo_width()
            vh = ventana.winfo_height()
            x = vx + (vw - ancho) // 2
            y = vy + (vh - alto) // 2
        except Exception:
            sw = ventana_juego.winfo_screenwidth()
            sh = ventana_juego.winfo_screenheight()
            x = (sw - ancho) // 2
            y = (sh - alto) // 2

        ventana_juego.geometry(f"{ancho}x{alto}+{x}+{y}")
        ventana_juego.configure(bg=BG_PRIMARY)

        # Emoji grande y visible
        tk.Label(ventana_juego, text=em, font=("Segoe UI Emoji", 64), bg=BG_PRIMARY, fg=TXT_PRIMARY).pack(pady=(18, 6))

        # Progreso con '_' para letras ocultas
        progreso = ["_" if c.isalnum() else c for c in nombre]
        lbl_progreso = tk.Label(ventana_juego, text=" ".join(progreso), font=("Consolas", 22), bg=BG_PRIMARY, fg=TXT_PRIMARY)
        lbl_progreso.pack(pady=10)

        pista_label = tk.Label(ventana_juego, text="", font=("Consolas", 13), bg="#FFF7AE", fg="#7C2D12", wraplength=ancho-40, justify="center")
        pista_label.pack(pady=(8, 6), padx=12, fill="x")

        entrada = tk.Entry(ventana_juego, font=("Consolas", 18))
        entrada.pack(pady=8, padx=20, fill="x")
        entrada.focus_set()

        def actualizar_progreso():
            lbl_progreso.config(text=" ".join(progreso))

        def revelar_letra():
            indices = [i for i, c in enumerate(progreso) if c == "_"]
            if indices:
                idx = random.choice(indices)
                progreso[idx] = nombre[idx]
                actualizar_progreso()

        def mostrar_pista():
            pista = f"Comienza con '{nombre[0]}' — {len(nombre)} caracteres"
            pista_label.config(text=f"🔎 Pista: {pista}", bg="#D1FAE5", fg="#065F46")

        def enviar():
            texto = entrada.get()
            # Permitir que el usuario escriba espacios en lugar de '_'
            texto = texto.replace(" ", "_")
            intento = normalize_text(texto)

            entrada.delete(0, tk.END)

            if intento == nombre:
                messagebox.showinfo("Correcto", "¡Has acertado! 🎉")
                ventana_juego.destroy()
                return

            # Si falla, revelamos una letra para ayudarle a progresar.
            revelar_letra()

            # Si ya no quedan caracteres ocultos, el jugador no logró
            # adivinar y mostramos la respuesta final.
            if "_" not in progreso:
                messagebox.showerror("Perdiste", f"La respuesta era:\n{nombre}")
                ventana_juego.destroy()

        btn_enviar = tk.Button(ventana_juego, text="Enviar", command=enviar, font=("Arial", 14, "bold"), bg=BTN_MAIN, fg="white", width=12)
        btn_enviar.pack(pady=12)

        entrada.bind("<Return>", lambda e: enviar())

        ventana_juego.transient(ventana)
        ventana_juego.grab_set()
        ventana.wait_window(ventana_juego)

    except Exception:
        messagebox.showerror("Error", "Hubo un fallo en el minijuego Identifica Emoji")
