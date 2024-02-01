from typing import Iterable, Optional, Union, List, Protocol
from dataclasses import dataclass
from abc import ABCMeta
from enum import Enum

from crdlib.chemical_substances.exceptions import (
    InvalidChemicalReactionFactorBinaryOperation,
    InvalidChemicalCompoundComponentBinaryOperation,
)
from crdlib.properties.properties import (
    Temperature,
    Pressure,
    MolarVolume,
    FormationEnthalpy,
    FormationGibbsFreeEnergy,
)
from crdlib.properties.units import TemperatureUnit
from crdlib.utils.protocols import implements


class ChemicalCompoundComponent(Protocol):
    def __lshift__(self, other: "ChemicalCompoundComponent") -> "ChemicalCompound":
        ...


class ChemicalReactionFactor(Protocol):
    def __mul__(self, coeff: int) -> "ChemicalReactionParticipant":
        ...

    def __add__(self, other: "ChemicalReactionFactor") -> "ChemicalReactionFactors":
        ...


class ChemicalGroup(str, Enum):
    NON_METAL = "NON_METAL"
    NOBLE_GAS = "NOBLE_GAS"
    ALKALI_METAL = "ALKALI_METAL"
    ALKALINE_EARTH_METAL = "ALKALINE_EARTH_METAL"
    METALLOID = "METALLOID"
    HALOGEN = "HALOGEN"
    POST_TRANSITION_METAL = "POST_TRANSITION_METAL"
    TRANSITION_METAL = "TRANSITION_METAL"
    LANTHANIDE = "LANTHANIDE"
    ACTINIDE = "ACTINIDE"


@dataclass(frozen=True)
@implements(ChemicalCompoundComponent)
class Atom:
    atomic_number: int
    atomic_mass: float
    symbol: str
    chemical_group: ChemicalGroup

    def __mul__(self, coeff: int) -> "ChemicalElement":
        if not isinstance(coeff, int) or coeff <= 0:
            raise InvalidChemicalCompoundComponentBinaryOperation(
                f"cannot multiply {self} with {coeff}; `number_of_atoms` must"
                " be a positive int. "
            )
        return ChemicalElement(self, coeff)

    def __lshift__(self, other: ChemicalCompoundComponent) -> "ChemicalCompound":
        if isinstance(other, (Atom, ChemicalElement)):
            return ChemicalCompound([self, other])
        elif isinstance(other, ChemicalCompound):
            elements = other.elements
            elements.append(ChemicalElement(self))
            return ChemicalCompound(elements)
        else:
            raise InvalidChemicalCompoundComponentBinaryOperation(
                f"cannot add {other} to {self}. "
            )


@dataclass
class ChemicalReactionFactors:
    participants: List["ChemicalReactionParticipant"]

    def __init__(self, factors: Iterable[ChemicalReactionFactor]) -> None:
        _factors = []
        for f in factors:
            if isinstance(f, (ChemicalCompound, ChemicalElement)):
                _factors.append(ChemicalReactionParticipant(f))
            elif isinstance(f, ChemicalReactionParticipant):
                _factors.append(f)
            else:
                raise TypeError(f"cannot create ChemicalReactionFactors with {f}. ")
        self.participants = _factors

    def __mul__(self, coeff: int) -> "ChemicalReactionFactors":
        if not isinstance(coeff, int) or coeff <= 0:
            raise InvalidChemicalReactionFactorBinaryOperation(
                f"cannot multiply chemical reaction factors with {coeff}; `coeff` must"
                " be an int. "
            )
        for f in self.participants:
            f *= coeff
        return self

    def __add__(self, other: ChemicalReactionFactor) -> "ChemicalReactionFactors":
        if isinstance(other, ChemicalReactionParticipant):
            self.participants.append(other)
        elif isinstance(other, (ChemicalCompound, ChemicalElement)):
            self.participants.append(ChemicalReactionParticipant(other))
        else:
            raise InvalidChemicalReactionFactorBinaryOperation(
                f"cannot add {other} to chemical reaction factors. "
            )
        return self


@dataclass
class CriticalProperties:
    temperature: Temperature
    pressure: Pressure
    volume: MolarVolume


@dataclass
class StandardFormationProperties:
    enthalpy: FormationEnthalpy
    gibbs_free_energy: FormationGibbsFreeEnergy
    temperature: Temperature = Temperature(25, TemperatureUnit.CELCIUS)


@dataclass
@implements(ChemicalReactionFactor)
class ChemicalSubstance(metaclass=ABCMeta):
    molecular_weight: float
    symbol: Optional[str]
    critical_properties: Optional[CriticalProperties]
    standard_formation_properties: Optional[StandardFormationProperties]

    def set_critical_properties(self, critical_properties: CriticalProperties) -> None:
        self.critical_properties = critical_properties

    def set_standard_formation_properties(
        self, standard_formation_properties: StandardFormationProperties
    ) -> None:
        self.standard_formation_properties = standard_formation_properties

    def set_symbol(self, symbol: str) -> None:
        self.symbol = symbol

    def __mul__(self, coeff: int) -> "ChemicalReactionParticipant":
        if not isinstance(coeff, int) or coeff <= 0:
            raise InvalidChemicalReactionFactorBinaryOperation(
                f"cannot multiply {self} with {coeff}; `coeff` must be an int. "
            )
        return ChemicalReactionParticipant(self, coeff)

    def __add__(self, other: ChemicalReactionFactor) -> ChemicalReactionFactors:
        if isinstance(other, (Atom, ChemicalElement, ChemicalCompound)):
            return ChemicalReactionFactors(
                [ChemicalReactionParticipant(self, 1), other]
            )
        raise InvalidChemicalReactionFactorBinaryOperation(
            f"cannot add {other} to {self}. "
        )


@implements(ChemicalCompoundComponent)
class ChemicalElement(ChemicalSubstance):
    atom: Atom
    number_of_atoms: int

    def __init__(
        self,
        atom: Atom,
        number_of_atoms: int = 1,
        critical_properties: Optional[CriticalProperties] = None,
        standard_formation_properties: Optional[StandardFormationProperties] = None,
    ) -> None:
        self.atom = atom
        self.number_of_atoms = number_of_atoms
        self.critical_properties = critical_properties
        self.standard_formation_properties = standard_formation_properties
        self.molecular_weight = self.atom.atomic_mass * number_of_atoms
        self.symbol = atom.symbol + str(number_of_atoms)

    def __lshift__(self, other: "ChemicalCompoundComponent") -> "ChemicalCompound":
        if isinstance(other, (Atom, ChemicalElement)):
            return ChemicalCompound([self, other])
        elif isinstance(other, ChemicalCompound):
            elements = other.elements
            elements.append(self)
            return ChemicalCompound(elements)
        else:
            raise InvalidChemicalCompoundComponentBinaryOperation(
                f"cannot add {other} to {self}. "
            )


@implements(ChemicalCompoundComponent)
class ChemicalCompound(ChemicalSubstance):
    elements: list[ChemicalElement]

    def __init__(
        self,
        elements: Iterable[Union[ChemicalElement, Atom]],
        symbol: Optional[str] = None,
        critical_properties: Optional[CriticalProperties] = None,
        standard_formation_properties: Optional[StandardFormationProperties] = None,
    ) -> None:
        _elements: List[ChemicalElement] = []
        for element in elements:
            if isinstance(element, Atom):
                _elements.append(ChemicalElement(element))
            else:
                _elements.append(element)
        self.elements = _elements
        self.symbol = symbol
        self.critical_properties = critical_properties
        self.standard_formation_properties = standard_formation_properties
        self.molecular_weight = sum([e.molecular_weight for e in self.elements])

    def __lshift__(self, other: "ChemicalCompoundComponent") -> "ChemicalCompound":
        elements = self.elements
        if isinstance(other, Atom):
            elements.append(ChemicalElement(other))
            return ChemicalCompound(elements)
        elif isinstance(other, ChemicalElement):
            elements.append(other)
            return ChemicalCompound(elements)
        elif isinstance(other, ChemicalCompound):
            elements.extend(other.elements)
            return ChemicalCompound(elements)
        else:
            raise InvalidChemicalCompoundComponentBinaryOperation(
                f"cannot add {other} to {self}. "
            )


@dataclass
@implements(ChemicalReactionFactor)
class ChemicalReactionParticipant:
    substance: ChemicalSubstance
    stoichiometric_coefficient: int = 1

    def __mul__(self, coeff: int) -> "ChemicalReactionParticipant":
        self.stoichiometric_coefficient *= coeff
        return self

    def __add__(self, other: ChemicalReactionFactor) -> ChemicalReactionFactors:
        return ChemicalReactionFactors([self, other])
