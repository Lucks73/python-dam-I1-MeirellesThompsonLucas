"""Módulo `Aparcamiento`.

Gestiona la estructura interna de plazas y expone una API de dominio
segura que la GUI debe usar. Los métodos internos que manipulan la matriz
se mantienen privados (`_llenar_plaza`, `_vaciar_plaza`).
"""

from Coche import Coche


class Aparcamiento:
    """Gestor del aparcamiento: encapsula la lógica de plazas.

    Notas:
      - La GUI debe usar únicamente los métodos públicos: `entrar`, `salir`,
        `listar_coches`, `plazas_libres`, `resumen`.
      - Las estructuras internas (`plazas`, `plazas_libres`, ...) son privadas
        al dominio y no deben ser leídas por la interfaz gráfica.
    """

    def __init__(self, plantas: int, filas: int, columnas: int):
        # Dimensiones del aparcamiento
        self.plantas = plantas
        self.filas = filas
        self.columnas = columnas
        # Matriz 3D de plazas: None o instancias de Coche
        self.plazas = [[[None for _ in range(columnas)] for _ in range(filas)] for _ in range(plantas)]
        # Contador de plazas libres
        self.plazas_libres = plantas * filas * columnas
        # Indicador redundante usado internamente para comprobar disponibilidad
        self.hay_plazas_libres = self.plazas_libres > 0

    def entrar(self, matricula: str, tipo: str = "comun"):
        """Intentar aparcar una matrícula de un `tipo` dado.

        Retorna (ok: bool, mensaje: str). No modifica la GUI ni muestra diálogos.
        """
        matricula = matricula.strip().upper()
        if not matricula:
            return False, "Matrícula vacía"
        if not self.hay_plazas_libres or self.plazas_libres <= 0:
            return False, "No hay plazas libres disponibles"

        coche = Coche(matricula, tipo=tipo)
        posicion = self._llenar_plaza(coche)
        if posicion is None:
            return False, "No se pudo aparcar el vehículo"
        p, f, c = posicion
        return True, f"Vehículo {coche.matricula} aparcado en P{p+1}-F{f+1}-C{c+1}"

    def salir(self, matricula: str):
        """Procesa la salida de la matrícula indicada.

        Retorna (ok: bool, mensaje: str) con el resultado y el texto de pago.
        """
        matricula = matricula.strip().upper()
        if not matricula:
            return False, "Matrícula vacía"

        coche_encontrado = None
        # Buscar el coche en la matriz (operación interna de dominio)
        for p in range(self.plantas):
            for f in range(self.filas):
                for c in range(self.columnas):
                    coche = self.plazas[p][f][c]
                    if coche and coche.matricula == matricula:
                        coche_encontrado = coche
                        break
                if coche_encontrado:
                    break
            if coche_encontrado:
                break

        if coche_encontrado:
            mensaje = self._vaciar_plaza(coche_encontrado)
            return True, mensaje
        return False, f"Vehículo {matricula} no encontrado en el aparcamiento"

    def listar_coches(self) -> list:
        """Devuelve una lista de cadenas con la información visualizable en la GUI.

        Formato por elemento: "[P#-F#-C#]  MATRÍCULA (tipo) → Entrada: hh:mm:ss"
        """
        resultados = []
        for p in range(self.plantas):
            for f in range(self.filas):
                for c in range(self.columnas):
                    coche = self.plazas[p][f][c]
                    if coche:
                        entrada = coche.hora_entrada.strftime("%H:%M:%S")
                        resultados.append(f"[P{p+1}-F{f+1}-C{c+1}]  {coche.matricula:<12} ({coche.tipo}) → Entrada: {entrada}")
        return resultados

    def plazas_libres_count(self) -> int:
        """Devuelve el número de plazas libres (método interno).

        La GUI puede usar `plazas_libres()` como alias público.
        """
        return self.plazas_libres

    def plazas_libres(self) -> int:
        """Alias público para consultar plazas libres."""
        return self.plazas_libres_count()

    def resumen(self) -> dict:
        """Devuelve un resumen con `total`, `libres` y `ocupadas`.

        Útil para estadísticas de la GUI sin exponer estructuras internas.
        """
        total = self.plantas * self.filas * self.columnas
        ocupadas = total - self.plazas_libres
        return {"total": total, "libres": self.plazas_libres, "ocupadas": ocupadas}

    # --- métodos internos (no acceder desde la GUI) ---
    def _vaciar_plaza(self, coche: Coche) -> str:
        """Eliminar un coche de la matriz e incrementar plazas libres.

        Devuelve el mensaje de pago generado por `Coche.pagar()`.
        """
        for p in range(self.plantas):
            for f in range(self.filas):
                for c in range(self.columnas):
                    if self.plazas[p][f][c] == coche:
                        self.plazas[p][f][c] = None
                        self.plazas_libres += 1
                        self.hay_plazas_libres = True
                        return coche.pagar()
        return f"ERROR: Coche con matrícula {coche.matricula} no encontrado en el aparcamiento"

    def _llenar_plaza(self, coche: Coche):
        """Colocar un coche en la primera plaza libre y actualizar contadores.

        Retorna la posición (p, f, c) o None si no hay plazas.
        """
        if not self.hay_plazas_libres:
            return None
        for p in range(self.plantas):
            for f in range(self.filas):
                for c in range(self.columnas):
                    if self.plazas[p][f][c] is None:
                        self.plazas[p][f][c] = coche
                        self.plazas_libres -= 1
                        if self.plazas_libres == 0:
                            self.hay_plazas_libres = False
                        return (p, f, c)
        return None
