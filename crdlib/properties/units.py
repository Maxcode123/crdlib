"""
This module includes definitions for generic unit descriptors and unit descriptors.

A unit descriptor is an interface that describes a measurement unit. It can represent
anything like °C, m^3, mol/m^3/s etc.

A generic unit descriptor is an interface that describes a generic measurement unit. It
can represent e.g. a temperature unit, a volume unit, a reaction rate unit etc.
"""
from enum import Enum, EnumMeta
from typing import List, Union, Protocol, TypeAlias, Optional, TypeVar
from dataclasses import dataclass, field

from crdlib.properties.exceptions import (
    InvalidUnitDescriptorBinaryOperation,
    WrongUnitDescriptorType,
)
from crdlib.utils.protocols import implements


class GenericUnitDescriptor(Protocol):
    """
    Descriptor for a property unit that does not have a specific unit.

    e.g. a  generic descriptor can represent a Temperature unit that does not have a
    specific value like Celcius or Fahrenheit.
    """

    def __mul__(self, generic: "GenericUnitDescriptor") -> "GenericCompositeDimension":
        ...

    def __truediv__(
        self, generic: "GenericUnitDescriptor"
    ) -> "GenericCompositeDimension":
        ...

    def __eq__(self, generic) -> bool:
        ...

    def __hash__(self) -> int:
        ...

    def __str__(self) -> str:
        ...


class UnitDescriptor(Protocol):
    """
    Descriptor for a property unit that has a specific unit, e.g. cm^2 or ft^2.
    """

    def isinstance(self, generic: GenericUnitDescriptor) -> bool:
        ...

    def to_generic(self) -> GenericUnitDescriptor:
        ...

    def __mul__(self, descriptor: "UnitDescriptor") -> "CompositeDimension":
        ...

    def __truediv__(self, descriptor: "UnitDescriptor") -> "CompositeDimension":
        ...

    def __hash__(self) -> int:
        ...

    def __str__(self) -> str:
        ...


@implements(GenericUnitDescriptor)
class MeasurementUnitMeta(EnumMeta):
    """
    Metaclass for `MeasurementUnit`. Defines multiplication, division and exponent
    operations for `MeasurementUnit` class (and subclasses). These operations produce
    `GenericUnitDescriptor(s)`.

    This metaclass is needed to be able to write expression like below:
    ```
    class Unit1(MeasurementUnit): ...
    class Unit2(MeasurementUnit): ...
    generic1 = Unit1 * Unit2
    generic2 = Unit1 / Unit2
    ```
    """

    def __mul__(unit_cls, other: GenericUnitDescriptor) -> "GenericCompositeDimension":
        if isinstance(other, GenericCompositeDimension):
            numerator = other.numerator.copy()
            denominator = other.denominator.copy()
            numerator.append(GenericDimension(unit_cls))
            return GenericCompositeDimension(
                numerator=numerator, denominator=denominator
            )
        elif isinstance(other, GenericDimension):
            return GenericCompositeDimension(
                numerator=[GenericDimension(unit_cls), other]
            )
        elif type(other) == MeasurementUnitType:
            return GenericCompositeDimension(
                numerator=[
                    GenericDimension(unit_cls),
                    GenericDimension(other),
                ]
            )
        raise InvalidUnitDescriptorBinaryOperation(
            f"cannot multiply {unit_cls} with {other}. "
        )

    def __truediv__(
        unit_cls, other: GenericUnitDescriptor
    ) -> "GenericCompositeDimension":
        if isinstance(other, GenericCompositeDimension):
            numerator = other.denominator.copy()
            denominator = other.numerator.copy()
            numerator.append(GenericDimension(unit_cls))
            return GenericCompositeDimension(
                numerator=numerator, denominator=denominator
            )
        elif isinstance(other, GenericDimension):
            return GenericCompositeDimension(
                numerator=[GenericDimension(unit_cls)], denominator=[other]
            )
        elif type(other) == MeasurementUnitType:
            return GenericCompositeDimension(
                numerator=[GenericDimension(unit_cls)],
                denominator=[GenericDimension(other)],
            )
        raise InvalidUnitDescriptorBinaryOperation(
            f"cannot divide {unit_cls} with {other}. "
        )

    def __pow__(unit_cls, power: Union[float, int]) -> "GenericDimension":
        return GenericDimension(unit_cls, power)


@implements(UnitDescriptor)
class MeasurementUnit(Enum, metaclass=MeasurementUnitMeta):
    """
    Base class for all measurement units of physical quantities.

    Each measurement-unit class is an enumeration of the available units for a
    quantity.

    Subclasses should only enumerate measurement units of primitive physical
    quantities, i.e. units that cannot be produced from other units.
    e.g. length is an acceptable quantity, but volume is not because its' units are
    produced from length units.
    """

    @staticmethod
    def from_descriptor(descriptor: UnitDescriptor) -> "MeasurementUnit":
        """
        Create a MeasurementUnit from given descriptor.

        Raises `WrongUnitDescriptorType` if given descriptor cannot be translated
        to a MeasurementUnit instance.
        """
        if isinstance(descriptor, Dimension):
            return descriptor.unit
        elif isinstance(descriptor, MeasurementUnit):
            return descriptor
        raise WrongUnitDescriptorType(
            f"cannot create MeasurementUnit from descriptor: {descriptor}"
        )

    def isinstance(self, generic: GenericUnitDescriptor) -> bool:
        return type(self) == generic

    def to_generic(self) -> GenericUnitDescriptor:
        return self.__class__

    def __mul__(self, descriptor: UnitDescriptor) -> "CompositeDimension":
        if isinstance(descriptor, MeasurementUnit):
            return Dimension(self) * Dimension(descriptor)
        elif isinstance(descriptor, (Dimension, CompositeDimension)):
            return Dimension(self) * descriptor
        raise InvalidUnitDescriptorBinaryOperation(
            f"cannot multiply {self} with {descriptor}. "
        )

    def __truediv__(self, descriptor: UnitDescriptor) -> "CompositeDimension":
        if isinstance(descriptor, MeasurementUnit):
            return Dimension(self) / Dimension(descriptor)
        elif isinstance(descriptor, (Dimension, CompositeDimension)):
            return Dimension(self) / descriptor
        raise InvalidUnitDescriptorBinaryOperation(
            f"cannot divide {self} with {descriptor}. "
        )

    def __pow__(self, power: Union[float, int]) -> "Dimension":
        return Dimension(self) ** power

    def __hash__(self) -> int:
        return hash(self.value)

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return self.value


# mypy does treat Type[MeasurementUnit] and MeasurementUnitMeta as equals.
# use MeasurementUnitType instead of Type[MeasurementUnit].
MeasurementUnitType: TypeAlias = MeasurementUnitMeta


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


class EnergyUnit(MeasurementUnit):
    JOULE = "J"
    KILO_JOULE = "kJ"
    MEGA_JOULE = "MJ"
    GIGA_JOULE = "GJ"
    CALORIE = "cal"
    KILO_CALORIE = "kcal"
    BTU = "Btu"


SI_UNITS: dict[MeasurementUnitType, MeasurementUnit] = {
    TemperatureUnit: TemperatureUnit.KELVIN,
    LengthUnit: LengthUnit.METER,
    MassUnit: MassUnit.KILO_GRAM,
    AmountUnit: AmountUnit.MOL,
    TimeUnit: TimeUnit.SECOND,
}


@dataclass
@implements(GenericUnitDescriptor)
class GenericDimension:
    """
    Represents a generic property unit or a generic property unit to some power.

    e.g. a generic dimension can be a temperature dimension or a volume dimension
    (length dimension to the 3rd power).
    """

    unit_type: MeasurementUnitType
    power: Union[float, int] = 1

    def __mul__(self, generic: GenericUnitDescriptor) -> "GenericCompositeDimension":
        if isinstance(generic, GenericCompositeDimension):
            numerator = generic.numerator.copy()
            denominator = generic.denominator.copy()
            numerator.append(self)
            return GenericCompositeDimension(
                numerator=numerator, denominator=denominator
            )
        elif isinstance(generic, GenericDimension):
            return GenericCompositeDimension(numerator=[self, generic])
        elif type(generic) == MeasurementUnitType:
            return GenericCompositeDimension(
                numerator=[self, GenericDimension(generic)]
            )
        raise InvalidUnitDescriptorBinaryOperation(
            f"cannot multiply {self} with {generic}. "
        )

    def __truediv__(
        self, generic: GenericUnitDescriptor
    ) -> "GenericCompositeDimension":
        if isinstance(generic, GenericCompositeDimension):
            numerator = generic.denominator.copy()
            denominator = generic.numerator.copy()
            numerator.append(self)
            return GenericCompositeDimension(
                numerator=numerator, denominator=denominator
            )
        elif isinstance(generic, GenericDimension):
            return GenericCompositeDimension(numerator=[self], denominator=[generic])
        elif type(generic) == MeasurementUnitType:
            return GenericCompositeDimension(
                numerator=[self], denominator=[GenericDimension(generic)]
            )
        raise InvalidUnitDescriptorBinaryOperation(
            f"cannot divide {self} with {generic}. "
        )

    def __pow__(self, power: Union[float, int]) -> "GenericDimension":
        self.power *= power
        return self

    def __eq__(self, generic) -> bool:
        if not isinstance(generic, GenericDimension):
            return False
        return self.unit_type == generic.unit_type and self.power == generic.power

    def __hash__(self) -> int:
        return hash(str(self))


@dataclass
@implements(UnitDescriptor)
class Dimension:
    """
    A `Dimension` is a wrapper around `MeasurementUnit`.

    Objects of this class can represent either a simple `MeasurementUnit` or a
    `MeasurementUnit` to some power.

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

    @staticmethod
    def from_descriptor(descriptor: UnitDescriptor) -> "Dimension":
        """
        Create a Dimension from given descriptor.

        Raises `WrongUnitDescriptorType` if given descriptor cannot be translated
        to a Dimension instance.
        """
        if isinstance(descriptor, Dimension):
            return descriptor
        elif isinstance(descriptor, MeasurementUnit):
            return Dimension(descriptor)
        raise WrongUnitDescriptorType(
            f"cannot create Dimension from descriptor: {descriptor}"
        )

    def isinstance(self, generic: GenericUnitDescriptor) -> bool:
        if type(generic) == MeasurementUnitType:
            generic = GenericDimension(generic)
        if not isinstance(generic, GenericDimension):
            return False
        if isinstance(self.unit, generic.unit_type) and self.power == generic.power:
            return True
        return False

    def to_generic(self) -> GenericDimension:
        return GenericDimension(type(self.unit), self.power)

    def __mul__(self, descriptor: "UnitDescriptor") -> "CompositeDimension":
        if isinstance(descriptor, CompositeDimension):
            numerator = descriptor.numerator.copy()
            denominator = descriptor.denominator.copy()
            numerator.append(self)
            return CompositeDimension(numerator=numerator, denominator=denominator)
        elif isinstance(descriptor, Dimension):
            return CompositeDimension(numerator=[self, descriptor])
        elif isinstance(descriptor, MeasurementUnit):
            return CompositeDimension(numerator=[self, Dimension(descriptor)])
        raise InvalidUnitDescriptorBinaryOperation(
            f"cannot multiply {self} with {descriptor}. "
        )

    def __truediv__(self, descriptor: "UnitDescriptor") -> "CompositeDimension":
        if isinstance(descriptor, CompositeDimension):
            numerator = descriptor.denominator.copy()
            denominator = descriptor.numerator.copy()
            numerator.append(self)
            return CompositeDimension(numerator=numerator, denominator=denominator)
        elif isinstance(descriptor, Dimension):
            return CompositeDimension(numerator=[self], denominator=[descriptor])
        elif isinstance(descriptor, MeasurementUnit):
            return CompositeDimension(
                numerator=[self], denominator=[Dimension(descriptor)]
            )
        raise InvalidUnitDescriptorBinaryOperation(
            f"cannot divide {self} with  {descriptor}. "
        )

    def __pow__(self, power: Union[float, int]) -> "Dimension":
        if isinstance(self, CompositeDimension):
            raise InvalidUnitDescriptorBinaryOperation(
                "power operand `**` is not supported for CompositeDimension. "
            )
        self.power *= power
        return self

    def __hash__(self) -> int:
        return hash(str(self))

    def __eq__(self, dimension) -> bool:
        if not isinstance(dimension, Dimension):
            return False
        return self.unit == dimension.unit and self.power == dimension.power

    def __repr__(self) -> str:
        return "Dimension: " + str(self)

    def __str__(self) -> str:
        if self.power != 1:
            return "(" + self.unit.value + ") ^ " + str(self.power)
        return self.unit.value


@dataclass
@implements(GenericUnitDescriptor)
class GenericCompositeDimension:
    """
    A `GenericCompositeDimension` represents a generic measurement unit that is composed
    from other generic measurement units.

    Objects of this class can represent either multiplication or division between two
    `GenericDimension` objects.

    Create objects by multiplying and diving `GenericDimension` or `MeasurementUnitMeta`
    objects:
    ```
    generic_molal_volume_dimension = (
        (GenericDimension(LengthUnit) ** 3) / GenericDimension(AmountUnit)
    )  # [volume/amount]

    # the same as above
    generic_molal_volume_dimension = (LengthUnit**3) / AmountUnit
    """

    numerator: List[GenericDimension] = field(default_factory=list)
    denominator: List[GenericDimension] = field(default_factory=list)

    def __mul__(self, generic: GenericUnitDescriptor) -> "GenericCompositeDimension":
        numerator = self.numerator.copy()
        denominator = self.denominator.copy()
        if isinstance(generic, GenericCompositeDimension):
            numerator.extend(generic.numerator)
            denominator.extend(generic.denominator)
            return GenericCompositeDimension(
                numerator=numerator, denominator=denominator
            )

        elif isinstance(generic, GenericDimension):
            numerator.append(generic)
            return GenericCompositeDimension(
                numerator=numerator, denominator=denominator
            )

        elif type(generic) == MeasurementUnitType:
            numerator.append(GenericDimension(generic))
            return GenericCompositeDimension(
                numerator=numerator, denominator=denominator
            )
        raise InvalidUnitDescriptorBinaryOperation(
            f"cannot multiply {self} with {generic}. "
        )

    def __truediv__(
        self, generic: GenericUnitDescriptor
    ) -> "GenericCompositeDimension":
        numerator = self.numerator.copy()
        denominator = self.denominator.copy()
        if isinstance(generic, GenericCompositeDimension):
            numerator.extend(generic.denominator)
            denominator.extend(generic.numerator)
            return GenericCompositeDimension(
                numerator=numerator, denominator=denominator
            )
        elif isinstance(generic, GenericDimension):
            denominator.append(generic)
            return GenericCompositeDimension(
                numerator=numerator, denominator=denominator
            )
        elif type(generic) == MeasurementUnitType:
            denominator.append(GenericDimension(generic))
            return GenericCompositeDimension(
                numerator=numerator, denominator=denominator
            )
        raise InvalidUnitDescriptorBinaryOperation(
            f"cannot divide {self} with {generic}. "
        )

    def __eq__(self, generic) -> bool:
        if not isinstance(generic, GenericCompositeDimension):
            return False
        return set(self.numerator) == set(generic.numerator) and set(
            self.denominator
        ) == set(generic.denominator)

    def __hash__(self) -> int:
        return hash(str(self))

    def __str__(self):
        numerators = " * ".join(sorted([str(n) for n in self.numerator]))
        denominators = " / ".join(sorted([str(d) for d in self.denominator]))
        if len(denominators) > 0:
            denominators = " / " + denominators
        return numerators + denominators


@dataclass
@implements(UnitDescriptor)
class CompositeDimension:
    """
    A `CompositeDimension` represents a measurement unit that is composed from other
    measurement units.

    Objects of this class can represent either multiplication or division between two
    `Dimension` objects.

    Create objects by multiplying and diving `Dimension` or `MeasurementUnit` objects:
    ```
    molal_volume_dimension = (
        (Dimension(LengthUnit.METER) ** 3) / Dimension(AmountUnit.KILO_MOL)
    )  # [m^3/kmol]

    # the same as above
    molal_volume_dimension = (LengthUnit.METER**3) / AmountUnit.KILO_MOL
    ```
    """

    Default = TypeVar("Default")  # default return type for `get` functions.

    numerator: List[Dimension] = field(default_factory=list)
    denominator: List[Dimension] = field(default_factory=list)

    @staticmethod
    def from_descriptor(descriptor: UnitDescriptor) -> "CompositeDimension":
        """
        Create a CompositeDimension from given descriptor.

        Raises `WrongUnitDescriptorType` if given descriptor cannot be translated
        to a CompositeDimension instance.
        """
        if not isinstance(descriptor, CompositeDimension):
            raise WrongUnitDescriptorType(
                f"cannot create CompositeDimension from descriptor {descriptor}"
            )
        return descriptor

    def isinstance(self, generic: GenericUnitDescriptor) -> bool:
        if not isinstance(generic, GenericCompositeDimension):
            return False
        return self.to_generic() == generic

    def to_generic(self) -> GenericCompositeDimension:
        return GenericCompositeDimension(
            numerator=[n.to_generic() for n in self.numerator],
            denominator=[d.to_generic() for d in self.denominator],
        )

    def get_numerator(
        self, generic: GenericDimension, default: Optional[Default] = None
    ) -> Union[Dimension, Optional[Default]]:
        for n in self.numerator:
            if n.isinstance(generic):
                return n
        return default

    def get_denominator(
        self, generic: GenericDimension, default: Optional[Default] = None
    ) -> Union[Dimension, Optional[Default]]:
        for d in self.denominator:
            if d.isinstance(generic):
                return d
        return default

    def __mul__(self, descriptor: "UnitDescriptor") -> "CompositeDimension":
        numerator = self.numerator.copy()
        denominator = self.denominator.copy()
        if isinstance(descriptor, CompositeDimension):
            numerator.extend(descriptor.numerator)
            denominator.extend(descriptor.denominator)
            return CompositeDimension(numerator=numerator, denominator=denominator)
        elif isinstance(descriptor, Dimension):
            numerator.append(descriptor)
            return CompositeDimension(numerator=numerator, denominator=denominator)
        elif isinstance(descriptor, MeasurementUnit):
            numerator.append(Dimension(descriptor))
            return CompositeDimension(numerator=numerator, denominator=denominator)
        raise InvalidUnitDescriptorBinaryOperation(
            f"cannot multiply {self} with {descriptor}. "
        )

    def __truediv__(self, descriptor: "UnitDescriptor") -> "CompositeDimension":
        numerator = self.numerator.copy()
        denominator = self.denominator.copy()
        if isinstance(descriptor, CompositeDimension):
            numerator.extend(descriptor.denominator)
            denominator.extend(descriptor.denominator)
            return CompositeDimension(numerator=numerator, denominator=denominator)
        elif isinstance(descriptor, Dimension):
            denominator.append(descriptor)
            return CompositeDimension(numerator=numerator, denominator=denominator)
        elif isinstance(descriptor, MeasurementUnit):
            denominator.append(Dimension(descriptor))
            return CompositeDimension(numerator=numerator, denominator=denominator)
        raise InvalidUnitDescriptorBinaryOperation(
            f"cannot divide {self} with {descriptor}. "
        )

    def __hash__(self) -> int:
        return hash(str(self))

    def __eq__(self, dimension) -> bool:
        if not isinstance(dimension, CompositeDimension):
            return False
        return set(self.numerator) == set(dimension.numerator) and set(
            self.denominator
        ) == set(dimension.denominator)

    def __str__(self):
        numerators = " * ".join(sorted([str(n) for n in self.numerator]))
        denominators = " / ".join(sorted([str(d) for d in self.denominator]))
        if len(denominators) > 0:
            denominators = " / " + denominators
        return numerators + denominators
