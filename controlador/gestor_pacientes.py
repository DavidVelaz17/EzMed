import json
from modelo.paciente import Paciente
from pathlib import Path
from utils.validaciones import validar_nombre,validar_telefono,validar_fecha_paciente, generar_id, validar_persona_duplicado
from shutil import copyfile

class GestorPacientes:
    """
    Clase que gestiona las operaciones relacionadas con pacientes.

    Esta clase permite agregar, buscar, listar pacientes, así como cargar y guardar datos desde/hacia archivos JSON.

        Attributes:
            _pacientes (list): Lista de objetos Paciente registrados.
    """

    def __init__(self):
        """
        Inicializa el gestor de pacientes y carga los datos desde el archivo JSON.

        Crea una lista vacía y la rellena con pacientes cargados desde el archivo `pacientes.json` si existe.
        """
        self.file_path = Path('datos') / 'pacientes.json'
        self._pacientes = []
        self.cargar_datos()

    def agregar_paciente(self, paciente_data: dict)  -> bool:
        """
        Agrega un nuevo paciente al sistema luego de validar sus datos.

            Args:
                paciente_data (dict): Diccionario con los datos del paciente, incluyendo nombre, apellido,
                                      fecha de nacimiento y teléfono.

            Returns:
                bool: True si el paciente fue agregado correctamente, False si falló la validación.

            Raises:
                ValueError: Si ya existe un paciente con los mismos datos (nombre, apellido, fecha y teléfono).
        """
        # Validar formatos correctos
        if not all([
            validar_nombre(paciente_data['nombre']),
            validar_nombre(paciente_data['apellido']),
            validar_fecha_paciente(paciente_data['fecha_nacimiento']),
            validar_telefono(paciente_data['telefono'])
        ]):
            return False

        # Validar que no haya un paciente con la misma información
        if validar_persona_duplicado('datos/pacientes.json', paciente_data):
            raise ValueError(
                "Error: Ya existe un paciente idéntico (mismo nombre, apellido, fecha nacimiento y teléfono)")

        # Generar ID automático
        ultimo_id = max([p.id_paciente for p in self._pacientes], default=None)
        paciente_data['id_paciente'] = generar_id("PAC", ultimo_id)

        paciente = Paciente.desde_json(paciente_data)
        self._pacientes.append(paciente)
        self.guardar_datos()
        return True

    def buscar_paciente(self, id_paciente: str) -> Paciente:
        """
        Busca un paciente por su ID único.

            Args:
                id_paciente (str): ID del paciente a buscar.

            Returns:
                Paciente: Objeto Paciente si se encuentra, o None si no existe.
        """
        for paciente in self._pacientes:
            if paciente.id_paciente == id_paciente:
                return paciente
        return None

    def listar_pacientes(self) -> list:
        """
        Retorna la lista completa de pacientes registrados.

            Returns:
                list: Lista de objetos Paciente.
        """
        return self._pacientes

    def cargar_datos(self):
        """
        Carga los datos de los pacientes desde un archivo JSON.

        Intenta leer el archivo `pacientes.json` y construir objetos Paciente a partir de los datos almacenados.
        En caso de error, imprime un mensaje.
        """
        self._pacientes.clear()
        try:
            if self.file_path.exists():
                with open(self.file_path, 'r', encoding='utf-8') as archivo:
                    datos = json.load(archivo)
                    self._pacientes = [Paciente.desde_json(p) for p in datos]
        except Exception as e:
            print(f"Error al cargar pacientes: {e}")

    def guardar_datos(self):
        """
        Guarda los datos actuales de los pacientes en un archivo JSON.

        Serializa los objetos Paciente en formato JSON y los guarda en `pacientes.json`.
        En caso de error, imprime un mensaje.
        """
        try:
            if self.file_path.exists():
                copia = self.file_path.with_suffix('.json.bak')
                copyfile(self.file_path, copia)

            with open(self.file_path, 'w', encoding='utf-8') as archivo:
                json.dump([p.a_json() for p in self._pacientes], archivo, indent=4)
        except Exception as e:
            print(f"Error al guardar pacientes: {e}")