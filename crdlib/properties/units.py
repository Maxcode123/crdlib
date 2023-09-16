from enum import Enum
from typing import List, Union
from dataclasses import dataclass, field

from crdlib.exceptions.exceptions import PropertyUnitOperationError


class MeasurementUnit(str, Enum):
    """
    Base class for all measurement units of physical quantities.

    Each measurement-unit class is an enumeration of the available units for a
    quantity.

    Subclasses should only enumerate measurement units of primitive physical
    quantities, i.e. units that cannot be produced from other units.
    e.g. length is an acceptable quantity, but volume is not because its' units are
    produced from length units.
    """

    pass


class NonDimensionalUnit(MeasurementUnit):
    """
    This enum is used to denote physical quantities that do not have a unit of
    measurement.
    """

    NON_DIMENSIONAL = ""


class CompositeUnit(MeasurementUnit):
    """
    This enum serves the sole purpose of providing a value for the `unit` attribute of
    the `CompositeDimension` class.
    """

    COMPOSITE_UNIT = "COMPOSITE_UNIT"


class TemperatureUnit(MeasurementUnit):
    CELCIUS = "°C"
    KELVIN = "K"
    FAHRENHEIT = "°F"
    RANKINE = "°R"


class PressureUnit(MeasurementUnit):
    MILLI_BAR = "mbar"
    BAR = "bar"
    PSI = "psi"
    PASCAL = "Pa"
    KILO_PASCAL = "kPa"


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
    POUND = "lb"


class AmountUnit(MeasurementUnit):
    MOL = "mol"
    KILO_MOL = "kmol"


class TimeUnit(MeasurementUnit):
    MILLI_SECOND = "ms"
    SECOND = "s"
    HOUR = "hr"
    DAY = "d"


class EnergyUnit(MeasurementUnit):
    JOULE = "J"
    KILO_JOULE = "kJ"
    GIGA_JOULE = "GJ"
    CALORIE = "cal"
    KILO_CALORIE = "kcal"
    BTU = "Btu"


@dataclass
class Dimension:
    """
    A `Dimension` is a wrapper around `MeasurementUnit`.

    Objects of this class can represent either a simple `MeasurementUnit` or a
    `MeasurementUnit` to some power.

    `Dimension` is an implementation of the leaf component of the Composite Design
    Pattern.

    Create objects by giving a MeasurementUnit:
    ```
    energy_dimension = Dimension(EnergyUnit.KILO_JOULE)  # [kJ]
    energy_dimension_sq = energy_dimension ** 2  # [kJ^2]
    ```
    """

    unit: MeasurementUnit
    power: Union[float, int] = 1

    def __init__(self, unit: MeasurementUnit) -> None:
        self.unit = unit

    def __mul__(self, dimension: "Dimension") -> "CompositeDimension":
        if isinstance(dimension, CompositeDimension):
            numerator = dimension.numerator.copy()
            denominator = dimension.denominator.copy()
            if isinstance(self, CompositeDimension):
                numerator.extend(self.numerator)
                denominator.extend(self.denominator)
            else:
                numerator.append(self)
            return CompositeDimension(numerator=numerator, denominator=denominator)
        if isinstance(self, CompositeDimension):
            return dimension * self
        return CompositeDimension(numerator=[self, dimension])

    def __truediv__(self, dimension: "Dimension") -> "CompositeDimension":
        if isinstance(dimension, CompositeDimension):
            numerator = dimension.denominator.copy()
            denominator = dimension.numerator.copy()
            if isinstance(self, CompositeDimension):
                numerator.extend(dimension.denominator)
                denominator.extend(dimension.numerator)
            else:
                numerator.append(self)
            return CompositeDimension(numerator=numerator, denominator=denominator)
        if isinstance(self, CompositeDimension):
            numerator = self.numerator.copy()
            denominator = self.denominator.copy()
            denominator.append(dimension)
            return CompositeDimension(numerator=numerator, denominator=denominator)
        return CompositeDimension(numerator=[self], denominator=[dimension])

    def __pow__(self, power: Union[float, int]) -> "Dimension":
        if isinstance(self, CompositeDimension):
            raise PropertyUnitOperationError(
                "power operand `**` is not supported for CompositeDimension. "
            )
        self.power = power
        return self

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        if self.power != 1:
            return "(" + self.unit.value + ") ^ " + str(self.power)
        return self.unit.value


@dataclass
class CompositeDimension(Dimension):
    """
    A `CompositeDimension` represents a measurement unit that is composed from other
    measurement units.

    Objects of this class can represent either multiplication or division between two
    `Dimension` objects.

    `CompositeDimension` is an implementation of the composite component of the
    Composite Design Pattern.

    Create objects by multiplying and diving `Dimension` objects:
    ```
    molal_volume_dimension = (
        (Dimension(LengthUnit.METER) ** 3) / Dimension(AmountUnit.KILO_MOL)
    )  # [m^3/kmol]
    ```
    """

    unit: MeasurementUnit = CompositeUnit.COMPOSITE_UNIT
    numerator: List[Dimension] = field(default_factory=list)
    denominator: List[Dimension] = field(default_factory=list)

    def __str__(self):
        numerators = " * ".join([str(n) for n in self.numerator])
        denominators = " / ".join([str(d) for d in self.denominator])
        if len(denominators) > 0:
            denominators = " / " + denominators
        return numerators + denominators
