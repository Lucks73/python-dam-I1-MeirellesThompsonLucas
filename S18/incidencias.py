"""
Gestor de incidencias simple para estudiantes.

Contiene:
- Clase `Incidencia` con encapsulación del estado.
- Tres subclases: técnica, administrativa y de usuario.
- Clase `GestorIncidencias` que almacena y gestiona incidencias.
- Menú interactivo y opción `--demo` para ejecutar una demostración automática.

Ejecutar: `python S18/gestor.py` para usar el menú.
       `python S18/gestor.py --demo` para ver una demo no interactiva.
"""

import sys


class Incidencia:
    """Clase base que representa una incidencia.

    Atributos:
        id (int): identificador único automático.
        descripcion (str): texto con la descripción del problema.
        prioridad (str): 'baja', 'media' o 'alta'.
        responsable (str): persona encargada.
        _estado (str): privado; solo puede cambiar mediante métodos.
    """

    _next_id = 1

    def __init__(self, descripcion, prioridad, responsable):
        self.id = Incidencia._next_id
        Incidencia._next_id += 1
        self.descripcion = descripcion
        self.prioridad = prioridad
        self.responsable = responsable
        self._estado = 'abierta'  # estado por defecto

    @property
    def estado(self):
        """Propiedad de solo lectura para consultar el estado."""
        return self._estado

    def abrir(self):
        """Abrir la incidencia (cambiar su estado a 'abierta')."""
        if self._estado != 'abierta':
            self._estado = 'abierta'

    def cerrar(self):
        """Cerrar la incidencia (cambiar su estado a 'cerrada')."""
        if self._estado != 'cerrada':
            self._estado = 'cerrada'

    def mostrar_info(self):
        """Devolver una cadena con la información básica de la incidencia."""
        return (
            f"[{self.id}] {self.descripcion} | Prioridad: {self.prioridad} | "
            f"Responsable: {self.responsable} | Estado: {self._estado}"
        )


class IncidenciaTecnica(Incidencia):
    """Incidencia técnica con campo extra `equipo`."""

    def __init__(self, descripcion, prioridad, responsable, equipo='Desconocido'):
        super().__init__(descripcion, prioridad, responsable)
        self.equipo = equipo

    def mostrar_info(self):
        base = super().mostrar_info()
        return base + f" | Tipo: Técnica | Equipo: {self.equipo}"


class IncidenciaAdministrativa(Incidencia):
    """Incidencia administrativa con campo extra `departamento`."""

    def __init__(self, descripcion, prioridad, responsable, departamento='General'):
        super().__init__(descripcion, prioridad, responsable)
        self.departamento = departamento

    def mostrar_info(self):
        base = super().mostrar_info()
        return base + f" | Tipo: Administrativa | Departamento: {self.departamento}"


class IncidenciaUsuario(Incidencia):
    """Incidencia de usuario con campo extra `usuario`."""

    def __init__(self, descripcion, prioridad, responsable, usuario='Anónimo'):
        super().__init__(descripcion, prioridad, responsable)
        self.usuario = usuario

    def mostrar_info(self):
        base = super().mostrar_info()
        return base + f" | Tipo: Usuario | Usuario: {self.usuario}"


class GestorIncidencias:
    """Clase que almacena y gestiona incidencias usando composición."""

    def __init__(self):
        self._incidencias = []  # lista privada de incidencias

    def crear_incidencia(self, tipo, descripcion, prioridad, responsable, extra=''):
        """Crear una incidencia del `tipo` indicado.

        `tipo` puede ser: 't' (técnica), 'a' (administrativa), 'u' (usuario).
        """
        tipo = tipo.lower()
        if tipo == 't':
            inc = IncidenciaTecnica(descripcion, prioridad, responsable, equipo=extra or 'Desconocido')
        elif tipo == 'a':
            inc = IncidenciaAdministrativa(descripcion, prioridad, responsable, departamento=extra or 'General')
        else:
            inc = IncidenciaUsuario(descripcion, prioridad, responsable, usuario=extra or 'Anónimo')

        self._incidencias.append(inc)
        return inc

    def listar_incidencias(self):
        """Devolver una lista de cadenas con la información de cada incidencia."""
        return [inc.mostrar_info() for inc in self._incidencias]

    def obtener_por_id(self, id_buscar):
        """Buscar una incidencia por su id. Devuelve la instancia o None."""
        for inc in self._incidencias:
            if inc.id == id_buscar:
                return inc
        return None

    def cambiar_estado(self, id_buscar, accion):
        """Cambiar el estado llamando a los métodos de la incidencia.

        `accion` puede ser 'abrir' o 'cerrar'.
        """
        inc = self.obtener_por_id(id_buscar)
        if not inc:
            return False, 'Incidencia no encontrada'

        if accion == 'abrir':
            inc.abrir()
            return True, 'Incidencia abierta'
        elif accion == 'cerrar':
            inc.cerrar()
            return True, 'Incidencia cerrada'
        else:
            return False, 'Acción inválida'


def pedir_prioridad():
    """Pedir prioridad al usuario y devolverla validada."""
    while True:
        p = input('Prioridad (baja/media/alta): ').strip().lower()
        if p in ('baja', 'media', 'alta'):
            return p
        print('Prioridad no válida. Intente de nuevo.')


def menu():
    gestor = GestorIncidencias()

    while True:
        print('\n--- Gestor de Incidencias ---')
        print('1. Crear incidencia')
        print('2. Listar incidencias')
        print('3. Cambiar estado')
        print('4. Salir')

        opcion = input('Elige una opción: ').strip()

        if opcion == '1':
            print('Tipos: (t)écnica, (a)dministrativa, (u)suario')
            tipo = input('Tipo: ').strip().lower()
            descripcion = input('Descripción: ').strip()
            prioridad = pedir_prioridad()
            responsable = input('Responsable: ').strip()
            extra = ''
            if tipo == 't':
                extra = input('Equipo afectado: ').strip()
            elif tipo == 'a':
                extra = input('Departamento: ').strip()
            else:
                extra = input('Usuario afectado: ').strip()

            inc = gestor.crear_incidencia(tipo, descripcion, prioridad, responsable, extra)
            print(f'Incidencia creada con id {inc.id}')

        elif opcion == '2':
            listado = gestor.listar_incidencias()
            if not listado:
                print('No hay incidencias registradas.')
            else:
                print('\n'.join(listado))

        elif opcion == '3':
            try:
                id_sel = int(input('Id de la incidencia: ').strip())
            except ValueError:
                print('Id no válido.')
                continue

            accion = input("Acción ('abrir' o 'cerrar'): ").strip().lower()
            ok, msg = gestor.cambiar_estado(id_sel, accion)
            print(msg)

        elif opcion == '4':
            print('Saliendo. ¡Hasta luego!')
            break
        else:
            print('Opción no reconocida. Intente otra vez.')


def demo():
    """Demostración no interactiva para comprobar el funcionamiento."""
    gestor = GestorIncidencias()
    gestor.crear_incidencia('t', 'Pantalla azul al iniciar', 'alta', 'María', extra='PC-01')
    gestor.crear_incidencia('a', 'Solicitud de material', 'baja', 'Carlos', extra='Compras')
    gestor.crear_incidencia('u', 'No puedo acceder a la app', 'media', 'Ana', extra='ana@example.com')

    print('Listado inicial:')
    for line in gestor.listar_incidencias():
        print(line)

    print('\nCerrando la incidencia 1...')
    gestor.cambiar_estado(1, 'cerrar')

    print('\nListado tras cerrar la 1:')
    for line in gestor.listar_incidencias():
        print(line)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--demo':
        demo()
    else:
        menu()
