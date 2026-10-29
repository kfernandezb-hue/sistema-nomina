from abc import ABC, abstractmethod
from nomina.constantes import PORCENTAJE_SEGURO_SOCIAL_PENSION, TASA_ARL_RIESGO_1


class Deduccion(ABC):
    """Clase abstracta para cualquier deducción sobre el salario."""

    @abstractmethod
    def calcular(self, salario_bruto: float) -> float:
        pass


class PensionSeguroSocial(Deduccion):
    """Deducción obligatoria de Salud/Pensión (4% del bruto)."""

    def calcular(self, salario_bruto: float) -> float:
        return salario_bruto * PORCENTAJE_SEGURO_SOCIAL_PENSION


class Arl(Deduccion):
    """Deducción por riesgos laborales (ARL)."""

    def __init__(self, tasa: float = TASA_ARL_RIESGO_1):
        self.tasa = tasa

    def calcular(self, salario_bruto: float) -> float:
        return salario_bruto * self.tasa