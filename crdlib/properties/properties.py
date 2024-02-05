from dataclasses import dataclass
from typing import Type, ClassVar, TypeAlias
from typing_extensions import Self
from abc import ABCMeta, abstractmethod

from crdlib.properties.units.units import (
    TemperatureUnit,
    PressureUnit,
    LengthUnit,
    MassUnit,
    AmountUnit,
    TimeUnit,
    EnergyUnit,
)
from crdlib.properties.units.descriptors import (
    MeasurementUnit,
    Dimension,
    CompositeDimension,
    UnitDescriptor,
    GenericUnitDescriptor,
    AliasedMeasurementUnit,
)
from crdlib.properties.units.converters import (
    get_converter,
    PhysicalPropertyUnitConverter,
)
from crdlib.properties.exceptions import WrongUnitDescriptorType


class AbstractPhysicalProperty(metaclass=ABCMeta):
    """
    Base class for different types of physical properties.
    """

    value: float
    unit_descriptor: UnitDescriptor
    generic_descriptor: ClassVar[GenericUnitDescriptor]

    @abstractmethod
    def __init__(self, value: float, unit: UnitDescriptor) -> None:
        ...

    def to_unit(self, unit: UnitDescriptor) -> Self:
        """
        Create a new PhysicalProperty object with specified unit.
        """
        return self.from_physical_property(self, unit)

    @classmethod
    def from_physical_property(
        cls, physical_property: "AbstractPhysicalProperty", to_unit: UnitDescriptor
    ) -> Self:
        """
        Create a new PhysicalProperty object with specified unit from given object.
        """
        return cls(
            value=cls._get_converter().convert(
                physical_property.value,
                physical_property.unit_descriptor,
                to_unit,
            ),
            unit=to_unit,
        )

    @classmethod
    def _get_converter(cls) -> Type[PhysicalPropertyUnitConverter]:
        return get_converter(cls.generic_descriptor)


@dataclass
class PhysicalProperty(AbstractPhysicalProperty):
    """
    A physical property with a generic unit descriptor of type `MeasurementUnit`.

    e.g.\n
    Temperature is a PhysicalProperty because its' generic unit descriptor is
    `TemperatureUnit`.\n
    Enthalpy is not a PhysicalProperty because its' generic unit descriptor is
    EnergyUnit / MassUnit, which is a `CompositeDimension`.
    """

    def __init__(self, value: float, unit: UnitDescriptor) -> None:
        self.value = value
        try:
            self.unit_descriptor = MeasurementUnit.from_descriptor(unit)
        except WrongUnitDescriptorType:
            raise WrongUnitDescriptorType(
                f"cannot instantiate {self.__class__.__name__} with unit: {unit}. "
            )


@dataclass
class ExponentPhysicalProperty(AbstractPhysicalProperty):
    """
    A physical property with a generic unit descriptor of type `Dimension`.

    An exponent physical property is produced from raising a physical property to some
    power. e.g. Volume is produced by raising Length to the 3rd power.
    """

    def __init__(self, value: float, unit: UnitDescriptor) -> None:
        self.value = value
        try:
            self.unit_descriptor = Dimension.from_descriptor(unit)
        except WrongUnitDescriptorType:
            raise WrongUnitDescriptorType(
                f"cannot instantiate {self.__class__.__name__} with unit: {unit}. "
            )


@dataclass
class AliasedPhysicalProperty(AbstractPhysicalProperty):
    """A physical property with an aliased generic unit descriptor."""

    base_units_generic_descriptor: ClassVar[GenericUnitDescriptor]
    reference_unit_mapping: ClassVar[dict[str, UnitDescriptor]]

    def __init__(self, value: float, unit: UnitDescriptor) -> None:
        self.value = value
        try:
            self.unit_descriptor = AliasedMeasurementUnit.from_descriptor(unit)
        except WrongUnitDescriptorType:
            raise WrongUnitDescriptorType(
                f"cannot instantiate {self.__class__.__name__} with unit: {unit}"
            )

    def to_base_units(self) -> "CompositePhysicalProperty":
        """
        Create a new `CompositePhyicalProperty` from this aliased property by converting
        to composite base units.
        """
        return CompositePhysicalProperty(
            value=self.to_unit(self.reference_unit_mapping["alias"]).value,
            unit=self.reference_unit_mapping["composite"],
        )


@dataclass
class CompositePhysicalProperty(AbstractPhysicalProperty):
    """
    A physical property with a generic unit descriptor of type `CompositeDimension`
    """

    def __init__(self, value: float, unit: UnitDescriptor) -> None:
        self.value = value
        try:
            self.unit_descriptor = CompositeDimension.from_descriptor(unit)
        except WrongUnitDescriptorType:
            raise WrongUnitDescriptorType(
                f"cannot instantiate {self.__class__.__name__} with unit: {unit}"
            )


@dataclass
class AliasedCompositePhysicalProperty(AbstractPhysicalProperty):
    """
    A physical property with a generic unit descriptor of type `CompositeDimension`
    that includes `AliasedMeasurementUnit`s.
    """

    base_units_generic_descriptor: ClassVar[GenericUnitDescriptor]
    reference_unit_mapping: ClassVar[dict[str, UnitDescriptor]]

    def __init__(self, value: float, unit: UnitDescriptor) -> None:
        self.value = value
        try:
            self.unit_descriptor = CompositeDimension.from_descriptor(unit)
        except WrongUnitDescriptorType:
            raise WrongUnitDescriptorType(
                f"cannot instantiate {self.__class__.__name__} with unit: {unit}"
            )

    def to_base_units(self) -> "CompositePhysicalProperty":
        """
        Create a new `CompositePhyicalProperty` from this aliased property by converting
        to composite base units.
        """
        return CompositePhysicalProperty(
            value=self.to_unit(self.reference_unit_mapping["alias"]).value,
            unit=self.reference_unit_mapping["composite"],
        )


class Temperature(PhysicalProperty):
    generic_descriptor = TemperatureUnit


class Length(PhysicalProperty):
    generic_descriptor = LengthUnit


class Mass(PhysicalProperty):
    generic_descriptor = MassUnit


class Amount(PhysicalProperty):
    generic_descriptor = AmountUnit


class Time(PhysicalProperty):
    generic_descriptor = TimeUnit


class Volume(ExponentPhysicalProperty):
    generic_descriptor = LengthUnit**3


class Pressure(AliasedPhysicalProperty):
    generic_descriptor = PressureUnit
    base_units_generic_descriptor = MassUnit / LengthUnit / (TimeUnit**2)
    reference_unit_mapping = {
        "alias": PressureUnit.PASCAL,
        "composite": MassUnit.KILO_GRAM / LengthUnit.METER / (TimeUnit.SECOND**2),
    }


class Energy(AliasedPhysicalProperty):
    generic_descriptor = EnergyUnit
    base_units_generic_descriptor = MassUnit * (LengthUnit**2) / (TimeUnit**2)
    reference_unit_mapping = {
        "alias": EnergyUnit.JOULE,
        "composite": MassUnit.KILO_GRAM
        * (LengthUnit.METER**2)
        / (TimeUnit.SECOND**2),
    }


class MassRate(CompositePhysicalProperty):
    generic_descriptor = MassUnit / TimeUnit


class MolarVolume(CompositePhysicalProperty):
    generic_descriptor = (LengthUnit**3) / AmountUnit


class MolarEnergy(AliasedCompositePhysicalProperty):
    generic_descriptor = EnergyUnit / AmountUnit
    base_units_generic_descriptor = Energy.base_units_generic_descriptor / AmountUnit
    reference_unit_mapping = {
        "alias": Energy.reference_unit_mapping["alias"] / AmountUnit.MOL,
        "composite": Energy.reference_unit_mapping["composite"] / AmountUnit.MOL,
    }


FormationEnthalpy: TypeAlias = MolarEnergy
FormationGibbsFreeEnergy: TypeAlias = MolarEnergy


class GasConstant(CompositePhysicalProperty):
    generic_descriptor = (
        MassUnit * (LengthUnit**2) / (TimeUnit**2) / TemperatureUnit / AmountUnit
    )


class ThermalCapacity(AliasedCompositePhysicalProperty):
    generic_descriptor = EnergyUnit / AmountUnit / TemperatureUnit
    base_units_generic_descriptor = (
        MolarEnergy.base_units_generic_descriptor / TemperatureUnit
    )
    reference_unit_mapping = {
        "alias": MolarEnergy.reference_unit_mapping["alias"] / TemperatureUnit.KELVIN,
        "composite": MolarEnergy.reference_unit_mapping["composite"]
        / TemperatureUnit.KELVIN,
    }


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
