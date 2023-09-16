from unittest import TestCase, main

from crdlib.properties.units import Dimension, TemperatureUnit
from crdlib.properties.properties import Temperature


class TestTemperature(TestCase):
    def test_to_unit_C_to_K(self):
        C = Temperature(0, TemperatureUnit.CELCIUS)
        K = C.to_unit(TemperatureUnit.KELVIN)
        self.assertEqual(K.value, 273.15)

    def test_to_unit_K_to_R(self):
        K = Temperature(1000, TemperatureUnit.KELVIN)
        R = K.to_unit(TemperatureUnit.RANKINE)
        self.assertEqual(R.value, 1800)

    def test_from_physical_property(self):
        K = Temperature(500, TemperatureUnit.KELVIN)
        F = Temperature.from_physical_property(K, TemperatureUnit.FAHRENHEIT)
        self.assertAlmostEqual(F.value, (500 - 273.15) * 1.8 + 32, 2)


if __name__ == "__main__":
    main()
