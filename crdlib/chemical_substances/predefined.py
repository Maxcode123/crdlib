from typing import Any
from enum import Enum

from crdlib.chemical_substances.atom import Atom, ChemicalGroup
from crdlib.properties.units import TemperatureUnit, PressureUnit
from crdlib.properties.properties import Temperature, Pressure, Volume
from crdlib.chemical_substances.substance import (
    ChemicalElement,
    ChemicalCompound,
    CriticalProperties,
)
from crdlib.chemical_substances.exceptions import PredefinedSetAttributeError


class UnsettableClass:
    def __setattr__(self, __name: str, __value: Any) -> None:
        raise PredefinedSetAttributeError()


class PredefinedAtoms(UnsettableClass):
    HYDROGEN = Atom(1, 1.0080, "H", ChemicalGroup.NON_METAL)
    HELIUM = Atom(2, 4.00260, "He", ChemicalGroup.NOBLE_GAS)
    LITHIUM = Atom(3, 7.0, "Li", ChemicalGroup.ALKALI_METAL)
    BERYLLIUM = Atom(4, 9.012183, "Be", ChemicalGroup.ALKALINE_EARTH_METAL)
    BORON = Atom(5, 10.81, "B", ChemicalGroup.METALLOID)
    CARBON = Atom(6, 12.011, "C", ChemicalGroup.NON_METAL)
    NITROGEN = Atom(7, 14.007, "N", ChemicalGroup.NON_METAL)
    OXYGEN = Atom(8, 15.999, "O", ChemicalGroup.NON_METAL)
    FLUORINE = Atom(9, 18.99840316, "F", ChemicalGroup.HALOGEN)
    NEON = Atom(10, 20.180, "Ne", ChemicalGroup.NOBLE_GAS)
    SODIUM = Atom(11, 22.9897693, "Na", ChemicalGroup.ALKALI_METAL)
    MAGNESIUM = Atom(12, 24.305, "Mg", ChemicalGroup.ALKALINE_EARTH_METAL)
    ALUMINUM = Atom(13, 26.981538, "Al", ChemicalGroup.POST_TRANSITION_METAL)
    SILLICON = Atom(14, 28.085, "Si", ChemicalGroup.METALLOID)
    PHOSPHORUS = Atom(15, 30.97376200, "P", ChemicalGroup.NON_METAL)
    SULFUR = Atom(16, 32.07, "S", ChemicalGroup.NON_METAL)
    CHLORINE = Atom(17, 35.45, "Cl", ChemicalGroup.HALOGEN)
    ARGON = Atom(18, 39.9, "Ar", ChemicalGroup.NOBLE_GAS)
    POTASSIUM = Atom(19, 39.0983, "K", ChemicalGroup.ALKALI_METAL)
    CALCIUM = Atom(20, 40.08, "Ca", ChemicalGroup.ALKALINE_EARTH_METAL)
    SCANDIUM = Atom(21, 44.95591, "Sc", ChemicalGroup.TRANSITION_METAL)
    TITANIUM = Atom(22, 47.867, "Ti", ChemicalGroup.TRANSITION_METAL)
    VANADIUM = Atom(23, 50.9415, "V", ChemicalGroup.TRANSITION_METAL)
    CHROMIUM = Atom(24, 51.996, "Cr", ChemicalGroup.TRANSITION_METAL)
    MANGANESE = Atom(25, 54.93804, "Mn", ChemicalGroup.TRANSITION_METAL)
    IRON = Atom(26, 55.84, "Fe", ChemicalGroup.TRANSITION_METAL)
    COBALT = Atom(27, 58.93319, "Co", ChemicalGroup.TRANSITION_METAL)
    NICKEL = Atom(28, 58.693, "Ni", ChemicalGroup.TRANSITION_METAL)
    COPPER = Atom(29, 63.55, "Cu", ChemicalGroup.TRANSITION_METAL)
    ZINC = Atom(30, 65.4, "Zn", ChemicalGroup.TRANSITION_METAL)
    GALLIUM = Atom(31, 69.723, "Ga", ChemicalGroup.POST_TRANSITION_METAL)
    GERMANIUM = Atom(32, 72.63, "Ge", ChemicalGroup.METALLOID)
    ARSENIC = Atom(33, 74.92159, "As", ChemicalGroup.METALLOID)
    SELENIUM = Atom(34, 78.97, "Se", ChemicalGroup.NON_METAL)
    BROMINE = Atom(35, 79.90, "Br", ChemicalGroup.HALOGEN)
    KRYPTON = Atom(36, 83.80, "Kr", ChemicalGroup.NOBLE_GAS)
    RUBIDIUM = Atom(37, 85.468, "Rb", ChemicalGroup.ALKALI_METAL)
    STRONTIUM = Atom(38, 87.62, "Sr", ChemicalGroup.ALKALINE_EARTH_METAL)
    YTRIUM = Atom(39, 88.90584, "Y", ChemicalGroup.TRANSITION_METAL)
    ZITRONIUM = Atom(40, 91.22, "Zr", ChemicalGroup.TRANSITION_METAL)
    NIOBIUM = Atom(41, 92.90637, "Nb", ChemicalGroup.TRANSITION_METAL)
    MOLYBDENIUM = Atom(42, 95.95, "Mo", ChemicalGroup.TRANSITION_METAL)
    TECHNETIUM = Atom(43, 96.90636, "Tc", ChemicalGroup.TRANSITION_METAL)
    RUTHENIUM = Atom(44, 101.1, "Ru", ChemicalGroup.TRANSITION_METAL)
    RHODIUM = Atom(45, 102.9055, "Rh", ChemicalGroup.TRANSITION_METAL)
    PALLADIUM = Atom(46, 106.42, "Pd", ChemicalGroup.TRANSITION_METAL)
    SILVER = Atom(47, 107.868, "Ag", ChemicalGroup.TRANSITION_METAL)
    CADMIUM = Atom(48, 112.41, "Cd", ChemicalGroup.TRANSITION_METAL)
    INDIUM = Atom(49, 114.818, "In", ChemicalGroup.POST_TRANSITION_METAL)
    TIN = Atom(50, 118.71, "Sn", ChemicalGroup.POST_TRANSITION_METAL)
    ANTIMONY = Atom(51, 121.760, "Sb", ChemicalGroup.METALLOID)
    TELLURIUM = Atom(52, 127.6, "Te", ChemicalGroup.METALLOID)
    IODINE = Atom(53, 126.9045, "I", ChemicalGroup.HALOGEN)
    XENON = Atom(54, 131.29, "Xe", ChemicalGroup.NOBLE_GAS)
    CESIUM = Atom(55, 132.9054520, "Cs", ChemicalGroup.ALKALI_METAL)
    BARIUM = Atom(56, 137.33, "Ba", ChemicalGroup.ALKALINE_EARTH_METAL)
    HAFNIUM = Atom(72, 178.49, "Hf", ChemicalGroup.TRANSITION_METAL)
    TANTALUM = Atom(73, 180.9479, "Ta", ChemicalGroup.TRANSITION_METAL)


class PredefinedChemicalSubstances(Enum):
    pass
    # HYDROGEN = ChemicalElement(
    #     PredefinedAtoms.HYDROGEN,
    #     2,
    #     CriticalProperties(
    #         Temperature(33.19, TemperatureUnit.KELVIN),
    #     ),
    # )
    # OXYGEN = ChemicalElement(...)
    # WATER = ChemicalCompound(...)
    # METHANE = ChemicalCompound(...)
    # CARBON_MONOXIDE = ChemicalCompound(...)
    # CARBON_DIOXIDE = ChemicalCompound(...)
