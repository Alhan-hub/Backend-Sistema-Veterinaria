class Propietario:
    def __init__(self, nombre:str, documento:str, telefono:str):
        self._nombre = nombre.strip()
        self._documento = documento.strip()
        self._telefono = telefono.strip()

    @property
    def nombre(self) -> str:
        return self._nombre
    
    @property
    def documento(self) -> str:
        return self._documento
    
    @property
    def telefono(self) -> str:
        return self._telefono
    
    def __str__(self) -> str:
        return f"Propietario: {self._nombre}  Documento: {self._documento}"