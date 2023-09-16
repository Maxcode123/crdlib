from abc import ABCMeta, abstractmethod

from crdlib.properties.units import TemperatureUnit, PressureUnit, MeasurementUnit
from crdlib.exceptions.exceptions import InvalidMeasurementUnit


class PhysicalPropertyUnitConverter(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def convert(
        value: float, from_unit: MeasurementUnit, to_unit: MeasurementUnit
    ) -> float:
        ...


class TemperatureUnitConverter(PhysicalPropertyUnitConverter):
    @classmethod
    def convert(
        cls, value: float, from_unit: TemperatureUnit, to_unit: TemperatureUnit
    ) -> float:
        if from_unit == TemperatureUnit.CELCIUS:
            return cls.convert_from_celcius(value, to_unit)
        elif from_unit == TemperatureUnit.FAHRENHEIT:
            return cls.convert_from_celcius(
                cls.from_fahrenhet_to_celcius(value), to_unit
            )
        elif from_unit == TemperatureUnit.KELVIN:
            return cls.convert_from_celcius(cls.from_kelvin_to_celcius(value), to_unit)
        elif from_unit == TemperatureUnit.RANKINE:
            return cls.convert_from_celcius(cls.from_rankine_to_celcius(value), to_unit)
        raise InvalidMeasurementUnit(
            "cannot convert Temperature unit; invalid `from_unit` TemperatureUnit. "
        )

    @classmethod
    def convert_from_celcius(cls, value: float, to_unit: TemperatureUnit) -> float:
        if to_unit == TemperatureUnit.CELCIUS:
            return value
        elif to_unit == TemperatureUnit.FAHRENHEIT:
            return cls.from_celcius_to_fahrenheit(value)
        elif to_unit == TemperatureUnit.KELVIN:
            return cls.from_celcius_to_kelvin(value)
        elif to_unit == TemperatureUnit.RANKINE:
            return cls.from_celcius_to_rankine(value)
        raise InvalidMeasurementUnit(
            "cannot convert Temperature unit; invalid `to_unit` TemperatureUnit. "
        )

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


class PressureUnitConverter(PhysicalPropertyUnitConverter):
    @classmethod
    def convert(
        cls, value: float, from_unit: PressureUnit, to_unit: PressureUnit
    ) -> float:
        if from_unit == PressureUnit.BAR:
            return cls.convert_from_bar(value)
        elif from_unit == PressureUnit.MILLI_BAR:
            return cls.convert_from_bar(cls.from_millibar_to_bar(value), to_unit)
        elif from_unit == PressureUnit.PSI:
            return cls.convert_from_bar(cls.from_psi_to_bar(value), to_unit)
        elif from_unit == PressureUnit.PASCAL:
            return cls.convert_from_bar(cls.from_pascal_to_bar(value), to_unit)
        elif from_unit == PressureUnit.KILO_PASCAL:
            return cls.convert_from_bar(cls.from_kilopascal_to_bar(value), to_unit)
        raise InvalidMeasurementUnit(
            "cannot convert Pressure unit; invalid `from_unit` PressureUnit. "
        )

    @classmethod
    def convert_from_bar(cls, value: float, to_unit: PressureUnit) -> float:
        if to_unit == PressureUnit.BAR:
            return value
        elif to_unit == PressureUnit.MILLI_BAR:
            return cls.from_bar_to_millibar(value)
        elif to_unit == PressureUnit.PSI:
            return cls.from_bar_to_psi(value)
        elif to_unit == PressureUnit.PASCAL:
            return cls.from_bar_to_pascal(value)
        elif to_unit == PressureUnit.KILO_PASCAL:
            return cls.from_bar_to_kilopascal(value)
        raise InvalidMeasurementUnit(
            "cannot convert Pressure unit; invalid `to_unit` PressureUnit. "
        )

    @staticmethod
    def from_bar_to_millibar(bar: float) -> float:
        return bar * 1_000

    @staticmethod
    def from_bar_to_psi(bar: float) -> float:
        return bar * 14.5038

    @staticmethod
    def from_bar_to_pascal(bar: float) -> float:
        return bar * 100_000

    @staticmethod
    def from_bar_to_kilopascal(bar: float) -> float:
        return bar * 100

    @staticmethod
    def from_millibar_to_bar(millibar: float) -> float:
        return millibar / 1_000

    @staticmethod
    def from_psi_to_bar(psi: float) -> float:
        return psi / 14.5038

    @staticmethod
    def from_pascal_to_bar(pascal: float) -> float:
        return pascal / 100_00

    @staticmethod
    def from_kilopascal_to_bar(kilopascal: float) -> float:
        return kilopascal * 1_000
