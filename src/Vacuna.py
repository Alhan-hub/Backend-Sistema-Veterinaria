from datetime import date
from decimal import Decimal

class Vacuna:

    def __init__(self, fecha: date, nombre_vacuna: str, costo: Decimal) -> None:
        self._fecha = fecha
        self._nombre_vacuna = nombre_vacuna.strip()
        self._costo = costo

    @property
    def fecha(self) -> date:
        return self._fecha
    
    @property
    def nombre_vacuna(self) -> str:
        return self._nombre_vacuna

    @property
    def costo(self) -> Decimal:
        return self._costo