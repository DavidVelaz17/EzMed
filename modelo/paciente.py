from modelo.persona import Persona


class Paciente(Persona):
    """
    Clase que representa a un paciente en el sistema de gestión clínica.

    Hereda de Persona y añade atributos específicos de pacientes.

        Attributes:
            id_paciente (str): Identificador único del paciente.
            historial_medico (list): Lista de consultas médicas del paciente.
    """

    def __init__(self, nombre: str, apellido: str, fecha_nacimiento: str,
                 telefono: str, id_paciente: str):
        """
        Inicializa una nueva instancia de Paciente.

            Args:
                nombre (str): Nombre del paciente.
                apellido (str): Apellido del paciente.
                fecha_nacimiento (str): Fecha de nacimiento en formato DD/MM/AAAA.
                telefono (str): Número de teléfono del paciente.
                id_paciente (str): Identificador único del paciente.
        """
        super().__init__(nombre, apellido, fecha_nacimiento, telefono)
        self._id_paciente = id_paciente
        self._historial_medico = []

    def agregar_consulta(self, consulta: dict):
        """
        Agrega una consulta médica al historial del paciente.

            Args:
                consulta (dict): Diccionario con los datos de la consulta.
        """
        self._historial_medico.append(consulta)

    def obtener_historial(self) -> list:
        """
        Obtiene el historial médico completo del paciente.

            Returns:
                list: Lista de todas las consultas médicas del paciente.
        """
        return self._historial_medico

    @property
    def id_paciente(self) -> str:
        """
        str: Devuelve el identificador único del paciente.
        """
        return self._id_paciente

    def a_json(self) -> dict:
        """
        Serializa el paciente a un diccionario JSON.
        """
        return {
            'nombre': self.nombre,
            'apellido': self.apellido,
            'fecha_nacimiento': self.fecha_nacimiento,
            'telefono': self.telefono,
            'id_paciente': self.id_paciente
        }

    @classmethod
    def desde_json(cls, data: dict):
        """
        Crea una instancia de Paciente a partir de un diccionario.

        Args:
            data (dict): Diccionario con los datos del paciente.

        Returns:
            Paciente: Instancia del paciente reconstruida.
        """
        return cls(
            data['nombre'],
            data['apellido'],
            data['fecha_nacimiento'],
            data['telefono'],
            data['id_paciente']
        )