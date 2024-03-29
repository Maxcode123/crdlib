from unittest import TestCase, main

from crdlib.properties.units.units import (
    TemperatureUnit,
    PressureUnit,
    LengthUnit,
    MassUnit,
    TimeUnit,
    EnergyUnit,
    AmountUnit,
)
from crdlib.properties.units.descriptors import Dimension
from crdlib.properties.properties import (
    Temperature,
    Pressure,
    Volume,
    Length,
    MassRate,
    MolarEnergy,
)
from crdlib.properties.exceptions import InvalidUnitConversion


class TestPhysicalProperty(TestCase):
    def test_to_unit_C_to_K(self):
        C = Temperature(0, TemperatureUnit.CELCIUS)
        K = C.to_unit(TemperatureUnit.KELVIN)
        self.assertEqual(K.value, 273.15)

    def test_to_unit_K_to_R(self):
        K = Temperature(1000, TemperatureUnit.KELVIN)
        R = K.to_unit(TemperatureUnit.RANKINE)
        self.assertEqual(R.value, 1800)

    def test_to_unit_raises(self):
        with self.assertRaises(InvalidUnitConversion):
            Temperature(0, TemperatureUnit.CELCIUS).to_unit(PressureUnit.BAR)

    def test_from_physical_property(self):
        K = Temperature(500, TemperatureUnit.KELVIN)
        F = Temperature.from_physical_property(K, TemperatureUnit.FAHRENHEIT)
        self.assertAlmostEqual(F.value, (500 - 273.15) * 1.8 + 32, 2)

    def test_temperature_to_si_from_C(self):
        C = Temperature(0, TemperatureUnit.CELCIUS)
        K = C.to_si()
        self.assertEqual(K.value, 273.15)
        self.assertEqual(K.unit_descriptor, TemperatureUnit.KELVIN)

    def test_length_to_si_from_millimeters(self):
        mm = Length(2_000, LengthUnit.MILLI_METER)
        m = mm.to_si()
        self.assertEqual(m.value, 2)
        self.assertEqual(m.unit_descriptor, LengthUnit.METER)


class TestExponentPhysicalProperty(TestCase):
    def test_to_unit_m3_to_cm3(self):
        V1 = Volume(10, Dimension(LengthUnit.METER) ** 3)
        V2 = V1.to_unit(Dimension(LengthUnit.CENTI_METER) ** 3)
        self.assertEqual(V2.value, 10_000_000)

    def test_to_unit_raises_wrong_exponent(self):
        V1 = Volume(2, Dimension(LengthUnit.MILLI_METER) ** 3)
        with self.assertRaises(InvalidUnitConversion):
            V1.to_unit(Dimension(LengthUnit.METER) ** 2)

    def test_to_unit_raises_wrong_unit(self):
        V1 = Volume(1, Dimension(LengthUnit.FOOT) ** 3)
        with self.assertRaises(InvalidUnitConversion):
            V1.to_unit(Dimension(TemperatureUnit.CELCIUS) ** 3)

    def test_to_unit_raises_wrong_unit_and_exponent(self):
        V1 = Volume(5, Dimension(LengthUnit.INCH) ** 3)
        with self.assertRaises(InvalidUnitConversion):
            V1.to_unit(Dimension(PressureUnit.PSI))

    def test_to_si(self):
        V1 = Volume(5_000, LengthUnit.CENTI_METER**3)
        V2 = V1.to_si()

        self.assertAlmostEqual(V2.value, 0.005)
        self.assertEqual(V2.unit_descriptor, LengthUnit.METER**3)


class TestCompositePhysicalProperty(TestCase):
    def test_to_unit(self):
        M1 = MassRate(10, Dimension(MassUnit.KILO_GRAM) / Dimension(TimeUnit.HOUR))
        M2 = M1.to_unit(Dimension(MassUnit.METRIC_TONNE) / Dimension(TimeUnit.DAY))
        self.assertAlmostEqual(M2.value, 10 / 1_000 * 24, 2)

    def test_to_si(self):
        M1 = MassRate(10, MassUnit.METRIC_TONNE / TimeUnit.HOUR)
        M2 = M1.to_si()

        self.assertAlmostEqual(M2.value, 10 * 1_000 / 60 / 60)
        self.assertEqual(M2.unit_descriptor, MassUnit.KILO_GRAM / TimeUnit.SECOND)


class TestAliasedPhysicalProperty(TestCase):
    def test_to_unit_bar_to_Pa(self):
        P1 = Pressure(2, PressureUnit.BAR)
        P2 = P1.to_unit(PressureUnit.PASCAL)
        self.assertEqual(P2.value, 200_000)

    def test_to_unit_kPa_to_psi(self):
        P1 = Pressure(200, PressureUnit.KILO_PASCAL)
        P2 = P1.to_unit(PressureUnit.PSI)
        self.assertAlmostEqual(P2.value, 2 * 14.5038, 4)

    def test_to_base_units(self):
        P1 = Pressure(15, PressureUnit.BAR)
        P2 = P1.to_base_units()
        self.assertEqual(
            P2.unit_descriptor,
            MassUnit.KILO_GRAM / LengthUnit.METER / (TimeUnit.SECOND**2),
        )
        self.assertEqual(P2.value, 15 * 100_000)

    def test_to_base_units_from_base_units(self):
        P1 = Pressure(200_000, PressureUnit.PASCAL)  # Pa is equivalent to base units
        P2 = P1.to_base_units()
        self.assertEqual(
            P2.unit_descriptor,
            MassUnit.KILO_GRAM / LengthUnit.METER / (TimeUnit.SECOND**2),
        )
        self.assertEqual(P2.value, 200_000)


class TestAliasedCompositePhysicalProperty(TestCase):
    def test_to_base_units_composite_value(self):
        E = MolarEnergy(10, EnergyUnit.KILO_JOULE / AmountUnit.MOL)

        self.assertEqual(E.to_base_units().value, 10_000)

    def test_to_base_units_composite_dimensions(self):
        E = MolarEnergy(10, EnergyUnit.KILO_CALORIE / AmountUnit.KILO_MOL)

        self.assertEqual(
            E.to_base_units().unit_descriptor,
            MassUnit.KILO_GRAM
            * (LengthUnit.METER**2)
            / (TimeUnit.SECOND**2)
            / AmountUnit.MOL,
        )


if __name__ == "__main__":
    main()
