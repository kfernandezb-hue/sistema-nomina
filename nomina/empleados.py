from abc import ABC, abstractmethod
from typing import List
from nomina.beneficios import Beneficio, BonoAlimentacion, FondoAhorro
from nomina.constantes import (
    ANTIGUEDAD_BONO_ASALARIADO,
    ANTIGUEDAD_FONDO_AHORRO,
    FACTOR_HORA_EXTRA,
    HORAS_ORDINARIAS_MAX,
    PORCENTAJE_BONO_ASALARIADO,
    PORCENTAJE_BONO_COMISION,
    UMBRAL_VENTAS_BONO,
)
from nomina.deducciones import Arl, Deduccion, PensionSeguroSocial
from nomina.excepciones import DatoInvalidoError, SalarioNetoNegativoError
from nomina.liquidacion import Liquidacion


class Empleado(ABC):
    """Clase base abstracta para todos los tipos de empleados."""

    def __init__(self, nombre: str, identificacion: str, deducciones: List[Deduccion] = None):
        self.nombre = nombre
        self.identificacion = identificacion
        self.deducciones = deducciones if deducciones is not None else [PensionSeguroSocial(), Arl()]

    @abstractmethod
    def calcular_salario_base(self) -> float:
        pass

    @abstractmethod
    def calcular_bonos(self) -> float:
        pass

    def _beneficios_aplicables(self) -> List[Beneficio]:
        return []

    def liquidar(self) -> Liquidacion:
        """Aplica el patrón Template Method para generar la liquidación."""
        salario_base = self.calcular_salario_base()
        bonos = self.calcular_bonos()
        salario_bruto = salario_base + bonos

        deducciones_totales = sum(d.calcular(salario_bruto) for d in self.deducciones)
        salario_neto = salario_bruto - deducciones_totales

        if salario_neto < 0:
            raise SalarioNetoNegativoError(
                f"El salario neto para {self.nombre} es negativo ({salario_neto})."
            )

        beneficios = self._beneficios_aplicables()
        beneficios_totales = sum(b.calcular(salario_bruto) for b in beneficios)
        detalles_beneficios = [b.__class__.__name__ for b in beneficios]

        return Liquidacion(
            empleado_id=self.identificacion,
            empleado_nombre=self.nombre,
            empleado_tipo=self.__class__.__name__,
            salario_base=salario_base,
            bonos=bonos,
            salario_bruto=salario_bruto,
            deducciones_totales=deducciones_totales,
            salario_neto=salario_neto,
            beneficios_totales=beneficios_totales,
            detalles_beneficios=detalles_beneficios,
        )

    @staticmethod
    def _validar_no_negativo(valor: float, nombre_campo: str) -> None:
        if valor < 0:
            raise DatoInvalidoError(f"El valor de '{nombre_campo}' no puede ser negativo.")


class EmpleadoAsalariado(Empleado):
    def __init__(self, nombre: str, identificacion: str, salario_fijo: float, anios_antiguedad: int = 0):
        super().__init__(nombre, identificacion)
        self._validar_no_negativo(salario_fijo, "salario_fijo")
        self._validar_no_negativo(anios_antiguedad, "anios_antiguedad")
        self.salario_fijo = salario_fijo
        self.anios_antiguedad = anios_antiguedad

    def calcular_salario_base(self) -> float:
        return self.salario_fijo

    def calcular_bonos(self) -> float:
        if self.anios_antiguedad > ANTIGUEDAD_BONO_ASALARIADO:
            return self.salario_fijo * PORCENTAJE_BONO_ASALARIADO
        return 0.0

    def _beneficios_aplicables(self) -> List[Beneficio]:
        return [BonoAlimentacion()]


class EmpleadoPorHoras(Empleado):
    def __init__(self, nombre: str, identificacion: str, horas_trabajadas: float, tarifa_hora: float, anios_antiguedad: int = 0, acepta_fondo_ahorro: bool = False):
        super().__init__(nombre, identificacion)
        self._validar_no_negativo(horas_trabajadas, "horas_trabajadas")
        self._validar_no_negativo(tarifa_hora, "tarifa_hora")
        self._validar_no_negativo(anios_antiguedad, "anios_antiguedad")
        self.horas_trabajadas = horas_trabajadas
        self.tarifa_hora = tarifa_hora
        self.anios_antiguedad = anios_antiguedad
        self.acepta_fondo_ahorro = acepta_fondo_ahorro

    def calcular_salario_base(self) -> float:
        horas_normales = min(self.horas_trabajadas, HORAS_ORDINARIAS_MAX)
        return horas_normales * self.tarifa_hora

    def calcular_bonos(self) -> float:
        if self.horas_trabajadas > HORAS_ORDINARIAS_MAX:
            horas_extras = self.horas_trabajadas - HORAS_ORDINARIAS_MAX
            return horas_extras * self.tarifa_hora * FACTOR_HORA_EXTRA
        return 0.0

    def _beneficios_aplicables(self) -> List[Beneficio]:
        beneficios = []
        if self.anios_antiguedad > ANTIGUEDAD_FONDO_AHORRO and self.acepta_fondo_ahorro:
            beneficios.append(FondoAhorro())
        return beneficios


class EmpleadoPorComision(Empleado):
    def __init__(self, nombre: str, identificacion: str, salario_base: float, porcentaje_comision: float, ventas: float):
        super().__init__(nombre, identificacion)
        self._validar_no_negativo(salario_base, "salario_base")
        self._validar_no_negativo(porcentaje_comision, "porcentaje_comision")
        self._validar_no_negativo(ventas, "ventas")
        self.salario_base = salario_base
        self.porcentaje_comision = porcentaje_comision
        self.ventas = ventas

    def calcular_salario_base(self) -> float:
        return self.salario_base + (self.ventas * self.porcentaje_comision)

    def calcular_bonos(self) -> float:
        if self.ventas > UMBRAL_VENTAS_BONO:
            return self.ventas * PORCENTAJE_BONO_COMISION
        return 0.0

    def _beneficios_aplicables(self) -> List[Beneficio]:
        return [BonoAlimentacion()]


class EmpleadoTemporal(Empleado):
    def __init__(self, nombre: str, identificacion: str, salario_fijo: float, duracion_contrato_meses: int):
        super().__init__(nombre, identificacion)
        self._validar_no_negativo(salario_fijo, "salario_fijo")
        self._validar_no_negativo(duracion_contrato_meses, "duracion_contrato_meses")
        self.salario_fijo = salario_fijo
        self.duracion_contrato_meses = duracion_contrato_meses

    def calcular_salario_base(self) -> float:
        return self.salario_fijo

    def calcular_bonos(self) -> float:
        return 0.0