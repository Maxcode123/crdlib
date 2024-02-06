from random import randint, random
from typing import Optional

from crdlib.chemical_substances.substance import (
    ChemicalElement,
    Atom,
    ChemicalSubstance,
    ChemicalGroup,
)


class SubstanceFactory:
    @staticmethod
    def build() -> ChemicalSubstance:
        return ChemicalElement(AtomFactory.build())


class AtomFactory:
    @staticmethod
    def build(
        atomic_number: Optional[int] = None,
        atomic_mass: Optional[float] = None,
        symbol: str = "_",
        chemical_group: ChemicalGroup = ChemicalGroup.NON_METAL,
    ) -> Atom:
        atomic_number = randint(1, 73) if atomic_number is None else atomic_number
        atomic_mass = randint(1, 180) * random() if atomic_mass is None else atomic_mass
        return Atom(atomic_number, atomic_mass, symbol, chemical_group)
