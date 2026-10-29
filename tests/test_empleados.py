import unittest
from nomina.empleados import (
    EmpleadoAsalariado,
    EmpleadoPorComision,
    EmpleadoPorHoras,
    EmpleadoTemporal,
)
from nomina.excepciones import DatoInvalidoError, SalarioNetoNegativoError


class TestEmpleados(unittest.TestCase):

    def test_asalariado_sin_bono(self):
        emp = EmpleadoAsalariado("Juan", "1", 3_000_000, anios_antiguedad=3)
        liq = emp.liquidar()
        self.assertEqual(liq.salario_base, 3_000_000)
        self.assertEqual(liq.bonos, 0)
        self.assertEqual(liq.salario_bruto, 3_000_000)

    def test_asalariado_con_bono(self):
        emp = EmpleadoAsalariado("Ana", "2", 4_000_000, anios_antiguedad=6)
        liq = emp.liquidar()
        self.assertEqual(liq.bonos, 400_000)
        self.assertEqual(liq.salario_bruto, 4_400_000)

    def test_horas_sin_extras(self):
        emp = EmpleadoPorHoras("Luis", "3", horas_trabajadas=40, tarifa_hora=20_000)
        liq = emp.liquidar()
        self.assertEqual(liq.salario_base, 800_000)
        self.assertEqual(liq.bonos, 0)

    def test_horas_con_extras(self):
        emp = EmpleadoPorHoras("Carlos", "4", horas_trabajadas=48, tarifa_hora=20_000)
        liq = emp.liquidar()
        self.assertEqual(liq.salario_base, 800_000)
        self.assertEqual(liq.bonos, 240_000)

    def test_comision_con_bono(self):
        emp = EmpleadoPorComision("Marta", "5", salario_base=1_500_000, porcentaje_comision=0.05, ventas=25_000_000)
        liq = emp.liquidar()
        self.assertEqual(liq.salario_base, 2_750_000)
        self.assertEqual(liq.bonos, 750_000)

    def test_temporal(self):
        emp = EmpleadoTemporal("Pedro", "6", 2_000_000, duracion_contrato_meses=6)
        liq = emp.liquidar()
        self.assertEqual(liq.bonos, 0)
        self.assertEqual(len(liq.detalles_beneficios), 0)

    def test_validacion_horas_negativas(self):
        with self.assertRaises(DatoInvalidoError):
            EmpleadoPorHoras("Error", "7", horas_trabajadas=-10, tarifa_hora=20_000)


if __name__ == "__main__":
    unittest.main()