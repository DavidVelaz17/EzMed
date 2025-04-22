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
        medicos_citas = {}
        for cita in gestor_citas.listar_citas():
            medico_id = cita.medico.id_medico
            medicos_citas[medico_id] = medicos_citas.get(medico_id, 0) + 1

        if not medicos_citas:
            return None, 0

        medico_mas_solicitado_id = max(medicos_citas, key=medicos_citas.get)
        medico = gestor_medicos.buscar_medico(medico_mas_solicitado_id)
        num_citas = medicos_citas[medico_mas_solicitado_id]
        return medico, num_citas

    def paciente_con_mas_citas(self, gestor_pacientes, gestor_citas):
        """Devuelve el paciente con más citas y el número de citas que tiene."""
        pacientes_citas = {}
        for cita in gestor_citas.listar_citas():
            paciente_id = cita.paciente.id_paciente
            pacientes_citas[paciente_id] = pacientes_citas.get(paciente_id, 0) + 1

        if not pacientes_citas:
            return None, 0

        paciente_mas_citas_id = max(pacientes_citas, key=pacientes_citas.get)
        paciente = gestor_pacientes.buscar_paciente(paciente_mas_citas_id)
        num_citas = pacientes_citas[paciente_mas_citas_id]
        return paciente, num_citas

    def promedio_atencion_mensual(self, gestor_citas) -> float:
        """Calcula el promedio de citas atendidas por mes.

        Args:
            gestor_citas: Instancia de GestorCitas.

        Returns:
            float: Promedio de citas por mes.
        """
        citas_por_mes = defaultdict(int)

        for cita in gestor_citas.listar_citas():
            if cita.estado == "completada" or "pendiente":
                fecha = datetime.strptime(cita.fecha, "%d/%m/%Y")
                mes_anio = f"{fecha.month}/{fecha.year}"
                citas_por_mes[mes_anio] += 1

        if not citas_por_mes:
            return 0.0

        total_citas = sum(citas_por_mes.values())
        total_meses = len(citas_por_mes)

        return total_citas / total_meses