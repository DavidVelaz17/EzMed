import json
from modelo.paciente import Paciente
from pathlib import Path


class GestorPacientes:
    """Clase que gestiona las operaciones relacionadas con pacientes.

    Attributes:
        pacientes (list): Lista de pacientes registrados en el sistema.
    """

    def __init__(self):
        """Inicializa el gestor de pacientes y carga datos desde archivo JSON."""
        self._pacientes = []
        self.cargar_datos()

    def agregar_paciente(self, paciente: Paciente):
        """Agrega un nuevo paciente al sistema.

        Args:
            paciente: Objeto Paciente a agregar.
        """
        self._pacientes.append(paciente)
        self.guardar_datos()

    def buscar_paciente(self, id_paciente: str) -> Paciente:
        """Busca un paciente por su ID.

        Args:
            id_paciente: ID del paciente a buscar.

        Returns:
            Paciente: Objeto Paciente si se encuentra, None en caso contrario.
        """
        for paciente in self._pacientes:
            if paciente.id_paciente == id_paciente:
                return paciente
        return None

    def listar_pacientes(self) -> list:
        """Obtiene la lista completa de pacientes.

        Returns:
            list: Lista de objetos Paciente.
        """
        return self._pacientes

    def cargar_datos(self):
        """Carga los datos de pacientes desde un archivo JSON."""
        try:
            ruta = Path("datos") / "pacientes.json"
            if ruta.exists():
                with open(ruta, 'r', encoding='utf-8') as archivo:
                    datos = json.load(archivo)
                    for paciente_data in datos:
                        paciente = Paciente(
                            paciente_data['nombre'],
                            paciente_data['apellido'],
                            paciente_data['fecha_nacimiento'],
                            paciente_data['telefono'],
                            paciente_data['id_paciente']
                        )
                        self._pacientes.append(paciente)
        except Exception as e:
            print(f"Error al cargar pacientes: {e}")

    def guardar_datos(self):
        """Guarda los datos de pacientes en un archivo JSON."""
        try:
            ruta = Path("datos") / "pacientes.json"
            datos = []
            for paciente in self._pacientes:
                datos.append({
                    'nombre': paciente.nombre,
                    'apellido': paciente.apellido,
                    'fecha_nacimiento': paciente.fecha_nacimiento,
                    'telefono': paciente.telefono,
                    'id_paciente': paciente.id_paciente
                })

            with open(ruta, 'w', encoding='utf-8') as archivo:
                json.dump(datos, archivo, indent=4)
        except Exception as e:
            print(f"Error al guardar pacientes: {e}")