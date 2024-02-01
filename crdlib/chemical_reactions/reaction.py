from dataclasses import dataclass
from math import exp

from crdlib.chemical_substances.substance import ChemicalReactionFactors
from crdlib.equations.equation import Term
from crdlib.properties.properties import Temperature
from crdlib.properties.constants import GLOBAL_GAS_CONSTANT


@dataclass
class ChemicalReaction:
    reactants: ChemicalReactionFactors
    products: ChemicalReactionFactors
    reaction_rate: Term

    def equilibrium_constant(self, temperature: Temperature) -> float:
        return self.calculate_equilibrium_constant(
            temperature, self.reactants, self.products
        )

    @classmethod
    def calculate_equilibrium_constant(
        cls,
        temperature: Temperature,
        reactants: ChemicalReactionFactors,
        products: ChemicalReactionFactors,
    ) -> float:
        pass

    def standard_gibbs_free_energy_diff(self) -> float:
        return self._standard_property_diff("gibbs_free_energy")

    def standard_enthalpy_diff(self) -> float:
        return self._standard_property_diff("enthalpy")

    def _standard_property_diff(self, property: str) -> float:
        return self.__class__._standard_property_diff(
            self.reactants, self.products, property
        )

    @classmethod
    def _standard_property_diff(
        cls,
        reactans: ChemicalReactionFactors,
        products: ChemicalReactionFactors,
        property: str,
    ) -> float:
        return cls._standard_property_sum(
            reactans, property
        ) - cls._standard_property_sum(products, property)

    @staticmethod
    def _standard_property_sum(
        factors: ChemicalReactionFactors, property: str
    ) -> float:
        prop = 0
        for p in factors.participants:
            prop += p.stoichiometric_coefficient * getattr(
                p.substance.standard_formation_properties, property
            )
        return prop

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
