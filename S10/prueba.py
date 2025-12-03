'''

'''

import random

def emoji_translate(text: str) -> str:
    # Diccionario palabra → emoji
    mapping = {
        # Animales
        "perro": "🐶", "gato": "🐱", "raton": "🐭", "tigre": "🐯",
        "conejo": "🐰", "oso": "🐻", "panda": "🐼", "koala": "🐨",
        "mono": "🐵", "cerdo": "🐷", "vaca": "🐮", "pollo": "🐔",
        "pinguino": "🐧", "pulpo": "🐙", "pez": "🐟", "tortuga": "🐢",

        # Emociones / personas
        "sonrisa": "😀", "feliz": "😄", "triste": "😢", "llorar": "😭",
        "enojado": "😡", "amor": "❤️", "beso": "😘", "risa": "😂",
        "miedo": "😱", "pensando": "🤔", "cool": "😎", "ok": "👌",
        "fuerza": "💪", "aplauso": "👏", "hola": "👋",

        # Tecnología
        "python": "🐍", "computadora": "💻", "telefono": "📱",
        "libro": "📚", "bombilla": "💡", "cafe": "☕",
        "dinero": "💸", "cohete": "🚀", "robot": "🤖",

        # Naturaleza
        "fuego": "🔥", "arbol": "🌳", "flor": "🌸", "estrella": "🌟",
        "sol": "☀️", "luna": "🌙", "nube": "☁️", "lluvia": "🌧️",
        "arcoiris": "🌈", "montaña": "⛰️", "mar": "🌊",

        # Comida
        "pizza": "🍕", "hamburguesa": "🍔", "banana": "🍌",
        "manzana": "🍎", "uvas": "🍇", "taco": "🌮",
        "pastel": "🎂", "helado": "🍦", "pan": "🍞",

        # Actividades
        "musica": "🎧", "pelicula": "🎬", "juego": "🎮",
        "deporte": "⚽", "baloncesto": "🏀", "tenis": "🎾",
        "viaje": "✈️", "regalo": "🎁", "fiesta": "🎉",
    }

    # Crear diccionario inverso emoji → palabra
    reverse_mapping = {emoji: word for word, emoji in mapping.items()}

    text = text.strip().lower()

    # Si es palabra → emoji
    if text in mapping:
        return mapping[text]

    # Si es emoji → palabra
    if text in reverse_mapping:
        return reverse_mapping[text]

    return "❓"  # Por defecto si no encuentra nada



def generar_clave():
    # Conjunto de emojis para codificar
    emojis = [
        "😀","😃","😄","😁","😆","😅","🤣","😂","🙂","🙃",
        "😉","😊","😇","🥰","😍","🤩","😘","😗","😚","😙",
        "😋","😛","😜","🤪","😝","🤑","🤗","🤭","🤫","🤔",
        "🤨","😐","😑","😶","😏","😒","🙄","😬","🤥","😌",
        "😔","😪","🤤","😴","😷","🤒","🤕","🤢","🤧","🥵",
        "🥶","🥴","😵","🤯","🤠","🥳","😎","🤓","🧐","😕",
        "😟","🙁","😮","😯","😲","😳","😦","😧","😢","😭",
    ]

    # Todos los caracteres permitidos
    caracteres = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ,.!?-"

    if len(emojis) < len(caracteres):
        raise ValueError("No hay suficientes emojis para mapear todos los caracteres")

    random.shuffle(emojis)

    clave = {c: emojis[i] for i, c in enumerate(caracteres)}
    return clave


def codificar(texto, clave):
    codificado = ""
    for c in texto:
        if c in clave:
            codificado += clave[c]
        else:
            codificado += c  # carácter desconocido: se deja igual
    return codificado


def decodificar(texto_codificado, clave):
    # Crear diccionario inverso emoji → carácter
    inversa = {v: k for k, v in clave.items()}

    decodificado = ""
    i = 0
    while i < len(texto_codificado):
        ch = texto_codificado[i]
        if ch in inversa:
            decodificado += inversa[ch]
        else:
            decodificado += ch
        i += 1

    return decodificado


