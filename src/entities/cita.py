class Cita:
    """
    Gestiona la agenda y facturacion de consultas veterinarias
    """

    def __init__(
        self, id_cita: str, id_mascota: str, motivo: str, costo: float
    ) -> None:
        self._id_cita = id_cita
        self._id_mascota = id_mascota
        self._motivo = motivo
        self._costo = costo

    @property
    def id_cita(self) -> str:
        return self._id_cita

    @property
    def id_mascota(self) -> str:
        return self._id_mascota

    @property
    def motivo(self) -> str:
        return self._motivo

    @property
    def costo(self) -> float:
        return self._costo

    def generar_recibo(self) -> str:
        return f"Cita: {self._id_cita} | Mascota: {self._id_mascota} | Motivo: {self._motivo} | Costo: {self._costo}"
