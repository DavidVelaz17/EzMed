
# EzMed

**EzMed** es una aplicación de escritorio para la gestión de consultas médicas generales en clínicas pequeñas o medianas. Permite llevar un control eficiente de pacientes, médicos y citas médicas mediante una interfaz amigable y un diseño modular basado en programación orientada a objetos en Python.

## Características

- Gestión de pacientes (alta, edición, búsqueda).
- Registro y administración de médicos.
- Agendamiento y visualización de citas médicas.
- Registro de diagnósticos, tratamientos y observaciones por parte del médico tratante
- Incorpora funcionalidades estadísticas como número de consultas por especialidad, médico más solicitado, o promedio de atencion mensual
- Diseño modular siguiendo el patrón MVC.
- Persistencia de datos usando archivos JSON.
- Interfaz gráfica desarrollada con Tkinter.

## Tecnologías utilizadas

- Python 3.x
- Tkinter (para GUI)
- JSON (para almacenamiento de datos)
- PEP 8 (buenas prácticas y estilo de código)

## Estructura del proyecto

```
EzMed/
├── modelo/                 
│   ├── cita.py             
│   ├── diagnostico.py      
│   ├── especialidad.py    
│   ├── medico.py           
│   ├── paciente.py        
│   └── persona.py          
├── vista/
│   ├── gui.py         
├── controlador/
│   ├── gestor_citas.py
│   ├── gestor_pacientes.py
│   ├── gestor_medicos.py
│   ├── gestor_diagnosticos.py
│   ├── gestor_estadisticas.py
│   ├── gestor_especialidades.py
├── datos/
│   ├── pacientes.json
│   ├── medicos.json
│   ├── citas.json
│   ├── especialidades.json
│   ├── diagnosticos.json
├── utils/                  
│   └── validaciones.py     
├── main.py
└── README.md
```

## Instalación

### 1. Clona el repositorio:

```bash
    git clone https://github.com/DavidVelaz17/EzMed.git
    cd EzMed
```

### 2. Ejecuta la aplicación:

```bash
    python main.py
```
## Documentación
El sistema utiliza docstrings completos para documentación. Ejemplo:
```
class Cita:
    """Representa una cita médica en el sistema.
    
    Attributes:
        id_cita (str): Identificador único
        fecha (str): DD/MM/AAAA
        hora (str): HH:MM
        estado (str): ['pendiente','completada','cancelada']
        paciente (Paciente): Paciente asociado
        medico (Medico): Médico asignado
    
    Methods:
        cancelar(): Marca cita como cancelada
        completar(): Marca cita como completada
        reagendar(nueva_fecha, nueva_hora): Cambia fecha/hora
    """
```
## Requisitos

- Python 3.7 o superior

## Contribuciones

Las contribuciones son bienvenidas. Si deseas colaborar, abre un issue o haz un pull request con tus mejoras.


Desarrollado por David Gustavo Lara Velázquez
