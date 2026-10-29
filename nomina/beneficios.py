from abc import ABC, abstractmethod
from nomina.constantes import BONO_ALIMENTACION_MONTO, PORCENTAJE_FONDO_AHORRO


class Beneficio(ABC):
    """Clase abstracta para beneficios corporativos."""

    @abstractmethod
    def calcular(self, salario_bruto: float) -> float:
        pass


class BonoAlimentacion(Beneficio):
    """Bono mensual fijo cubierto por la empresa ($1.000.000)."""

    def calcular(self, salario_bruto: float) -> float:
        return BONO_ALIMENTACION_MONTO


class FondoAhorro(Beneficio):
    """Aporte al fondo de ahorro (2% del salario bruto)."""

    def calcular(self, salario_bruto: float) -> float:
        return salario_bruto * PORCENTAJE_FONDO_AHORRO