from unittest import TestCase, main
from typing import Type

from parameterized import parameterized

from crdlib.properties.units.units import (
    MeasurementUnit,
    TemperatureUnit,
    PressureUnit,
    LengthUnit,
    MassUnit,
)
from crdlib.properties.units.descriptors import (
    Dimension,
    CompositeDimension,
    GenericDimension,
)
from crdlib.properties.exceptions import InvalidUnitDescriptorBinaryOperation


class TestUnitDescriptors(TestCase):
    pass


class TestDimensions(TestUnitDescriptors):
    @staticmethod
    def create(unit: MeasurementUnit) -> Dimension:
        return Dimension(unit)

    def test_eq(self):
        self.assertTrue(
            self.create(TemperatureUnit.KELVIN) == self.create(TemperatureUnit.KELVIN)
        )

    def test_ne(self):
        self.assertFalse(
            self.create(TemperatureUnit.CELCIUS) == self.create(TemperatureUnit.RANKINE)
        )

    def test_composite_eq(self):
        c1 = self.create(TemperatureUnit.KELVIN) * self.create(PressureUnit.BAR)
        c2 = self.create(PressureUnit.BAR) * self.create(TemperatureUnit.KELVIN)
        self.assertTrue(c1 == c2)

    def test_composite_str(self):
        c1 = self.create(TemperatureUnit.KELVIN) * self.create(PressureUnit.BAR)
        c2 = self.create(PressureUnit.BAR) * self.create(TemperatureUnit.KELVIN)
        self.assertEqual(str(c1), str(c2))

    def test_primitives_multiplication(self):
        composite = self.create(TemperatureUnit.CELCIUS) * self.create(PressureUnit.BAR)
        self.assertEqual(len(composite.numerator), 2)
        self.assertEqual(len(composite.denominator), 0)
        self.assertEqual(str(composite), "bar * °C")

    def test_composite_multiplication(self):
        composite = (
            self.create(TemperatureUnit.KELVIN)
            * self.create(PressureUnit.PASCAL)
            * self.create(MassUnit.GRAM)
        )
        self.assertEqual(len(composite.numerator), 3)
        self.assertEqual(len(composite.denominator), 0)
        self.assertEqual(str(composite), "K * Pa * g")

    @parameterized.expand([(None,), (2,), (object()), ("str",), (list(),)])
    def test_multiplication_raises(self, factor):
        with self.assertRaises(InvalidUnitDescriptorBinaryOperation):
            self.create(TemperatureUnit.KELVIN) * factor

    def test_primitives_division(self):
        composite = self.create(MassUnit.KILO_GRAM) / self.create(LengthUnit.KILO_METER)
        self.assertEqual(len(composite.numerator), 1)
        self.assertEqual(len(composite.denominator), 1)
        self.assertEqual(str(composite), "kg / km")

    def test_composite_division(self):
        composite = (
            self.create(MassUnit.GRAM)
            / self.create(PressureUnit.BAR)
            / self.create(LengthUnit.FOOT)
        )
        self.assertEqual(len(composite.numerator), 1)
        self.assertEqual(len(composite.denominator), 2)
        self.assertEqual(str(composite), "g / bar / ft")

    @parameterized.expand([(None,), (1,), ("sad",), (object(),), (list(),)])
    def test_division_raises(self, factor):
        with self.assertRaises(InvalidUnitDescriptorBinaryOperation):
            self.create(MassUnit.KILO_GRAM) / factor

    def test_power(self):
        dimension = self.create(TemperatureUnit.KELVIN) ** 3
        self.assertEqual(str(dimension), "(K) ^ 3")
        self.assertGreaterEqual(dimension.power, 3)

    def test_multiple_operations(self):
        composite = (
            self.create(TemperatureUnit.KELVIN) ** 1.5
            * self.create(LengthUnit.CENTI_METER)
            / self.create(MassUnit.GRAM)
            / self.create(PressureUnit.BAR)
        )
        self.assertEqual(len(composite.numerator), 2)
        self.assertEqual(len(composite.denominator), 2)
        self.assertEqual(str(composite), "(K) ^ 1.5 * cm / bar / g")


class TestUnits(TestDimensions):
    """
    Run tests of `TestDimensions`, but substitute any instance of Dimension with its'
    unit.
    """

    @staticmethod
    def create(unit: MeasurementUnit) -> MeasurementUnit:
        return unit


class TestIsInstance(TestUnitDescriptors):
    @parameterized.expand(
        [
            (LengthUnit.METER, LengthUnit),
            (LengthUnit.FOOT, LengthUnit),
            (TemperatureUnit.CELCIUS, TemperatureUnit),
        ]
    )
    def test_dimension_isinstance(self, unit, unit_type):
        self.assertTrue(Dimension(unit).isinstance(unit_type))

    @parameterized.expand(
        [(LengthUnit.CENTI_METER, PressureUnit), (TemperatureUnit.CELCIUS, MassUnit)]
    )
    def test_dimension_not_isinstance(self, unit, unit_type):
        self.assertFalse(Dimension(unit).isinstance(unit_type))

    def test_composite_dimension_isinstance(self):
        composite = CompositeDimension(
            numerator=[
                Dimension(LengthUnit.CENTI_METER) ** 2,
                Dimension(TemperatureUnit.KELVIN),
            ],
            denominator=[Dimension(MassUnit.GRAM), Dimension(PressureUnit.BAR) ** 3],
        )
        generic = TemperatureUnit * (LengthUnit**2) / MassUnit / (PressureUnit**3)
        self.assertTrue(composite.isinstance(generic))

    def test_composite_dimension_not_isinstance(self):
        composite = CompositeDimension(
            numerator=[Dimension(LengthUnit.CENTI_METER) ** 3],
            denominator=[Dimension(MassUnit.GRAM), Dimension(PressureUnit.BAR)],
        )
        self.assertFalse(
            composite.isinstance((LengthUnit**3) / MassUnit / TemperatureUnit)
        )


class TestCompositeDimensionGet(TestUnitDescriptors):
    def composite(self):
        composite = CompositeDimension(
            numerator=[
                Dimension(LengthUnit.CENTI_METER) ** 2,
                Dimension(MassUnit.GRAM),
            ],
            denominator=[
                Dimension(PressureUnit.BAR) ** 3,
                Dimension(TemperatureUnit.CELCIUS),
            ],
        )
        return composite

    def test_get_numerator(self):
        dimension = self.composite().get_numerator(LengthUnit**2)
        self.assertIsNotNone(dimension)
        self.assertEqual(dimension.unit, LengthUnit.CENTI_METER)
        self.assertEqual(dimension.power, 2)

    def test_get_numerator_default(self):
        dimension = self.composite().get_numerator(LengthUnit, "def")
        self.assertEqual(dimension, "def")

    def test_get_denominator(self):
        dimension = self.composite().get_denominator(TemperatureUnit)
        self.assertIsNotNone(dimension)
        self.assertEqual(dimension.unit, TemperatureUnit.CELCIUS)
        self.assertEqual(dimension.power, 1)

    def test_get_denominator_default(self):
        dimension = self.composite().get_denominator(PressureUnit, 2)
        self.assertEqual(dimension, 2)


class TestGenericUnitDescriptors(TestCase):
    pass


class TestGenericDimensions(TestGenericUnitDescriptors):
    @staticmethod
    def create(unit_type: Type[MeasurementUnit]) -> GenericDimension:
        return GenericDimension(unit_type)

    def test_generic_eq(self):
        self.assertTrue(self.create(LengthUnit) == self.create(LengthUnit))

    def test_generic_ne(self):
        self.assertFalse(self.create(LengthUnit) == self.create(MassUnit))

    def test_generic_composite_eq(self):
        c1 = self.create(TemperatureUnit) * self.create(PressureUnit)
        c2 = self.create(PressureUnit) * self.create(TemperatureUnit)
        self.assertTrue(c1 == c2)

    def test_generic_primitives_multiplication(self):
        generic = self.create(TemperatureUnit) * self.create(LengthUnit)
        self.assertEqual(len(generic.numerator), 2)
        self.assertEqual(len(generic.denominator), 0)

    def test_generic_composite_multiplication(self):
        generic = (self.create(TemperatureUnit) * self.create(MassUnit)) * self.create(
            LengthUnit
        )
        self.assertEqual(len(generic.numerator), 3)

    @parameterized.expand([(None,), (0,), (str(),), (object(),)])
    def test_generic_multiplication_raises(self, factor):
        with self.assertRaises(InvalidUnitDescriptorBinaryOperation):
            self.create(TemperatureUnit) * factor

    def test_generic_primitive_division(self):
        generic = self.create(MassUnit) / self.create(LengthUnit)
        self.assertEqual(len(generic.numerator), 1)
        self.assertEqual(len(generic.denominator), 1)

    def test_generic_composite_division(self):
        generic = (
            self.create(LengthUnit)
            / self.create(TemperatureUnit)
            / self.create(PressureUnit)
        )
        self.assertEqual(len(generic.numerator), 1)
        self.assertEqual(len(generic.denominator), 2)

    @parameterized.expand([(None,), (0,), (str(),), (object(),)])
    def test_generic_division_raises(self, factor):
        with self.assertRaises(InvalidUnitDescriptorBinaryOperation):
            self.create(LengthUnit) / factor

    def test_generic_primitive_power(self):
        generic = self.create(LengthUnit) ** 3
        self.assertEqual(generic.power, 3)

    def test_generic_multiple_operations(self):
        generic = ((self.create(LengthUnit) ** 3) * self.create(TemperatureUnit)) / (
            self.create(MassUnit) * (self.create(PressureUnit) ** 2)
        )
        self.assertEqual(len(generic.numerator), 2)
        self.assertEqual(len(generic.denominator), 2)


class TestGenericUnits(TestGenericDimensions):
    """
    Run tests of `TestGenericDimensions`, but substitute any instance of
    GenericDimension with its' generic unit.
    """

    @staticmethod
    def create(unit_type: Type[MeasurementUnit]) -> Type[MeasurementUnit]:
        return unit_type


if __name__ == "__main__":
    main()
