from modelo.cita import Cita


class Diagnostico:
    """Clase que representa un diagnóstico médico en el sistema.

    Attributes:
        id_diagnostico (str): Identificador único del diagnóstico.
        descripcion (str): Descripción del diagnóstico.
        tratamiento (str): Tratamiento recomendado.
        observaciones (str): Observaciones adicionales.
        cita (Cita): Cita asociada al diagnóstico.
    """

    def __init__(self, id_diagnostico: str, descripcion: str, tratamiento: str,
                 observaciones: str, cita: Cita):
        """Inicializa una nueva instancia de Diagnostico.

        Args:
            id_diagnostico: Identificador único del diagnóstico.
            descripcion: Descripción del diagnóstico.
            tratamiento: Tratamiento recomendado.
            observaciones: Observaciones adicionales.
            cita: Cita asociada al diagnóstico.
        """
        self._id_diagnostico = id_diagnostico
        self._descripcion = descripcion
        self._tratamiento = tratamiento
        self._observaciones = observaciones
        self._cita = cita

    @property
    def id_diagnostico(self) -> str:
        return self._id_diagnostico

    @property
    def descripcion(self) -> str:
        return self._descripcion

    @property
    def tratamiento(self) -> str:
        return self._tratamiento

    @property
    def observaciones(self) -> str:
        return self._observaciones

    @property
    def cita(self) -> Cita:
        return self._cita