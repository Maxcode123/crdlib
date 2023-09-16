from unittest import TestCase, main

from crdlib.properties.units import (
    Dimension,
    TemperatureUnit,
    PressureUnit,
    LengthUnit,
    MassUnit,
)
from crdlib.exceptions.exceptions import PropertyUnitOperationError


class TestUnits(TestCase):
    def test_primitives_multiplication(self):
        composite = Dimension(TemperatureUnit.CELCIUS) * Dimension(PressureUnit.BAR)
        self.assertEqual(len(composite.numerator), 2)
        self.assertEqual(len(composite.denominator), 0)
        self.assertEqual(str(composite), "°C * bar")

    def test_composite_multiplication(self):
        composite = (
            Dimension(TemperatureUnit.KELVIN)
            * Dimension(PressureUnit.PASCAL)
            * Dimension(MassUnit.GRAM)
        )
        self.assertEqual(len(composite.numerator), 3)
        self.assertEqual(len(composite.denominator), 0)
        self.assertEqual(str(composite), "K * Pa * g")

    def test_primitives_division(self):
        composite = Dimension(MassUnit.KILO_GRAM) / Dimension(LengthUnit.KILO_METER)
        self.assertEqual(len(composite.numerator), 1)
        self.assertEqual(len(composite.denominator), 1)
        self.assertEqual(str(composite), "kg / km")

    def test_composite_division(self):
        composite = (
            Dimension(MassUnit.GRAM)
            / Dimension(PressureUnit.BAR)
            / Dimension(LengthUnit.FOOT)
        )
        self.assertEqual(len(composite.numerator), 1)
        self.assertEqual(len(composite.denominator), 2)
        self.assertEqual(str(composite), "g / bar / ft")

    def test_power(self):
        dimension = Dimension(TemperatureUnit.KELVIN) ** 3
        self.assertEqual(str(dimension), "(K) ^ 3")

    def test_composite_dimension_power_raises(self):
        with self.assertRaises(PropertyUnitOperationError):
            (Dimension(TemperatureUnit.KELVIN) * Dimension(MassUnit.GRAM)) ** 2

    def test_multiple_operations(self):
        composite = (
            Dimension(TemperatureUnit.KELVIN) ** 1.5
            * Dimension(LengthUnit.CENTI_METER)
            / Dimension(MassUnit.GRAM)
            / Dimension(PressureUnit.BAR)
        )
        self.assertEqual(len(composite.numerator), 2)
        self.assertEqual(len(composite.denominator), 2)
        self.assertEqual(str(composite), "(K) ^ 1.5 * cm / g / bar")


if __name__ == "__main__":
    main()
