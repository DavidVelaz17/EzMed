from modelo.paciente import Paciente
from modelo.medico import Medico


class Cita:
    """Clase que representa una cita médica en el sistema.

    Attributes:
        id_cita (str): Identificador único de la cita.
        fecha (str): Fecha de la cita en formato DD/MM/AAAA.
        hora (str): Hora de la cita en formato HH:MM.
        estado (str): Estado actual de la cita (pendiente, completada, cancelada).
        paciente (Paciente): Paciente asociado a la cita.
        medico (Medico): Médico asignado a la cita.
    """

    def __init__(self, id_cita: str, fecha: str, hora: str, paciente: Paciente, medico: Medico):
        """Inicializa una nueva instancia de Cita.

        Args:
            id_cita: Identificador único de la cita.
            fecha: Fecha de la cita en formato DD/MM/AAAA.
            hora: Hora de la cita en formato HH:MM.
            paciente: Paciente asociado a la cita.
            medico: Médico asignado a la cita.
        """
        self._id_cita = id_cita
        self._fecha = fecha
        self._hora = hora
        self._estado = "pendiente"
        self._paciente = paciente
        self._medico = medico

    def cancelar(self):
        """Cancela la cita, cambiando su estado a 'cancelada'."""
        self._estado = "cancelada"

    def completar(self):
        """Marca la cita como completada, cambiando su estado."""
        self._estado = "completada"

    def reagendar(self, nueva_fecha: str, nueva_hora: str):
        """Reagenda la cita con una nueva fecha y hora.

        Args:
            nueva_fecha: Nueva fecha en formato DD/MM/AAAA.
            nueva_hora: Nueva hora en formato HH:MM.
        """
        self._fecha = nueva_fecha
        self._hora = nueva_hora

    @property
    def id_cita(self) -> str:
        return self._id_cita

    @property
    def fecha(self) -> str:
        return self._fecha

    @property
    def hora(self) -> str:
        return self._hora

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def paciente(self) -> Paciente:
        return self._paciente

    @property
    def medico(self) -> Medico:
        return self._medico