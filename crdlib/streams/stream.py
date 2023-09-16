from typing import Iterable

from pydantic import BaseModel

from crdlib.properties.properties import (
    Temperature,
    Pressure,
    MassFraction,
    VolumeFraction,
    MolecularFraction,
    MassRate,
    VolumetricRate,
    MolecularRate,
)
from crdlib.chemical_substances.substance import ChemicalSubstance


class Component(BaseModel):
    species: ChemicalSubstance


class MassComponent(Component):
    fraction: MassFraction


class VolumetricComponent(Component):
    fraction: VolumeFraction


class MolecularComponent(Component):
    fraction: MolecularFraction


class MassComposition(BaseModel):
    components: Iterable[MassComponent]


class VolumetricComposition(BaseModel):
    components: Iterable[VolumetricComponent]


class MolecularComposition(BaseModel):
    components: Iterable[MolecularComponent]


class StreamComposition(BaseModel):
    mass: MassComposition
    volumetric: VolumetricComposition
    molecular: MolecularComposition


class StreamRate(BaseModel):
    mass: MassRate
    volumetric: VolumetricRate
    molecular: MolecularRate


class Stream(BaseModel):
    temperature: Temperature
    pressure: Pressure
    composition: StreamComposition
    rate: StreamRate
