## Uso de la IA en el desarrollo del proyecto

He utilizado la inteligencia artificial como una herramienta de apoyo durante la creación de este pequeño gestor de incidencias. Mi interacción fue sencilla y directa: pedí explícitamente que el código fuera claramente comprensible para un estudiante que está empezando en Python. La instrucción fue breve y concreta, y el resultado que obtuve en la primera versión entregada por la IA ya cumplía exactamente con ese objetivo.

La IA me ayudó a diseñar la estructura básica (clase base `Incidencia`, subclases para los distintos tipos, y un `GestorIncidencias` que almacena y gestiona los objetos), a proponer nombres de métodos intuitivos (`abrir`,
`cerrar`, `mostrar_info`) y a escribir comentarios y ejemplos de uso que facilitan la lectura. También sugirió una pequeña función `demo()` para verificar rápidamente el comportamiento sin necesidad de interactuar.

Decidí no modificar la primera versión ofrecida por la IA porque la
interfaz y el diseño ya eran lo suficientemente simples y funcionales para los objetivos del ejercicio. La primera entrega incluía:

- Código legible y bien comentado.
- Una interfaz de texto muy directa (menú) apta para estudiantes.
- Validaciones básicas (prioridad válida, comprobación de id entero).

Por mi parte revisé el código, ejecuté la demostración y comprobé que las funciones principales trabajaban correctamente. Dado que la primera versión era clara y apropiada para una entrega educativa, no fue necesario hacer reestructuraciones profundas ni añadir complejidad innecesaria.

En resumen: la IA ofreció una solución útil y pedagógica con una sola

La versión inicial ya era clara y funcional, por lo que no fue
necesario cambiar `incidencias.py` pero añadí externamente una clase GUI (`gui.py`) que ofrece una interfaz gráfica atractiva sin modificar el código original; la GUI utiliza `incidencias.py`
tal cual.

Vale decir que la IA también me ayudó con la correcta formatación
de este documento "uso_ia.md".
