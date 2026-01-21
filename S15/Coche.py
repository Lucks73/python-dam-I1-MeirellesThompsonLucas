from datetime import datetime
import math

class Coche:
    """Clase para gestionar un coche en un parking"""
    
    TARIFA_POR_HORA = 2.50  # Tarifa en euros por hora
    
    def __init__(self, matricula: str, hora_entrada: datetime = None):
        """
        Inicializa un coche en el parking
        
        Args:
            matricula: Matrícula del vehículo
            hora_entrada: Hora de entrada (por defecto la hora actual)
        """
        self.matricula = matricula.upper()
        self.hora_entrada = hora_entrada if hora_entrada else datetime.now()
        self.hora_salida = None
    
    def pagar(self) -> str:
        """
        Calcula el importe a pagar y registra la salida
        
        Returns:
            String con la información del pago
        """
        if self.hora_salida is not None:
            return f"ERROR: El vehículo {self.matricula} ya ha sido procesado"
        
        self.hora_salida = datetime.now()
        
        # Calcular tiempo de estancia
        tiempo_estancia = self.hora_salida - self.hora_entrada
        horas_totales = tiempo_estancia.total_seconds() / 3600
        horas_cobrar = math.ceil(horas_totales)
        
        # Calcular importe
        importe = horas_cobrar * self.TARIFA_POR_HORA

        return f"Matrícula {self.matricula} ha salido del parking: ha estado {horas_cobrar} hora(s) - Total a pagar: {importe:.2f} €"


# Ejemplo de uso
if __name__ == "__main__":
    coche1 = Coche("1234ABC")
    print(coche1.pagar())