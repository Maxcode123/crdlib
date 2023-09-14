from typing import Iterable, Any

from pydantic import BaseModel

from crdlib.chemical_substances.substance import ChemicalSubstance

class ChemicalReaction(BaseModel):
    reactants: Iterable[ChemicalSubstance]
    products: Iterable[ChemicalSubstance]
    properties: dict[str, Any]
