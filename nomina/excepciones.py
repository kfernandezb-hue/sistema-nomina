class NominaError(Exception):
    """Excepción base para errores del sistema de nómina."""
    pass

class DatoInvalidoError(NominaError):
    """Se lanza cuando los datos de entrada no son válidos (ej. horas < 0)."""
    pass

class SalarioNetoNegativoError(NominaError):
    """Se lanza cuando la liquidación da como resultado un neto menor a 0."""
    pass