class Propietario:
    def __init__(self, nombre:str, documento:str, telefono:str, email:str) -> None:
        self._nombre = nombre.strip()
        self._documento = documento.strip()
        self._telefono = telefono.strip()
        self._email = email.strip()

    @property
    def nombre(self) -> str:
        return self._nombre
    
    @property
    def documento(self) -> str:
        return self._documento
    
    @property
    def telefono(self) -> str:
        return self._telefono
    
    @property
    def email(self) -> str:
        return self._email

    def __str__(self) -> str:
        return f"Propietario: {self._nombre}  Documento: {self._documento}"