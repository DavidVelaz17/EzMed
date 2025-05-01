from modelo.persona import Persona
from modelo.especialidad import Especialidad


class Medico(Persona):
    """
    Clase que representa a un médico en el sistema de gestión clínica.

    Hereda de la clase Persona e incluye información específica del profesional médico.

        Attributes:
            id_medico (str): Identificador único del médico.
            especialidad (Especialidad): Especialidad médica del profesional.
            citas (list): Lista de objetos Cita asignadas al médico.
    """

    def __init__(self, nombre: str, apellido: str, fecha_nacimiento: str,
                 telefono: str, id_medico: str, especialidad: Especialidad):
        """
        Inicializa una nueva instancia de Medico.

            Args:
                nombre (str): Nombre del médico.
                apellido (str): Apellido del médico.
                fecha_nacimiento (str): Fecha de nacimiento del médico (formato DD/MM/AAAA).
                telefono (str): Número de teléfono del médico.
                id_medico (str): Identificador único asignado al médico.
                especialidad (Especialidad): Especialidad médica del profesional.
        """
        super().__init__(nombre, apellido, fecha_nacimiento, telefono)
        self._id_medico = id_medico
        self._especialidad = especialidad
        self._citas = []

    def agregar_cita(self, cita):
        """
        Agrega una cita a la lista de citas del médico.

            Args:
                cita (Cita): Objeto de tipo Cita a agregar a la lista.
        """
        self._citas.append(cita)

    def obtener_citas(self) -> list:
        """
        Obtiene la lista de citas asignadas al médico.

            Returns:
                list: Lista de objetos Cita.
        """
        return self._citas

    @property
    def id_medico(self) -> str:
        """
        str: Devuelve el identificador único del médico.
        """
        return self._id_medico

    @property
    def especialidad(self) -> Especialidad:
        """
        Especialidad: Devuelve la especialidad médica del médico.
        """
        return self._especialidad