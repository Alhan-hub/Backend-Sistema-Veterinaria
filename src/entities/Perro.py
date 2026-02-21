from src.entities.Especie import Especie


class Perro(Especie):
    def __init__(self, nombre: str) -> None:
        super().__init__(nombre)

    def hacer_sonido(self) -> str:
        return "Guau"
