import json
from modelo.cita import Cita
from pathlib import Path
from utils.validaciones import validar_fecha_citas, generar_id, validar_hora
from shutil import copyfile

class GestorCitas:
    """
    Clase que gestiona las operaciones relacionadas con citas médicas.

        Attributes:
            _citas (list): Lista de objetos Cita registrados.
            file_path (Path): Ruta del archivo JSON donde se almacenan las citas.
    """

    def __init__(self):
        """
        Inicializa una instancia de GestorCitas, cargando los datos desde el archivo JSON.
        """
        self.file_path = Path("datos") / 'citas.json'
        self._citas = []
        self.cargar_datos()

    def agendar_cita(self, fecha: str, hora: str, paciente, medico) -> bool:
        """
        Agrega una nueva cita al sistema si la fecha y hora son válidas.

            Args:
                fecha (str): Fecha de la cita en formato DD/MM/AAAA.
                hora (str): Hora de la cita en formato HH:MM.
                paciente (Paciente): Objeto Paciente.
                medico (Medico): Objeto Medico.

            Returns:
                bool: True si la cita se agenda exitosamente, False si hay errores de validación.
        """
        # Validar formato y rango de la nueva fecha
        if not validar_fecha_citas(fecha):
            return False

        # Validar formato de la nueva hora
        if not validar_hora(hora):
            return False

        # Generar ID automático
        ultimo_id = max([c.id_cita for c in self._citas], default=None)
        id_cita = generar_id("CIT", ultimo_id)

        cita = Cita(fecha=fecha, hora=hora, paciente=paciente, medico=medico, id_cita=id_cita)
        self._citas.append(cita)
        self.guardar_datos()
        return True

    def cancelar_cita(self, id_cita: str) -> bool:
        """Marca una cita como cancelada tanto en memoria como en el archivo JSON

               Args:
                   id_cita: ID de la cita a cancelar.

               Returns:
                   bool: True si la cita fue encontrada y cancelada, False en caso contrario
           """
        cita_encontrada = False

        # Actualizar en memoria
        for cita in self._citas:
            if cita.id_cita == id_cita and cita.estado == "pendiente":
                cita.cancelar()
                cita_encontrada = True
                break

        if cita_encontrada:
            try:
                self.guardar_datos()
            except Exception as e:
                print(f"Error al guardar los cambios: {e}")
                # Revertir el cambio en memoria si falla el guardado
                for cita in self._citas:
                    if cita.id_cita == id_cita:
                        cita._estado = "pendiente"  # Accedemos al atributo protegido directamente para revertir
                        break
                return False

        return cita_encontrada

    def reagendar_cita(self, id_cita: str, nueva_fecha: str, nueva_hora: str):
        """
        Modifica la fecha y hora de una cita existente si es válida y pendiente.

            Args:
                id_cita (str): ID de la cita a reagendar.
                nueva_fecha (str): Nueva fecha en formato DD/MM/AAAA.
                nueva_hora (str): Nueva hora en formato HH:MM.

            Returns:
                bool: True si la cita fue reagendada exitosamente, False si falla la validación.
        """
        cita = self.buscar_cita(id_cita)

        # Verificar que la nueva fecha/hora sean diferentes a las actuales
        if cita.fecha == nueva_fecha and cita.hora == nueva_hora:
            return False

        # Validar formato y rango de la nueva fecha
        if not validar_fecha_citas(nueva_fecha):
            return False

        # Validar formato de la nueva hora
        if not validar_hora(nueva_hora):
            return False

        if cita and cita.estado == "pendiente":
            cita.reagendar(nueva_fecha, nueva_hora)
            self.guardar_datos()
            return True
        return  False

    def citas_por_paciente(self, id_paciente: str) -> list:
        """
        Obtiene todas las citas asociadas a un paciente específico.

            Args:
                id_paciente (str): ID del paciente.

            Returns:
                list: Lista de objetos Cita correspondientes al paciente.
        """
        return [cita for cita in self._citas if cita.paciente.id_paciente == id_paciente]

    def citas_por_medico(self, id_medico: str) -> list:
        """Obtiene las citas de un médico específico.

            Args:
                id_medico: ID del médico.

            Returns:
                list: Lista de citas del médico.
        """
        return [cita for cita in self._citas if cita.medico.id_medico == id_medico]

    def buscar_cita(self, id_cita: str):
        """Busca una cita por su ID.

            Args:
                id_cita (str): ID de la cita a buscar.

            Returns:
                Cita | None: Objeto Cita si se encuentra, None en caso contrario.
        """
        for cita in self._citas:
            if cita.id_cita == id_cita:
                return cita
        return None

    def cargar_datos(self):
        """
        Carga las citas desde el archivo JSON, reconstruyendo los objetos Cita con sus respectivos pacientes y médicos.
        """
        try:
            if self.file_path.exists():
                with open(self.file_path, 'r', encoding='utf-8') as archivo:
                    datos = json.load(archivo)
                    # Necesitamos los gestores de pacientes y médicos para reconstruir las citas
                    from controlador.gestor_pacientes import GestorPacientes
                    from controlador.gestor_medicos import GestorMedicos

                    gestor_pacientes = GestorPacientes()
                    gestor_medicos = GestorMedicos()

                    for cita_data in datos:
                        paciente = gestor_pacientes.buscar_paciente(cita_data['id_paciente'])
                        medico = gestor_medicos.buscar_medico(cita_data['id_medico'])

                        if paciente and medico:
                            cita = Cita(
                                cita_data['id_cita'],
                                cita_data['fecha'],
                                cita_data['hora'],
                                paciente,
                                medico
                            )
                            cita._estado = cita_data['estado']
                            self._citas.append(cita)
        except json.JSONDecodeError as e:
            print(f"Error al cargar citas: {e}")

    def guardar_datos(self):
        """
        Guarda la lista de citas en el archivo JSON de manera persistente.
        """
        try:
            datos = []
            for cita in self._citas:
                datos.append({
                    'id_cita': cita.id_cita,
                    'fecha': cita.fecha,
                    'hora': cita.hora,
                    'estado': cita.estado,
                    'id_paciente': cita.paciente.id_paciente,
                    'id_medico': cita.medico.id_medico
                })
            # Crear respaldo antes de sobrescribir el archivo
            if self.file_path.exists():
                copia = self.file_path.with_suffix('.json.bak')
                copyfile(self.file_path, copia)

            # Guardar en el archivo original
            with open(self.file_path, 'w', encoding='utf-8') as archivo:
                json.dump(datos, archivo, indent=4)
        except Exception as e:
            print(f"Error al guardar citas: {e}")

    def listar_citas(self) -> list:
        """
        Devuelve la lista completa de citas registradas.

            Returns:
                list: Lista de objetos Cita registrados en el sistema.
        """
        return self._citas