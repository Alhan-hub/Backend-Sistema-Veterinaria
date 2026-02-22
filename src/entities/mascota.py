from entities import Propietario


class Mascota:
    def __init__(
        self, nombre: str, edad: int, raza: str, propietario: Propietario
    ) -> None:

        if not nombre or not nombre.strip():
            raise ValueError("El nombre de la mascota no puede estar vacío.")

        if not isinstance(edad, int) or edad < 0:
            raise ValueError("La edad debe ser un número entero positivo.")

        if not raza or not raza.strip():
            raise ValueError("La raza no puede estar vacía.")

        if not isinstance(propietario, Propietario):
            raise TypeError("El propietario debe ser una instancia de Propietario.")

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

    def __str__(self) -> str:
        return f"{self._nombre} ({self._raza}) - {self._edad} años"
