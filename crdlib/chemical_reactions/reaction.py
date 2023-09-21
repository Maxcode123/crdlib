from typing import Iterable
from dataclasses import dataclass
from abc import ABCMeta

from crdlib.chemical_substances.substance import ChemicalReactionFactors
from crdlib.equations.equation import Term


@dataclass
class ChemicalReaction:
    reactants: ChemicalReactionFactors
    products: ChemicalReactionFactors
    reaction_rate: Term

    @property
    def thermodynamical_properties(self):
        pass
