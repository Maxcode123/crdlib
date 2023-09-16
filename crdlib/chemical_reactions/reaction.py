from typing import Iterable

from pydantic import BaseModel

from crdlib.chemical_substances.substance import ChemicalSubstance
from crdlib.equations.equation import Term


class ChemicalReaction(BaseModel):
    reactants: Iterable[ChemicalSubstance]
    products: Iterable[ChemicalSubstance]
    reaction_rate: Term

    @property
    def thermodynamical_properties(self):
        pass
