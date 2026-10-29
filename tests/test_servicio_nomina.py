import unittest
from nomina import (
    EmpleadoAsalariado,
    EmpleadoPorHoras,
    ServicioNomina,
)


class TestServicioNomina(unittest.TestCase):

    def test_servicio_nomina_calculos_globales(self):
        servicio = ServicioNomina()
        servicio.agregar_empleado(
            EmpleadoAsalariado("Ana Torres", "1001", 4_000_000, anios_antiguedad=0)
        )
        servicio.agregar_empleado(
            EmpleadoPorHoras("Luis Perez", "1002", horas_trabajadas=40, tarifa_hora=20_000)
        )

        liquidaciones = servicio.liquidar_todos()
        self.assertEqual(len(liquidaciones), 2)
        self.assertGreater(servicio.total_salarios_netos(), 0)
        self.assertGreater(servicio.costo_total_empresa(), servicio.total_salarios_netos())


if __name__ == "__main__":
    unittest.main()