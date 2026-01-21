from Coche import Coche

class Aparcamiento:
    """Clase para gestionar un aparcamiento con múltiples plantas"""
    
    def __init__(self, plantas: int, filas: int, columnas: int):
        """
        Inicializa el aparcamiento
        
        Args:
            plantas: Número de plantas
            filas: Número de filas por planta
            columnas: Número de columnas por fila
        """
        self.plantas = plantas
        self.filas = filas
        self.columnas = columnas
        self.plazas = [[[None for _ in range(columnas)] for _ in range(filas)] for _ in range(plantas)]
        self.plazas_libres = plantas * filas * columnas
        self.hay_plazas_libres = self.plazas_libres > 0
    
    def vaciar_plaza(self, coche: Coche) -> str:
        """
        Vacía la plaza ocupada por el coche dado, calcula el pago y devuelve la información
        
        Args:
            coche: El objeto Coche que ocupa la plaza a vaciar
            
        Returns:
            String con la información del pago o mensaje de error
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
    
    def llenar_plaza(self, coche: Coche):
        """
        Coloca el coche en la primera plaza libre disponible
        
        Args:
            coche: El objeto Coche a aparcar
        """
        if not self.hay_plazas_libres:
            print("No hay plazas libres disponibles")
            return
        
        for p in range(self.plantas):
            for f in range(self.filas):
                for c in range(self.columnas):
                    if self.plazas[p][f][c] is None:
                        self.plazas[p][f][c] = coche
                        self.plazas_libres -= 1
                        if self.plazas_libres == 0:
                            self.hay_plazas_libres = False
                        return
