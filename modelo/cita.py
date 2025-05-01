from modelo.paciente import Paciente
from modelo.medico import Medico


class Cita:
    """
    Clase que representa una cita médica en el sistema.

    Esta clase encapsula los datos y comportamientos de una cita médica, incluyendo su estado,
    paciente asociado, médico asignado, y operaciones como cancelación, finalización o reagendamiento.

        Attributes:
            id_cita (str): Identificador único de la cita.
            fecha (str): Fecha de la cita en formato DD/MM/AAAA.
            hora (str): Hora de la cita en formato HH:MM.
            estado (str): Estado actual de la cita. Puede ser 'pendiente', 'completada' o 'cancelada'.
            paciente (Paciente): Paciente asociado a la cita.
            medico (Médico): Médico asignado a la cita.
    """

    def __init__(self, id_cita: str, fecha: str, hora: str, paciente: Paciente, medico: Medico):
        """
        Inicializa una nueva instancia de Cita.

            Args:
                id_cita (str): Identificador único de la cita.
                fecha (str): Fecha de la cita en formato DD/MM/AAAA.
                hora (str): Hora de la cita en formato HH:MM.
                paciente (Paciente): Objeto Paciente asociado a la cita.
                médico (Médico): Objeto Médico asignado a la cita.
        """
        self._id_cita = id_cita
        self._fecha = fecha
        self._hora = hora
        self._estado = "pendiente"
        self._paciente = paciente
        self._medico = medico

    def cancelar(self):
        """
        Cancela la cita, estableciendo su estado a 'cancelada'.
        """
        self._estado = "cancelada"

    def completar(self):
        """
        Marca la cita como completada, estableciendo su estado a 'completada'.
        """
        self._estado = "completada"

    def reagendar(self, nueva_fecha: str, nueva_hora: str):
        """
        Reagenda la cita con una nueva fecha y hora.

            Args:
                nueva_fecha (str): Nueva fecha para la cita (formato DD/MM/AAAA).
                nueva_hora (str): Nueva hora para la cita (formato HH:MM).
        """
        self._fecha = nueva_fecha
        self._hora = nueva_hora

    def id_cita(self) -> str:
        """
        str: Devuelve el identificador único de la cita.
        """
        return self._id_cita

    def fecha(self) -> str:
        """
        str: Devuelve la fecha de la cita.
        """
        return self._fecha

    def hora(self) -> str:
        """
        str: Devuelve la hora de la cita.
        """
        return self._hora

    def estado(self) -> str:
        """
        str: Devuelve el estado actual de la cita.
        """
        return self._estado

    def paciente(self) -> Paciente:
        """
        Paciente: Devuelve el objeto Paciente asociado a la cita.
        """
        return self._paciente

    def medico(self) -> Medico:
        """
        Médico: Devuelve el objeto Médico asignado a la cita.
        """
        return self._medico