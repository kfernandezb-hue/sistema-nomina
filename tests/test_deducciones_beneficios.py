import unittest
from nomina.beneficios import BonoAlimentacion, FondoAhorro
from nomina.deducciones import Arl, PensionSeguroSocial


class TestDeduccionesBeneficios(unittest.TestCase):

    def test_pension_seguro_social(self):
        deduccion = PensionSeguroSocial()
        self.assertAlmostEqual(deduccion.calcular(2_000_000), 80_000)

    def test_arl_por_defecto(self):
        arl = Arl()
        self.assertAlmostEqual(arl.calcular(1_000_000), 5_220)

    def test_bono_alimentacion(self):
        bono = BonoAlimentacion()
        self.assertEqual(bono.calcular(3_000_000), 1_000_000)

    def test_fondo_ahorro(self):
        fondo = FondoAhorro()
        self.assertAlmostEqual(fondo.calcular(1_000_000), 20_000)


if __name__ == "__main__":
    unittest.main()