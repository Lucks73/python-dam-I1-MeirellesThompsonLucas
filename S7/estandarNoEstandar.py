import math
import requests # pip install requests

# Parte de matemáticas
print("Raíz cuadrada de 16:", math.sqrt(16))
print("2 elevado a 3:", math.pow(2, 3))
print("El valor de pi es:", math.pi)

# Parte de chistes
url = "https://official-joke-api.appspot.com/random_joke"
try:
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        chiste = respuesta.json()  # Convertimos la respuesta JSON a diccionario
        print(f"\nURL del chiste: {respuesta.url}")
        print("Chiste del día:")
        print(chiste["setup"])  # Primera parte del chiste
        print(chiste["punchline"])  # Remate
    else:
        print("No se pudo obtener el chiste. Código de estado:", respuesta.status_code)
except requests.RequestException as e:
    print("Ocurrió un error al solicitar el chiste:", e)
