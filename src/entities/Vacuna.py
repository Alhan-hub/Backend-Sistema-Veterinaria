from datetime import date
from decimal import Decimal
from entities import Mascota
class Vacuna:

    def __init__(self, fecha: date, nombre_vacuna: str, costo: Decimal, mascota:Mascota) -> None:
        self.validar_costo(costo)
        self.validar_mascota(mascota)
        self._fecha = fecha
        self._nombre_vacuna = nombre_vacuna.strip()
        self._costo = costo
        self._mascota = mascota

    @property
    def fecha(self) -> date:
        return self._fecha
    
    @property
    def nombre_vacuna(self) -> str:
        return self._nombre_vacuna

    @property
    def costo(self) -> Decimal:
        return self._costo
    
    def validar_costo(self, costo: Decimal) -> None:
        if(costo < Decimal("0")):
            raise ValueError("El costo no puede ser negativo")
        
    def validar_mascota(self, mascota:Mascota) -> None:
        if mascota is None:
            raise ValueError("No se puede registrar una vacuna sin la mascota a la que se le va a aplicar")