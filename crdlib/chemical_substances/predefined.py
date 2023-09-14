from enum import Enum

from crdlib.chemical_substances.substance import (
    ChemicalElement, ChemicalCompound)

class PredefinedChemicalSubstances(Enum):
    HYDROGEN = ChemicalElement(...)
    OXYGEN = ChemicalElement(...)
    WATER = ChemicalCompound(...)
