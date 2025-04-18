class Especialidad:
    """Clase que representa una especialidad médica en el sistema.

    Attributes:
        nombre (str): Nombre de la especialidad médica.
        descripcion (str): Descripción de la especialidad.
    """

    def __init__(self, nombre: str, descripcion: str):
        """Inicializa una nueva instancia de Especialidad.

        Args:
            nombre: Nombre de la especialidad médica.
            descripcion: Descripción de la especialidad.
        """
        self._nombre = nombre
        self._descripcion = descripcion

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def descripcion(self) -> str:
        return self._descripcion

    def __str__(self):
        return f"{self._nombre}: {self._descripcion}"