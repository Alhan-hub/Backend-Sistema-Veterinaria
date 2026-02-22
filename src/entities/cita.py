class Cita:
    def __init__(
        self, id_cita: str, id_mascota: str, motivo: str, costo: float
    ) -> None:
        self._id_cita = id_cita
        self._id_mascota = id_mascota
        self._motivo = motivo
        self._costo = costo
