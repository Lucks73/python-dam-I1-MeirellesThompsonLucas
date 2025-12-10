#REALIZADO POR: 
# JUAN CARLOS SANMIGUEL
# GONZALO FERNÁNDEZ
# ANA PADILLA
# ANAÍS GONZÁLEZ
# DANIEL RAMOS JIMÉNEZ
# LUCAS MEIRELLES THOMPSON


#Ana	Funciones auxiliares y Configuración Global (# ---------------------- Funciones auxiliares ----------------------)	Se trata de actualizar la UI y normalizar texto. 
#Anais	Traducción emoji (# ---------------------- Traducción emoji --------------------------)	Requiere entender emoji.emojize y demojize.
#Gonzalo	Generar clave (# ---------------------- Generar clave -----------------------------) + Código principal (# ----------------------------- Cödigo ---------------------------)	Mezcla de diccionarios y codificación/decodificación.
#Juan Carlos	Historial (# ---------------------- Historial ------------------------)	Solo registrar y mostrar, exportar y limpiar historial.
#Lucas	Juegos (# ---------------------- Juegos ---------------------------)	Varias funciones de minijuegos con lógica y ventanas emergentes.
#Daniel Ramos	Guardar/cargar clave + Interfaz UI + Wrappers de botones	Más largo, pero mayormente gestión de UI y botones, más fácil que juegos complicados.


# EmojiCiper
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import random
import emoji
import json
import unicodedata

from datetime import datetime

# Mejoras de limpieza de código:
# - Nombres de variables y funciones claros
# - Try/except
# - Comentarios aclaratorios

# Mejoras funcionales en S12:
# - Añadir un historial de codificaciones/decodificaciones realizadas.
# - Permitir exportar el historial a un archivo TXT. 
# - Mejorar la función de mostrar clave, ahora se muestra ordenada.
# Además, ahora se muestran correctamente todos los emojis, antes había algunos que no se detectaban correctamente. 
# - Nuevo minijuego añadido (Adivinar nombre de emoji por cantidad de letras)



# ================================================================
# ---------------------- Configuración global --------------------
# ================================================================
clave_actual = None #clave usada para codificar/decodificar
estado_clave_label = None #indicador visual en la UI

# Paleta de colores para la interfaz
BG_PRIMARY = "#0F172A"
BG_SECONDARY = "#1E293B"
TXT_PRIMARY = "#EAEAEA"
BTN_MAIN = "#6366F1"
BTN_ALT = "#22C55E"
BTN_GAME = "#F59E0B"
INPUT_BG = "#0B1220"

historial = []

# ==================================================================
# ---------------------- Funciones auxiliares ----------------------
# ==================================================================

def actualizar_estado_clave(texto: str):
    """
    Actualiza el texto de la etiqueta de estado de la clave en la interfaz gráfica.
    Parámetros:
        texto (str): Mensaje que se mostrará en la etiqueta de estado.

    Efectos secundarios:
        - Modifica directamente la etiqueta gráfica `estado_clave_label`.
    """
    global estado_clave_label
    if estado_clave_label is not None:
        estado_clave_label.config(text=f"🔐 {texto}")


def normalize_text(s: str) -> str:
    """
    Limpia un texto eliminando acentos y convirtiéndolo a minúsculas.

    Parámetros:
        s (str): Texto de entrada que se desea normalizar.

    Retorna:
        str: Texto normalizado sin acentos, en minúsculas y sin espacios externos.
    """
    s = s.strip().lower()
    nfkd = unicodedata.normalize('NFD', s)
    return "".join(ch for ch in nfkd if not unicodedata.combining(ch))

# ==================================================================
# ---------------------- Traducción emoji --------------------------
# ==================================================================

def emoji_translate(text: str) -> str:
    """
    Traduce palabra → emoji o emoji → palabra.
    Maneja errores en caso de textos no reconocidos.
    Parámetros:
        text (str): Texto o emoji a traducir.

    Retorna:
        str: Emoji correspondiente o palabra; si no se reconoce, devuelve un mensaje de error.
    """
    try:
        text = text.strip()

        # Intento de traducción palabra → emoji
        for lang in ["es", "alias"]:
            em = emoji.emojize(f":{text}:", language=lang)
            if em != f":{text}:":
                return em

        # Intento emoji → palabra (español o inglés)
        dem_es = emoji.demojize(text, language='es')
        dem_en = emoji.demojize(text, language='alias')

        if dem_es != text:
            return dem_es.strip(":")
        if dem_en != text:
            return dem_en.strip(":")

        return "Emoji desconocido"

    except Exception:
        return "Error al traducir"

def formato_clave_legible(clave: dict) -> str:
    """
    Convierte una clave de codificación en un texto legible para mostrar.

    Parámetros:
        clave (dict): Diccionario con caracteres y sus emojis correspondientes.

    Retorna:
        str: Texto formateado mostrando cada par de carácter → emoji.
    """
    texto = "Clave actual:\n\n"
    for k, v in clave.items():
        texto += f"{k} → {v}\n"
    return texto


# ==================================================================
# ---------------------- Generar clave -----------------------------
# ==================================================================

def generar_clave() -> dict:
    """Genera una clave aleatoria asignando un emoji a cada carácter.
    Parámetros:
        Ninguno

    Retorna:
        dict: Diccionario con caracteres como claves y emojis como valores.
              Si ocurre un error, retorna un diccionario vacío.
    """
    try:
        lista_emojis = list(emoji.EMOJI_DATA.keys())
        caracteres = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ,.!?-"

        random.shuffle(lista_emojis)
        lista_emojis = lista_emojis[:len(caracteres)]
        random.shuffle(lista_emojis)

        return {caracteres[i]: lista_emojis[i] for i in range(len(caracteres))}
    except Exception:
        messagebox.showerror("Error", "No se pudo generar la clave")
        return {}


# ================================================================
# ----------------------------- Cödigo ---------------------------
# ================================================================

def codificar(texto: str, clave: dict) -> str:
    """Codifica un texto usando la clave actual.
    
    Parámetros:
        texto (str): Texto a codificar.
        clave (dict): Diccionario que mapea caracteres a emojis.

    Retorna:
        str: Texto codificado; si ocurre un error, devuelve un mensaje de error.
    """
    try:
        return "".join(clave.get(c, c) for c in texto)
    except Exception:
        return "Error al codificar"


def decodificar(texto: str, clave: dict) -> str:
    """Decodifica texto en emojis usando la clave inversa.
    
    Parámetros:
        texto (str): Texto codificado con emojis.
        clave (dict): Diccionario que mapea caracteres a emojis.

    Retorna:
        str: Texto decodificado; si ocurre un error, devuelve un mensaje de error.
    """
    try:
        inversa = {v: k for k, v in clave.items()}
        claves_ordenadas = sorted(inversa.keys(), key=len, reverse=True)

        resultado = ""
        i = 0

        while i < len(texto):
            match = None
            for em in claves_ordenadas:
                if texto.startswith(em, i):
                    match = em
                    break
            if match:
                resultado += inversa[match]
                i += len(match)
            else:
                resultado += texto[i]
                i += 1

        return resultado

    except Exception:
        return "Error al decodificar"
    
# =========================================================
# ---------------------- Historial ------------------------
# =========================================================    

def registrar_historial(tipo, original, resultado):
    """
    Registra una acción en el historial de codificación o decodificación.

    Parámetros:
        tipo (str): Tipo de acción ('Codificado' o 'Decodificado').
        original (str): Texto original antes de la acción.
        resultado (str): Texto resultante después de la acción.

    Retorna:
        None
    """
    registro = {
        "fecha": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "tipo": tipo,
        "original": original,
        "resultado": resultado
    }
    historial.append(registro)

def mostrar_historial(text_widget):
    """
    Muestra el historial de codificación y decodificación en un widget de texto.

    Parámetros:
        text_widget (tk.Text o scrolledtext.ScrolledText): Widget donde se mostrará el historial.

    Retorna:
        None
    """
    text_widget.delete("1.0", tk.END)
    
    if not historial:
        text_widget.insert(tk.END, "No hay registros aún.")
        return

    for i, reg in enumerate(historial, start=1):
        bloque = (
            f"#{i}\n"
            f"Fecha: {reg['fecha']}\n"
            f"Tipo: {reg['tipo']}\n"
            f"Original: {reg['original']}\n"
            f"Resultado: {reg['resultado']}\n"
            f"{'-'*50}\n"
        )
        text_widget.insert(tk.END, bloque)

def limpiar_historial():
    """
    Limpia todos los registros del historial de codificación y decodificación.
    """
    historial.clear()
    messagebox.showinfo("Historial", "Historial eliminado correctamente.")

def exportar_historial_txt():
    """
    Exporta el historial de codificación y decodificación a un archivo TXT.
    """
    if not historial:
        messagebox.showwarning("Aviso", "No hay historial para exportar.")
        return

    archivo = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Archivos TXT", "*.txt")],
        title="Exportar historial"
    )

    if archivo:
        with open(archivo, "w", encoding="utf-8") as f:
            for reg in historial:
                f.write(
                    f"Fecha: {reg['fecha']}\n"
                    f"Tipo: {reg['tipo']}\n"
                    f"Original: {reg['original']}\n"
                    f"Resultado: {reg['resultado']}\n"
                    f"{'-'*50}\n"
                )
        messagebox.showinfo("Éxito", "Historial exportado correctamente.")

# =========================================================
# ---------------------- Juegos ---------------------------
# =========================================================

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

ultima_frase = None
ultima_peli = None

def elegir_item_sin_repetir(diccionario: dict, ultimo):
    """Elige un item al azar evitando repetir el último usado.
    
    Parámetros:
        diccionario (dict): Diccionario del cual seleccionar un elemento.
        ultimo: Clave del último elemento elegido, para evitar repetirlo.

    Retorna:
        tuple: (clave elegida, valor correspondiente) o (None, None) si ocurre un error."""
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
    """Genera pista simple con iniciales y número de palabras.
    
    Parámetros:
        respuesta (str): Texto original del cual generar la pista.

    Retorna:
        str: Pista en formato legible."""
    partes = respuesta.split()
    iniciales = " ".join(p[0] for p in partes)
    return f"Pista: iniciales {iniciales} — {len(partes)} palabra(s)."


def cifrar_parcial_dialogo(dialogo: str, clave: dict) -> str:
    """Cifra parcialmente un diálogo usando la clave.

    Regla simple para que un alumno lo entienda:
    - Para cada palabra, se deja la primera y la última letra sin cifrar
      (si la palabra tiene longitud <=2 se deja completa),
    - Las letras intermedias se reemplazan por su equivalente en la clave
      (si existe), así el texto resultante mezcla letras y emojis.

    Esto hace que "no todas las letras del diálogo estén cifradas".
    """
    if not clave:
        # Si no hay clave, devolvemos el diálogo tal cual
        return dialogo

    palabras = dialogo.split()
    partes_cifradas = []

    for palabra in palabras:
        if len(palabra) <= 2:
            partes_cifradas.append(palabra)
            continue

        # Conservamos la primera y la última letra
        primera = palabra[0]
        ultima = palabra[-1]
        medio = palabra[1:-1]

        # Ciframos caracter a caracter el fragmento 'medio'
        medio_cifrado = ""
        for ch in medio:
            medio_cifrado += clave.get(ch, ch)

        partes_cifradas.append(primera + medio_cifrado + ultima)

    # Unimos con espacios manteniendo cierta legibilidad
    return " ".join(partes_cifradas)


def pedir_respuesta(titulo, mensaje):
    """Ventana emergente que solicita respuesta al usuario.
    
    Parámetros:
        titulo (str): Título de la ventana emergente.
        mensaje (str): Mensaje que se mostrará al usuario.

    Retorna:
        str: Respuesta ingresada por el usuario; None si se cierra la ventana sin responder.
    """
    ventana_resp = tk.Toplevel(ventana)
    ventana_resp.title(titulo)
    ventana_resp.geometry("420x230")

    tk.Label(ventana_resp, text=mensaje, font=("Consolas", 13)).pack(pady=20)

    entrada = tk.Entry(ventana_resp, font=("Consolas", 12))
    entrada.pack(pady=10, fill="x")

    resultado = {"respuesta": None}

    def enviar():
        """Envía el texto ingresado por el usuario y cierra la ventana de respuesta.

    Parámetros:
        (No recibe parámetros directamente; utiliza variables del entorno
        externo, como entrada, resultado y ventana_resp.)

    Retorna:
        None
            Esta función no devuelve valores directamente. Su efecto es
            actualizar resultado["respuesta"] para que pueda ser leído por el
            código que llamó a la ventana de diálogo.
    """

        
        resultado["respuesta"] = entrada.get()
        ventana_resp.destroy()

    tk.Button(ventana_resp, text="Enviar", command=enviar).pack(pady=10)
    entrada.bind("<Return>", lambda e: enviar())

    ventana_resp.transient(ventana)
    ventana_resp.grab_set()
    ventana.wait_window(ventana_resp)

    return resultado["respuesta"]


def jugar_frase_emoji():
    """Minijuego: adivinar frase según emojis.

    Mejoras respecto a la versión original:
    - 3 intentos en lugar de 2
    - Ventana más grande y centralizada
    - Emojis y texto en fuente grande
    - Intentos mostrados gráficamente con corazones
    - Pista mostrada con colores para mayor claridad

    El código está escrito de forma clara y con comentarios para
    que un alumno primerizo lo entienda.
    """
    global ultima_frase
    try:
        # Elegir una frase distinta a la última
        frase, em = elegir_item_sin_repetir(frases_emoji, ultima_frase)
        if not frase:
            return

        ultima_frase = frase
        vidas = 3  # ahora hay 3 intentos/vidas

        # Crear una ventana modal propia para el minijuego
        ventana_juego = tk.Toplevel(ventana)
        ventana_juego.title("Adivina la frase")

        # Tamaño grande y centrado respecto a la ventana principal
        ancho, alto = 700, 420
        try:
            # Intentamos centrar respecto a la ventana principal
            vx = ventana.winfo_rootx()
            vy = ventana.winfo_rooty()
            vw = ventana.winfo_width()
            vh = ventana.winfo_height()
            x = vx + (vw - ancho) // 2
            y = vy + (vh - alto) // 2
        except Exception:
            # Fallback: centrar en pantalla
            sw = ventana_juego.winfo_screenwidth()
            sh = ventana_juego.winfo_screenheight()
            x = (sw - ancho) // 2
            y = (sh - alto) // 2

        ventana_juego.geometry(f"{ancho}x{alto}+{x}+{y}")
        ventana_juego.configure(bg=BG_PRIMARY)

        # Mostrar los emojis en tamaño grande
        lbl_emoji = tk.Label(
            ventana_juego,
            text=em,
            font=("Segoe UI Emoji", 56),
            bg=BG_PRIMARY,
            fg=TXT_PRIMARY
        )
        lbl_emoji.pack(pady=(18, 6))

        # Marco para los corazones (vidas)
        frame_vidas = tk.Frame(ventana_juego, bg=BG_PRIMARY)
        frame_vidas.pack()

        corazones = []
        for i in range(vidas):
            # Cada corazón es una etiqueta que actualizaremos
            lbl = tk.Label(frame_vidas, text="❤️", font=("Arial", 28), bg=BG_PRIMARY)
            lbl.pack(side="left", padx=6)
            corazones.append(lbl)

        # Pista (vacía al principio). Cuando se muestre, tendrá colores.
        pista_label = tk.Label(
            ventana_juego,
            text="",
            font=("Consolas", 13),
            bg="#FFF7AE",  # fondo suave amarillo
            fg="#7C2D12",  # texto marrón oscuro
            wraplength=ancho - 40,
            justify="center"
        )
        pista_label.pack(pady=(12, 6), padx=20, fill="x")

        # Entrada para la respuesta (texto grande)
        entrada = tk.Entry(ventana_juego, font=("Consolas", 20))
        entrada.pack(pady=8, padx=20, fill="x")
        entrada.focus_set()

        # Función auxiliar para actualizar la vista de corazones según vidas
        def actualizar_corazones(n_vidas):
            for idx, lbl in enumerate(corazones):
                if idx < n_vidas:
                    lbl.config(text="❤️")
                else:
                    lbl.config(text="🤍")  # corazón vacío

        # Generar y mostrar pista con estilo cuando quede 1 vida
        def mostrar_pista():
            pista = generar_pista(frase)
            # Cambiamos colores para que la pista llame la atención
            pista_label.config(
                text=f"🎯 Pista: {pista}",
                bg="#D1FAE5",  # verde suave
                fg="#065F46"   # verde oscuro
            )

        # Lógica que se ejecuta al enviar la respuesta
        def enviar():
            nonlocal vidas
            respuesta = entrada.get()

            # Si el usuario cierra o envía vacío, no hacemos nada
            if respuesta is None or respuesta.strip() == "":
                return

            # Comprobación normalizada (quita acentos y espacios)
            if normalize_text(respuesta) == normalize_text(frase):
                messagebox.showinfo("Correcto", "¡Has acertado! 🎉")
                ventana_juego.destroy()
                return

            # Respuesta incorrecta: restar una vida y actualizar UI
            vidas -= 1
            actualizar_corazones(vidas)

            if vidas == 1:
                # Mostrar pista más vistosa cuando queda una vida
                mostrar_pista()
                # Pequeño aviso informativo para el jugador
                messagebox.showinfo("Pista", "Te dejo una pista para ayudarte 💡")

            if vidas <= 0:
                # Se acabaron los intentos: revelar la frase
                messagebox.showerror("Fin del juego", f"La frase era:\n\n{frase}")
                ventana_juego.destroy()

        # Botón Enviar grande y claro
        btn_enviar = tk.Button(
            ventana_juego,
            text="Enviar",
            command=enviar,
            font=("Arial", 14, "bold"),
            bg=BTN_MAIN,
            fg="white",
            width=12
        )
        btn_enviar.pack(pady=12)

        # Permitir enviar con Enter
        entrada.bind("<Return>", lambda e: enviar())

        # Modal: evitar interacción con la ventana principal
        ventana_juego.transient(ventana)
        ventana_juego.grab_set()
        ventana.wait_window(ventana_juego)

    except Exception:
        messagebox.showerror("Error", "Hubo un fallo en el minijuego")

def jugar_pelicula_emoji():
    """Minijuego: adivinar película según emojis.

    Mejoras aplicadas:
    - 3 intentos (vidas) mostradas como corazones
    - Ventana más grande y centrada
    - Pista con colores cuando queda 1 vida
    - Debajo de los emojis se muestra una frase cifrada (diálogo famoso)
    - Al iniciar, salta una ventana con la clave actual como pista

    Código claro y comentado para estudiantes principiantes.
    """
    global ultima_peli, clave_actual
    try:
        peli, em = elegir_item_sin_repetir(peliculas_emoji, ultima_peli)
        if not peli:
            return

        ultima_peli = peli
        vidas = 3  # usamos 3 intentos

        # Algunos diálogos famosos para las películas (pequeña muestra)
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

        # Tomamos el diálogo correspondiente, o un mensaje por defecto
        dialogo = dialogos.get(peli.lower(), "Diálogo no disponible")

        # Si hay clave, ciframos el diálogo para mostrarlo (es una pista cifrada)
        if clave_actual:
            dialogo_cifrado = codificar(dialogo, clave_actual)
        else:
            dialogo_cifrado = "(No hay clave cargada para cifrar la frase)"

        # Crear ventana del juego
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

        # Mostrar emojis en grande
        lbl_emoji = tk.Label(ventana_juego, text=em, font=("Segoe UI Emoji", 56), bg=BG_PRIMARY, fg=TXT_PRIMARY)
        lbl_emoji.pack(pady=(18, 6))

        # Creamos una estructura de dos columnas: izquierda para emojis y diálogo,
        # derecha para mostrar la clave (pista) dentro de la misma ventana.
        contenido = tk.Frame(ventana_juego, bg=BG_PRIMARY)
        contenido.pack(expand=True, fill="both", padx=12, pady=6)

        col_izq = tk.Frame(contenido, bg=BG_PRIMARY)
        col_izq.pack(side="left", expand=True, fill="both")

        col_der = tk.Frame(contenido, bg=BG_PRIMARY)
        col_der.pack(side="right", fill="y", padx=(8, 0))

        # Mostrar la frase cifrada debajo de los emojis (esta es la pista cifrada),
        # pero cifrada parcialmente para que no todas las letras estén cifradas.
        dialogo_parcial = cifrar_parcial_dialogo(dialogo, clave_actual) if clave_actual else dialogo

        lbl_cifrado = tk.Label(
            col_izq,
            text=dialogo_parcial,
            font=("Consolas", 12),
            bg="#0b1a2b",
            fg="#D1FAE5",
            wraplength=(ancho // 2) - 40,
            justify="center"
        )
        lbl_cifrado.pack(pady=(6, 12), padx=20, fill="x")

        # En la columna derecha mostramos la clave actual en un cuadro con scroll.
        tk.Label(col_der, text="Clave (pista)", font=("Consolas", 11, "bold"), bg=BG_PRIMARY, fg=TXT_PRIMARY).pack(pady=(6, 4))

        clave_box = scrolledtext.ScrolledText(col_der, width=30, height=18, font=("Consolas", 10))
        clave_box.pack(padx=4, pady=4)
        if clave_actual:
            clave_box.insert(tk.END, formato_clave_legible(clave_actual))
        else:
            clave_box.insert(tk.END, "No hay clave cargada. Genera o carga una clave para ver la pista.")
        clave_box.config(state="disabled")

        # Marco para las vidas (corazones) en la columna izquierda, bajo el diálogo
        frame_vidas = tk.Frame(col_izq, bg=BG_PRIMARY)
        frame_vidas.pack(pady=(6, 0))

        corazones = []
        for i in range(vidas):
            lbl = tk.Label(frame_vidas, text="❤️", font=("Arial", 28), bg=BG_PRIMARY)
            lbl.pack(side="left", padx=6)
            corazones.append(lbl)

        # Pista legible (vacía inicialmente). Se mostrará con colores cuando quede 1 vida
        pista_label = tk.Label(
            col_izq,
            text="",
            font=("Consolas", 13),
            bg="#FFF7AE",
            fg="#7C2D12",
            wraplength=(ancho // 2) - 40,
            justify="center"
        )
        pista_label.pack(pady=(12, 6), padx=20, fill="x")

        # Entrada para adivinar la película (columna izquierda)
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
            pista_label.config(
                text=f"🎬 Pista: {pista}",
                bg="#E0F2FE",  # azul claro
                fg="#0369A1"   # azul oscuro
            )

        # Lógica del envío de respuesta
        def enviar():
            nonlocal vidas
            respuesta = entrada.get()
            if respuesta is None or respuesta.strip() == "":
                return

            if normalize_text(respuesta) == normalize_text(peli):
                messagebox.showinfo("Correcto", "¡Has acertado! 🎉")
                ventana_juego.destroy()
                return

            # respuesta incorrecta
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
    """Minijuego: adivinar nombre del emoji (versión gráfica).

    Mejoras:
    - 3 intentos (vidas) mostradas como corazones
    - Ventana centrada y más grande
    - Pista con colores cuando queda 1 vida
    - Si el usuario introduce espacios en la respuesta, se interpretan
      como '_' para que no tenga que escribir el guion bajo manualmente.

    El código está escrito de forma clara para estudiantes principiantes.
    """
    try:
        em = random.choice(lista_emojis_identificar)
        # Obtenemos el nombre del emoji y lo normalizamos
        nombre = emoji.demojize(em, language='es').strip(":")
        nombre = normalize_text(nombre)
        # Para nombres compuestos usamos '_' como separador interno
        nombre = nombre.replace(" ", "_")

        # Configuración de la ventana del juego
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

        # Mostrar emoji en grande
        tk.Label(ventana_juego, text=em, font=("Segoe UI Emoji", 64), bg=BG_PRIMARY, fg=TXT_PRIMARY).pack(pady=(18, 6))

        # Progreso del nombre: ocultamos letras (alfanuméricas) con '_' pero
        # dejamos caracteres no alfanuméricos (por ejemplo guiones o '_') visibles.
        # Este juego NO usa vidas: se van revelando letras hasta completar.
        progreso = ["_" if c.isalnum() else c for c in nombre]
        lbl_progreso = tk.Label(ventana_juego, text=" ".join(progreso), font=("Consolas", 22), bg=BG_PRIMARY, fg=TXT_PRIMARY)
        lbl_progreso.pack(pady=10)

        # Pista visual (vacía al principio)
        pista_label = tk.Label(ventana_juego, text="", font=("Consolas", 13), bg="#FFF7AE", fg="#7C2D12", wraplength=ancho-40, justify="center")
        pista_label.pack(pady=(8, 6), padx=12, fill="x")

        # Entrada amplia para escribir la respuesta
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
            # Pista simple: mostrar primera letra y número de caracteres
            pista = f"Comienza con '{nombre[0]}' — {len(nombre)} caracteres"
            pista_label.config(text=f"🔎 Pista: {pista}", bg="#D1FAE5", fg="#065F46")

        # Lógica al enviar respuesta (sin vidas)
        def enviar():
            texto = entrada.get()
            # Permitimos que el usuario ponga espacios en lugar de '_' — los convertimos
            texto = texto.replace(" ", "_")
            intento = normalize_text(texto)

            entrada.delete(0, tk.END)

            if intento == nombre:
                messagebox.showinfo("Correcto", "¡Has acertado! 🎉")
                ventana_juego.destroy()
                return

            # fallo: revelar una letra
            revelar_letra()

            # Si ya no quedan guiones, el usuario pierde (todas las letras han sido reveladas)
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


# ================================================================
# --------------------- Guardar o cargar clave -------------------
# ================================================================

def guardar_clave():
    """Guarda la clave actual en un archivo JSON."""
    global clave_actual
    if not clave_actual:
        messagebox.showwarning("Aviso", "No hay clave para guardar")
        return

    archivo = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("Archivos JSON", "*.json")],
        title="Guardar clave"
    )

    if archivo:
        try:
            with open(archivo, "w", encoding="utf-8") as f:
                json.dump(clave_actual, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Éxito", "Clave guardada correctamente.")
        except Exception:
            messagebox.showerror("Error", "No se pudo guardar la clave")


def cargar_clave():
    """Carga una clave desde archivo JSON."""
    global clave_actual
    archivo = filedialog.askopenfilename(
        filetypes=[("Archivos JSON", "*.json")],
        title="Cargar clave"
    )

    if archivo:
        try:
            with open(archivo, "r", encoding="utf-8") as f:
                clave_actual = json.load(f)

            actualizar_estado_clave("Clave cargada ✔")
            messagebox.showinfo("Éxito", "Clave cargada correctamente.")
            mostrar_main_ui()

        except Exception:
            messagebox.showerror("Error", "Archivo de clave inválido o corrupto")

# ==================================================================
# ------------------------- Interfaz UI ----------------------------
# ==================================================================
ventana = tk.Tk()
ventana.title("EmojiCipher")
ventana.geometry("1200x800")
ventana.configure(bg=BG_PRIMARY)
ventana.resizable(False, False)

# Pantalla inicial
pantalla_inicio = tk.Frame(ventana, bg=BG_PRIMARY)
pantalla_inicio.pack(expand=True, fill="both")

tk.Label(
    pantalla_inicio, text="EmojiCipher",
    font=("Arial", 36, "bold"), bg=BG_PRIMARY, fg=BTN_MAIN
).pack(pady=40)

tk.Label(
    pantalla_inicio,
    text="Genera o carga tu clave para acceder",
    font=("Arial", 16), bg=BG_PRIMARY, fg=TXT_PRIMARY
).pack(pady=20)


def generar_y_cargar_clave():
    """Genera una clave y entra a la app."""
    global clave_actual
    clave_actual = generar_clave()
    actualizar_estado_clave("Clave generada ✔")
    messagebox.showinfo("Clave", "Clave generada correctamente.")
    mostrar_main_ui()


tk.Button(
    pantalla_inicio, text="Generar clave",
    font=("Arial", 14, "bold"), bg=BTN_MAIN, fg="white",
    width=25, height=2, command=generar_y_cargar_clave
).pack(pady=10)

tk.Button(
    pantalla_inicio, text="Cargar clave",
    font=("Arial", 14, "bold"), bg=BTN_ALT, fg="white",
    width=25, height=2, command=cargar_clave
).pack(pady=10)

# ==================================================================
# ----------------- Función que muestra el menú --------------------
# ==================================================================
def mostrar_main_ui():
    pantalla_inicio.pack_forget()

    main_frame = tk.Frame(ventana, bg=BG_PRIMARY)
    main_frame.pack(expand=True, fill="both")

    global estado_clave_label
    estado_clave_label = tk.Label(
        main_frame, text="Clave actual ✔",
        font=("Consolas", 12, "bold"),
        bg=BG_PRIMARY, fg=TXT_PRIMARY
    )
    estado_clave_label.pack(pady=5)

    notebook = ttk.Notebook(main_frame)
    notebook.pack(expand=True, fill="both", padx=10, pady=10)

    # ---------------------- PESTAÑA CODIFICACIÓN ----------------------
    tab_cod = tk.Frame(notebook, bg=BG_SECONDARY)
    notebook.add(tab_cod, text="Codificación")

    entrada_cod = scrolledtext.ScrolledText(
        tab_cod, width=85, height=10, font=("Consolas", 12),
        bg=INPUT_BG, fg=TXT_PRIMARY, insertbackground=TXT_PRIMARY
    )
    entrada_cod.pack(padx=10, pady=10)

    salida_cod = scrolledtext.ScrolledText(
        tab_cod, width=85, height=10, font=("Consolas", 12),
        bg=INPUT_BG, fg=TXT_PRIMARY, insertbackground=TXT_PRIMARY
    )
    salida_cod.pack(padx=10, pady=10)

    frame_cod_btn = tk.Frame(tab_cod, bg=BG_SECONDARY)
    frame_cod_btn.pack(pady=10)

    def add_btn(parent, text, cmd, color):
        return tk.Button(
            parent, text=text, command=cmd,
            font=("Arial", 12, "bold"),
            bg=color, fg="white", width=28, height=3
        )

    add_btn(frame_cod_btn, "Codificar", lambda: codificar_wrapper(entrada_cod, salida_cod), BTN_MAIN).grid(row=0, column=0, padx=10, pady=5)
    add_btn(frame_cod_btn, "Decodificar", lambda: decodificar_wrapper(salida_cod), BTN_ALT).grid(row=0, column=1, padx=10, pady=5)
    add_btn(frame_cod_btn, "Traducir emoji/palabra", lambda: traducir_wrapper(entrada_cod, salida_cod), BTN_GAME).grid(row=1, column=0, padx=10, pady=5)
    add_btn(frame_cod_btn, "Ver clave", lambda: messagebox.showinfo("Clave actual", formato_clave_legible(clave_actual)), BTN_MAIN).grid(row=1, column=1, padx=10, pady=5)

    # ---------------------- PESTAÑA JUEGOS ----------------------
    tab_juegos = tk.Frame(notebook, bg=BG_SECONDARY)
    notebook.add(tab_juegos, text="Minijuegos")

    frame_juegos = tk.Frame(tab_juegos, bg=BG_SECONDARY)
    frame_juegos.pack(pady=40)

    add_btn(frame_juegos, "Adivina la frase con emojis", jugar_frase_emoji, BTN_GAME).grid(row=0, column=0, padx=10, pady=5)
    add_btn(frame_juegos, "Adivina la película", jugar_pelicula_emoji, BTN_GAME).grid(row=0, column=1, padx=10, pady=5)
    add_btn(frame_juegos, "Identifica el emoji", jugar_identifica_emoji, BTN_GAME).grid(row=1, column=0, padx=10, pady=5)



    # ---------------------- PESTAÑA CLAVE ----------------------
    tab_clave = tk.Frame(notebook, bg=BG_SECONDARY)
    notebook.add(tab_clave, text="Gestionar clave")

    frame_clave = tk.Frame(tab_clave, bg=BG_SECONDARY)
    frame_clave.pack(pady=40)

    add_btn(frame_clave, "Guardar clave", guardar_clave, BTN_MAIN).grid(row=0, column=0, padx=10, pady=5)
    add_btn(frame_clave, "Cargar clave", cargar_clave, BTN_ALT).grid(row=0, column=1, padx=10, pady=5)

    #  ---------------------- PESTAÑA HISTORIAL  ----------------------
    tab_historial = tk.Frame(notebook, bg=BG_SECONDARY)
    notebook.add(tab_historial, text="Historial")

    frame_hist = tk.Frame(tab_historial, bg=BG_SECONDARY)
    frame_hist.pack(pady=10)

    historial_text = scrolledtext.ScrolledText(
        tab_historial,
        width=110,
        height=25,
        font=("Consolas", 11),
        bg=INPUT_BG,
        fg=TXT_PRIMARY,
        insertbackground=TXT_PRIMARY
    )
    historial_text.pack(padx=10, pady=10)

# Botones del historial
    btn_ver_hist = tk.Button(
        frame_hist,
        text="Ver historial",
        font=("Arial", 12, "bold"),
        bg=BTN_MAIN,
        fg="white",
        width=22,
        command=lambda: mostrar_historial(historial_text)
    )

    btn_limpiar_hist = tk.Button(
        frame_hist,
        text="Limpiar historial",
        font=("Arial", 12, "bold"),
        bg=BTN_ALT,
        fg="white",
        width=22,
        command=lambda: limpiar_historial()
    )

    btn_exportar_hist = tk.Button(
        frame_hist,
        text="Exportar historial",
        font=("Arial", 12, "bold"),
        bg=BTN_GAME,
        fg="white",
        width=22,
        command=lambda: exportar_historial_txt()
    )

    btn_ver_hist.grid(row=0, column=0, padx=10)
    btn_limpiar_hist.grid(row=0, column=1, padx=10)
    btn_exportar_hist.grid(row=0, column=2, padx=10)


# ================================================================
# ---------------------- WRAPPERS DE BOTONES ----------------------
# ================================================================

def codificar_wrapper(entrada_widget, salida_widget):
    """
    Obtiene texto de un widget, lo codifica usando la clave actual y muestra el resultado.

    Parámetros:
        entrada_widget (tk.Text o scrolledtext.ScrolledText): Widget de entrada con el texto a codificar.
        salida_widget (tk.Text o scrolledtext.ScrolledText): Widget donde se mostrará el texto codificado.

    Retorna:
        None
    """
    global clave_actual
    texto = entrada_widget.get("1.0", tk.END).strip()
    
    if not texto:
        messagebox.showwarning("Aviso", "Escribe algo para codificar")
        return

    resultado = codificar(texto, clave_actual)
    salida_widget.delete("1.0", tk.END)
    salida_widget.insert(tk.END, resultado)

    registrar_historial("Codificado", texto, resultado)


def decodificar_wrapper(salida_widget):
    """
    Obtiene texto de un widget, lo decodifica usando la clave actual y muestra el resultado.

    Parámetros:
        salida_widget (tk.Text o scrolledtext.ScrolledText): Widget que contiene el texto a decodificar y donde se mostrará el resultado.

    Retorna:
        None
    """
    global clave_actual
    texto = salida_widget.get("1.0", tk.END).strip()

    if not texto:
        messagebox.showwarning("Aviso", "No hay texto para decodificar")
        return

    resultado = decodificar(texto, clave_actual)
    salida_widget.delete("1.0", tk.END)
    salida_widget.insert(tk.END, resultado)

    registrar_historial("Decodificado", texto, resultado)



def traducir_wrapper(entrada, salida):
    """Traduce palabra ↔ emoji."""
    texto = entrada.get("1.0", tk.END).strip()
    if not texto:
        messagebox.showwarning("Aviso", "Escribe algo para traducir")
        return
    salida.delete("1.0", tk.END)
    salida.insert(tk.END, emoji_translate(texto))


# Lanzar aplicación
ventana.mainloop()
