from modelo.persona import Persona


class Paciente(Persona):
    """Clase que representa a un paciente en el sistema de gestión clínica.

    Hereda de Persona y añade atributos específicos de pacientes.

    Attributes:
        id_paciente (str): Identificador único del paciente.
        historial_medico (list): Lista de consultas médicas del paciente.
    """

    def __init__(self, nombre: str, apellido: str, fecha_nacimiento: str,
                 telefono: str, id_paciente: str):
        """Inicializa una nueva instancia de Paciente.

        Args:
            nombre: Nombre del paciente.
            apellido: Apellido del paciente.
            fecha_nacimiento: Fecha de nacimiento en formato DD/MM/AAAA.
            telefono: Número de teléfono de contacto.
            id_paciente: Identificador único del paciente.
        """
        super().__init__(nombre, apellido, fecha_nacimiento, telefono)
        self._id_paciente = id_paciente
        self._historial_medico = []

    def agregar_consulta(self, consulta: dict):
        """Agrega una consulta médica al historial del paciente.

        Args:
            consulta: Diccionario con los datos de la consulta.
        """
        self._historial_medico.append(consulta)

    def obtener_historial(self) -> list:
        """Obtiene el historial médico completo del paciente.

        Returns:
            list: Lista de todas las consultas médicas del paciente.
        """
        return self._historial_medico

    @property
    def id_paciente(self) -> str:
        return self._id_paciente