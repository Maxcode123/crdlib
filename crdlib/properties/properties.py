from dataclasses import dataclass
from typing import Type

from crdlib.properties.units import Dimension, MeasurementUnit
from crdlib.properties.unit_converters import (
    TemperatureUnitConverter,
    PhysicalPropertyUnitConverter,
    PressureUnitConverter,
)


@dataclass
class PhysicalProperty:
    value: float
    dimension: Dimension
    converter: Type[PhysicalPropertyUnitConverter]

    def __init__(self, value: float, unit: MeasurementUnit) -> None:
        self.value = value
        self.dimension = Dimension(unit)

    def to_unit(self, unit: MeasurementUnit) -> "PhysicalProperty":
        """
        Create a new PhysicalProperty object with specified unit.
        """
        return self.from_physical_property(self, unit)

    @classmethod
    def from_physical_property(
        cls, physical_property: "PhysicalProperty", to_unit: MeasurementUnit
    ) -> "PhysicalProperty":
        """
        Create a new PhysicalProperty object with specified unit from given object.
        """
        return cls(
            value=cls.converter.convert(
                physical_property.value,
                physical_property.dimension.unit,
                to_unit,
            ),
            unit=to_unit,
        )


class Temperature(PhysicalProperty):
    converter: Type[PhysicalPropertyUnitConverter] = TemperatureUnitConverter


class Pressure(PhysicalProperty):
    converter: Type[PhysicalPropertyUnitConverter] = PressureUnitConverter


class Volume(PhysicalProperty):
    pass


class MassRate(PhysicalProperty):
    pass


class VolumetricRate(PhysicalProperty):
    pass


class MolecularRate(PhysicalProperty):
    pass


class MassFraction(PhysicalProperty):
    pass


class VolumeFraction(PhysicalProperty):
    pass


class MolecularFraction(PhysicalProperty):
    pass
