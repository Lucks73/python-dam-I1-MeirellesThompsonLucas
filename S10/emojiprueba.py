# EmojiCipher GUI completo con emojis reales (librería emoji)
#REALIZADO POR: 
# JUAN CARLOS SANMIGUEL
# LUCAS MEIRELLES
# GONZALO FERNÁNDEZ
# ANA PADILLA
# ANAÍS GONZÁLEZ
"""
FICHERO DE PRUEBA PARA EmojiCipher.PY
"""

import string
import random
import itertools
import tkinter as tk
from tkinter import messagebox, filedialog
import emoji

# --------------------------------------
# Generar lista grande de emojis
# --------------------------------------

def obtener_todos_los_emojis():
    # Diccionario de la librería emoji V2
    lista = []
    for nombre, codigo in emoji.EMOJI_DATA.items():
        if len(nombre) == 1:  # Es un emoji real, no alias
            lista.append(nombre)
    return lista

TODOS_EMOJIS = obtener_todos_los_emojis()

# --------------------------------------
# Generación de clave
# --------------------------------------

def generar_clave():
    letras = list(string.ascii_lowercase)
    random.shuffle(TODOS_EMOJIS)
    ciclo = itertools.cycle(TODOS_EMOJIS)
    clave = {}
    for letra in letras:
        clave[letra] = next(ciclo)
    return clave

clave_global = generar_clave()

# --------------------------------------
# Codificar
# --------------------------------------

def codificar(texto, clave):
    resultado = ""
    for c in texto.lower():
        resultado += clave.get(c, c)
    return resultado

# --------------------------------------
# Decodificar
# --------------------------------------

def decodificar(texto, clave):
    inversa = {v: k for k, v in clave.items()}
    resultado = ""
    temp = ""
    for ch in texto:
        if ch in TODOS_EMOJIS:
            temp = ch
            if temp in inversa:
                resultado += inversa[temp]
                temp = ""
        else:
            resultado += ch
    return resultado

# --------------------------------------
# Sugerir emoji
# --------------------------------------

def sugerir_emoji(palabra, clave):
    inicial = palabra[0].lower()
    return clave.get(inicial, "(sin emoji)")

# --------------------------------------
# Reemplazar palabras en archivo
# --------------------------------------

def reemplazar_archivo(ruta, clave):
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            txt = f.read()
        palabras = txt.split()
        nuevo = []
        for p in palabras:
            em = sugerir_emoji(p, clave)
            if em != "(sin emoji)":
                nuevo.append(em)
            else:
                nuevo.append(p)
        return " ".join(nuevo)
    except FileNotFoundError:
        return "Error: archivo no encontrado"

# --------------------------------------
# GUI - Tkinter
# --------------------------------------

root = tk.Tk()
root.title("EmojiCipher - GUI")
root.geometry("650x550")
root.config(bg="#F0F0F0")

# Caja de entrada
entrada = tk.Text(root, height=6, width=60)
entrada.pack(pady=10)

salida = tk.Text(root, height=6, width=60)
salida.pack(pady=10)

# --------------------------------------
# Funciones para botones
# --------------------------------------

def accion_codificar():
    txt = entrada.get("1.0", tk.END).strip()
    salida.delete("1.0", tk.END)
    salida.insert(tk.END, codificar(txt, clave_global))

def accion_decodificar():
    txt = entrada.get("1.0", tk.END).strip()
    salida.delete("1.0", tk.END)
    salida.insert(tk.END, decodificar(txt, clave_global))

def accion_sugerir():
    txt = entrada.get("1.0", tk.END).strip()
    if not txt:
        messagebox.showerror("Error", "Escribe al menos una palabra.")
        return
    palabra = txt.split()[0]
    messagebox.showinfo("Sugerencia", f"Emoji sugerido: {sugerir_emoji(palabra, clave_global)}")

def accion_archivo():
    ruta = filedialog.askopenfilename()
    if ruta:
        resultado = reemplazar_archivo(ruta, clave_global)
        salida.delete("1.0", tk.END)
        salida.insert(tk.END, resultado)

def accion_clave():
    messagebox.showinfo("Clave actual", str(clave_global))

# --------------------------------------
# Botonera
# --------------------------------------

frame = tk.Frame(root, bg="#DCDCDC")
frame.pack(pady=15)

btn1 = tk.Button(frame, text="Codificar", width=15, command=accion_codificar)
btn2 = tk.Button(frame, text="Decodificar", width=15, command=accion_decodificar)
btn3 = tk.Button(frame, text="Sugerir emoji", width=15, command=accion_sugerir)
btn4 = tk.Button(frame, text="Archivo a emojis", width=15, command=accion_archivo)
btn5 = tk.Button(frame, text="Mostrar clave", width=15, command=accion_clave)

btn1.grid(row=0, column=0, padx=5, pady=5)
btn2.grid(row=0, column=1, padx=5, pady=5)
btn3.grid(row=1, column=0, padx=5, pady=5)
btn4.grid(row=1, column=1, padx=5, pady=5)
btn5.grid(row=2, column=0, columnspan=2, pady=10)

# --------------------------------------
# Comentario sobre ayuda de la IA
# --------------------------------------
"""
La IA ayudó a transformar el programa original en:
- Una aplicación con ventana emergente (Tkinter)
- Uso de todos los emojis reales mediante la librería emoji
- Arquitectura más clara y modular
- Manejo de errores y GUI
"""

root.mainloop()
