from entities.Mascota import Mascota
from entities import Propietario


class Perro(Mascota):
    def __init__(
        self, nombre: str, edad: int, raza: str, propietario: Propietario
    ) -> None:
        super().__init__(nombre, edad, raza, propietario)
