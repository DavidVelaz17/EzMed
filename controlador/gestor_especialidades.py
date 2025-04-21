import json
from pathlib import Path
from modelo.especialidad import Especialidad


class GestorEspecialidades:
    """Gestor para operaciones CRUD de especialidades médicas."""

    def __init__(self):
        self.file_path = Path("datos") / "especialidades.json"
        self._especialidades = []
        self.cargar_datos()

    def cargar_datos(self):
        """Carga las especialidades desde el archivo JSON."""
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
        """Guarda las especialidades en el archivo JSON."""
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
        """Añade una nueva especialidad."""
        if not self.buscar_especialidad(nombre):
            self._especialidades.append(Especialidad(nombre, descripcion))
            self.guardar_datos()
            return True
        return False

    def buscar_especialidad(self, nombre: str) -> Especialidad:
        """Busca una especialidad por nombre."""
        return next((e for e in self._especialidades if e.nombre == nombre), None)

    def listar_especialidades(self) -> list:
        """Devuelve todas las especialidades."""
        return self._especialidades.copy()

    def eliminar_especialidad(self, nombre: str) -> bool:
        """Elimina una especialidad."""
        initial_len = len(self._especialidades)
        self._especialidades = [e for e in self._especialidades if e.nombre != nombre]
        if len(self._especialidades) < initial_len:
            self.guardar_datos()
            return True
        return False