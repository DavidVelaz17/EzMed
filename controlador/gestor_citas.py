import json
from modelo.cita import Cita
from pathlib import Path


class GestorCitas:
    """Clase que gestiona las operaciones relacionadas con citas médicas.

    Attributes:
        citas (list): Lista de citas registradas en el sistema.
    """

    def __init__(self):
        """Inicializa el gestor de citas y carga datos desde archivo JSON."""
        self.file_path = Path("datos") / 'citas.json'
        self._citas = []
        self.cargar_datos()

    def agendar_cita(self, cita: Cita):
        """Agrega una nueva cita al sistema.

        Args:
            cita: Objeto Cita a agregar.
        """
        self._citas.append(cita)
        self.guardar_datos()

    def cancelar_cita(self, id_cita: str) -> bool:
        """Elimina una cita tanto del archivo como de la lista en memoria

        Args:
            id_cita: ID de la cita a cancelar.
        """
        # Eliminar de memoria
        initial_count = len(self._citas)
        self._citas = [c for c in self._citas if c.id_cita != id_cita]

        if len(self._citas) < initial_count:
            # Leer archivo actual
            with open(self.file_path, 'r', encoding='utf-8') as file:
                citas_json = json.load(file)

            # Filtrar la cita
            citas_actualizadas = [c for c in citas_json if c['id_cita'] != id_cita]

            # Escribir cambios
            with open(self.file_path, 'w', encoding='utf-8') as file:
                json.dump(citas_actualizadas, file, indent=4, ensure_ascii=False)

            return True
        return False

    def reagendar_cita(self, id_cita: str, nueva_fecha: str, nueva_hora: str):
        """Reagenda una cita existente.

        Args:
            id_cita: ID de la cita a reagendar.
            nueva_fecha: Nueva fecha para la cita.
            nueva_hora: Nueva hora para la cita.
        """
        cita = self.buscar_cita(id_cita)
        if cita:
            cita.reagendar(nueva_fecha, nueva_hora)
            self.guardar_datos()
            return True
        return  False

    def citas_por_paciente(self, id_paciente: str) -> list:
        """Obtiene las citas de un paciente específico.

        Args:
            id_paciente: ID del paciente.

        Returns:
            list: Lista de citas del paciente.
        """
        return [cita for cita in self._citas if cita.paciente.id_paciente == id_paciente]

    def citas_por_medico(self, id_medico: str) -> list:
        """Obtiene las citas de un médico específico.

        Args:
            id_medico: ID del médico.

        Returns:
            list: Lista de citas del médico.
        """
        return [cita for cita in self._citas if cita.medico.id_medico == id_medico]

    def buscar_cita(self, id_cita: str):
        """Busca una cita por su ID.

        Args:
            id_cita: ID de la cita a buscar.

        Returns:
            Cita: Objeto Cita si se encuentra, None en caso contrario.
        """
        for cita in self._citas:
            if cita.id_cita == id_cita:
                return cita
        return None

    def cargar_datos(self):
        """Carga los datos de citas desde un archivo JSON."""
        try:
            if self.file_path.exists():
                with open(self.file_path, 'r', encoding='utf-8') as archivo:
                    datos = json.load(archivo)
                    # Necesitamos los gestores de pacientes y médicos para reconstruir las citas
                    from controlador.gestor_pacientes import GestorPacientes
                    from controlador.gestor_medicos import GestorMedicos

                    gestor_pacientes = GestorPacientes()
                    gestor_medicos = GestorMedicos()

                    for cita_data in datos:
                        paciente = gestor_pacientes.buscar_paciente(cita_data['id_paciente'])
                        medico = gestor_medicos.buscar_medico(cita_data['id_medico'])

                        if paciente and medico:
                            cita = Cita(
                                cita_data['id_cita'],
                                cita_data['fecha'],
                                cita_data['hora'],
                                paciente,
                                medico
                            )
                            cita._estado = cita_data['estado']
                            self._citas.append(cita)
        except json.JSONDecodeError as e:
            print(f"Error al cargar citas: {e}")

    def guardar_datos(self):
        """Guarda los datos de citas en un archivo JSON."""
        try:
            datos = []
            for cita in self._citas:
                datos.append({
                    'id_cita': cita.id_cita,
                    'fecha': cita.fecha,
                    'hora': cita.hora,
                    'estado': cita.estado,
                    'id_paciente': cita.paciente.id_paciente,
                    'id_medico': cita.medico.id_medico
                })

            with open(self.file_path, 'w', encoding='utf-8') as archivo:
                json.dump(datos, archivo, indent=4)
        except Exception as e:
            print(f"Error al guardar citas: {e}")

    def listar_citas(self) -> list:
        """Devuelve la lista completa de citas.

        Returns:
            list: Lista de objetos Cita registrados en el sistema.
        """
        return self._citas