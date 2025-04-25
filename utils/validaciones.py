import re
import json
from typing import Dict, Any
from datetime import datetime, timedelta

def validar_fecha_citas(fecha: str) -> bool:
    """
    Valida que la fecha:
     - Tenga formato DD/MM/AAAA
     - Sea posterior al día actual
     - No sea mayor a 1 año a partir de la fecha actual

     Args:
         fecha (str): Fecha a validar en formato DD/MM/AAAA

     Returns:
         bool: True si la fecha es válida, False si no cumple los requisitos
     """
    try:
        # Convertir la fecha ingresada a objeto datetime
        fecha_ingresada = datetime.strptime(fecha, "%d/%m/%Y")

        # Obtener fecha actual y fecha límite (1 año después)
        hoy = datetime.now()
        limite_maximo = hoy + timedelta(days=365)

        # Validar rango
        return hoy < fecha_ingresada <= limite_maximo

    except ValueError:
        return False  # Formato inválido

def validar_fecha_paciente(fecha: str) -> bool:
    """
    Valida que la fecha de nacimiento del paciente::
        - Tenga formato DD/MM/AAAA
        - Sea previa o igual al día actual
        - No sea mayor a 200 años en el pasado

        Args:
            fecha (str): Fecha a validar en formato DD/MM/AAAA

        Returns:
            bool: True si la fecha es válida, False si no cumple los requisitos
    """
    try:
        fecha_ingresada = datetime.strptime(fecha, "%d/%m/%Y").date()
        hoy = datetime.now().date()

        # Calcula la fecha mínima permitida (200 años antes de hoy)
        fecha_minima = hoy.replace(year=hoy.year - 200)

        return fecha_minima <= fecha_ingresada <= hoy

    except ValueError:
        return False  # Formato inválido o fecha imposible (ej: 29/02 en año no bisiesto)

def validar_fecha_medico(fecha: str) -> bool:
    """
    Valida que la fecha de nacimiento del médico:
         - Tenga formato DD/MM/AAAA
         - Indique una edad entre 25 y 70 años
         - Sea una fecha válida y real

         Args:
             fecha (str): Fecha de nacimiento en formato DD/MM/AAAA

         Returns:
             bool: True si la fecha es válida, False si no cumple los requisitos
     """
    try:
        fecha_nacimiento = datetime.strptime(fecha, "%d/%m/%Y").date()
        hoy = datetime.now().date()

        # Calcular edad exacta considerando mes y día
        edad = hoy.year - fecha_nacimiento.year - (
                    (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))

        return 25 <= edad <= 70

    except ValueError:
        return False  # Formato inválido o fecha imposible

def validar_telefono(telefono: str) -> bool:
    """
    Valida que el número de teléfono tenga 10 dígitos y pueda comenzar con '+' opcionalmente.

      Args:
          telefono (str): Número de teléfono a validar.

      Returns:
          bool: True si el formato es válido, False en caso contrario.
    """
    return re.match(r'^(\+?\d{10})$', telefono) is not None

def validar_nombre(nombre: str) -> bool:
    """
    Valida que el nombre contenga solo letras y espacios, con al menos 2 caracteres.

        Args:
            nombre (str): Nombre a validar.

        Returns:
            bool: True si el nombre es válido, False en caso contrario.
    """
    return re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]{2,}$', nombre) is not None

def validar_hora(hora: str) -> bool:
    """
    Valida que la hora esté en formato HH:MM y que los valores estén en un rango válido.

       Args:
           hora (str): Hora en formato HH:MM (24 horas).

       Returns:
           bool: True si la hora es válida, False en caso contrario.
    """
    if not re.match(r'^\d{2}:\d{2}$', hora):
        return False

    # Validación adicional de rangos (opcional)
    horas, minutos = map(int, hora.split(':'))
    if not (0 <= horas < 24 and 0 <= minutos < 60):
        return False

    return True

def validar_persona_duplicado(file_path: str, nueva_persona: Dict) -> bool:
    """
    Verifica si ya existe una persona con los mismos datos en el archivo JSON.

        Args:
            file_path (str): Ruta al archivo JSON que contiene la lista de personas.
            nueva_persona (Dict): Diccionario con los datos de la nueva persona. Debe incluir las claves:
                - 'nombre' (str)
                - 'apellido' (str)
                - 'fecha_nacimiento' (str en formato DD/MM/AAAA)
                - 'telefono' (str)

        Returns:
            bool: True si se encuentra un duplicado exacto, False si es único.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            personas = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return False  # No hay duplicados si el archivo no existe o está vacío

    campos_clave = ['nombre', 'apellido', 'fecha_nacimiento', 'telefono']

    for persona in personas:
        if all(str(persona.get(campo)).strip().lower() == str(nueva_persona.get(campo)).strip().lower()
               for campo in campos_clave):
            return True  # Encontró un duplicado exacto

    return False

def generar_id(prefijo: str, ultimo_id: str) -> str:
    """
    Genera un nuevo ID autoincremental basado en el último ID registrado y un prefijo.

        Args:
            prefijo (str): Prefijo del ID (por ejemplo, 'MED', 'PAC').
            ultimo_id (str): Último ID generado (por ejemplo, 'MED012').

        Returns:
            str: Nuevo ID autoincrementado (por ejemplo, 'MED013').
    """
    if not ultimo_id:
        return f"{prefijo}001"

    numero = int(ultimo_id.replace(prefijo, ""))
    return f"{prefijo}{numero + 1:03d}"
