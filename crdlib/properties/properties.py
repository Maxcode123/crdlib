from enum import Enum
from pydantic import BaseModel

from crdlib.properties.units import TemperatureUnit
from crdlib.properties.unit_converters import TemperatureUnitConverter


class Property(BaseModel):
    value: float
    unit: Enum


class Temperature(Property):

    def to_unit(self, unit: TemperatureUnit) -> 'Temperature':
        """
        Convert Temperature to specified unit.
        Returns new object; does not modify caller object.
        """
        return self.from_temperature(self, unit)

    @classmethod
    def from_temperature(
        cls,
        temperature: 'Temperature',
        conversion_unit: TemperatureUnit,
            ) -> 'Temperature':
        """
        Create a Temperature by converting the given Temperature to the
        specified unit. 
        """
        return Temperature(
            value=TemperatureUnitConverter.convert(
                temperature.value, temperature.unit, conversion_unit),
            unit=conversion_unit)


class Pressure(Property):
    pass
