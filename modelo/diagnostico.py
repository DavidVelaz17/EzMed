from modelo.cita import Cita


class Diagnostico:
    """
    Clase que representa un diagnóstico médico en el sistema.

    Un diagnóstico contiene información médica derivada de una consulta específica (cita),
    incluyendo su descripción, tratamiento recomendado y observaciones.

        Attributes:
            id_diagnostico (str): Identificador único del diagnóstico.
            descripcion (str): Descripción médica del diagnóstico.
            tratamiento (str): Tratamiento sugerido para el paciente.
            observaciones (str): Observaciones adicionales del médico.
            cita (Cita): Cita médica a la cual pertenece el diagnóstico.
    """
    def __init__(self, id_diagnostico: str, descripcion: str, tratamiento: str,
                 observaciones: str, cita: Cita):
        """
        Inicializa una nueva instancia de Diagnostico.

            Args:
                id_diagnostico (str): Identificador único del diagnóstico.
                descripcion (str): Descripción del diagnóstico médico.
                tratamiento (str): Tratamiento recomendado.
                observaciones (str): Observaciones adicionales del médico.
                cita (Cita): Cita médica a la que se asocia este diagnóstico.
        """
        self._id_diagnostico = id_diagnostico
        self._descripcion = descripcion
        self._tratamiento = tratamiento
        self._observaciones = observaciones
        self._cita = cita

    @property
    def id_diagnostico(self) -> str:
        """
        str: Devuelve el identificador único del diagnóstico.
        """
        return self._id_diagnostico

    @property
    def descripcion(self) -> str:
        """
        str: Devuelve la descripción del diagnóstico.
        """
        return self._descripcion

    @property
    def tratamiento(self) -> str:
        """
        str: Devuelve el tratamiento recomendado.
        """
        return self._tratamiento

    @property
    def observaciones(self) -> str:
        """
        str: Devuelve las observaciones adicionales del médico.
        """
        return self._observaciones

    @property
    def cita(self) -> Cita:
        """
        Cita: Devuelve la cita médica asociada a este diagnóstico.
        """
        return self._cita