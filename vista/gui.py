import tkinter as tk
from tkinter import ttk, messagebox
from controlador.gestor_pacientes import GestorPacientes
from controlador.gestor_medicos import GestorMedicos
from controlador.gestor_citas import GestorCitas
from controlador.gestor_estadisticas import GestorEstadisticas
from modelo.paciente import Paciente
from modelo.medico import Medico
from modelo.especialidad import Especialidad
from modelo.cita import Cita


class GUI:
    """Clase que representa la interfaz gráfica del sistema de gestión clínica."""

    def __init__(self):
        """Inicializa la interfaz gráfica y sus componentes."""
        self.gestor_pacientes = GestorPacientes()
        self.gestor_medicos = GestorMedicos()
        self.gestor_citas = GestorCitas()
        self.gestor_estadisticas = GestorEstadisticas()

        self.root = tk.Tk()
        self.root.title("Sistema de Gestión Clínica")
        self.root.geometry("800x600")

        self.crear_menu_principal()

    def crear_menu_principal(self):
        """Crea el menú principal de la aplicación."""
        self.limpiar_pantalla()

        lbl_titulo = tk.Label(self.root, text="Sistema de Gestión Clínica", font=("Arial", 16))
        lbl_titulo.pack(pady=20)

        frame_botones = tk.Frame(self.root)
        frame_botones.pack(pady=20)

        btn_pacientes = tk.Button(frame_botones, text="Gestión de Pacientes",
                                  command=self.mostrar_formulario_paciente)
        btn_pacientes.grid(row=0, column=0, padx=10, pady=10)

        btn_medicos = tk.Button(frame_botones, text="Gestión de Médicos",
                                command=self.mostrar_formulario_medico)
        btn_medicos.grid(row=0, column=1, padx=10, pady=10)

        btn_citas = tk.Button(frame_botones, text="Gestión de Citas",
                              command=self.mostrar_formulario_cita)
        btn_citas.grid(row=1, column=0, padx=10, pady=10)

        btn_reportes = tk.Button(frame_botones, text="Reportes y Estadísticas",
                                 command=self.mostrar_reportes)
        btn_reportes.grid(row=1, column=1, padx=10, pady=10)

    def limpiar_pantalla(self):
        """Limpia todos los widgets de la pantalla."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def mostrar_formulario_paciente(self):
        """Muestra el formulario para gestión de pacientes."""
        self.limpiar_pantalla()

        lbl_titulo = tk.Label(self.root, text="Registro de Pacientes", font=("Arial", 14))
        lbl_titulo.pack(pady=10)

        frame_formulario = tk.Frame(self.root)
        frame_formulario.pack(pady=10)

        # Campos del formulario
        tk.Label(frame_formulario, text="Nombre:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        entry_nombre = tk.Entry(frame_formulario)
        entry_nombre.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_formulario, text="Apellido:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        entry_apellido = tk.Entry(frame_formulario)
        entry_apellido.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_formulario, text="Fecha Nacimiento (DD/MM/AAAA):").grid(row=2, column=0, sticky="e", padx=5,
                                                                               pady=5)
        entry_fecha_nac = tk.Entry(frame_formulario)
        entry_fecha_nac.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(frame_formulario, text="Teléfono:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        entry_telefono = tk.Entry(frame_formulario)
        entry_telefono.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(frame_formulario, text="ID Paciente:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        entry_id = tk.Entry(frame_formulario)
        entry_id.grid(row=4, column=1, padx=5, pady=5)

        frame_botones = tk.Frame(self.root)
        frame_botones.pack(pady=10)

        def guardar_paciente():
            """Recolecta los datos del formulario y crea un nuevo paciente."""
            try:
                paciente = Paciente(
                    entry_nombre.get(),
                    entry_apellido.get(),
                    entry_fecha_nac.get(),
                    entry_telefono.get(),
                    entry_id.get()
                )
                self.gestor_pacientes.agregar_paciente(paciente)
                messagebox.showinfo("Éxito", "Paciente registrado correctamente")
                self.crear_menu_principal()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo registrar el paciente: {e}")

        btn_guardar = tk.Button(frame_botones, text="Guardar", command=guardar_paciente)
        btn_guardar.grid(row=0, column=0, padx=5)

        btn_cancelar = tk.Button(frame_botones, text="Cancelar", command=self.crear_menu_principal)
        btn_cancelar.grid(row=0, column=1, padx=5)

        # Lista de pacientes
        frame_lista = tk.Frame(self.root)
        frame_lista.pack(pady=10, fill="both", expand=True)

        lbl_lista = tk.Label(frame_lista, text="Pacientes Registrados")
        lbl_lista.pack()

        tree = ttk.Treeview(frame_lista, columns=("ID", "Nombre", "Apellido", "Teléfono"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Nombre", text="Nombre")
        tree.heading("Apellido", text="Apellido")
        tree.heading("Teléfono", text="Teléfono")
        tree.pack(fill="both", expand=True)

        for paciente in self.gestor_pacientes.listar_pacientes():
            tree.insert("", "end", values=(
                paciente.id_paciente,
                paciente.nombre,
                paciente.apellido,
                paciente.telefono
            ))

    def mostrar_formulario_medico(self):
        """Muestra el formulario para gestión de médicos."""
        self.limpiar_pantalla()

        lbl_titulo = tk.Label(self.root, text="Registro de Médicos", font=("Arial", 14))
        lbl_titulo.pack(pady=10)

        frame_formulario = tk.Frame(self.root)
        frame_formulario.pack(pady=10)

        # Campos del formulario
        tk.Label(frame_formulario, text="Nombre:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        entry_nombre = tk.Entry(frame_formulario)
        entry_nombre.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_formulario, text="Apellido:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        entry_apellido = tk.Entry(frame_formulario)
        entry_apellido.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_formulario, text="Fecha Nacimiento (DD/MM/AAAA):").grid(row=2, column=0, sticky="e", padx=5,
                                                                               pady=5)
        entry_fecha_nac = tk.Entry(frame_formulario)
        entry_fecha_nac.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(frame_formulario, text="Teléfono:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        entry_telefono = tk.Entry(frame_formulario)
        entry_telefono.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(frame_formulario, text="ID Médico:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        entry_id = tk.Entry(frame_formulario)
        entry_id.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(frame_formulario, text="Especialidad:").grid(row=5, column=0, sticky="e", padx=5, pady=5)
        entry_especialidad = tk.Entry(frame_formulario)
        entry_especialidad.grid(row=5, column=1, padx=5, pady=5)

        tk.Label(frame_formulario, text="Descripción Especialidad:").grid(row=6, column=0, sticky="e", padx=5, pady=5)
        entry_desc_especialidad = tk.Entry(frame_formulario)
        entry_desc_especialidad.grid(row=6, column=1, padx=5, pady=5)

        frame_botones = tk.Frame(self.root)
        frame_botones.pack(pady=10)

        def guardar_medico():
            """Recolecta los datos del formulario y crea un nuevo médico."""
            try:
                especialidad = Especialidad(
                    entry_especialidad.get(),
                    entry_desc_especialidad.get()
                )
                medico = Medico(
                    entry_nombre.get(),
                    entry_apellido.get(),
                    entry_fecha_nac.get(),
                    entry_telefono.get(),
                    entry_id.get(),
                    especialidad
                )
                self.gestor_medicos.agregar_medico(medico)
                messagebox.showinfo("Éxito", "Médico registrado correctamente")
                self.crear_menu_principal()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo registrar el médico: {e}")

        btn_guardar = tk.Button(frame_botones, text="Guardar", command=guardar_medico)
        btn_guardar.grid(row=0, column=0, padx=5)

        btn_cancelar = tk.Button(frame_botones, text="Cancelar", command=self.crear_menu_principal)
        btn_cancelar.grid(row=0, column=1, padx=5)

        # Lista de médicos
        frame_lista = tk.Frame(self.root)
        frame_lista.pack(pady=10, fill="both", expand=True)

        lbl_lista = tk.Label(frame_lista, text="Médicos Registrados")
        lbl_lista.pack()

        tree = ttk.Treeview(frame_lista, columns=("ID", "Nombre", "Apellido", "Especialidad"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Nombre", text="Nombre")
        tree.heading("Apellido", text="Apellido")
        tree.heading("Especialidad", text="Especialidad")
        tree.pack(fill="both", expand=True)

        for medico in self.gestor_medicos.listar_medicos():
            tree.insert("", "end", values=(
                medico.id_medico,
                medico.nombre,
                medico.apellido,
                medico.especialidad.nombre
            ))

    def mostrar_formulario_cita(self):
        """Muestra el formulario para gestión de citas con opciones de crear, modificar y cancelar."""
        self.limpiar_pantalla()
        self.cita_seleccionada = None

        lbl_titulo = tk.Label(self.root, text="Registro de Citas", font=("Arial", 14))
        lbl_titulo.pack(pady=10)

        frame_formulario = tk.Frame(self.root)
        frame_formulario.pack(pady=10)

        # Campos del formulario
        tk.Label(frame_formulario, text="ID Cita:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.entry_id = tk.Entry(frame_formulario)
        self.entry_id.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_formulario, text="Fecha (DD/MM/AAAA):").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.entry_fecha = tk.Entry(frame_formulario)
        self.entry_fecha.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_formulario, text="Hora (HH:MM):").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.entry_hora = tk.Entry(frame_formulario)
        self.entry_hora.grid(row=2, column=1, padx=5, pady=5)

        # Selección de paciente
        tk.Label(frame_formulario, text="Paciente:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        pacientes = [f"{p.id_paciente} - {p.get_nombre_completo()}" for p in self.gestor_pacientes.listar_pacientes()]
        self.combo_paciente = ttk.Combobox(frame_formulario, values=pacientes, state="readonly")
        self.combo_paciente.grid(row=3, column=1, padx=5, pady=5)

        # Selección de médico
        tk.Label(frame_formulario, text="Médico:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        medicos = [f"{m.id_medico} - {m.get_nombre_completo()} ({m.especialidad.nombre})"
                   for m in self.gestor_medicos.listar_medicos()]
        self.combo_medico = ttk.Combobox(frame_formulario, values=medicos, state="readonly")
        self.combo_medico.grid(row=4, column=1, padx=5, pady=5)

        frame_botones = tk.Frame(self.root)
        frame_botones.pack(pady=10)

        self.btn_guardar = tk.Button(frame_botones, text="Guardar", command=self.guardar_cita)
        self.btn_guardar.grid(row=0, column=0, padx=5)

        self.btn_cancelar_cita = tk.Button(frame_botones, text="Cancelar Cita", state=tk.DISABLED,
                                           command=self.cancelar_cita)
        self.btn_cancelar_cita.grid(row=0, column=2, padx=5)

        self.btn_modificar = tk.Button(frame_botones, text="Modificar Cita", state=tk.DISABLED,
                                       command=self.modificar_cita)
        self.btn_modificar.grid(row=0, column=1, padx=5)

        btn_regresar = tk.Button(frame_botones, text="Regresar", command=self.crear_menu_principal)
        btn_regresar.grid(row=0, column=3, padx=5)

        # Lista de citas
        frame_lista = tk.Frame(self.root)
        frame_lista.pack(pady=10, fill="both", expand=True)

        lbl_lista = tk.Label(frame_lista, text="Citas Registradas")
        lbl_lista.pack()

        self.tree = ttk.Treeview(frame_lista, columns=("ID", "Fecha", "Hora", "Paciente", "Médico", "Estado"),
                                 show="headings", selectmode="browse")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Fecha", text="Fecha")
        self.tree.heading("Hora", text="Hora")
        self.tree.heading("Paciente", text="Paciente")
        self.tree.heading("Médico", text="Médico")
        self.tree.heading("Estado", text="Estado")
        self.tree.pack(fill="both", expand=True)

        # Llenar el treeview con las citas existentes
        self.actualizar_lista_citas()

        # Configurar evento de selección
        self.tree.bind("<<TreeviewSelect>>", self.on_cita_seleccionada)

    def actualizar_lista_citas(self):
        """Actualiza la tabla leyendo directamente del gestor"""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Repoblar tabla
        for cita in self.gestor_citas.listar_citas():
            self.tree.insert("", "end", values=(
                cita.id_cita,
                cita.fecha,
                cita.hora,
                cita.paciente.get_nombre_completo(),
                cita.medico.get_nombre_completo(),
                cita.estado
            ))

    def on_cita_seleccionada(self, event):
        """Maneja la selección de una cita en el Treeview."""
        seleccion = self.tree.selection()
        if seleccion:
            item = self.tree.item(seleccion[0])
            id_cita = item['values'][0]
            self.cita_seleccionada = self.gestor_citas.buscar_cita(id_cita)

            # Habilitar botones de modificar/cancelar
            self.btn_cancelar_cita.config(state=tk.NORMAL)
            self.btn_modificar.config(state=tk.NORMAL)

            # Cargar datos en el formulario
            self.entry_id.delete(0, tk.END)
            self.entry_id.insert(0, self.cita_seleccionada.id_cita)
            self.entry_fecha.delete(0, tk.END)
            self.entry_fecha.insert(0, self.cita_seleccionada.fecha)
            self.entry_hora.delete(0, tk.END)
            self.entry_hora.insert(0, self.cita_seleccionada.hora)

            # Seleccionar paciente/médico en los combobox
            self.combo_paciente.set(
                f"{self.cita_seleccionada.paciente.id_paciente} - {self.cita_seleccionada.paciente.get_nombre_completo()}")
            self.combo_medico.set(
                f"{self.cita_seleccionada.medico.id_medico} - {self.cita_seleccionada.medico.get_nombre_completo()}")

    def guardar_cita(self):
        """Crea una nueva cita con los datos del formulario."""
        try:
            id_paciente = self.combo_paciente.get().split(" - ")[0]
            id_medico = self.combo_medico.get().split(" - ")[0]

            paciente = self.gestor_pacientes.buscar_paciente(id_paciente)
            medico = self.gestor_medicos.buscar_medico(id_medico)

            if not paciente or not medico:
                raise ValueError("Paciente o médico no encontrado")

            cita = Cita(
                self.entry_id.get(),
                self.entry_fecha.get(),
                self.entry_hora.get(),
                paciente,
                medico
            )
            self.gestor_citas.agendar_cita(cita)
            messagebox.showinfo("Éxito", "Cita agendada correctamente")
            self.actualizar_lista_citas()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agendar la cita: {e}")

    def cancelar_cita(self):
        """Cancela la cita seleccionada."""
        if not self.cita_seleccionada:
            return

        confirmacion = messagebox.askyesno(
            "Confirmar",
            f"¿Cancelar la cita {self.cita_seleccionada.id_cita}?"
        )

        if not confirmacion:
            return

        if self.gestor_citas.cancelar_cita(self.cita_seleccionada.id_cita):
            self.actualizar_lista_citas()
            self.limpiar_formulario()
            messagebox.showinfo("Éxito", "Cita cancelada correctamente")
        else:
            messagebox.showerror("Error", "La cita no pudo ser cancelada")

    def modificar_cita(self):
        """Modifica la cita seleccionada con los nuevos datos del formulario."""
        if self.cita_seleccionada:
            try:
                nueva_fecha = self.entry_fecha.get()
                nueva_hora = self.entry_hora.get()

                if not nueva_fecha or not nueva_hora:
                    raise ValueError("Fecha y hora son obligatorios")

                if self.gestor_citas.reagendar_cita(
                        self.cita_seleccionada.id_cita,
                        nueva_fecha,
                        nueva_hora
                ):
                    messagebox.showinfo("Éxito", "Cita modificada correctamente")
                    self.actualizar_lista_citas()
                else:
                    messagebox.showerror("Error", "No se pudo modificar la cita")
            except Exception as e:
                messagebox.showerror("Error", f"Error al modificar: {str(e)}")

    def limpiar_formulario(self):
        """Limpia todos los campos del formulario."""
        self.entry_id.delete(0, tk.END)
        self.entry_fecha.delete(0, tk.END)
        self.entry_hora.delete(0, tk.END)
        self.combo_paciente.set('')
        self.combo_medico.set('')
        self.cita_seleccionada = None
        self.btn_cancelar_cita.config(state=tk.DISABLED)
        self.btn_modificar.config(state=tk.DISABLED)

    def mostrar_reportes(self):
        """Muestra los reportes y estadísticas del sistema."""
        self.limpiar_pantalla()

        lbl_titulo = tk.Label(self.root, text="Reportes y Estadísticas", font=("Arial", 14))
        lbl_titulo.pack(pady=10)

        frame_reportes = tk.Frame(self.root)
        frame_reportes.pack(pady=10, fill="both", expand=True)

        # Consultas por especialidad
        lbl_especialidad = tk.Label(frame_reportes, text="Consultas por Especialidad", font=("Arial", 12))
        lbl_especialidad.pack()

        tree_especialidad = ttk.Treeview(frame_reportes, columns=("Especialidad", "Consultas"), show="headings")
        tree_especialidad.heading("Especialidad", text="Especialidad")
        tree_especialidad.heading("Consultas", text="Consultas")
        tree_especialidad.pack(fill="x", pady=5)

        consultas_especialidad = self.gestor_estadisticas.calcular_consultas_por_especialidad(
            self.gestor_medicos, self.gestor_citas
        )
        for especialidad, consultas in consultas_especialidad.items():
            tree_especialidad.insert("", "end", values=(especialidad, consultas))

        # Médico más solicitado
        lbl_medico = tk.Label(frame_reportes, text="Médico Más Solicitado", font=("Arial", 12))
        lbl_medico.pack(pady=(10, 0))

        medico_solicitado = self.gestor_estadisticas.medico_mas_solicitado(
            self.gestor_medicos, self.gestor_citas
        )
        if medico_solicitado:
            lbl_info = tk.Label(frame_reportes,
                                text=f"{medico_solicitado.get_nombre_completo()} - {medico_solicitado.especialidad.nombre}")
            lbl_info.pack()
        else:
            lbl_info = tk.Label(frame_reportes, text="No hay datos suficientes")
            lbl_info.pack()

        # Promedio de atención mensual
        lbl_promedio = tk.Label(frame_reportes, text="Promedio de Atención Mensual", font=("Arial", 12))
        lbl_promedio.pack(pady=(10, 0))

        promedio = self.gestor_estadisticas.promedio_atencion_mensual(self.gestor_citas)
        lbl_promedio_valor = tk.Label(frame_reportes, text=f"{promedio:.2f} consultas por mes")
        lbl_promedio_valor.pack()

        # Botón de regreso
        btn_regresar = tk.Button(self.root, text="Regresar", command=self.crear_menu_principal)
        btn_regresar.pack(pady=10)

    def ejecutar(self):
        """Inicia la aplicación."""
        self.root.mainloop()