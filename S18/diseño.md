# Diseño del Gestor de Incidencias

Este documento explica de forma clara y sencilla el diseño del mini-proyecto.

## Objetivo

Crear un gestor de incidencias fácil de entender para estudiantes que muestre
conceptos básicos de programación orientada a objetos: clases, herencia,
encapsulación y composición. También incluye un menú simple para interactuar
con el sistema.

## Estructura general

- `Incidencia` (clase base)
- Subclases: `IncidenciaTecnica`, `IncidenciaAdministrativa`, `IncidenciaUsuario`
- `GestorIncidencias` (almacena y gestiona objetos `Incidencia`)
- Script `gestor.py` que contiene la lógica del menú y una función `demo()`.

## Clase `Incidencia`

Propósito: representar una incidencia con datos y operaciones básicas.

Atributos principales:

- `id`: identificador único automático (gestiona la propia clase).
- `descripcion`: texto con el problema.
- `prioridad`: 'baja', 'media' o 'alta'.
- `responsable`: persona encargada.
- `_estado`: atributo privado que almacena el estado ('abierta' o 'cerrada').

Métodos principales:

- `abrir()`: cambia el estado a 'abierta'.
- `cerrar()`: cambia el estado a 'cerrada'.
- `mostrar_info()`: devuelve una cadena legible con los datos de la incidencia.

Encapsulación: el estado es privado (`_estado`) y solo se modifica mediante
los métodos `abrir` y `cerrar`. Esto evita cambios directos al atributo desde
el exterior y cumple el requisito de encapsulación.

## Herencia y subclases

Cada tipo de incidencia hereda de `Incidencia` y añade un atributo propio:

- `IncidenciaTecnica`: añade `equipo` (p. ej. 'PC-01').
- `IncidenciaAdministrativa`: añade `departamento` (p. ej. 'Compras').
- `IncidenciaUsuario`: añade `usuario` (p. ej. 'ana@example.com').

Comportamiento: las subclases sobrescriben `mostrar_info()` para incluir su
información adicional. Esto muestra cómo la herencia permite reutilizar código
y añadir comportamiento específico en cada tipo.

## Clase `GestorIncidencias` (composición)

Responsabilidad: mantener una colección (lista privada `_incidencias`) de
objetos `Incidencia` y ofrecer métodos para crear, listar, buscar y cambiar
el estado de incidencias.

API principal:

- `crear_incidencia(tipo, descripcion, prioridad, responsable, extra)`:
  crea la instancia adecuada según `tipo` ('t', 'a', 'u') y la añade a la lista.
- `listar_incidencias()`: devuelve una lista de cadenas con la información.
- `obtener_por_id(id)`: devuelve la instancia o `None`.
- `cambiar_estado(id, accion)`: cambia el estado usando `abrir()` o `cerrar()`.

La composición se ve en que `GestorIncidencias` contiene instancias de
`Incidencia` y delega en ellas las operaciones sobre el estado.

## Flujo del menú

1. Mostrar opciones al usuario: crear, listar, cambiar estado o salir.
2. Para crear, pedir tipo, descripción, prioridad y responsable. Preguntar
   también el dato extra según el tipo.
3. Para listar, recorrer la colección y mostrar `mostrar_info()` de cada una.
4. Para cambiar estado, pedir el `id` y la acción ('abrir' o 'cerrar'), y
   llamar a `GestorIncidencias.cambiar_estado`.

El menú es intencionalmente simple y con validaciones básicas (p. ej. prioridad
válida, id entero) para que sea fácil de seguir en clase.

## Validaciones y diseño seguro

- Las prioridades se validan al crear (`baja`, `media`, `alta`).
- El `id` se maneja internamente por la clase `Incidencia` para evitar
  colisiones y errores por introducir manualmente el identificador.
- Cambiar estado solo es posible mediante los métodos, no directamente.

## Extensiones posibles (siguientes pasos)

- Persistencia: guardar y cargar la lista de incidencias en JSON.
- Buscar por responsable, prioridad o estado.
- Añadir niveles de acceso o roles para permitir solo ciertos cambios.
- Interfaz gráfica simple (por ejemplo con Tkinter) o web ligera.

## Ejemplo de uso rápido

Para ver una demostración automática incluida en el script:

```bash
python S18/gestor.py --demo
```

Para usar el menú interactivo:

```bash
python S18/gestor.py
```

---

Este diseño busca claridad didáctica: cada parte tiene responsabilidad clara
y el código resultante es fácil de leer y ampliar.

## Nota sobre la interfaz gráfica externa

Se ha añadido posteriormente una clase externa (`gui.py`) que proporciona una
interfaz gráfica llamativa y completa. Esta clase trabaja exclusivamente desde
fuera y no modifica en absoluto el contenido de `incidencias.py`. La GUI
utiliza la funcionalidad existente (creación, listado y cambio de estado) y
solo mejora la experiencia de usuario sin afectar la lógica original.
