from typing import List
from nomina.empleados import Empleado
from nomina.liquidacion import Liquidacion


class ServicioNomina:
    """Servicio encargado de procesar la nómina de todos los empleados."""

    def __init__(self):
        self._empleados: List[Empleado] = []

    def agregar_empleado(self, empleado: Empleado) -> None:
        self._empleados.append(empleado)

    def liquidar_todos(self) -> List[Liquidacion]:
        return [emp.liquidar() for emp in self._empleados]

    def total_salarios_netos(self) -> float:
        return sum(liq.salario_neto for liq in self.liquidar_todos())

    def costo_total_empresa(self) -> float:
        return sum(
            liq.salario_bruto + liq.beneficios_totales
            for liq in self.liquidar_todos()
        )