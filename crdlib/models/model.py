from typing import Iterable

from pydantic import BaseModel

from crdlib.chemical_reactors.reactor import ChemicalReactor
from crdlib.chemical_reactions.reaction import ChemicalReaction
from crdlib.models.balance import EnergyBalance, MolecularBalance
from crdlib.models.regime import Regime
from crdlib.streams.stream import Stream


class ReactorModel(BaseModel):
    reactor: ChemicalReactor
    reactions: Iterable[ChemicalReaction]
    feed: Stream
    regimes: Iterable[Regime]

    @property
    def molecular_balances(self) -> Iterable[MolecularBalance]:
        pass

    @property
    def energy_balances(self) -> Iterable[EnergyBalance]:
        pass
