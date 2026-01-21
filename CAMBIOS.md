# Gestión de Parking con POO - Lucas Meirelles Thompson

## 1. Interfaz pública definida (qué métodos y por qué)

En este proyecto se ha definido una **interfaz pública clara** en la clase `Aparcamiento`.  
Esta interfaz es el único punto de comunicación entre la lógica del sistema y la interfaz gráfica (`ParkingGUI`).  
De esta forma, la GUI no accede directamente a estructuras internas como la matriz `plazas` ni a contadores internos.

Los métodos públicos disponibles son:

### `entrar(matricula, tipo)`
Registra la entrada de un coche al parking.

- Normaliza la matrícula.
- Comprueba si hay plazas disponibles.
- Crea un objeto `Coche`.
- Llama al método privado `_llenar_plaza()` para colocarlo.
- Devuelve un booleano y un mensaje.

Este método existe para que la GUI **no tenga que crear coches ni manipular la matriz interna**.

---

### `salir(matricula)`
Procesa la salida de un vehículo.

- Busca el coche dentro de la matriz.
- Llama al método privado `_vaciar_plaza()`.
- Devuelve el mensaje generado por `Coche.pagar()`.

Permite que la GUI solicite una salida sin conocer cómo se almacenan los coches.

---

### `listar_coches()`
Devuelve una lista de cadenas listas para mostrar en pantalla.

Cada elemento incluye:

- posición (planta, fila, columna)
- matrícula
- tipo
- hora de entrada

Este método evita que la GUI tenga que recorrer la matriz directamente.

---

### `plazas_libres()`
Devuelve el número actual de plazas disponibles.

Es un alias público que encapsula el acceso al contador interno.

---

### `resumen()`
Devuelve un diccionario con:

- plazas totales
- plazas libres
- plazas ocupadas

Este método permite mostrar estadísticas sin exponer datos internos.

---

Gracias a esta interfaz:

- La GUI solo llama a métodos.
- No toca variables internas.
- El código queda desacoplado y limpio.

---

## 2. Cambios futuros preparados

El diseño actual permite ampliaciones sin romper la aplicación:

- Si en el futuro quiero:
  - aplicar tarifas distintas según el tipo de coche
  - guardar datos en archivos
  - añadir reservas
  - mostrar informes o gráficos  
  Solo tendría que modificar `Aparcamiento` o `Coche`.

Los métodos privados:

- `_llenar_plaza()`
- `_vaciar_plaza()`

encapsulan completamente la lógica interna.  
Esto permite cambiar la estructura (por ejemplo usar una base de datos) sin tocar la GUI.

Además:

- El uso de `resumen()` permite añadir nuevas estadísticas fácilmente.
- `listar_coches()` puede ampliarse sin modificar la interfaz.

El proyecto queda preparado para escalar.

---

## 3. Parte que más me ayudó a entender la POO

Lo que más me ayudó a entender la POO fue ver claramente la separación entre:

- **Interfaz (ParkingGUI)**
- **Lógica (Aparcamiento)**
- **Datos (Coche)**

He comprendido que:

- La clase principal no debe gestionar datos directamente.
- Debe coordinar otras clases.
- Cada clase tiene una responsabilidad concreta.

Ejemplo real:

- La GUI no calcula pagos.
- La GUI no almacena coches.
- Solo llama a métodos.

Esto me permitió entender mejor:

- encapsulación
- comunicación entre objetos
- diseño limpio

Ahora entiendo cómo se construyen aplicaciones reales usando clases que colaboran entre sí.

---

## 4. Cómo usé la IA (qué acepté y qué descarté)

Utilicé la IA como herramienta de apoyo, no como sustituto.

La usé para:

- entender mejor la estructura entre clases
- mejorar la organización del código
- escribir documentación clara
- revisar buenas prácticas de POO

Acepté:

- sugerencias sobre encapsulación
- separación entre GUI y lógica
- uso de métodos privados
- diseño de API limpia

Descarté:

- código que no entendía
- soluciones demasiado complejas
- propuestas que no encajaban con el enunciado

Todo lo que incluí en el proyecto:

- lo revisé
- lo entendí
- lo adapté a mi estilo

En resumen:  
La IA me ayudó como guía, pero **las decisiones finales fueron mías**.

---

**Fin del documento**
