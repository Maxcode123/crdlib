from enum import Enum
from dataclasses import dataclass


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
class Atom:
    atomic_number: int
    atomic_mass: float
    symbol: str
    chemical_group: ChemicalGroup
