from crdlib.properties.units import TemperatureUnit

class TemperatureUnitConverter:
    @staticmethod
    def convert(
        value: float,
        from_unit: TemperatureUnit,
        to_unit: TemperatureUnit,
            ) -> float:
        ...

    @staticmethod
    def from_celcius_to_kelvin(value: float) -> float:
        return value + 273.15

    @staticmethod
    def from_celcius_to_fahrenheit(value: float) -> float: ...
    @staticmethod
    def from_celcius_to_rankine(value: float) -> float: ...
