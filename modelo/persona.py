class Persona:
    """Clase base que representa a una persona con información básica.

    Attributes:
        nombre (str): Nombre de la persona.
        apellido (str): Apellido de la persona.
        fecha_nacimiento (str): Fecha de nacimiento en formato DD/MM/AAAA.
        telefono (str): Número de teléfono de contacto.
    """

    def __init__(self, nombre: str, apellido: str, fecha_nacimiento: str, telefono: str):
        """Inicializa una nueva instancia de Persona.

        Args:
            nombre: Nombre de la persona.
            apellido: Apellido de la persona.
            fecha_nacimiento: Fecha de nacimiento en formato DD/MM/AAAA.
            telefono: Número de teléfono de contacto.
        """
        self._nombre = nombre
        self._apellido = apellido
        self._fecha_nacimiento = fecha_nacimiento
        self._telefono = telefono

    def get_nombre_completo(self) -> str:
        """Obtiene el nombre completo de la persona.

        Returns:
            str: Nombre completo en formato 'Apellido, Nombre'.
        """
        return f"{self._apellido}, {self._nombre}"

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def apellido(self) -> str:
        return self._apellido

    @property
    def fecha_nacimiento(self) -> str:
        return self._fecha_nacimiento

    @property
    def telefono(self) -> str:
        return self._telefono