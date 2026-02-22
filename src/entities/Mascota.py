from entities import Propietario

class Mascota:
    def __init__(self, nombre:str, edad:int, raza:str, propietario:Propietario) -> None:
        self.validar_edad(edad)
        self._nombre = nombre.strip()
        self._edad = edad
        self._raza = raza.strip()
        self._propietario = propietario

    @property
    def nombre(self) -> str:
        return self._nombre
    
    @property
    def edad(self) -> int:
        return self._edad
    
    @property
    def raza(self) -> str:
        return self._raza
    
    @property
    def propietario(self) -> Propietario:
        return self._propietario

    def validar_edad(self, edad:int) -> None:
        if edad < 0:
            raise ValueError("La edad de su mascota no puede ser negativa")