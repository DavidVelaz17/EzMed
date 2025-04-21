import re
from datetime import datetime


def validar_fecha(fecha: str) -> bool:
    """Valida que la fecha sea posterior al día actual y tenga formato DD/MM/AAAA"""
    try:
        fecha_ingresada = datetime.strptime(fecha, "%d/%m/%Y")
        return fecha_ingresada > datetime.now()
    except ValueError:
        return False


def validar_telefono(telefono: str) -> bool:
    """Valida formato de teléfono: 10 dígitos, puede empezar con +"""
    return re.match(r'^(\+?\d{10})$', telefono) is not None


def validar_nombre(nombre: str) -> bool:
    """Valida que solo contenga letras y espacios"""
    return re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]{2,}$', nombre) is not None


def generar_id(prefijo: str, ultimo_id: str) -> str:
    """Genera un ID autoincremental con prefijo"""
    if not ultimo_id:
        return f"{prefijo}001"

    numero = int(ultimo_id.replace(prefijo, ""))
    return f"{prefijo}{numero + 1:03d}"