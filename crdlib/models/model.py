from typing import Iterable

from pydantic import BaseModel

from crdlib.chemical_reactors.reactor import ChemicalReactor
from crdlib.chemical_reactions.reaction import ChemicalReaction
from crdlib.models.equation import EnergyBalance, MassBalance
from crdlib.streams.stream import Stream


class ReactorModel(BaseModel):
    reactor: ChemicalReactor
    reactions: Iterable[ChemicalReaction]
    mass_balances: Iterable[MassBalance]
    feed: Stream


class IsothermalReactorModel(ReactorModel):
    pass


class NonIsothermalReactorModel(ReactorModel):
    energy_balance: EnergyBalance
