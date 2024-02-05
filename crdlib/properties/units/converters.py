from abc import ABCMeta, abstractmethod
from typing import Protocol, Type

from crdlib.properties.units.units import (
    MeasurementUnit,
    TemperatureUnit,
    PressureUnit,
    LengthUnit,
    MassUnit,
    AmountUnit,
    TimeUnit,
    EnergyUnit,
)
from crdlib.properties.units.descriptors import (
    UnitDescriptor,
    GenericUnitDescriptor,
    Dimension,
    CompositeDimension,
)
from crdlib.properties.exceptions import InvalidUnitConversion, UndefinedConverter
from crdlib.utils.protocols import implements

_converters: dict[GenericUnitDescriptor, Type["PhysicalPropertyUnitConverter"]] = dict()


def get_converter(
    generic: GenericUnitDescriptor,
) -> Type["PhysicalPropertyUnitConverter"]:
    """
    Get converter for given generic descriptor.
    """
    try:
        return _converters[generic]
    except KeyError:
        raise UndefinedConverter(f"a converter has not been defined for {generic}")


def register_converter(generic: GenericUnitDescriptor):
    """
    Decorate a converter class to register the generic descriptor of the units it
    operates on.
    """

    def wrapper(cls):
        _converters[generic] = cls
        return cls

    return wrapper


def _from_milliunit_to_unit() -> float:
    return 1 / 1_000


def _from_centiunit_to_unit() -> float:
    return 1 / 100


def _from_kilounit_to_unit() -> float:
    return 1_000


def _from_megaunit_to_unit() -> float:
    return 1_000_000


def _from_gigaunit_to_unit() -> float:
    return 1_000_000_000


def _from_unit_to_milliunit() -> float:
    return 1_000


def _from_unit_to_centiunit() -> float:
    return 100


def _from_unit_to_kilounit() -> float:
    return 1 / 1_000.0


def _from_unit_to_megaunit() -> float:
    return 1 / 1_000_000.0


def _from_unit_to_gigaunit() -> float:
    return 1 / 1_000_000_000.0


class PhysicalPropertyUnitConverter(Protocol):
    """Protocol of classes that convert a value from one unit to another."""

    @classmethod
    def convert(
        cls,
        value: float,
        from_descriptor: UnitDescriptor,
        to_descriptor: UnitDescriptor,
    ) -> float:
        ...


@implements(PhysicalPropertyUnitConverter)
class AbsoluteUnitConverter(metaclass=ABCMeta):
    """
    Base converter class for measurement units that are absolute, i.e. not relative.

    e.g.
    Pressure units are absolute because the following applies:
    unit_i = unit_j * constant,
    where unit_i and unit_j can be any pressure units.

    Temperature units are not absolute because the above equation does not apply when
    converting from a relative temperature to an absolute temperature (e.g. from Celcius
    to Kelvin, or Fahrenheit to Rankine).
    """

    @classmethod
    def convert(
        cls,
        value: float,
        from_descriptor: UnitDescriptor,
        to_descriptor: UnitDescriptor,
    ) -> float:
        return value * cls.get_factor(from_descriptor, to_descriptor)

    @classmethod
    @abstractmethod
    def get_factor(
        cls, from_descriptor: UnitDescriptor, to_descriptor: UnitDescriptor
    ) -> float:
        ...


class CompositePhysicalPropertyUnitConverter(metaclass=ABCMeta):
    """
    Base class for converters that implement conversions for composite units.
    Composite unit conversions are absolute, that is the below applies:

    unit_i = unit_j * constant,
    where unit_i and unit_j can be any composite units of the same type.

    The `get_factor` method returns the above constant, which is the result of the
    divison between the numerator factor and the denominator factor.

    e.g.\n
    kJ * m^3 / min^2 / K = J * m^3 / s^2 / K * ( 1000 / 60^2 )\n
    1000 is the numerator factor extracted from converting kJ to J.\n
    60^2 is the denominator factor extracted from converting min^2 to s^2.
    """

    @classmethod
    def get_factor(
        cls, from_dimension: CompositeDimension, to_dimension: CompositeDimension
    ) -> float:
        return cls.get_numerator_factor(
            from_dimension, to_dimension
        ) / cls.get_denominator_factor(from_dimension, to_dimension)

    @staticmethod
    def get_numerator_factor(
        from_dimension: CompositeDimension, to_dimension: CompositeDimension
    ) -> float:
        numerator_factor = 1.0
        for from_d in from_dimension.numerator:
            to_d = to_dimension.get_numerator(from_d.to_generic())
            if to_d is None:
                raise InvalidUnitConversion(
                    f"cannot convert from {from_dimension} to {to_dimension}"
                )
            converter = get_converter(type(from_d.unit))
            if issubclass(converter, AbsoluteUnitConverter):
                numerator_factor *= converter.get_factor(from_d.unit, to_d.unit)
        return numerator_factor

    @staticmethod
    def get_denominator_factor(
        from_dimension: CompositeDimension, to_dimension: CompositeDimension
    ) -> float:
        denominator_factor = 1.0

        for from_d in from_dimension.denominator:
            to_d = to_dimension.get_denominator(from_d.to_generic())
            if to_d is None:
                raise InvalidUnitConversion(
                    f"cannot convert from {from_dimension} to {to_dimension}"
                )
            converter = get_converter(type(from_d.unit))
            if issubclass(converter, AbsoluteUnitConverter):
                denominator_factor *= converter.get_factor(from_d.unit, to_d.unit)
        return denominator_factor


@implements(PhysicalPropertyUnitConverter)
@register_converter(TemperatureUnit)
class TemperatureUnitConverter:
    @classmethod
    def convert(
        cls,
        value: float,
        from_descriptor: UnitDescriptor,
        to_descriptor: UnitDescriptor,
    ) -> float:
        if not from_descriptor.isinstance(TemperatureUnit):
            raise InvalidUnitConversion(
                f"cannot convert Temperature unit; unknown `from_unit`: {to_descriptor}. "
            )
        unit = MeasurementUnit.from_descriptor(from_descriptor)

        if unit == TemperatureUnit.CELCIUS:
            return cls.convert_from_celcius(value, to_descriptor)
        elif unit == TemperatureUnit.FAHRENHEIT:
            return cls.convert_from_celcius(
                cls.from_fahrenhet_to_celcius(value), to_descriptor
            )
        elif unit == TemperatureUnit.KELVIN:
            return cls.convert_from_celcius(
                cls.from_kelvin_to_celcius(value), to_descriptor
            )
        elif unit == TemperatureUnit.RANKINE:
            return cls.convert_from_celcius(
                cls.from_rankine_to_celcius(value), to_descriptor
            )
        else:
            return 0

    @classmethod
    def convert_from_celcius(cls, value: float, to_descriptor: UnitDescriptor) -> float:
        if not to_descriptor.isinstance(TemperatureUnit):
            raise InvalidUnitConversion(
                f"cannot convert Temperature unit; unknown `to_unit`: {to_descriptor}. "
            )
        unit = MeasurementUnit.from_descriptor(to_descriptor)

        if unit == TemperatureUnit.CELCIUS:
            return value
        elif unit == TemperatureUnit.FAHRENHEIT:
            return cls.from_celcius_to_fahrenheit(value)
        elif unit == TemperatureUnit.KELVIN:
            return cls.from_celcius_to_kelvin(value)
        elif unit == TemperatureUnit.RANKINE:
            return cls.from_celcius_to_rankine(value)
        else:
            return 0

    @staticmethod
    def from_celcius_to_kelvin(celcius: float) -> float:
        return celcius + 273.15

    @staticmethod
    def from_celcius_to_fahrenheit(celcius: float) -> float:
        return 1.8 * celcius + 32

    @classmethod
    def from_celcius_to_rankine(cls, celcius: float) -> float:
        return cls.from_celcius_to_kelvin(celcius) * 1.8

    @staticmethod
    def from_fahrenhet_to_celcius(fahrenheit: float) -> float:
        return (fahrenheit - 32) / 1.8

    @staticmethod
    def from_kelvin_to_celcius(kelvin: float) -> float:
        return kelvin - 273.15

    @classmethod
    def from_rankine_to_celcius(cls, rankine: float) -> float:
        return cls.from_kelvin_to_celcius(rankine / 1.8)


@register_converter(PressureUnit)
class AliasedPressureUnitConverter(AbsoluteUnitConverter):
    BAR_TO_PSI = 14.5038
    BAR_TO_PASCAL = 100_000
    BAR_TO_KILOPASCAL = 100

    @classmethod
    def get_factor(
        cls, from_descriptor: UnitDescriptor, to_descriptor: UnitDescriptor
    ) -> float:
        if not from_descriptor.isinstance(PressureUnit):
            raise InvalidUnitConversion(
                f"cannot convert Pressure unit; unknown `from_unit`: {to_descriptor}. "
            )
        unit = MeasurementUnit.from_descriptor(from_descriptor)

        if unit == PressureUnit.BAR:
            return cls.get_factor_from_bar(to_descriptor)
        elif unit == PressureUnit.MILLI_BAR:
            return _from_milliunit_to_unit() * cls.get_factor_from_bar(to_descriptor)
        elif unit == PressureUnit.PSI:
            return (1 / cls.BAR_TO_PSI) * cls.get_factor_from_bar(to_descriptor)
        elif unit == PressureUnit.PASCAL:
            return (1 / cls.BAR_TO_PASCAL) * cls.get_factor_from_bar(to_descriptor)
        elif unit == PressureUnit.KILO_PASCAL:
            return (1 / cls.BAR_TO_KILOPASCAL) * cls.get_factor_from_bar(to_descriptor)
        else:
            return 0

    @classmethod
    def get_factor_from_bar(cls, to_descriptor: UnitDescriptor) -> float:
        if not to_descriptor.isinstance(PressureUnit):
            raise InvalidUnitConversion(
                f"cannot convert Pressure unit; unknown `to_unit`: {to_descriptor}. "
            )
        unit = MeasurementUnit.from_descriptor(to_descriptor)

        if unit == PressureUnit.BAR:
            return 1
        elif unit == PressureUnit.MILLI_BAR:
            return _from_unit_to_milliunit()
        elif unit == PressureUnit.PSI:
            return cls.BAR_TO_PSI
        elif unit == PressureUnit.PASCAL:
            return cls.BAR_TO_PASCAL
        elif unit == PressureUnit.KILO_PASCAL:
            return _from_unit_to_kilounit()
        else:
            return 0


@register_converter(LengthUnit)
class LengthUnitConverter(AbsoluteUnitConverter):
    METER_TO_INCH = 39.37
    METER_TO_FOOT = 3.281

    @classmethod
    def get_factor(
        cls, from_descriptor: UnitDescriptor, to_descriptor: UnitDescriptor
    ) -> float:
        if not from_descriptor.isinstance(LengthUnit):
            raise InvalidUnitConversion(
                f"cannot convert Length unit; unknown `from_unit`: {from_descriptor}. "
            )
        unit = MeasurementUnit.from_descriptor(from_descriptor)

        if unit == LengthUnit.METER:
            return cls.get_factor_from_meter(to_descriptor)
        elif unit == LengthUnit.MILLI_METER:
            return _from_milliunit_to_unit() * cls.get_factor_from_meter(to_descriptor)
        elif unit == LengthUnit.CENTI_METER:
            return _from_centiunit_to_unit() * cls.get_factor_from_meter(to_descriptor)
        elif unit == LengthUnit.KILO_METER:
            return _from_kilounit_to_unit() * cls.get_factor_from_meter(to_descriptor)
        elif unit == LengthUnit.INCH:
            return (1 / cls.METER_TO_INCH) * cls.get_factor_from_meter(to_descriptor)
        elif unit == LengthUnit.FOOT:
            return (1 / cls.METER_TO_FOOT) * cls.get_factor_from_meter(to_descriptor)
        else:
            return 0

    @classmethod
    def get_factor_from_meter(cls, to_descriptor: UnitDescriptor) -> float:
        if not to_descriptor.isinstance(LengthUnit):
            raise InvalidUnitConversion(
                f"cannot convert Length unit; unknown `to_unit`: {to_descriptor}.  "
            )
        unit = MeasurementUnit.from_descriptor(to_descriptor)

        if unit == LengthUnit.METER:
            return 1
        elif unit == LengthUnit.MILLI_METER:
            return _from_unit_to_milliunit()
        elif unit == LengthUnit.CENTI_METER:
            return _from_unit_to_centiunit()
        elif unit == LengthUnit.KILO_METER:
            return _from_unit_to_kilounit()
        elif unit == LengthUnit.INCH:
            return cls.METER_TO_INCH
        elif unit == LengthUnit.FOOT:
            return cls.METER_TO_FOOT
        else:
            return 0


@register_converter(MassUnit)
class MassUnitConverter(AbsoluteUnitConverter):
    KILOGRAM_TO_MILLIGRAM = 1_000_000
    KILOGRAM_TO_METRIC_TONNE = 1 / 1_000
    KILOGRAM_TO_POUND = 2.205

    @classmethod
    def get_factor(
        cls, from_descriptor: UnitDescriptor, to_descriptor: UnitDescriptor
    ) -> float:
        if not from_descriptor.isinstance(MassUnit):
            raise InvalidUnitConversion(
                f"cannot convert Mass unit; unknown `from_unit`: {from_descriptor}. "
            )
        unit = MeasurementUnit.from_descriptor(from_descriptor)

        if unit == MassUnit.KILO_GRAM:
            return cls.get_factor_from_kilogram(to_descriptor)
        elif unit == MassUnit.MILLI_GRAM:
            return (1 / cls.KILOGRAM_TO_MILLIGRAM) * cls.get_factor_from_kilogram(
                to_descriptor
            )
        elif unit == MassUnit.GRAM:
            return _from_unit_to_kilounit() * cls.get_factor_from_kilogram(
                to_descriptor
            )
        elif unit == MassUnit.METRIC_TONNE:
            return (1 / cls.KILOGRAM_TO_METRIC_TONNE) * cls.get_factor_from_kilogram(
                to_descriptor
            )
        elif unit == MassUnit.POUND:
            return (1 / cls.KILOGRAM_TO_POUND) * cls.get_factor_from_kilogram(
                to_descriptor
            )
        else:
            return 0

    @classmethod
    def get_factor_from_kilogram(cls, to_descriptor: UnitDescriptor) -> float:
        if not to_descriptor.isinstance(MassUnit):
            raise InvalidUnitConversion(
                f"cannot convert Mass unit; unknown `to_unit`: {to_descriptor}. "
            )
        unit = MeasurementUnit.from_descriptor(to_descriptor)

        if unit == MassUnit.KILO_GRAM:
            return 1
        elif unit == MassUnit.MILLI_GRAM:
            return cls.KILOGRAM_TO_MILLIGRAM
        elif unit == MassUnit.GRAM:
            return _from_kilounit_to_unit()
        elif unit == MassUnit.METRIC_TONNE:
            return cls.KILOGRAM_TO_METRIC_TONNE
        elif unit == MassUnit.POUND:
            return cls.KILOGRAM_TO_POUND
        else:
            return 0


@register_converter(AmountUnit)
class AmountUnitConverter(AbsoluteUnitConverter):
    @classmethod
    def get_factor(
        cls, from_descriptor: UnitDescriptor, to_descriptor: UnitDescriptor
    ) -> float:
        if not from_descriptor.isinstance(AmountUnit):
            raise InvalidUnitConversion(
                f"cannot convert Amount unit; unknown `from_unit`: {from_descriptor}. "
            )
        unit = MeasurementUnit.from_descriptor(from_descriptor)

        if unit == AmountUnit.MOL:
            return cls.get_factor_from_mol(to_descriptor)
        elif unit == AmountUnit.KILO_MOL:
            return _from_kilounit_to_unit() * cls.get_factor_from_mol(to_descriptor)
        else:
            return 0

    @classmethod
    def get_factor_from_mol(cls, to_descriptor: UnitDescriptor) -> float:
        if not to_descriptor.isinstance(AmountUnit):
            raise InvalidUnitConversion(
                f"cannot convert Amount unit; unknown `to_unit`: {to_descriptor}. "
            )
        unit = MeasurementUnit.from_descriptor(to_descriptor)

        if unit == AmountUnit.MOL:
            return 1
        elif unit == AmountUnit.KILO_MOL:
            return _from_unit_to_kilounit()
        else:
            return 0


@register_converter(TimeUnit)
class TimeUnitConverter(AbsoluteUnitConverter):
    SECOND_TO_MINUTE = 1 / 60.0
    SECOND_TO_HOUR = 1 / 60.0 / 60
    SECOND_TO_DAY = 1 / 60.0 / 60 / 24

    @classmethod
    def get_factor(
        cls, from_descriptor: UnitDescriptor, to_descriptor: UnitDescriptor
    ) -> float:
        if not from_descriptor.isinstance(TimeUnit):
            raise InvalidUnitConversion(
                f"cannot convert Time unit; unknown `from_unit`: {from_descriptor}. "
            )
        unit = MeasurementUnit.from_descriptor(from_descriptor)

        if unit == TimeUnit.SECOND:
            return cls.get_factor_from_second(to_descriptor)
        elif unit == TimeUnit.MILLI_SECOND:
            return _from_milliunit_to_unit() * cls.get_factor_from_second(to_descriptor)
        elif unit == TimeUnit.MINUTE:
            return (1 / cls.SECOND_TO_MINUTE) * cls.get_factor_from_second(
                to_descriptor
            )
        elif unit == TimeUnit.HOUR:
            return (1 / cls.SECOND_TO_HOUR) * cls.get_factor_from_second(to_descriptor)
        elif unit == TimeUnit.DAY:
            return (1 / cls.SECOND_TO_DAY) * cls.get_factor_from_second(to_descriptor)
        else:
            return 0

    @classmethod
    def get_factor_from_second(cls, to_descriptor: UnitDescriptor) -> float:
        if not to_descriptor.isinstance(TimeUnit):
            raise InvalidUnitConversion(
                f"cannot convert Time unit; unknown `to_unit`: {to_descriptor}. "
            )
        unit = MeasurementUnit.from_descriptor(to_descriptor)

        if unit == TimeUnit.SECOND:
            return 1
        elif unit == TimeUnit.MILLI_SECOND:
            return _from_unit_to_milliunit()
        elif unit == TimeUnit.MINUTE:
            return cls.SECOND_TO_MINUTE
        elif unit == TimeUnit.HOUR:
            return cls.SECOND_TO_HOUR
        elif unit == TimeUnit.DAY:
            return cls.SECOND_TO_DAY
        else:
            return 0


@register_converter(EnergyUnit)
class EnergyUnitConverter(AbsoluteUnitConverter):
    JOULE_TO_CALORIE = 1 / 4.184
    JOULE_TO_KILOCALORIE = 1 / 4.184 / 1_000
    JOULE_TO_BTU = 1 / 1055

    @classmethod
    def get_factor(
        cls, from_descriptor: UnitDescriptor, to_descriptor: UnitDescriptor
    ) -> float:
        if not from_descriptor.isinstance(EnergyUnit):
            raise InvalidUnitConversion(
                f"cannot convert Energy unit; unknown `from_unit`: {from_descriptor}. "
            )
        unit = MeasurementUnit.from_descriptor(from_descriptor)

        if unit == EnergyUnit.JOULE:
            return cls.get_factor_from_joule(to_descriptor)
        elif unit == EnergyUnit.KILO_JOULE:
            return _from_kilounit_to_unit() * cls.get_factor_from_joule(to_descriptor)
        elif unit == EnergyUnit.GIGA_JOULE:
            return _from_gigaunit_to_unit() * cls.get_factor_from_joule(to_descriptor)
        elif unit == EnergyUnit.CALORIE:
            return (1 / cls.JOULE_TO_CALORIE) * cls.get_factor_from_joule(to_descriptor)
        elif unit == EnergyUnit.KILO_CALORIE:
            return (1 / cls.JOULE_TO_KILOCALORIE) * cls.get_factor_from_joule(
                to_descriptor
            )
        elif unit == EnergyUnit.BTU:
            return (cls.JOULE_TO_BTU) * cls.get_factor_from_joule(to_descriptor)
        else:
            return 0

    @classmethod
    def get_factor_from_joule(cls, to_descriptor: UnitDescriptor) -> float:
        if not to_descriptor.isinstance(EnergyUnit):
            raise InvalidUnitConversion(
                f"cannot convert Energy unit; unknown `to_unit`: {to_descriptor}. "
            )
        unit = MeasurementUnit.from_descriptor(to_descriptor)

        if unit == EnergyUnit.JOULE:
            return 1
        elif unit == EnergyUnit.KILO_JOULE:
            return _from_unit_to_kilounit()
        elif unit == EnergyUnit.GIGA_JOULE:
            return _from_gigaunit_to_unit()
        elif unit == EnergyUnit.CALORIE:
            return cls.JOULE_TO_CALORIE
        elif unit == EnergyUnit.KILO_CALORIE:
            return cls.JOULE_TO_KILOCALORIE
        elif unit == EnergyUnit.BTU:
            return cls.JOULE_TO_BTU
        else:
            return 0


@implements(PhysicalPropertyUnitConverter)
@register_converter(LengthUnit**3)
class VolumeUnitConverter:
    @classmethod
    def convert(
        cls,
        value: float,
        from_descriptor: UnitDescriptor,
        to_descriptor: UnitDescriptor,
    ) -> float:
        if (not to_descriptor.isinstance(LengthUnit**3)) or (
            not from_descriptor.isinstance(LengthUnit**3)
        ):
            raise InvalidUnitConversion(
                f"invalid Volume unit conversion; cannot convert from {from_descriptor}"
                f" to {to_descriptor}"
            )
        from_dimension = Dimension.from_descriptor(from_descriptor)
        to_dimension = Dimension.from_descriptor(to_descriptor)
        factor = LengthUnitConverter.get_factor(from_dimension.unit, to_dimension.unit)
        return value * (factor**to_dimension.power)


@implements(PhysicalPropertyUnitConverter)
@register_converter(MassUnit / TimeUnit)
class MassRateUnitConverter(CompositePhysicalPropertyUnitConverter):
    @classmethod
    def convert(
        cls,
        value: float,
        from_descriptor: UnitDescriptor,
        to_descriptor: UnitDescriptor,
    ) -> float:
        if (not to_descriptor.isinstance(MassUnit / TimeUnit)) or (
            not from_descriptor.isinstance(MassUnit / TimeUnit)
        ):
            raise InvalidUnitConversion(
                "invalid MassRate unit conversion; cannot convert from"
                f" {from_descriptor} to {to_descriptor}. "
            )
        from_dimension = CompositeDimension.from_descriptor(from_descriptor)
        to_dimension = CompositeDimension.from_descriptor(to_descriptor)
        return value * cls.get_factor(from_dimension, to_dimension)


@implements(PhysicalPropertyUnitConverter)
@register_converter((LengthUnit**3) / AmountUnit)
class MolarVolumeUnitConverter(CompositePhysicalPropertyUnitConverter):
    @classmethod
    def convert(
        cls,
        value: float,
        from_descriptor: UnitDescriptor,
        to_descriptor: UnitDescriptor,
    ) -> float:
        generic = (LengthUnit**3) / AmountUnit
        if (not to_descriptor.isinstance(generic)) or (
            not from_descriptor.isinstance(generic)
        ):
            raise InvalidUnitConversion(
                "invalid MolarVolume unit conversion; cannot convert from"
                f" {from_descriptor} to {to_descriptor}. "
            )
        from_dimension = CompositeDimension.from_descriptor(from_descriptor)
        to_dimension = CompositeDimension.from_descriptor(to_descriptor)
        return value * cls.get_factor(from_dimension, to_dimension)


@implements(PhysicalPropertyUnitConverter)
@register_converter(EnergyUnit / AmountUnit)
class AliasedMolarEnergyUnitConverter(CompositePhysicalPropertyUnitConverter):
    @classmethod
    def convert(
        cls,
        value: float,
        from_descriptor: UnitDescriptor,
        to_descriptor: UnitDescriptor,
    ) -> float:
        generic = EnergyUnit / AmountUnit
        if (not to_descriptor.isinstance(generic)) or (
            not from_descriptor.isinstance(generic)
        ):
            raise InvalidUnitConversion(
                "invalid MolarEnergy unit conversion; cannot convert from "
                f"{from_descriptor} to {to_descriptor}. "
            )
        from_dimension = CompositeDimension.from_descriptor(from_descriptor)
        to_dimension = CompositeDimension.from_descriptor(to_descriptor)
        return value * cls.get_factor(from_dimension, to_dimension)


@implements(PhysicalPropertyUnitConverter)
@register_converter(
    MassUnit * (LengthUnit**2) / (TimeUnit**2) / TemperatureUnit / AmountUnit
)
class GasConstantUnitConverter(CompositePhysicalPropertyUnitConverter):
    @classmethod
    def convert(
        cls,
        value: float,
        from_descriptor: UnitDescriptor,
        to_descriptor: UnitDescriptor,
    ) -> float:
        generic = (
            MassUnit
            * (LengthUnit**2)
            / (TimeUnit**2)
            / TemperatureUnit
            / AmountUnit
        )
        if (not to_descriptor.isinstance(generic)) or (
            not from_descriptor.isinstance(generic)
        ):
            raise InvalidUnitConversion(
                "invalid GasConstant unit conversion; cannot convert from "
                f"{from_descriptor} to {to_descriptor}. "
            )
        from_dimension = CompositeDimension.from_descriptor(from_descriptor)
        to_dimension = CompositeDimension.from_descriptor(to_descriptor)
        return value * cls.get_factor(from_dimension, to_dimension)


@implements(PhysicalPropertyUnitConverter)
@register_converter(MassUnit / LengthUnit / (TimeUnit**2))
class PressureUnitConverter(CompositePhysicalPropertyUnitConverter):
    @classmethod
    def convert(
        cls,
        value: float,
        from_descriptor: UnitDescriptor,
        to_descriptor: UnitDescriptor,
    ) -> float:
        generic = MassUnit / LengthUnit / (TimeUnit**2)
        if (not to_descriptor.isinstance(generic)) or (
            not from_descriptor.isinstance(generic)
        ):
            raise InvalidUnitConversion(
                "invalid Pressure unit conversion; cannot convert from "
                f"{from_descriptor} to {to_descriptor}."
            )
        from_dimension = CompositeDimension.from_descriptor(from_descriptor)
        to_dimension = CompositeDimension.from_descriptor(to_descriptor)
        return value * cls.get_factor(from_dimension, to_dimension)


@implements(PhysicalPropertyUnitConverter)
@register_converter(MassUnit / LengthUnit / (TimeUnit**2) / AmountUnit)
class MolarEnergyUnitConverter(CompositePhysicalPropertyUnitConverter):
    @classmethod
    def convert(
        cls,
        value: float,
        from_descriptor: UnitDescriptor,
        to_descriptor: UnitDescriptor,
    ) -> float:
        generic = MassUnit / LengthUnit / (TimeUnit**2) / AmountUnit
        if (not to_descriptor.isinstance(generic)) or (
            not from_descriptor.isinstance(generic)
        ):
            raise InvalidUnitConversion(
                "invalid MolarEnergy unit conversion; cannot convert from "
                f"{from_descriptor} to {to_descriptor}."
            )
        from_dimension = CompositeDimension.from_descriptor(from_descriptor)
        to_dimension = CompositeDimension.from_descriptor(to_descriptor)
        return value * cls.get_factor(from_dimension, to_dimension)
