from typing import Iterable, Optional, Union, List
from dataclasses import dataclass

from crdlib.chemical_substances.atom import Atom
from crdlib.properties.properties import Temperature, Pressure, Volume


@dataclass
class CriticalProperties:
    temperature: Temperature
    pressure: Pressure
    volume: Volume


@dataclass
class ChemicalSubstance:
    molecular_weight: float
    critical_properties: Optional[CriticalProperties]


class ChemicalElement(ChemicalSubstance):
    atom: Atom
    number_of_atoms: int
    symbol: str

    def __init__(
        self,
        atom: Atom,
        number_of_atoms: int,
        critical_properties: Optional[CriticalProperties] = None,
    ) -> None:
        self.atom = atom
        self.number_of_atoms = number_of_atoms
        self.critical_properties = critical_properties
        self.molecular_weight = self.atom.atomic_mass * number_of_atoms
        self.symbol = atom.symbol + str(number_of_atoms)


class ChemicalCompound(ChemicalSubstance):
    elements: Iterable[ChemicalElement]

    def __init__(
        self,
        elements: Iterable[Union[ChemicalElement, Atom]],
        critical_properties: Optional[CriticalProperties] = None,
    ) -> None:
        _elements: List[ChemicalElement] = []
        for element in elements:
            if isinstance(element, Atom):
                _elements.append(ChemicalElement(element, 1))
            else:
                _elements.append(element)
        self.elements = _elements
        self.molecular_weight = sum([e.molecular_weight for e in _elements])
        self.critical_properties = critical_properties
