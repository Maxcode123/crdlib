from enum import Enum
from typing import Iterable

from crdlib.chemical_substances.substance import ChemicalSubstance
from crdlib.phases.phase import Phase


class BalanceTerm(Enum):
    ACCUMULATION = "ACCUMULATION"


class MolecularBalanceTerm(BalanceTerm):
    REACTION_RATE = "REACTION_RATE"
    CONVECTION = "CONVECTION"
    DIFFUSION = "DIFFUSION"
    SURFACE_TRANSFER = "SURFACE_TRANSFER"


class EnergyBalanceTerm(BalanceTerm):
    REACTION_ENERGY = "REACTION_ENERGY"
    CONVECTION = "CONVECTION"
    CONDUCTION = "CONDUCTION"
    SURFACE_TRANSFER = "SURFACE_TRANSFER"


class Balance:
    """
    A balance equation in the Model domain.
    """
    pass


class MolecularBalance(Balance):
    species: ChemicalSubstance
    terms: Iterable[MolecularBalanceTerm]


class EnergyBalance(Balance):
    phase: Phase
    terms: Iterable[EnergyBalanceTerm]
