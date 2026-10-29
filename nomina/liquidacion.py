from dataclasses import dataclass, field
from typing import List


def formatear_pesos(monto: float) -> str:
    """Formatea un valor numérico a pesos colombianos."""
    return f"${monto:,.0f}".replace(",", ".")


@dataclass
class Liquidacion:
    """Representa el resumen del desprendible de pago de un empleado."""

    empleado_id: str
    empleado_nombre: str
    empleado_tipo: str
    salario_base: float
    bonos: float
    salario_bruto: float
    deducciones_totales: float
    salario_neto: float
    beneficios_totales: float
    detalles_beneficios: List[str] = field(default_factory=list)

    def resumen(self) -> str:
        beneficios_str = (
            ", ".join(self.detalles_beneficios)
            if self.detalles_beneficios
            else "Ninguno"
        )
        return (
            f"--- DESPRENDIBLE DE PAGO ---\n"
            f"ID: {self.empleado_id} | Nombre: {self.empleado_nombre} | Tipo: {self.empleado_tipo}\n"
            f"  Salario Base/Devengado : {formatear_pesos(self.salario_base)}\n"
            f"  Bonos / Extras         : {formatear_pesos(self.bonos)}\n"
            f"  Salario Bruto          : {formatear_pesos(self.salario_bruto)}\n"
            f"  Deducciones (4% + ARL) : {formatear_pesos(self.deducciones_totales)}\n"
            f"  SALARIO NETO A PAGAR   : {formatear_pesos(self.salario_neto)}\n"
            f"  Beneficios (Empresa)   : {formatear_pesos(self.beneficios_totales)} ({beneficios_str})"
        )