import json
from modelo.medico import Medico
from modelo.especialidad import Especialidad
from pathlib import Path
from utils.validaciones import validar_telefono, validar_nombre, validar_fecha_medico, generar_id, validar_persona_duplicado


class GestorMedicos:
    """
    Clase que gestiona las operaciones relacionadas con médicos.

    Esta clase permite agregar, buscar, listar y filtrar médicos, así como cargar y guardar datos desde/hacia archivos JSON.

        Attributes:
            _medicos (list): Lista de objetos Medico registrados.
    """

    def __init__(self):
        """
        Inicializa el gestor de médicos cargando datos desde un archivo JSON.

        Crea una lista vacía de médicos y carga los datos existentes desde el archivo `medicos.json`.
        """
        self._medicos = []
        self.cargar_datos()

    def agregar_medico(self, medico_data: dict) -> bool:
        """
        Agrega un nuevo médico al sistema después de validar sus datos.

            Args:
                medico_data (dict): Diccionario con los datos del médico, incluyendo nombre, apellido,
                                    fecha de nacimiento, teléfono y especialidad.

            Returns:
                bool: True si se agregó correctamente, False si hubo errores de validación.

            Raises:
                ValueError: Si ya existe un médico con los mismos datos (nombre, apellido, fecha y teléfono).
        """
        # Validar formatos correctos
        if not all([
            validar_nombre(medico_data['nombre']),
            validar_nombre(medico_data['apellido']),
            validar_fecha_medico(medico_data['fecha_nacimiento']),
            validar_telefono(medico_data['telefono'])
        ]):
            return False

        # Validar que no haya un paciente con la misma información
        if validar_persona_duplicado('datos/medicos.json', medico_data):
            raise ValueError(
                "Error: Ya existe un médico idéntico (mismo nombre, apellido, fecha nacimiento y teléfono)")

        # Generar ID automático
        ultimo_id = max([m.id_medico for m in self._medicos], default=None)
        medico_data['id_medico'] = generar_id("MED", ultimo_id)

        medico = Medico(**medico_data)
        self._medicos.append(medico)
        self.guardar_datos()
        return True

    def buscar_medico(self, id_medico: str) -> Medico:
        """
        Busca un médico por su ID único.

            Args:
                id_medico (str): ID del médico a buscar.

            Returns:
                Medico: Objeto Medico si se encuentra, o None si no existe.
        """
        for medico in self._medicos:
            if medico.id_medico == id_medico:
                return medico
        return None

    def listar_medicos(self) -> list:
        """
        Retorna la lista completa de médicos registrados.

            Returns:
                list: Lista de objetos Medico.
        """
        return self._medicos

    def medicos_por_especialidad(self, especialidad: str) -> list:
        """
        Filtra los médicos que pertenecen a una especialidad específica.

            Args:
                especialidad (str): Nombre de la especialidad.

            Returns:
                list: Lista de médicos que tienen la especialidad especificada.
        """
        return [medico for medico in self._medicos if medico.especialidad.nombre == especialidad]

    def cargar_datos(self):
        """
        Carga los datos de los médicos desde un archivo JSON.

        Intenta leer el archivo `medicos.json` y construir objetos Medico a partir de los datos almacenados.
        En caso de error, imprime un mensaje de error.
        """
        try:
            ruta = Path("datos") / "medicos.json"
            if ruta.exists():
                with open(ruta, 'r', encoding='utf-8') as archivo:
                    datos = json.load(archivo)
                    for medico_data in datos:
                        especialidad = Especialidad(
                            medico_data['especialidad']['nombre'],
                            medico_data['especialidad']['descripcion']
                        )
                        medico = Medico(
                            medico_data['nombre'],
                            medico_data['apellido'],
                            medico_data['fecha_nacimiento'],
                            medico_data['telefono'],
                            medico_data['id_medico'],
                            especialidad
                        )
                        self._medicos.append(medico)
        except Exception as e:
            print(f"Error al cargar médicos: {e}")

    def guardar_datos(self):
        """
        Guarda los datos actuales de los médicos en un archivo JSON.

        Serializa los objetos Medico en formato JSON y los guarda en `medicos.json`.
        En caso de error, imprime un mensaje de error.
        """
        try:
            ruta = Path("datos") / "medicos.json"
            datos = []
            for medico in self._medicos:
                datos.append({
                    'nombre': medico.nombre,
                    'apellido': medico.apellido,
                    'fecha_nacimiento': medico.fecha_nacimiento,
                    'telefono': medico.telefono,
                    'id_medico': medico.id_medico,
                    'especialidad': {
                        'nombre': medico.especialidad.nombre,
                        'descripcion': medico.especialidad.descripcion
                    }
                })

            with open(ruta, 'w', encoding='utf-8') as archivo:
                json.dump(datos, archivo, indent=4)
        except Exception as e:
            print(f"Error al guardar médicos: {e}")