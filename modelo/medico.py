from modelo.persona import Persona
from modelo.especialidad import Especialidad


class Medico(Persona):
    """Clase que representa a un médico en el sistema de gestión clínica.

    Hereda de Persona y añade atributos específicos de médicos.

    Attributes:
        id_medico (str): Identificador único del médico.
        especialidad (Especialidad): Especialidad médica del profesional.
        citas (list): Lista de citas asignadas al médico.
    """

    def __init__(self, nombre: str, apellido: str, fecha_nacimiento: str,
                 telefono: str, id_medico: str, especialidad: Especialidad):
        """Inicializa una nueva instancia de Medico.

        Args:
            nombre: Nombre del médico.
            apellido: Apellido del médico.
            fecha_nacimiento: Fecha de nacimiento en formato DD/MM/AAAA.
            telefono: Número de teléfono de contacto.
            id_medico: Identificador único del médico.
            especialidad: Especialidad médica del profesional.
        """
        super().__init__(nombre, apellido, fecha_nacimiento, telefono)
        self._id_medico = id_medico
        self._especialidad = especialidad
        self._citas = []

    def agregar_cita(self, cita):
        """Agrega una cita a la lista de citas del médico.

        Args:
            cita: Objeto Cita a agregar.
        """
        self._citas.append(cita)

    def obtener_citas(self) -> list:
        """Obtiene la lista de citas asignadas al médico.

        Returns:
            list: Lista de objetos Cita.
        """
        return self._citas

    @property
    def id_medico(self) -> str:
        return self._id_medico

    @property
    def especialidad(self) -> Especialidad:
        return self._especialidad