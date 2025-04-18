from datetime import datetime
from collections import defaultdict


class GestorEstadisticas:
    """Clase que gestiona las operaciones estadísticas del sistema."""

    def calcular_consultas_por_especialidad(self, gestor_medicos, gestor_citas) -> dict:
        """Calcula el número de consultas por especialidad médica.

        Args:
            gestor_medicos: Instancia de GestorMedicos.
            gestor_citas: Instancia de GestorCitas.

        Returns:
            dict: Diccionario con especialidades como keys y número de consultas como values.
        """
        estadisticas = defaultdict(int)

        for cita in gestor_citas.listar_citas():
            especialidad = cita.medico.especialidad.nombre
            estadisticas[especialidad] += 1

        return dict(estadisticas)

    def medico_mas_solicitado(self, gestor_medicos, gestor_citas):
        """Identifica al médico con más citas asignadas.

        Args:
            gestor_medicos: Instancia de GestorMedicos.
            gestor_citas: Instancia de GestorCitas.

        Returns:
            Medico: El médico con más citas.
        """
        conteo_medicos = defaultdict(int)

        for cita in gestor_citas.listar_citas():
            id_medico = cita.medico.id_medico
            conteo_medicos[id_medico] += 1

        if not conteo_medicos:
            return None

        id_mas_solicitado = max(conteo_medicos, key=conteo_medicos.get)
        return gestor_medicos.buscar_medico(id_mas_solicitado)

    def promedio_atencion_mensual(self, gestor_citas) -> float:
        """Calcula el promedio de citas atendidas por mes.

        Args:
            gestor_citas: Instancia de GestorCitas.

        Returns:
            float: Promedio de citas por mes.
        """
        citas_por_mes = defaultdict(int)

        for cita in gestor_citas.listar_citas():
            if cita.estado == "completada":
                fecha = datetime.strptime(cita.fecha, "%d/%m/%Y")
                mes_anio = f"{fecha.month}/{fecha.year}"
                citas_por_mes[mes_anio] += 1

        if not citas_por_mes:
            return 0.0

        total_citas = sum(citas_por_mes.values())
        total_meses = len(citas_por_mes)

        return total_citas / total_meses