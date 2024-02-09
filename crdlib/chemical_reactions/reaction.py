from dataclasses import dataclass
from math import exp
from typing import Optional

from crdlib.chemical_substances.substance import (
    ChemicalReactionFactors,
    ChemicalReactionParticipant,
    ChemicalSubstance,
)
from crdlib.equations.equation import Term
from crdlib.properties.properties import Temperature
from crdlib.properties.units.units import TemperatureUnit
from crdlib.properties.constants import GLOBAL_GAS_CONSTANT


@dataclass
class ChemicalReaction:
    reactants: ChemicalReactionFactors
    products: ChemicalReactionFactors
    reaction_rate: Optional[Term] = None
    reference_temperature = Temperature(25, TemperatureUnit.CELCIUS)

    def __init__(
        self,
        reactants: ChemicalReactionFactors
        | ChemicalReactionParticipant
        | ChemicalSubstance,
        products: ChemicalReactionFactors
        | ChemicalReactionParticipant
        | ChemicalSubstance,
    ) -> None:
        self.reactants = ChemicalReactionFactors.create(reactants)
        self.products = ChemicalReactionFactors.create(products)

    def calculate_equilibrium_constant(self, temperature: Temperature) -> float:
        pass

    def standard_gibbs_free_energy_change(self) -> float:
        """
        In SI base units: kg / m^2 / s^2 / mol
        """
        return self._standard_property_change("gibbs_free_energy")

    def standard_enthalpy_change(self) -> float:
        """
        In SI base units: kg / m^2 / s^2 / mol
        """
        return self._standard_property_change("enthalpy")

    def _standard_property_change(self, property: str) -> float:
        return self._standard_property_sum(
            self.reactants, property
        ) - self._standard_property_sum(self.products, property)

    @staticmethod
    def _standard_property_sum(
        factors: ChemicalReactionFactors, property: str
    ) -> float:
        prop = 0
        for p in factors.participants:
            prop += (
                p.stoichiometric_coefficient
                * getattr(p.substance.standard_formation_properties, property)
                .to_si()
                .value
            )
        return prop

    def _gibbs_free_energy_factor(self) -> float:
        GLOBAL_GAS_CONSTANT.to_si().value * self.standard_gibbs_free_energy_change()

    @staticmethod
    def _calculate_equilibrium_constant(
        delta_A: float,
        delta_B: float,
        delta_C: float,
        delta_D: float,
        standard_gibbs_free_energy_diff: float,
        standard_enthalpy_diff: float,
        temperature_Kelvin: float,
        standard_temperature_Kelvin: float = 298.15,
    ):
        gibbs_free_energy_factor = ...
        enthalpy_factor = ...
        enthalpy_change_factor = ...
        entropy_change_factor = ...
        return exp(
            -gibbs_free_energy_factor
            + enthalpy_factor
            - enthalpy_change_factor
            + entropy_change_factor
        )
