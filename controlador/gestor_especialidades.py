import json
from pathlib import Path
from modelo.especialidad import Especialidad


class GestorEspecialidades:
    """
    Gestor para operaciones CRUD de especialidades médicas.

        Attributes:
            file_path (Path): Ruta del archivo JSON que almacena las especialidades.
            _especialidades (list): Lista de objetos Especialidad cargados en memoria.
    """

    def __init__(self):
        """
        Inicializa el gestor de especialidades y carga los datos desde el archivo JSON.
        """
        self.file_path = Path("datos") / "especialidades.json"
        self._especialidades = []
        self.cargar_datos()

    def cargar_datos(self):
        """
        Carga las especialidades desde el archivo JSON, si existe.
        Si el archivo no existe o contiene errores, imprime un mensaje de error.
        """
        try:
            if self.file_path.exists():
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    datos = json.load(f)
                    self._especialidades = [
                        Especialidad(esp['nombre'], esp['descripcion'])
                        for esp in datos
                    ]
        except Exception as e:
            print(f"Error cargando especialidades: {e}")

    def guardar_datos(self):
        """
        Guarda las especialidades en el archivo JSON.
        Si ocurre un error durante el proceso de escritura, imprime un mensaje de error.
        """
        try:
            Path("datos").mkdir(exist_ok=True)
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(
                    [{"nombre": e.nombre, "descripcion": e.descripcion}
                     for e in self._especialidades],
                    f, indent=4, ensure_ascii=False
                )
        except Exception as e:
            print(f"Error guardando especialidades: {e}")

    def agregar_especialidad(self, nombre: str, descripcion: str) -> bool:
        """
        Añade una nueva especialidad al sistema si no existe previamente.

            Args:
                nombre (str): Nombre de la especialidad.
                descripcion (str): Descripción de la especialidad.

            Returns:
                bool: True si se añadió correctamente, False si ya existía.
        """
        if not self.buscar_especialidad(nombre):
            self._especialidades.append(Especialidad(nombre, descripcion))
            self.guardar_datos()
            return True
        return False

    def buscar_especialidad(self, nombre: str) -> Especialidad:
        """
        Busca una especialidad por su nombre.

            Args:
                nombre (str): Nombre de la especialidad a buscar.

            Returns:
                Especialidad: Objeto Especialidad si se encuentra, None si no.
        """
        return next((e for e in self._especialidades if e.nombre == nombre), None)

    def listar_especialidades(self) -> list:
        """
        Devuelve la lista completa de especialidades.

            Returns:
                list: Copia de la lista de objetos Especialidad.
        """
        return self._especialidades.copy()

    def eliminar_especialidad(self, nombre: str) -> bool:
        """
        Elimina una especialidad por su nombre.

            Args:
                nombre (str): Nombre de la especialidad a eliminar.

            Returns:
                bool: True si se eliminó correctamente, False si no se encontró.
        """
        initial_len = len(self._especialidades)
        self._especialidades = [e for e in self._especialidades if e.nombre != nombre]
        if len(self._especialidades) < initial_len:
            self.guardar_datos()
            return True
        return False