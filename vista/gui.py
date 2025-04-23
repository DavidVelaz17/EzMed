import tkinter as tk
from tkinter import ttk, messagebox
from controlador.gestor_diagnosticos import GestorDiagnosticos
from controlador.gestor_pacientes import GestorPacientes
from controlador.gestor_medicos import GestorMedicos
from controlador.gestor_citas import GestorCitas
from controlador.gestor_estadisticas import GestorEstadisticas
from controlador.gestor_especialidades import GestorEspecialidades


class GUI:
    """Clase que representa la interfaz gráfica del sistema de gestión clínica."""

    def __init__(self):
        """Inicializa la interfaz gráfica y sus componentes."""
        self.gestor_pacientes = GestorPacientes()
        self.gestor_medicos = GestorMedicos()
        self.gestor_citas = GestorCitas()
        self.gestor_estadisticas = GestorEstadisticas()
        self.gestor_especialidades = GestorEspecialidades()
        self.gestor_diagnosticos = GestorDiagnosticos(self.gestor_citas)

        self.root = tk.Tk()
        self.root.title("Sistema de Gestión Clínica")
        self.root.geometry("800x600")
        self.crear_menu_principal()

    def limpiar_widgets(self, *widgets):
        """Limpia los widgets proporcionados."""
        for widget in widgets:
            if isinstance(widget, tk.Entry):
                widget.delete(0, tk.END)
            elif isinstance(widget, (ttk.Combobox, tk.Text)):
                widget.delete(0 if isinstance(widget, ttk.Combobox) else "1.0", tk.END)
            elif isinstance(widget, ttk.Treeview):
                for item in widget.get_children():
                    widget.delete(item)

    def _crear_campo_formulario(self, frame, texto, row, col=0, tipo="entry", valores=None):
        """Crea un campo de formulario con su label."""
        tk.Label(frame, text=texto).grid(row=row, column=col, sticky="e", padx=5, pady=5)

        if tipo == "entry":
            widget = tk.Entry(frame)
        elif tipo == "combobox":
            widget = ttk.Combobox(frame, values=valores, state="readonly")
        elif tipo == "text":
            widget = tk.Text(frame, height=5, width=50)

        widget.grid(row=row, column=col + 1, padx=5, pady=5)
        return widget

    def _crear_botones(self, frame, texto_guardar, comando_guardar, texto_extra=None, comando_extra=None):
        """Crea los botones estándar de los formularios."""
        btn_guardar = tk.Button(frame, text=texto_guardar, command=comando_guardar)
        btn_guardar.grid(row=0, column=0, padx=5)

        if texto_extra and comando_extra:
            btn_extra = tk.Button(frame, text=texto_extra, command=comando_extra)
            btn_extra.grid(row=0, column=1, padx=5)

        btn_regresar = tk.Button(frame, text="Regresar", command=self.crear_menu_principal)
        btn_regresar.grid(row=0, column=2 if texto_extra else 1, padx=5)

    def _actualizar_treeview(self, tree, datos, columnas):
        """Actualiza un Treeview con los datos proporcionados."""
        self.limpiar_widgets(tree)
        for item in datos:
            tree.insert("", "end", values=tuple(item[col] for col in columnas))

    def _obtener_seleccion_treeview(self, tree, mensaje_error="Seleccione un elemento de la tabla"):
        """Obtiene el item seleccionado en un Treeview."""
        seleccion = tree.selection()
        if not seleccion:
            messagebox.showerror("Error", mensaje_error)
            return None
        return tree.item(seleccion[0])

    def _crear_titulo(self, texto):
        """Crea un título centrado en la pantalla."""
        lbl_titulo = tk.Label(self.root, text=texto, font=("Arial", 14))
        lbl_titulo.pack(pady=10)
        return lbl_titulo

    def _crear_frame_con_scroll(self):
        """Crea un frame con scrollbar vertical."""
        frame_principal = tk.Frame(self.root)
        frame_principal.pack(fill="both", expand=True)

        canvas = tk.Canvas(frame_principal)
        scrollbar = ttk.Scrollbar(frame_principal, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        return scrollable_frame

    def crear_menu_principal(self):
        """Crea el menú principal de la aplicación."""
        self.limpiar_pantalla()

        lbl_titulo = tk.Label(self.root, text="Sistema de Gestión Clínica", font=("Arial", 16))
        lbl_titulo.pack(pady=20)

        frame_principal = tk.Frame(self.root)
        frame_principal.pack(expand=True, fill='both')

        frame_botones = tk.Frame(frame_principal)
        frame_botones.pack(pady=20)

        ancho_botones = 25
        opciones_menu = [
            ("Gestión de Pacientes", self.mostrar_formulario_paciente),
            ("Gestión de Médicos", self.mostrar_formulario_medico),
            ("Gestión de Citas", self.mostrar_formulario_cita),
            ("Gestión de Diagnósticos", self.mostrar_formulario_diagnostico),
            ("Reportes y Estadísticas", self.mostrar_reportes),
            ("Gestión de Especialidades", self.mostrar_formulario_especialidades)
        ]

        for texto, comando in opciones_menu:
            btn = tk.Button(frame_botones, text=texto, command=comando, width=ancho_botones)
            btn.pack(pady=5, fill='x')

    def limpiar_pantalla(self):
        """Limpia todos los widgets de la pantalla."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def mostrar_formulario_paciente(self):
        """Muestra el formulario para gestión de pacientes."""
        self.limpiar_pantalla()
        self._crear_titulo("Registro de Pacientes")

        frame_formulario = tk.Frame(self.root)
        frame_formulario.pack(pady=10)

        entry_nombre = self._crear_campo_formulario(frame_formulario, "Nombre:", 0)
        entry_apellido = self._crear_campo_formulario(frame_formulario, "Apellido:", 1)
        entry_fecha_nac = self._crear_campo_formulario(frame_formulario, "Fecha Nacimiento (DD/MM/AAAA):", 2)
        entry_telefono = self._crear_campo_formulario(frame_formulario, "Teléfono:", 3)

        frame_botones = tk.Frame(self.root)
        frame_botones.pack(pady=10)

        def guardar_paciente():
            try:
                paciente = {
                    'nombre': entry_nombre.get(),
                    'apellido': entry_apellido.get(),
                    'fecha_nacimiento': entry_fecha_nac.get(),
                    'telefono': entry_telefono.get()
                }
                if not self.gestor_pacientes.agregar_paciente(paciente):
                    messagebox.showerror("Error",
                                         "Datos inválidos. Verifique:\n- Nombres/apellidos solo letras\n- Fecha previa a hoy (DD/MM/AAAA)\n- Teléfono 10 dígitos")
                else:
                    messagebox.showinfo("Éxito", "Paciente registrado")
                    self.crear_menu_principal()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo registrar el paciente: {e}")

        self._crear_botones(frame_botones, "Guardar", guardar_paciente)

        frame_lista = tk.Frame(self.root)
        frame_lista.pack(pady=10, fill="both", expand=True)

        tk.Label(frame_lista, text="Pacientes Registrados").pack()

        tree = ttk.Treeview(frame_lista, columns=("ID", "Nombre", "Apellido", "Teléfono"), show="headings")
        for col in tree["columns"]:
            tree.heading(col, text=col)
        tree.pack(fill="both", expand=True)

        datos = [{
            "ID": p.id_paciente,
            "Nombre": p.nombre,
            "Apellido": p.apellido,
            "Teléfono": p.telefono
        } for p in self.gestor_pacientes.listar_pacientes()]
        self._actualizar_treeview(tree, datos, ("ID", "Nombre", "Apellido", "Teléfono"))

    def mostrar_formulario_medico(self):
        """Muestra el formulario para gestión de médicos."""
        self.limpiar_pantalla()
        self._crear_titulo("Registro de Médicos")

        frame_formulario = tk.Frame(self.root)
        frame_formulario.pack(pady=10)

        entry_nombre = self._crear_campo_formulario(frame_formulario, "Nombre:", 0)
        entry_apellido = self._crear_campo_formulario(frame_formulario, "Apellido:", 1)
        entry_fecha_nac = self._crear_campo_formulario(frame_formulario, "Fecha Nacimiento (DD/MM/AAAA):", 2)
        entry_telefono = self._crear_campo_formulario(frame_formulario, "Teléfono:", 3)

        especialidades = [e.nombre for e in self.gestor_especialidades.listar_especialidades()]
        combo_especialidad = self._crear_campo_formulario(
            frame_formulario, "Especialidad:", 4, tipo="combobox", valores=especialidades)

        frame_botones = tk.Frame(self.root)
        frame_botones.pack(pady=10)

        def guardar_medico():
            try:
                nombre_esp = combo_especialidad.get()
                if not nombre_esp:
                    messagebox.showerror("Error", "Seleccione una especialidad válida")
                    return

                medico = {
                    'nombre': entry_nombre.get(),
                    'apellido': entry_apellido.get(),
                    'fecha_nacimiento': entry_fecha_nac.get(),
                    'telefono': entry_telefono.get(),
                    'especialidad': nombre_esp
                }

                if not self.gestor_medicos.agregar_medico(medico):
                    messagebox.showerror("Error",
                                         "Datos inválidos. Verifique:\n- Nombres/apellidos solo letras\n- Fecha previa a hoy (DD/MM/AAAA)\n- Teléfono 10 dígitos\n- Especialidad seleccionada")
                else:
                    messagebox.showinfo("Éxito", "Médico registrado")
                    self.crear_menu_principal()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo registrar el médico: {e}")

        self._crear_botones(frame_botones, "Guardar", guardar_medico)

        frame_lista = tk.Frame(self.root)
        frame_lista.pack(pady=10, fill="both", expand=True)

        tk.Label(frame_lista, text="Médicos Registrados").pack()

        tree = ttk.Treeview(frame_lista, columns=("ID", "Nombre", "Apellido", "Especialidad"), show="headings")
        for col in tree["columns"]:
            tree.heading(col, text=col)
        tree.pack(fill="both", expand=True)

        datos = [{
            "ID": m.id_medico,
            "Nombre": m.nombre,
            "Apellido": m.apellido,
            "Especialidad": m.especialidad.nombre
        } for m in self.gestor_medicos.listar_medicos()]
        self._actualizar_treeview(tree, datos, ("ID", "Nombre", "Apellido", "Especialidad"))

    def mostrar_formulario_cita(self):
        """Muestra el formulario para gestión de citas."""
        self.limpiar_pantalla()
        self.cita_seleccionada = None
        self._crear_titulo("Registro de Citas")

        frame_formulario = tk.Frame(self.root)
        frame_formulario.pack(pady=10)

        self.entry_fecha = self._crear_campo_formulario(frame_formulario, "Fecha (DD/MM/AAAA):", 0)
        self.entry_hora = self._crear_campo_formulario(frame_formulario, "Hora (HH:MM):", 1)

        pacientes = [f"{p.id_paciente} - {p.get_nombre_completo()}" for p in self.gestor_pacientes.listar_pacientes()]
        self.combo_paciente = self._crear_campo_formulario(
            frame_formulario, "Paciente:", 2, tipo="combobox", valores=pacientes)

        medicos = [f"{m.id_medico} - {m.get_nombre_completo()} ({m.especialidad.nombre})"
                   for m in self.gestor_medicos.listar_medicos()]
        self.combo_medico = self._crear_campo_formulario(
            frame_formulario, "Médico:", 3, tipo="combobox", valores=medicos)

        frame_botones = tk.Frame(self.root)
        frame_botones.pack(pady=10)

        self.btn_guardar = tk.Button(frame_botones, text="Guardar", command=self.guardar_cita)
        self.btn_guardar.grid(row=0, column=0, padx=5)

        self.btn_modificar = tk.Button(frame_botones, text="Modificar Cita", state=tk.DISABLED,
                                       command=self.modificar_cita)
        self.btn_modificar.grid(row=0, column=1, padx=5)

        self.btn_cancelar_cita = tk.Button(frame_botones, text="Cancelar Cita", state=tk.DISABLED,
                                           command=self.cancelar_cita)
        self.btn_cancelar_cita.grid(row=0, column=2, padx=5)

        btn_regresar = tk.Button(frame_botones, text="Regresar", command=self.crear_menu_principal)
        btn_regresar.grid(row=0, column=3, padx=5)

        frame_filtros = tk.Frame(self.root)
        frame_filtros.pack(pady=10, fill=tk.X)

        tk.Label(frame_filtros, text="Filtrar por paciente:").grid(row=0, column=0, padx=5)
        opciones_pacientes = ["Todos"] + pacientes
        self.combo_filtro_paciente = ttk.Combobox(frame_filtros, values=opciones_pacientes, state="readonly")
        self.combo_filtro_paciente.grid(row=0, column=1, padx=5)
        self.combo_filtro_paciente.set("Todos")
        self.combo_filtro_paciente.bind("<<ComboboxSelected>>", self.aplicar_filtros)

        tk.Label(frame_filtros, text="Filtrar por médico:").grid(row=0, column=2, padx=5)
        opciones_medicos = ["Todos"] + medicos
        self.combo_filtro_medico = ttk.Combobox(frame_filtros, values=opciones_medicos, state="readonly")
        self.combo_filtro_medico.grid(row=0, column=3, padx=5)
        self.combo_filtro_medico.set("Todos")
        self.combo_filtro_medico.bind("<<ComboboxSelected>>", self.aplicar_filtros)

        btn_limpiar = tk.Button(frame_filtros, text="Limpiar filtros", command=self.limpiar_filtros)
        btn_limpiar.grid(row=0, column=4, padx=5)

        frame_lista = tk.Frame(self.root)
        frame_lista.pack(pady=10, fill="both", expand=True)

        tk.Label(frame_lista, text="Citas Registradas").pack()

        self.tree = ttk.Treeview(frame_lista, columns=("ID", "Fecha", "Hora", "Paciente", "Médico", "Estado"),
                                 show="headings", selectmode="browse")
        for i, col in enumerate(("ID", "Fecha", "Hora", "Paciente", "Médico", "Estado")):
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True)

        self.actualizar_lista_citas()
        self.tree.bind("<<TreeviewSelect>>", self.on_cita_seleccionada)

    def mostrar_formulario_diagnostico(self):
        """Muestra el formulario para gestionar diagnósticos médicos."""
        self.limpiar_pantalla()
        self._crear_titulo("Gestión de Diagnósticos")

        scrollable_frame = self._crear_frame_con_scroll()

        frame_medico = tk.Frame(scrollable_frame)
        frame_medico.pack(pady=10, fill="x")

        tk.Label(frame_medico, text="Selecciona el médico que realizará el diagnóstico:").pack(side="left", padx=5)

        medicos = [f"{m.id_medico} - {m.get_nombre_completo()}" for m in self.gestor_medicos.listar_medicos()]
        self.combo_medico_diag = ttk.Combobox(frame_medico, values=medicos, state="readonly")
        self.combo_medico_diag.pack(side="left", padx=5, fill="x", expand=True)
        self.combo_medico_diag.bind("<<ComboboxSelected>>", self.actualizar_citas_pendientes)

        frame_tabla = tk.Frame(scrollable_frame)
        frame_tabla.pack(pady=10, fill="both", expand=True)

        tk.Label(frame_tabla, text="Citas pendientes para diagnóstico").pack()

        self.tree_citas = ttk.Treeview(frame_tabla, columns=("ID", "Fecha", "Hora", "Paciente"), show="headings")
        for col in self.tree_citas["columns"]:
            self.tree_citas.heading(col, text=col)
        self.tree_citas.pack(fill="both", expand=True)

        frame_formulario = tk.Frame(scrollable_frame)
        frame_formulario.pack(pady=10, fill="x")

        self.entry_descripcion = self._crear_campo_formulario(frame_formulario, "Descripción:", 0, tipo="text")
        self.entry_tratamiento = self._crear_campo_formulario(frame_formulario, "Tratamiento:", 1, tipo="text")
        self.entry_observaciones = self._crear_campo_formulario(frame_formulario, "Observaciones:", 2, tipo="text")

        frame_botones = tk.Frame(scrollable_frame)
        frame_botones.pack(pady=10)

        self._crear_botones(frame_botones, "Guardar Diagnóstico", self.guardar_diagnostico)

        if len(medicos) == 1:
            self.combo_medico_diag.set(medicos[0])
            self.actualizar_citas_pendientes()

    def actualizar_citas_pendientes(self, event=None):
        """Actualiza la tabla de citas pendientes según el médico seleccionado."""
        self.limpiar_widgets(self.tree_citas)

        medico_sel = self.combo_medico_diag.get()
        if not medico_sel:
            return

        id_medico = medico_sel.split(" - ")[0]
        citas_medico = [c for c in self.gestor_citas.listar_citas()
                        if c.medico.id_medico == id_medico and c.estado == "pendiente"]

        datos = [{
            "ID": c.id_cita,
            "Fecha": c.fecha,
            "Hora": c.hora,
            "Paciente": c.paciente.get_nombre_completo()
        } for c in citas_medico]
        self._actualizar_treeview(self.tree_citas, datos, ("ID", "Fecha", "Hora", "Paciente"))

    def guardar_diagnostico(self):
        """Guarda un nuevo diagnóstico con los datos del formulario."""
        try:
            item = self._obtener_seleccion_treeview(self.tree_citas, "Seleccione una cita de la tabla")
            if not item:
                return

            id_cita = item['values'][0]
            cita = self.gestor_citas.buscar_cita(id_cita)

            descripcion = self.entry_descripcion.get("1.0", tk.END).strip()
            if not descripcion:
                messagebox.showerror("Error", "La descripción es obligatoria")
                return

            tratamiento = self.entry_tratamiento.get("1.0", tk.END).strip()
            observaciones = self.entry_observaciones.get("1.0", tk.END).strip()

            if self.gestor_diagnosticos.registrar_diagnostico(
                    descripcion=descripcion,
                    tratamiento=tratamiento,
                    observaciones=observaciones,
                    cita=cita
            ):
                messagebox.showinfo("Éxito", "Diagnóstico registrado correctamente")
                self.actualizar_citas_pendientes()
                self.limpiar_widgets(self.entry_descripcion, self.entry_tratamiento, self.entry_observaciones)
            else:
                messagebox.showerror("Error", "No se pudo registrar el diagnóstico")

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al guardar: {str(e)}")

    def actualizar_lista_citas(self):
        """Actualiza la tabla aplicando los filtros actuales."""
        filtro_paciente = self.combo_filtro_paciente.get().split(" - ")[
            0] if self.combo_filtro_paciente.get() != "Todos" else None
        filtro_medico = self.combo_filtro_medico.get().split(" - ")[
            0] if self.combo_filtro_medico.get() != "Todos" else None

        citas_filtradas = [c for c in self.gestor_citas.listar_citas()
                           if (filtro_paciente is None or c.paciente.id_paciente == filtro_paciente) and
                           (filtro_medico is None or c.medico.id_medico == filtro_medico)]

        datos = [{
            "ID": c.id_cita,
            "Fecha": c.fecha,
            "Hora": c.hora,
            "Paciente": c.paciente.get_nombre_completo(),
            "Médico": c.medico.get_nombre_completo(),
            "Estado": c.estado
        } for c in citas_filtradas]
        self._actualizar_treeview(self.tree, datos, ("ID", "Fecha", "Hora", "Paciente", "Médico", "Estado"))

    def on_cita_seleccionada(self, event):
        """Maneja la selección de una cita en el Treeview."""
        item = self._obtener_seleccion_treeview(self.tree)
        if not item:
            return

        id_cita = item['values'][0]
        self.cita_seleccionada = self.gestor_citas.buscar_cita(id_cita)

        self.btn_cancelar_cita.config(state=tk.NORMAL)
        self.btn_modificar.config(state=tk.NORMAL)

        self.limpiar_widgets(self.entry_fecha, self.entry_hora)
        self.entry_fecha.insert(0, self.cita_seleccionada.fecha)
        self.entry_hora.insert(0, self.cita_seleccionada.hora)

        self.combo_paciente.set(
            f"{self.cita_seleccionada.paciente.id_paciente} - {self.cita_seleccionada.paciente.get_nombre_completo()}")
        self.combo_medico.set(
            f"{self.cita_seleccionada.medico.id_medico} - {self.cita_seleccionada.medico.get_nombre_completo()}")

        self.combo_medico.config(state=tk.DISABLED)
        self.combo_paciente.config(state=tk.DISABLED)

    def guardar_cita(self):
        """Crea una nueva cita con los datos del formulario."""
        try:
            id_paciente = self.combo_paciente.get().split(" - ")[0]
            id_medico = self.combo_medico.get().split(" - ")[0]

            paciente = self.gestor_pacientes.buscar_paciente(id_paciente)
            medico = self.gestor_medicos.buscar_medico(id_medico)

            if not paciente or not medico:
                raise ValueError("Paciente o médico no encontrado")

            fecha = self.entry_fecha.get()
            hora = self.entry_hora.get()

            if not self.gestor_citas.agendar_cita(fecha, hora, paciente, medico):
                messagebox.showerror("Error",
                                     "Datos inválidos. Verifique:\n- Fecha posterior a hoy (DD/MM/AAAA)\n- Hora en formato HH:MM")
            else:
                messagebox.showinfo("Éxito", "Cita agendada")
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
        if not self.cita_seleccionada:
            return

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
        self.limpiar_widgets(self.entry_fecha, self.entry_hora, self.combo_paciente, self.combo_medico)
        self.combo_paciente.set('')
        self.combo_medico.set('')
        self.cita_seleccionada = None
        self.btn_cancelar_cita.config(state=tk.DISABLED)
        self.btn_modificar.config(state=tk.DISABLED)
        self.combo_medico.config(state="readonly")
        self.combo_paciente.config(state="readonly")

    def mostrar_reportes(self):
        """Muestra los reportes y estadísticas del sistema."""
        self.limpiar_pantalla()
        self._crear_titulo("Reportes y Estadísticas")

        frame_reportes = tk.Frame(self.root)
        frame_reportes.pack(pady=10, fill="both", expand=True)

        # Consultas por especialidad
        tk.Label(frame_reportes, text="Consultas por Especialidad", font=("Arial", 12)).pack()

        tree_especialidad = ttk.Treeview(frame_reportes, columns=("Especialidad", "Consultas"), show="headings")
        for col in tree_especialidad["columns"]:
            tree_especialidad.heading(col, text=col)
        tree_especialidad.pack(fill="x", pady=5)

        consultas = self.gestor_estadisticas.calcular_consultas_por_especialidad(
            self.gestor_medicos, self.gestor_citas
        )
        datos = [{"Especialidad": k, "Consultas": v} for k, v in consultas.items()]
        self._actualizar_treeview(tree_especialidad, datos, ("Especialidad", "Consultas"))

        # Médico más solicitado
        tk.Label(frame_reportes, text="Médico más Solicitado", font=("Arial", 12)).pack(pady=(10, 0))

        medico_solicitado, num_citas = self.gestor_estadisticas.medico_mas_solicitado(
            self.gestor_medicos, self.gestor_citas
        )
        texto_medico = (
            f"{medico_solicitado.get_nombre_completo()} ({num_citas} citas) - {medico_solicitado.especialidad.nombre}"
            if medico_solicitado else "No hay datos suficientes de médicos")
        tk.Label(frame_reportes, text=texto_medico).pack()

        # Paciente con más citas
        tk.Label(frame_reportes, text="Paciente frecuente", font=("Arial", 12)).pack(pady=(10, 0))

        paciente_mas_citas, num_citas = self.gestor_estadisticas.paciente_con_mas_citas(
            self.gestor_pacientes, self.gestor_citas
        )
        texto_paciente = (f"{paciente_mas_citas.get_nombre_completo()} ({num_citas} citas)"
                          if paciente_mas_citas else "No hay datos suficientes de pacientes")
        tk.Label(frame_reportes, text=texto_paciente).pack()

        # Promedio de atención mensual
        tk.Label(frame_reportes, text="Promedio de Atención Mensual", font=("Arial", 12)).pack(pady=(10, 0))

        promedio = self.gestor_estadisticas.promedio_atencion_mensual(self.gestor_citas)
        tk.Label(frame_reportes, text=f"{promedio:.2f} consultas por mes").pack()

        self._crear_botones(tk.Frame(self.root), "Regresar", self.crear_menu_principal)

    def aplicar_filtros(self, event=None):
        """Aplica los filtros seleccionados a la lista de citas."""
        widget_disparador = event.widget if event else None

        if widget_disparador == self.combo_filtro_paciente:
            if self.combo_filtro_paciente.get() != "Todos":
                self.combo_filtro_medico.set("Todos")
                self.combo_filtro_medico.config(state=tk.DISABLED)
            else:
                self.combo_filtro_medico.config(state="readonly")

        elif widget_disparador == self.combo_filtro_medico:
            if self.combo_filtro_medico.get() != "Todos":
                self.combo_filtro_paciente.set("Todos")
                self.combo_filtro_paciente.config(state=tk.DISABLED)
            else:
                self.combo_filtro_paciente.config(state="readonly")

        self.actualizar_lista_citas()

    def limpiar_filtros(self):
        """Restablece todos los filtros a sus valores por defecto."""
        self.combo_filtro_paciente.set("Todos")
        self.combo_filtro_medico.set("Todos")
        self.combo_filtro_paciente.config(state="readonly")
        self.combo_filtro_medico.config(state="readonly")
        self.actualizar_lista_citas()

    def mostrar_formulario_especialidades(self):
        """Muestra el formulario para gestión de especialidades."""
        self.limpiar_pantalla()
        self._crear_titulo("Gestión de Especialidades")

        frame_formulario = tk.Frame(self.root)
        frame_formulario.pack(pady=10)

        entry_nombre = self._crear_campo_formulario(frame_formulario, "Nombre:", 0)
        entry_desc = self._crear_campo_formulario(frame_formulario, "Descripción:", 1)

        frame_botones = tk.Frame(self.root)
        frame_botones.pack(pady=10)

        def guardar_especialidad():
            nombre = entry_nombre.get()
            desc = entry_desc.get()
            if nombre and desc:
                if self.gestor_especialidades.agregar_especialidad(nombre, desc):
                    messagebox.showinfo("Éxito", "Especialidad agregada")
                    actualizar_lista()
                    self.limpiar_widgets(entry_nombre, entry_desc)
                else:
                    messagebox.showerror("Error", "La especialidad ya existe")
            else:
                messagebox.showerror("Error", "Complete todos los campos")

        def eliminar_seleccionada():
            item = self._obtener_seleccion_treeview(tree, "Seleccione una especialidad para eliminar")
            if not item:
                return

            nombre = item['values'][0]
            if self.gestor_especialidades.eliminar_especialidad(nombre):
                messagebox.showinfo("Éxito", "Especialidad eliminada")
                actualizar_lista()
            else:
                messagebox.showerror("Error", "No se pudo eliminar")

        self._crear_botones(frame_botones, "Guardar", guardar_especialidad, "Eliminar", eliminar_seleccionada)

        frame_lista = tk.Frame(self.root)
        frame_lista.pack(pady=10, fill="both", expand=True)

        tk.Label(frame_lista, text="Especialidades Registradas").pack()

        tree = ttk.Treeview(frame_lista, columns=("Nombre", "Descripción"), show="headings")
        for col in tree["columns"]:
            tree.heading(col, text=col)
        tree.pack(fill="both", expand=True)

        def actualizar_lista():
            datos = [{"Nombre": e.nombre, "Descripción": e.descripcion}
                     for e in self.gestor_especialidades.listar_especialidades()]
            self._actualizar_treeview(tree, datos, ("Nombre", "Descripción"))

        actualizar_lista()

    def ejecutar(self):
        """Inicia la aplicación."""
        self.root.mainloop()