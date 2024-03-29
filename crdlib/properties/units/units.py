from crdlib.properties.units.descriptors import (
    MeasurementUnit,
    AliasedMeasurementUnit,
    GenericUnitDescriptor,
)


class NonDimensionalUnit(MeasurementUnit):
    """
    This enum is used to denote physical quantities that do not have a unit of
    measurement.
    """

    NON_DIMENSIONAL = ""


class TemperatureUnit(MeasurementUnit):
    CELCIUS = "°C"
    KELVIN = "K"
    FAHRENHEIT = "°F"
    RANKINE = "°R"


class LengthUnit(MeasurementUnit):
    MILLI_METER = "mm"
    CENTI_METER = "cm"
    METER = "m"
    KILO_METER = "km"
    INCH = "in"
    FOOT = "ft"


class MassUnit(MeasurementUnit):
    MILLI_GRAM = "mg"
    GRAM = "g"
    KILO_GRAM = "kg"
    METRIC_TONNE = "MT"
    POUND = "lb"


class AmountUnit(MeasurementUnit):
    MOL = "mol"
    KILO_MOL = "kmol"


class TimeUnit(MeasurementUnit):
    MILLI_SECOND = "ms"
    SECOND = "s"
    MINUTE = "min"
    HOUR = "hr"
    DAY = "d"


class PressureUnit(AliasedMeasurementUnit):
    MILLI_BAR = "mbar"
    BAR = "bar"
    PSI = "psi"
    PASCAL = "Pa"
    KILO_PASCAL = "kPa"


class EnergyUnit(AliasedMeasurementUnit):
    JOULE = "J"
    KILO_JOULE = "kJ"
    MEGA_JOULE = "MJ"
    GIGA_JOULE = "GJ"
    CALORIE = "cal"
    KILO_CALORIE = "kcal"
    BTU = "Btu"


SI_UNITS: dict[GenericUnitDescriptor, MeasurementUnit] = {
    TemperatureUnit: TemperatureUnit.KELVIN,
    LengthUnit: LengthUnit.METER,
    MassUnit: MassUnit.KILO_GRAM,
    AmountUnit: AmountUnit.MOL,
    TimeUnit: TimeUnit.SECOND,
}
