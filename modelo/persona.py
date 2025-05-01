class Persona:
    """
    Clase base que representa a una persona con información básica.

        Attributes:
            nombre (str): Nombre de la persona.
            apellido (str): Apellido de la persona.
            fecha_nacimiento (str): Fecha de nacimiento en formato DD/MM/AAAA.
            telefono (str): Número de teléfono de contacto.
    """

    def __init__(self, nombre: str, apellido: str, fecha_nacimiento: str, telefono: str):
        """
        Inicializa una nueva instancia de Persona.

            Args:
                nombre (str): Nombre de la persona.
                apellido (str): Apellido de la persona.
                fecha_nacimiento (str): Fecha de nacimiento en formato DD/MM/AAAA.
                telefono (str): Número de teléfono de contacto.
        """
        self._nombre = nombre
        self._apellido = apellido
        self._fecha_nacimiento = fecha_nacimiento
        self._telefono = telefono

    def get_nombre_completo(self) -> str:
        """
        Obtiene el nombre completo de la persona.

            Returns:
                str: Nombre completo en formato 'Apellido, Nombre'.
        """
        return f"{self._apellido}, {self._nombre}"

    def nombre(self) -> str:
        """
        str: Devuelve el nombre de la persona.
        """
        return self._nombre

    def apellido(self) -> str:
        """
        str: Devuelve el apellido de la persona.
        """
        return self._apellido

    def fecha_nacimiento(self) -> str:
        """
        str: Devuelve la fecha de nacimiento de la persona.
        """
        return self._fecha_nacimiento

    def telefono(self) -> str:
        """
        str: Devuelve el número de teléfono de la persona.
        """
        return self._telefono