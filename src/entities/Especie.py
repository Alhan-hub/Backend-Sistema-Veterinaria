class Especie:
    def __init__(self, nombre: str) -> None:
        self._nombre = nombre.strip()

    @property
    def nombre(self) -> str:
        return self._nombre

    def hacer_sonido(self) -> str:
        return "Sonido desconocido"

    def __str__(self) -> str:
        return f"{self._nombre}"
