"""Módulo `Coche`.

Contiene la clase `Coche` que representa un vehículo dentro del aparcamiento.
Se documentan únicamente los elementos necesarios para entender su uso desde
`Aparcamiento` y la GUI. Se eliminó el código de ejemplo para mantener el
módulo limpio y apto para importación.
"""

from datetime import datetime
import math


class Coche:
    """Representa un coche aparcado.

    Atributos:
      - matricula: cadena en mayúsculas
      - hora_entrada: datetime de entrada
      - hora_salida: datetime de salida (None hasta la salida)
      - tipo: clasificación sencilla (comun/minusvalida/electrica/...)
    """

    TARIFA_POR_HORA = 2.50  # euros por hora
    TIPOS_VALIDOS = {"comun", "minusvalida", "electrica", "resident", "vip"}

    def __init__(self, matricula: str, hora_entrada: datetime = None, tipo: str = "comun"):
        # Normalizar matrícula y tipo
        self.matricula = matricula.upper()
        self.hora_entrada = hora_entrada if hora_entrada else datetime.now()
        self.hora_salida = None
        tipo_norm = tipo.strip().lower() if tipo else "comun"
        self.tipo = tipo_norm if tipo_norm in self.TIPOS_VALIDOS else "comun"

    def pagar(self) -> str:
        """Calcula el importe según el tiempo transcurrido y marca la salida.

        Devuelve un mensaje legible con la información de pago.
        """
        if self.hora_salida is not None:
            return f"ERROR: El vehículo {self.matricula} ya ha sido procesado"

        self.hora_salida = datetime.now()

        tiempo_estancia = self.hora_salida - self.hora_entrada
        horas_totales = tiempo_estancia.total_seconds() / 3600
        horas_cobrar = math.ceil(horas_totales)

        importe = horas_cobrar * self.TARIFA_POR_HORA

        return (f"Matrícula {self.matricula} ({self.tipo}) ha salido del parking: "
                f"ha estado {horas_cobrar} hora(s) - Total a pagar: {importe:.2f} €")