import json
from pathlib import Path
from modelo.diagnostico import Diagnostico
from modelo.cita import Cita
from utils.validaciones import generar_id


class GestorDiagnosticos:
    """Clase que gestiona las operaciones relacionadas con diagnósticos médicos."""

    def __init__(self, gestor_citas):
        """Inicializa el gestor de diagnósticos y carga datos desde archivo JSON."""
        self.file_path = Path("datos") / 'diagnosticos.json'
        self._diagnosticos = []
        self.gestor_citas = gestor_citas
        self.cargar_datos()

    def registrar_diagnostico(self, descripcion: str, tratamiento: str, observaciones: str, cita: Cita) -> bool:
        """Registra un nuevo diagnóstico en el sistema.

        Args:
            descripcion: Descripción del diagnóstico
            tratamiento: Tratamiento recomendado
            observaciones: Observaciones adicionales
            cita: Cita asociada al diagnóstico

        Returns:
            bool: True si se registró correctamente, False si hubo error
        """
        try:
            # Generar ID automático
            ultimo_id = max([d.id_diagnostico for d in self._diagnosticos], default=None)
            id_diagnostico = generar_id("DIA", ultimo_id)

            # Crear el diagnóstico
            diagnostico = Diagnostico(
                id_diagnostico=id_diagnostico,
                descripcion=descripcion,
                tratamiento=tratamiento,
                observaciones=observaciones,
                cita=cita
            )

            # Marcar la cita como completada
            cita.completar()
            self.gestor_citas.guardar_datos()

            # Guardar el diagnóstico
            self._diagnosticos.append(diagnostico)
            self.guardar_datos()
            return True

        except Exception as e:
            print(f"Error al registrar diagnóstico: {e}")
            return False

    def obtener_diagnosticos_completos(self) -> list:
        """Obtiene todos los diagnósticos con información completa.

        Returns:
            list: Lista de diccionarios con toda la información de cada diagnóstico
        """
        diagnosticos_completos = []
        for diagnostico in self._diagnosticos:
            cita = diagnostico.cita
            diagnosticos_completos.append({
                'id_diagnostico': diagnostico.id_diagnostico,
                'id_cita': cita.id_cita,
                'paciente': cita.paciente.get_nombre_completo(),
                'medico': cita.medico.get_nombre_completo(),
                'descripcion': diagnostico.descripcion,
                'tratamiento': diagnostico.tratamiento,
                'observaciones': diagnostico.observaciones
            })
        return diagnosticos_completos

    def obtener_diagnosticos_por_medico(self, id_medico: str) -> list:
        """Obtiene los diagnósticos realizados por un médico específico.

        Args:
            id_medico: ID del médico

        Returns:
            list: Lista de diagnósticos realizados por el médico
        """
        return [d for d in self._diagnosticos if d.cita.medico.id_medico == id_medico]

    def obtener_diagnosticos_por_paciente(self, id_paciente: str) -> list:
        """Obtiene los diagnósticos de un paciente específico.

        Args:
            id_paciente: ID del paciente

        Returns:
            list: Lista de diagnósticos del paciente
        """
        return [d for d in self._diagnosticos if d.cita.paciente.id_paciente == id_paciente]

    def cargar_datos(self):
        """Carga los datos de diagnósticos desde un archivo JSON."""
        try:
            if self.file_path.exists():
                with open(self.file_path, 'r', encoding='utf-8') as archivo:
                    datos = json.load(archivo)

                    for diag_data in datos:
                        # Buscar la cita asociada
                        cita = self.gestor_citas.buscar_cita(diag_data['id_cita'])

                        if cita:
                            diagnostico = Diagnostico(
                                id_diagnostico=diag_data['id_diagnostico'],
                                descripcion=diag_data['descripcion'],
                                tratamiento=diag_data['tratamiento'],
                                observaciones=diag_data['observaciones'],
                                cita=cita
                            )
                            self._diagnosticos.append(diagnostico)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error al cargar diagnósticos: {e}")

    def guardar_datos(self):
        """Guarda los datos de diagnósticos en un archivo JSON."""
        try:
            datos = []
            for diagnostico in self._diagnosticos:
                datos.append({
                    'id_diagnostico': diagnostico.id_diagnostico,
                    'descripcion': diagnostico.descripcion,
                    'tratamiento': diagnostico.tratamiento,
                    'observaciones': diagnostico.observaciones,
                    'id_cita': diagnostico.cita.id_cita
                })

            with open(self.file_path, 'w', encoding='utf-8') as archivo:
                json.dump(datos, archivo, indent=4)
        except Exception as e:
            print(f"Error al guardar diagnósticos: {e}")

    def listar_diagnosticos(self) -> list:
        """Devuelve la lista completa de diagnósticos.

        Returns:
            list: Lista de objetos Diagnostico registrados en el sistema
        """
        return self._diagnosticos