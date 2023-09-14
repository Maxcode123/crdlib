from typing import Iterable

from pydantic import BaseModel

from crdlib.chemical_substances.atom import Atom


class ChemicalSubstance(BaseModel):
    pass


class ChemicalElement(ChemicalSubstance):
    atom: Atom
    number_of_atoms: int

class ChemicalCompound(ChemicalSubstance):
    elements: Iterable[ChemicalElement]
