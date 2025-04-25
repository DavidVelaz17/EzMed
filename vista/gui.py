import tkinter as tk
from tkinter import ttk, messagebox

from controlador.gestor_diagnosticos import GestorDiagnosticos
from controlador.gestor_pacientes import GestorPacientes
from controlador.gestor_medicos import GestorMedicos
from controlador.gestor_citas import GestorCitas
from controlador.gestor_estadisticas import GestorEstadisticas
from controlador.gestor_especialidades import GestorEspecialidades

class GUI:
    """
    Interfaz gráfica para el sistema de gestión clínica.

    Administra la visualización de los formularios y menús para gestionar pacientes, médicos, citas, diagnósticos y reportes.
    """
    def __init__(self):
        """
        Inicializa la ventana principal y los gestores de datos.

        Crea la ventana principal, establece el título y la geometría, y llama a la función para crear el menú principal.
        """
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

    def crear_menu_principal(self):
        """
        Crea el menú principal con opciones para acceder a las diferentes funcionalidades del sistema.

        Incluye botones para gestión de pacientes, médicos, citas, diagnósticos, reportes y más.
        """
        self.limpiar_pantalla()

        lbl_titulo = tk.Label(self.root, text="Sistema de Gestión Clínica", font=("Arial", 16))
        lbl_titulo.pack(pady=20)

        # Frame principal para centrar todo
        frame_principal = tk.Frame(self.root)
        frame_principal.pack(expand=True, fill='both')

        # Frame para los botones
        frame_botones = tk.Frame(frame_principal)
        frame_botones.pack(pady=20)

        # Configurar un ancho común para todos los botones
        ancho_botones = 25

        btn_pacientes = tk.Button(frame_botones, text="Gestión de Pacientes",
                                  command=self.mostrar_formulario_paciente, width=ancho_botones)
        btn_pacientes.pack(pady=5, fill='x')

        btn_medicos = tk.Button(frame_botones, text="Gestión de Médicos",
                                command=self.mostrar_formulario_medico, width=ancho_botones)
        btn_medicos.pack(pady=5, fill='x')

        btn_especialidades = tk.Button(frame_botones, text="Gestión de Especialidades",
                                       command=self.mostrar_formulario_especialidades, width=ancho_botones)
        btn_especialidades.pack(pady=5, fill='x')

        btn_citas = tk.Button(frame_botones, text="Gestión de Citas",
                              command=self.mostrar_formulario_cita, width=ancho_botones)
        btn_citas.pack(pady=5, fill='x')

        btn_diagnosticos = tk.Button(frame_botones, text="Gestión de Diagnósticos",
                                     command=self.mostrar_formulario_diagnostico, width=ancho_botones)
        btn_diagnosticos.pack(pady=5, fill='x')

        btn_lista_diagnosticos = tk.Button(frame_botones, text="Listado de Diagnósticos",
                                           command=self.mostrar_lista_diagnosticos, width=ancho_botones)
        btn_lista_diagnosticos.pack(pady=5, fill='x')

        btn_reportes = tk.Button(frame_botones, text="Reportes y Estadísticas",
                                 command=self.mostrar_reportes, width=ancho_botones)
        btn_reportes.pack(pady=5, fill='x')


    def limpiar_pantalla(self):
        """
        Limpia la pantalla eliminando todos los widgets actualmente visibles.
        """
        for widget in self.root.winfo_children():
            widget.destroy()

    def mostrar_formulario_paciente(self):
        """
        Muestra el formulario para el registro de pacientes.

        Permite ingresar datos como nombre, apellido, fecha de nacimiento y teléfono.
        También muestra una lista de pacientes registrados.
        """
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

        frame_botones = tk.Frame(self.root)
        frame_botones.pack(pady=10)

        def guardar_paciente():
            """
            Recolecta los datos del formulario y crea un nuevo paciente.

            Excepciones:
                Si ocurre un error durante el proceso de registro, se captura y muestra un mensaje de error con los detalles.
            """
            try:
                paciente = {
                    'nombre': entry_nombre.get(),
                    'apellido': entry_apellido.get(),
                    'fecha_nacimiento': entry_fecha_nac.get(),
                    'telefono': entry_telefono.get()
                }
                if not self.gestor_pacientes.agregar_paciente(paciente):
                    messagebox.showerror("Error", "Datos inválidos. Verifique:"
                                                  "\n- Nombres/apellidos solo letras"
                                                  "\n- Fecha previa a hoy (DD/MM/AAAA)"
                                                  "\n- Teléfono 10 dígitos")
                else:
                    messagebox.showinfo("Éxito", "Paciente registrado")
                    self.crear_menu_principal()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo registrar el paciente: {e}")

        btn_guardar = tk.Button(frame_botones, text="Guardar", command=guardar_paciente)
        btn_guardar.grid(row=0, column=0, padx=5)

        btn_regresar = tk.Button(frame_botones, text="Regresar", command=self.crear_menu_principal)
        btn_regresar.grid(row=0, column=1, padx=5)

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
        """
        Muestra el formulario para el registro de médicos.

        Permite ingresar datos como nombre, apellido, fecha de nacimiento, teléfono y especialidad.
        También muestra una lista de médicos registrados.
        """
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

        tk.Label(frame_formulario, text="Especialidad:").grid(row=5, column=0, sticky="e", padx=5, pady=5)
        especialidades = [e.nombre for e in self.gestor_especialidades.listar_especialidades()]
        combo_especialidad = ttk.Combobox(frame_formulario, values=especialidades, state="readonly")
        combo_especialidad.grid(row=5, column=1, padx=5, pady=5)

        frame_botones = tk.Frame(self.root)
        frame_botones.pack(pady=10)

        def guardar_medico():
            """
            Recolecta los datos del formulario y crea un nuevo médico.

            Excepciones:
                Si ocurre un error durante el proceso de registro, se captura y muestra un mensaje de error con los detalles.
            """
            try:
                nombre_esp = combo_especialidad.get()
                if not nombre_esp:
                    messagebox.showerror("Error", "Seleccione una especialidad válida")
                    return

                # Obtener el objeto Especialidad completo
                especialidad_obj = None
                for esp in self.gestor_especialidades.listar_especialidades():
                    if esp.nombre == nombre_esp:
                        especialidad_obj = esp
                        break

                if not especialidad_obj:
                    messagebox.showerror("Error", "Especialidad no encontrada")
                    return

                medico = {
                    'nombre': entry_nombre.get(),
                    'apellido': entry_apellido.get(),
                    'fecha_nacimiento': entry_fecha_nac.get(),
                    'telefono': entry_telefono.get(),
                    'especialidad': especialidad_obj
                }

                if not self.gestor_medicos.agregar_medico(medico):
                    messagebox.showerror("Error", "Datos inválidos. Verifique:"
                                                  "\n- Nombres/apellidos solo letras"
                                                  "\n- Fecha previa a hoy (DD/MM/AAAA)"
                                                  "\n- Teléfono 10 dígitos"
                                                  "\n- Especialidad seleccionada")
                else:
                    messagebox.showinfo("Éxito", "Médico registrado")
                    self.crear_menu_principal()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo registrar el médico: {e}")

        btn_guardar = tk.Button(frame_botones, text="Guardar", command=guardar_medico)
        btn_guardar.grid(row=0, column=0, padx=5)

        btn_regresar = tk.Button(frame_botones, text="Regresar", command=self.crear_menu_principal)
        btn_regresar.grid(row=0, column=1, padx=5)

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
                medico.especialidad.nombre if hasattr(medico.especialidad, 'nombre') else medico.especialidad
            ))

    def mostrar_formulario_cita(self):
        """
        Muestra el formulario para el registro de citas médicas.

        Permite seleccionar paciente, médico, fecha y hora de la cita, y gestionar las citas registradas.
        """
        self.limpiar_pantalla()
        self.cita_seleccionada = None
        self.filtro_paciente = None
        self.filtro_medico = None

        lbl_titulo = tk.Label(self.root, text="Registro de Citas", font=("Arial", 14))
        lbl_titulo.pack(pady=10)

        # Frame para formulario
        frame_formulario = tk.Frame(self.root)
        frame_formulario.pack(pady=10)

        # Campos del formulario
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

        # Frame para filtros
        frame_filtros = tk.Frame(self.root)
        frame_filtros.pack(pady=10, fill=tk.X)

        # Filtro por paciente
        tk.Label(frame_filtros, text="Filtrar por paciente:").grid(row=0, column=0, padx=5)
        opciones_pacientes = ["Todos"] + [f"{p.id_paciente} - {p.get_nombre_completo()}"
                                          for p in self.gestor_pacientes.listar_pacientes()]
        self.combo_filtro_paciente = ttk.Combobox(
            frame_filtros,
            values=opciones_pacientes,
            state="readonly"
        )
        self.combo_filtro_paciente.grid(row=0, column=1, padx=5)
        self.combo_filtro_paciente.set("Todos")
        self.combo_filtro_paciente.bind("<<ComboboxSelected>>", self.aplicar_filtros)

        # Filtro por médico
        tk.Label(frame_filtros, text="Filtrar por médico:").grid(row=0, column=2, padx=5)
        opciones_medicos = ["Todos"] + [f"{m.id_medico} - {m.get_nombre_completo()}"
                                        for m in self.gestor_medicos.listar_medicos()]
        self.combo_filtro_medico = ttk.Combobox(
            frame_filtros,
            values=opciones_medicos,
            state="readonly"
        )
        self.combo_filtro_medico.grid(row=0, column=3, padx=5)
        self.combo_filtro_medico.set("Todos")
        self.combo_filtro_medico.bind("<<ComboboxSelected>>", self.aplicar_filtros)

        # Asegurarse que los combobox de filtros están habilitados inicialmente
        self.combo_filtro_paciente.config(state="readonly")
        self.combo_filtro_medico.config(state="readonly")

        # Botón para limpiar filtros
        btn_limpiar = tk.Button(frame_filtros, text="Limpiar filtros", command=self.limpiar_filtros)
        btn_limpiar.grid(row=0, column=4, padx=5)

        # Frame para la lista de citas
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

    def mostrar_formulario_diagnostico(self):
        """
        Muestra el formulario para gestionar diagnósticos médicos.

        Permite seleccionar un médico, ver citas pendientes y registrar diagnósticos, tratamiento y observaciones.
        """
        self.limpiar_pantalla()

        lbl_titulo = tk.Label(self.root, text="Gestión de Diagnósticos", font=("Arial", 14))
        lbl_titulo.pack(pady=10)

        # Frame principal con scroll
        frame_principal = tk.Frame(self.root)
        frame_principal.pack(fill="both", expand=True)

        canvas = tk.Canvas(frame_principal)
        scrollbar = ttk.Scrollbar(frame_principal, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Selección de médico
        frame_medico = tk.Frame(scrollable_frame)
        frame_medico.pack(pady=10, fill="x")

        tk.Label(frame_medico, text="Selecciona el médico que realizará el diagnóstico:").pack(side="left", padx=5)

        medicos = [f"{m.id_medico} - {m.get_nombre_completo()}" for m in self.gestor_medicos.listar_medicos()]
        self.combo_medico_diag = ttk.Combobox(frame_medico, values=medicos, state="readonly")
        self.combo_medico_diag.pack(side="left", padx=5, fill="x", expand=True)
        self.combo_medico_diag.bind("<<ComboboxSelected>>", self.actualizar_citas_pendientes)

        # Tabla de citas pendientes
        frame_tabla = tk.Frame(scrollable_frame)
        frame_tabla.pack(pady=10, fill="both", expand=True)

        lbl_tabla = tk.Label(frame_tabla, text="Citas pendientes para diagnóstico")
        lbl_tabla.pack()

        self.tree_citas = ttk.Treeview(frame_tabla, columns=("ID", "Fecha", "Hora", "Paciente"), show="headings")
        self.tree_citas.heading("ID", text="ID Cita")
        self.tree_citas.heading("Fecha", text="Fecha")
        self.tree_citas.heading("Hora", text="Hora")
        self.tree_citas.heading("Paciente", text="Paciente")
        self.tree_citas.pack(fill="both", expand=True)

        # Formulario de diagnóstico
        frame_formulario = tk.Frame(scrollable_frame)
        frame_formulario.pack(pady=10, fill="x")

        tk.Label(frame_formulario, text="Descripción:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.entry_descripcion = tk.Text(frame_formulario, height=5, width=50)
        self.entry_descripcion.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_formulario, text="Tratamiento:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.entry_tratamiento = tk.Text(frame_formulario, height=5, width=50)
        self.entry_tratamiento.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_formulario, text="Observaciones:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.entry_observaciones = tk.Text(frame_formulario, height=5, width=50)
        self.entry_observaciones.grid(row=2, column=1, padx=5, pady=5)

        # Botones
        frame_botones = tk.Frame(scrollable_frame)
        frame_botones.pack(pady=10)

        btn_guardar = tk.Button(frame_botones, text="Guardar Diagnóstico", command=self.guardar_diagnostico)
        btn_guardar.pack(side="left", padx=5)

        btn_regresar = tk.Button(frame_botones, text="Regresar", command=self.crear_menu_principal)
        btn_regresar.pack(side="left", padx=5)

        # Inicializar con médico seleccionado si hay solo uno
        if len(medicos) == 1:
            self.combo_medico_diag.set(medicos[0])
            self.actualizar_citas_pendientes()

    def actualizar_citas_pendientes(self, event=None):
        """
        Actualiza la lista de citas pendientes del médico seleccionado en la interfaz.
        """
        # Limpiar tabla
        for item in self.tree_citas.get_children():
            self.tree_citas.delete(item)

        # Obtener médico seleccionado
        medico_sel = self.combo_medico_diag.get()
        if not medico_sel:
            return

        id_medico = medico_sel.split(" - ")[0]

        # Obtener citas pendientes del médico
        citas_medico = [c for c in self.gestor_citas.listar_citas()
                        if c.medico.id_medico == id_medico and c.estado == "pendiente"]

        # Llenar tabla
        for cita in citas_medico:
            self.tree_citas.insert("", "end", values=(
                cita.id_cita,
                cita.fecha,
                cita.hora,
                cita.paciente.get_nombre_completo()
            ))

    def guardar_diagnostico(self):
        """
        Guarda el diagnóstico, tratamiento y observaciones de una cita médica seleccionada.
        """
        try:
            # Validar selección de cita
            seleccion = self.tree_citas.selection()
            if not seleccion:
                messagebox.showerror("Error", "Seleccione una cita de la tabla")
                return

            item = self.tree_citas.item(seleccion[0])
            id_cita = item['values'][0]
            cita = self.gestor_citas.buscar_cita(id_cita)

            # Validar campos del formulario
            descripcion = self.entry_descripcion.get("1.0", tk.END).strip()
            tratamiento = self.entry_tratamiento.get("1.0", tk.END).strip()
            observaciones = self.entry_observaciones.get("1.0", tk.END).strip()

            if not descripcion:
                messagebox.showerror("Error", "La descripción es obligatoria")
                return

            # Registrar el diagnóstico
            if self.gestor_diagnosticos.registrar_diagnostico(
                    descripcion=descripcion,
                    tratamiento=tratamiento,
                    observaciones=observaciones,
                    cita=cita
            ):
                messagebox.showinfo("Éxito", "Diagnóstico registrado correctamente")
                self.actualizar_citas_pendientes()
                # Limpiar formulario
                self.entry_descripcion.delete("1.0", tk.END)
                self.entry_tratamiento.delete("1.0", tk.END)
                self.entry_observaciones.delete("1.0", tk.END)
            else:
                messagebox.showerror("Error", "No se pudo registrar el diagnóstico")

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al guardar: {str(e)}")

    def actualizar_lista_citas(self):
        """
        Actualiza la lista de citas según los filtros aplicados (paciente y/o médico).
        """
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Obtener filtros
        filtro_paciente = self.combo_filtro_paciente.get().split(" - ")[
            0] if self.combo_filtro_paciente.get() != "Todos" else None
        filtro_medico = self.combo_filtro_medico.get().split(" - ")[
            0] if self.combo_filtro_medico.get() != "Todos" else None

        # Aplicar filtros
        citas_filtradas = []
        for cita in self.gestor_citas.listar_citas():
            cumple_paciente = (filtro_paciente is None) or (cita.paciente.id_paciente == filtro_paciente)
            cumple_medico = (filtro_medico is None) or (cita.medico.id_medico == filtro_medico)

            if cumple_paciente and cumple_medico:
                citas_filtradas.append(cita)

        # Llenar tabla con citas filtradas
        for cita in citas_filtradas:
            self.tree.insert("", "end", values=(
                cita.id_cita,
                cita.fecha,
                cita.hora,
                cita.paciente.get_nombre_completo(),
                cita.medico.get_nombre_completo(),
                cita.estado
            ))

    def on_cita_seleccionada(self, event):
        """
        Maneja la selección de una cita y carga los datos en el formulario de modificación.
        """
        seleccion = self.tree.selection()
        if seleccion:
            item = self.tree.item(seleccion[0])
            id_cita = item['values'][0]
            self.cita_seleccionada = self.gestor_citas.buscar_cita(id_cita)

            # Habilitar botones de modificar/cancelar
            self.btn_cancelar_cita.config(state=tk.NORMAL)
            self.btn_modificar.config(state=tk.NORMAL)

            # Cargar datos en el formulario
            self.entry_fecha.delete(0, tk.END)
            self.entry_fecha.insert(0, self.cita_seleccionada.fecha)
            self.entry_hora.delete(0, tk.END)
            self.entry_hora.insert(0, self.cita_seleccionada.hora)

            # Seleccionar paciente/médico en los combobox
            self.combo_paciente.set(
                f"{self.cita_seleccionada.paciente.id_paciente} - {self.cita_seleccionada.paciente.get_nombre_completo()}")
            self.combo_medico.set(
                f"{self.cita_seleccionada.medico.id_medico} - {self.cita_seleccionada.medico.get_nombre_completo()}")

            # Deshabilitar selección de pacientes y médicos
            self.combo_medico.config(state=tk.DISABLED)
            self.combo_paciente.config(state=tk.DISABLED)


    def guardar_cita(self):
        """
        Guarda una nueva cita médica con los datos proporcionados.
        """
        try:
            id_paciente = self.combo_paciente.get().split(" - ")[0]
            id_medico = self.combo_medico.get().split(" - ")[0]

            paciente = self.gestor_pacientes.buscar_paciente(id_paciente)
            medico = self.gestor_medicos.buscar_medico(id_medico)

            if not paciente or not medico:
                raise ValueError("Paciente o médico no encontrado")

            fecha = self.entry_fecha.get()
            hora = self.entry_hora.get()

            if not self.gestor_citas.agendar_cita(fecha,hora, paciente, medico):
                messagebox.showerror("Error", "Datos inválidos. Verifique:"
                                              "\n- Fecha posterior a hoy (DD/MM/AAAA)"
                                              "\n- Hora en formato HH:MM")
            else:
                messagebox.showinfo("Éxito", "Cita agendada")
                self.actualizar_lista_citas()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agendar la cita: {e}")

    def cancelar_cita(self):
        """
        Cancela una cita médica seleccionada.
        """
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
        """
        Modifica la fecha y hora de una cita médica seleccionada.
        """
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
        """
        Limpia los campos del formulario de cita.
        """
        self.entry_fecha.delete(0, tk.END)
        self.entry_hora.delete(0, tk.END)
        self.combo_paciente.set('')
        self.combo_medico.set('')
        self.cita_seleccionada = None
        self.btn_cancelar_cita.config(state=tk.DISABLED)
        self.btn_modificar.config(state=tk.DISABLED)

    def mostrar_reportes(self):
        """
        Muestra los reportes y estadísticas del sistema (consultas por especialidad, médico más solicitado, etc.).
        """
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
        lbl_medico = tk.Label(frame_reportes, text="Médico más Solicitado", font=("Arial", 12))
        lbl_medico.pack(pady=(10, 0))

        medico_solicitado, num_citas_medico = self.gestor_estadisticas.medico_mas_solicitado(
            self.gestor_medicos, self.gestor_citas
        )
        if medico_solicitado :
            lbl_info_medico = tk.Label(frame_reportes,
                                       text=f"{medico_solicitado.get_nombre_completo()} ({num_citas_medico} citas) - {medico_solicitado.especialidad.nombre}")
            lbl_info_medico.pack()
        else:
            lbl_info_medico = tk.Label(frame_reportes, text="No hay datos suficientes de médicos")
            lbl_info_medico.pack()

        # Paciente con más citas
        lbl_paciente_mas_citas = tk.Label(frame_reportes, text="Paciente frecuente", font=("Arial", 12))
        lbl_paciente_mas_citas.pack(pady=(10, 0))

        paciente_mas_citas, num_citas_paciente = self.gestor_estadisticas.paciente_con_mas_citas(
            self.gestor_pacientes, self.gestor_citas
        )
        if paciente_mas_citas:
            lbl_info_paciente = tk.Label(frame_reportes,
                                         text=f"{paciente_mas_citas.get_nombre_completo()} ({num_citas_paciente} citas)")
            lbl_info_paciente.pack()
        else:
            lbl_info_paciente = tk.Label(frame_reportes, text="No hay datos suficientes de pacientes")
            lbl_info_paciente.pack()

        # Promedio de atención mensual
        lbl_promedio = tk.Label(frame_reportes, text="Promedio de Atención Mensual", font=("Arial", 12))
        lbl_promedio.pack(pady=(10, 0))

        promedio = self.gestor_estadisticas.promedio_atencion_mensual(self.gestor_citas)
        lbl_promedio_valor = tk.Label(frame_reportes, text=f"{promedio:.2f} consultas por mes")
        lbl_promedio_valor.pack()

        # Botón de regreso
        btn_regresar = tk.Button(self.root, text="Regresar", command=self.crear_menu_principal)
        btn_regresar.pack(pady=10)

    def aplicar_filtros(self, event=None):
        """
        Aplica los filtros de paciente y médico a la lista de citas.
        """
        # Determinar qué combobox disparó el evento
        widget_disparador = event.widget if event else None

        # Si se modificó el filtro de paciente
        if widget_disparador == self.combo_filtro_paciente:
            # Deshabilitar el filtro de médico si se seleccionó un paciente específico
            if self.combo_filtro_paciente.get() != "Todos":
                self.combo_filtro_medico.set("Todos")
                self.combo_filtro_medico.config(state=tk.DISABLED)
            else:
                self.combo_filtro_medico.config(state="readonly")

        # Si se modificó el filtro de médico
        elif widget_disparador == self.combo_filtro_medico:
            # Deshabilitar el filtro de paciente si se seleccionó un médico específico
            if self.combo_filtro_medico.get() != "Todos":
                self.combo_filtro_paciente.set("Todos")
                self.combo_filtro_paciente.config(state=tk.DISABLED)
            else:
                self.combo_filtro_paciente.config(state="readonly")

        # Actualizar lista con filtros
        self.actualizar_lista_citas()

    def limpiar_filtros(self):
        """
        Limpia los filtros aplicados y muestra todas las citas.
        """
        self.combo_filtro_paciente.set("Todos")
        self.combo_filtro_medico.set("Todos")
        # Habilitar ambos combobox
        self.combo_filtro_paciente.config(state="readonly")
        self.combo_filtro_medico.config(state="readonly")
        self.actualizar_lista_citas()

    def mostrar_formulario_especialidades(self):
        """
        Muestra el formulario de gestión de especialidades (agregar, eliminar, listar).
        """
        self.limpiar_pantalla()

        lbl_titulo = tk.Label(self.root, text="Gestión de Especialidades", font=("Arial", 14))
        lbl_titulo.pack(pady=10)

        frame_formulario = tk.Frame(self.root)
        frame_formulario.pack(pady=10)

        # Campos del formulario
        tk.Label(frame_formulario, text="Nombre:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        entry_nombre = tk.Entry(frame_formulario)
        entry_nombre.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_formulario, text="Descripción:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        entry_desc = tk.Entry(frame_formulario)
        entry_desc.grid(row=1, column=1, padx=5, pady=5)

        frame_botones = tk.Frame(self.root)
        frame_botones.pack(pady=10)

        def guardar_especialidad():
            """Guarda una nueva especialidad."""
            nombre = entry_nombre.get()
            desc = entry_desc.get()
            if nombre and desc:
                if self.gestor_especialidades.agregar_especialidad(nombre, desc):
                    messagebox.showinfo("Éxito", "Especialidad agregada")
                    actualizar_lista()
                    entry_nombre.delete(0, tk.END)
                    entry_desc.delete(0, tk.END)
                else:
                    messagebox.showerror("Error", "La especialidad ya existe")
            else:
                messagebox.showerror("Error", "Complete todos los campos")

        btn_guardar = tk.Button(frame_botones, text="Guardar", command=guardar_especialidad)
        btn_guardar.grid(row=0, column=0, padx=5)

        def eliminar_seleccionada():
            """Elimina la especialidad seleccionada."""
            seleccion = tree.selection()
            if seleccion:
                item = tree.item(seleccion[0])
                nombre = item['values'][0]
                if self.gestor_especialidades.eliminar_especialidad(nombre):
                    messagebox.showinfo("Éxito", "Especialidad eliminada")
                    actualizar_lista()
                else:
                    messagebox.showerror("Error", "No se pudo eliminar")

        btn_eliminar = tk.Button(frame_botones, text="Eliminar", command=eliminar_seleccionada)
        btn_eliminar.grid(row=0, column=1, padx=5)

        btn_regresar = tk.Button(frame_botones, text="Regresar", command=self.crear_menu_principal)
        btn_regresar.grid(row=0, column=2, padx=5)

        # Lista de especialidades
        frame_lista = tk.Frame(self.root)
        frame_lista.pack(pady=10, fill="both", expand=True)

        lbl_lista = tk.Label(frame_lista, text="Especialidades Registradas")
        lbl_lista.pack()

        tree = ttk.Treeview(frame_lista, columns=("Nombre", "Descripción"), show="headings")
        tree.heading("Nombre", text="Nombre")
        tree.heading("Descripción", text="Descripción")
        tree.pack(fill="both", expand=True)

        def actualizar_lista():
            """Actualiza la lista de especialidades."""
            tree.delete(*tree.get_children())
            for esp in self.gestor_especialidades.listar_especialidades():
                tree.insert("", "end", values=(esp.nombre, esp.descripcion))

        actualizar_lista()

    def mostrar_lista_diagnosticos(self):
        """
        Muestra un listado de todos los diagnósticos registrados.
        """
        self.limpiar_pantalla()

        lbl_titulo = tk.Label(self.root, text="Listado de Diagnósticos", font=("Arial", 14))
        lbl_titulo.pack(pady=10)

        # Frame principal con scroll
        frame_principal = tk.Frame(self.root)
        frame_principal.pack(fill="both", expand=True)

        canvas = tk.Canvas(frame_principal)
        scrollbar = ttk.Scrollbar(frame_principal, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Tabla de diagnósticos
        frame_tabla = tk.Frame(scrollable_frame)
        frame_tabla.pack(pady=10, fill="both", expand=True)

        # Crear Treeview con scroll
        frame_tree = tk.Frame(frame_tabla)
        frame_tree.pack(fill="both", expand=True)

        scroll_y = ttk.Scrollbar(frame_tree)
        scroll_y.pack(side="right", fill="y")

        tree = ttk.Treeview(
            frame_tree,
            columns=("ID Diagnóstico", "ID Cita", "Paciente", "Médico", "Descripción", "Tratamiento", "Observaciones"),
            show="headings",
            yscrollcommand=scroll_y.set,
            height=15
        )
        scroll_y.config(command=tree.yview)

        # Configurar columnas
        tree.heading("ID Diagnóstico", text="ID Diagnóstico")
        tree.heading("ID Cita", text="ID Cita")
        tree.heading("Paciente", text="Paciente")
        tree.heading("Médico", text="Médico")
        tree.heading("Descripción", text="Descripción")
        tree.heading("Tratamiento", text="Tratamiento")
        tree.heading("Observaciones", text="Observaciones")

        tree.column("ID Diagnóstico", width=100, anchor="w")
        tree.column("ID Cita", width=80, anchor="w")
        tree.column("Paciente", width=120, anchor="w")
        tree.column("Médico", width=120, anchor="w")
        tree.column("Descripción", width=200, anchor="w")
        tree.column("Tratamiento", width=200, anchor="w")
        tree.column("Observaciones", width=200, anchor="w")

        tree.pack(fill="both", expand=True)

        # Obtener y mostrar datos
        diagnosticos = self.gestor_diagnosticos.obtener_diagnosticos_completos()
        for diag in diagnosticos:
            tree.insert("", "end", values=(
                diag['id_diagnostico'],
                diag['id_cita'],
                diag['paciente'],
                diag['medico'],
                diag['descripcion'],
                diag['tratamiento'],
                diag['observaciones']
            ))

        # Botones
        frame_botones = tk.Frame(scrollable_frame)
        frame_botones.pack(pady=10)

        btn_regresar = tk.Button(frame_botones, text="Regresar", command=self.crear_menu_principal)
        btn_regresar.pack()

    def ejecutar(self):
        """
        Inicia la aplicación y muestra la ventana principal.
        """
        self.root.mainloop()