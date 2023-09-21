from typing import Iterable, Optional, Union, List, Protocol
from dataclasses import dataclass
from abc import ABCMeta
from enum import Enum

from crdlib.chemical_substances.exceptions import (
    InvalidChemicalReactionFactorBinaryOperation,
    InvalidChemicalCompoundComponentBinaryOperation,
)
from crdlib.properties.properties import Temperature, Pressure, Volume
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

    def __mul__(self, number_of_atoms: int) -> "ChemicalElement":
        if not isinstance(number_of_atoms, int) or number_of_atoms <= 0:
            raise InvalidChemicalCompoundComponentBinaryOperation(
                f"cannot multiply {self} with {number_of_atoms}; `number_of_atoms` must"
                " be a positive int. "
            )
        return ChemicalElement(self, number_of_atoms)

    def __lshift__(self, other: ChemicalCompoundComponent) -> "ChemicalCompound":
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


@dataclass
class ChemicalReactionFactors:
    factors: List[ChemicalReactionFactor]

    def __mul__(self, coeff: int) -> "ChemicalReactionFactors":
        if not isinstance(coeff, int):
            raise InvalidChemicalReactionFactorBinaryOperation(
                f"cannot multiply chemical reaction factors with {coeff}; `coeff` must"
                " be an int. "
            )
        for f in self.factors:
            f *= coeff

    def __add__(self, other: ChemicalReactionFactor) -> "ChemicalReactionFactors":
        if isinstance(other, ChemicalSubstance, ChemicalReactionParticipant):
            self.factors.append(other)
        else:
            raise InvalidChemicalReactionFactorBinaryOperation(
                f"cannot add {other} to chemical reaction factors. "
            )


@dataclass
class CriticalProperties:
    temperature: Temperature
    pressure: Pressure
    volume: Volume


@dataclass
@implements(ChemicalReactionFactor)
class ChemicalSubstance(metaclass=ABCMeta):
    molecular_weight: float
    critical_properties: Optional[CriticalProperties]

    def __mul__(self, coeff: int) -> "ChemicalReactionParticipant":
        if not isinstance(coeff, int):
            raise InvalidChemicalReactionFactorBinaryOperation(
                f"cannot multiply {self} with {coeff}; `coeff` must be an int. "
            )
        return ChemicalReactionParticipant(self, coeff)

    def __add__(self, other: ChemicalReactionFactor) -> ChemicalReactionFactors:
        return ChemicalReactionFactors([ChemicalReactionParticipant(self, 1), other])


@dataclass
@implements(ChemicalCompoundComponent)
class ChemicalElement(ChemicalSubstance):
    atom: Atom
    number_of_atoms: int
    symbol: str

    def __init__(
        self,
        atom: Atom,
        number_of_atoms: int = 1,
        critical_properties: Optional[CriticalProperties] = None,
    ) -> None:
        self.atom = atom
        self.number_of_atoms = number_of_atoms
        self.critical_properties = critical_properties
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
        critical_properties: Optional[CriticalProperties] = None,
    ) -> None:
        _elements: List[ChemicalElement] = []
        for element in elements:
            if isinstance(element, Atom):
                _elements.append(ChemicalElement(element))
            else:
                _elements.append(element)
        self.elements = _elements
        self.critical_properties = critical_properties
        self.molecular_weight = sum([e.molecular_weight for e in self.elements])

    def __lshift__(self, other: "ChemicalCompoundComponent") -> "ChemicalCompound":
        elements = self.elements
        if isinstance(other, (Atom, ChemicalElement)):
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
    stoichiometric_coefficient: int

    def __mul__(self, coeff: int) -> "ChemicalReactionParticipant":
        self.stoichiometric_coefficient *= coeff
        return self

    def __add__(self, other: ChemicalReactionFactor) -> ChemicalReactionFactors:
        return ChemicalReactionFactors([self, other])
