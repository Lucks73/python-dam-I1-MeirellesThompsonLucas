# Diseño: Sistema de pedidos - S17

**Descripción del sistema**

Un sistema sencillo para gestionar pedidos de una tienda de videojuegos. Permite:
- Definir juegos con su precio y descripción.
- Mantener tiendas con inventario de juegos.
- Crear pedidos que contengan juegos, pagar, enviar y cancelar pedidos.

Se han diseñado reglas para evitar estados inválidos (p. ej. no enviar un pedido sin pagar).

**Listado de clases**

- `Game`
- `Store`
- `Order`

**Qué representa cada clase**

- `Game`: un videojuego con título, precio, descripción y lista de tiendas donde está disponible.
- `Store`: una tienda física/virtual que mantiene un inventario de `Game` y su stock.
- `Order`: un pedido de cliente que contiene juegos, cantidades, importe total y estado (CREATED, PAID, SHIPPED, CANCELLED).

**Responsabilidades de cada clase**

- `Game`:
  - Almacenar la información básica del juego (título, precio, descripción).
  - Consultar disponibilidad por tienda.
  - Proveer métodos de acceso (getters) en lugar de acceso público a atributos.

- `Store`:
  - Mantener un inventario (qué juegos tiene y en qué cantidad).
  - Añadir juegos al inventario y comprobar disponibilidad.
  - No modifica pedidos; solo gestiona su propio stock.

- `Order`:
  - Gestionar la colección de juegos y cantidades en el pedido.
  - Calcular y mantener el importe total (recalculado internamente).
  - Controlar el flujo de estados mediante métodos: `add_item`, `remove_item`, `pay`, `ship`, `cancel`.
  - Evitar transiciones inválidas (por ejemplo, pagar dos veces o enviar sin pagar).

**Notas de diseño**

- Encapsulación: los atributos principales son privados (prefijados con `_`) y solo cambian mediante métodos.
- Métodos representativos del dominio: pagar, enviar, cancelar, añadir/quitar artículos.
- Validaciones: cantidades positivas, stock positivo al añadir a la tienda, total no negativo.

El archivo de implementación asociado es `s17_pedidos.py`.

Ruta de los archivos:
- Código: [S17/s17_pedidos.py](S17/s17_pedidos.py)
- Diseño: [S17/s17_diseño.md](S17/s17_diseño.md)

**Interfaz gráfica añadida**

- Se incluye una interfaz gráfica muy simple usando `tkinter` dentro de `s17_pedidos.py`.
- Funcionalidades visibles en la GUI:
  - Ver el inventario de la tienda y su stock.
  - Añadir juegos al pedido indicando cantidad.
  - Quitar items del pedido (quita 1 unidad por acción en esta versión simple).
  - Pagar, enviar y cancelar el pedido con validaciones (no enviar sin pagar, no pagar dos veces, etc.).
- La GUI está pensada como herramienta didáctica: interactiva y fácil de seguir para un principiante.

**Comentario final**

- `Uso de la IA` : Se ha utilizado la IA pra la codificación y comentario del código con base en
una serie de requisitos que se han pedido por prompt. La IA también ha creado el fichero `.md`
y comentado la estrucura del código creado.

- `Decisión personal` : Las decisiones personales que he tomado yo han sido relacionadas con la temática
del proyecto y también con el mínimo de funcionalidades que deberían estar dispuestas al usuario. Por
último he decidio que una interfaz gráfica, aunque sencilla, dejaría más clara la intención y funcionalidad
del sistema de compras.