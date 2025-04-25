from datetime import datetime
from collections import defaultdict


class GestorEstadisticas:
    """
    Clase que gestiona las operaciones estadísticas del sistema.

    Esta clase provee métodos para obtener estadísticas como:
    - Consultas por especialidad
    - Médico más solicitado
    - Paciente con más citas
    - Promedio de atención mensual
    """

    def calcular_consultas_por_especialidad(self, gestor_medicos, gestor_citas) -> dict:
        """
        Calcula el número de consultas realizadas por cada especialidad médica.

            Args:
                gestor_medicos: Instancia del gestor de médicos.
                gestor_citas: Instancia del gestor de citas.

            Returns:
                dict: Diccionario donde las claves son nombres de especialidades y los valores son el número de consultas.
        """
        estadisticas = defaultdict(int)

        for cita in gestor_citas.listar_citas():
            especialidad = cita.medico.especialidad.nombre
            estadisticas[especialidad] += 1

        return dict(estadisticas)

    def medico_mas_solicitado(self, gestor_medicos, gestor_citas):
        """
        Identifica al médico con mayor cantidad de citas asignadas.

            Args:
                gestor_medicos: Instancia del gestor de médicos.
                gestor_citas: Instancia del gestor de citas.

            Returns:
                tuple: Una tupla con el objeto Medico más solicitado y el número de citas asignadas.
                       Si no hay datos, devuelve (None, 0).
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
        """
        Devuelve el paciente con más citas registradas.

            Args:
                gestor_pacientes: Instancia del gestor de pacientes.
                gestor_citas: Instancia del gestor de citas.

            Returns:
                tuple: Una tupla con el objeto Paciente que tiene más citas y el número de citas.
                       Si no hay datos, devuelve (None, 0).
        """
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
        """
        Calcula el promedio de citas completadas o pendientes por mes.

            Args:
                gestor_citas: Instancia del gestor de citas.

            Returns:
                float: Promedio de citas por mes. Devuelve 0.0 si no hay datos.
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