import json
from modelo.medico import Medico
from modelo.especialidad import Especialidad
from pathlib import Path
from utils.validaciones import validar_telefono, validar_nombre, validar_fecha, generar_id


class GestorMedicos:
    """Clase que gestiona las operaciones relacionadas con médicos.

    Attributes:
        medicos (list): Lista de médicos registrados en el sistema.
    """

    def __init__(self):
        """Inicializa el gestor de médicos y carga datos desde archivo JSON."""
        self._medicos = []
        self.cargar_datos()

    def agregar_medico(self, medico_data: dict) -> bool:
        """Agrega un nuevo médico al sistema.

        Args:
            medico: Objeto Medico a agregar.
        """
        if not all([
            validar_nombre(medico_data['nombre']),
            validar_nombre(medico_data['apellido']),
            validar_fecha(medico_data['fecha_nacimiento']),
            validar_telefono(medico_data['telefono'])
        ]):
            return False

            # Generar ID automático
        ultimo_id = max([m.id_medico for m in self._medicos], default=None)
        medico_data['id_medico'] = generar_id("MED", ultimo_id)

        medico = Medico(**medico_data)
        self._medicos.append(medico)
        self.guardar_datos()
        return True

    def buscar_medico(self, id_medico: str) -> Medico:
        """Busca un médico por su ID.

        Args:
            id_medico: ID del médico a buscar.

        Returns:
            Medico: Objeto Medico si se encuentra, None en caso contrario.
        """
        for medico in self._medicos:
            if medico.id_medico == id_medico:
                return medico
        return None

    def listar_medicos(self) -> list:
        """Obtiene la lista completa de médicos.

        Returns:
            list: Lista de objetos Medico.
        """
        return self._medicos

    def medicos_por_especialidad(self, especialidad: str) -> list:
        """Filtra médicos por especialidad.

        Args:
            especialidad: Nombre de la especialidad a filtrar.

        Returns:
            list: Lista de médicos que tienen la especialidad especificada.
        """
        return [medico for medico in self._medicos if medico.especialidad.nombre == especialidad]

    def cargar_datos(self):
        """Carga los datos de médicos desde un archivo JSON."""
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
        """Guarda los datos de médicos en un archivo JSON."""
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