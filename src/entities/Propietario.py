class Propietario:
    def __init__(self, nombre:str, documento:str, telefono:str):
        self._nombre = nombre.strip()
        self._documento = documento.strip()
        self._telefono = telefono.strip()
