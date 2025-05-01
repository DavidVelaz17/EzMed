class Especialidad:
    """
    Clase que representa una especialidad médica en el sistema.

    Una especialidad define el campo médico en el que se desempeña un médico,
    incluyendo su nombre y una descripción detallada.

        Attributes:
            nombre (str): Nombre de la especialidad médica (ej. Cardiología, Pediatría).
            descripcion (str): Breve explicación o detalles de la especialidad.
    """

    def __init__(self, nombre: str, descripcion: str):
        """
        Inicializa una nueva instancia de Especialidad.

            Args:
                nombre (str): Nombre de la especialidad médica.
                descripcion (str): Descripción explicativa de la especialidad.
        """
        self._nombre = nombre
        self._descripcion = descripcion

    def nombre(self) -> str:
        """
        str: Devuelve el nombre de la especialidad médica.
        """
        return self._nombre

    def descripcion(self) -> str:
        """
        str: Devuelve la descripción de la especialidad médica.
        """
        return self._descripcion

    def __str__(self):
        """
       Devuelve una representación legible de la especialidad.

           Returns:
               str: Representación en formato "nombre: descripción".
       """
        return f"{self._nombre}: {self._descripcion}"