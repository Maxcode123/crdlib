from enum import Enum, EnumMeta

from crdlib.properties.units import (
    TemperatureUnit,
    PressureUnit,
    LengthUnit,
    AmountUnit,
    EnergyUnit,
)
from crdlib.properties.properties import (
    Temperature,
    Pressure,
    MolarVolume,
    FormationEnthalpy,
    FormationGibbsFreeEnergy,
)
from crdlib.chemical_substances.substance import (
    ChemicalElement,
    ChemicalCompound,
    ChemicalSubstance,
    CriticalProperties,
    StandardFormationProperties,
    ChemicalGroup,
    Atom,
)


def _create_atom(
    atomic_number: int, atomic_mass: float, symbol: str, chemical_group: ChemicalGroup
) -> Atom:
    _atom_map[symbol] = Atom(atomic_number, atomic_mass, symbol, chemical_group)
    return _atom_map[symbol]


_atom_map: dict[str, Atom] = dict()


class AtomsMeta(EnumMeta):
    def __getitem__(self, name: str) -> Atom:  # type: ignore
        return _atom_map[name]


class Atoms(Enum, metaclass=AtomsMeta):
    @staticmethod
    def create(
        atomic_number: int,
        atomic_mass: float,
        symbol: str,
        chemical_group: ChemicalGroup,
    ) -> Atom:
        return _create_atom(atomic_number, atomic_mass, symbol, chemical_group)

    @staticmethod
    def get(name: str) -> Atom:
        return Atoms.__getitem__(name)

    HYDROGEN = _create_atom(1, 1.0080, "H", ChemicalGroup.NON_METAL)
    HELIUM = _create_atom(2, 4.00260, "He", ChemicalGroup.NOBLE_GAS)
    LITHIUM = _create_atom(3, 7.0, "Li", ChemicalGroup.ALKALI_METAL)
    BERYLLIUM = _create_atom(4, 9.012183, "Be", ChemicalGroup.ALKALINE_EARTH_METAL)
    BORON = _create_atom(5, 10.81, "B", ChemicalGroup.METALLOID)
    CARBON = _create_atom(6, 12.011, "C", ChemicalGroup.NON_METAL)
    NITROGEN = _create_atom(7, 14.007, "N", ChemicalGroup.NON_METAL)
    OXYGEN = _create_atom(8, 15.999, "O", ChemicalGroup.NON_METAL)
    FLUORINE = _create_atom(9, 18.99840316, "F", ChemicalGroup.HALOGEN)
    NEON = _create_atom(10, 20.180, "Ne", ChemicalGroup.NOBLE_GAS)
    SODIUM = _create_atom(11, 22.9897693, "Na", ChemicalGroup.ALKALI_METAL)
    MAGNESIUM = _create_atom(12, 24.305, "Mg", ChemicalGroup.ALKALINE_EARTH_METAL)
    ALUMINUM = _create_atom(13, 26.981538, "Al", ChemicalGroup.POST_TRANSITION_METAL)
    SILLICON = _create_atom(14, 28.085, "Si", ChemicalGroup.METALLOID)
    PHOSPHORUS = _create_atom(15, 30.97376200, "P", ChemicalGroup.NON_METAL)
    SULFUR = _create_atom(16, 32.07, "S", ChemicalGroup.NON_METAL)
    CHLORINE = _create_atom(17, 35.45, "Cl", ChemicalGroup.HALOGEN)
    ARGON = _create_atom(18, 39.9, "Ar", ChemicalGroup.NOBLE_GAS)
    POTASSIUM = _create_atom(19, 39.0983, "K", ChemicalGroup.ALKALI_METAL)
    CALCIUM = _create_atom(20, 40.08, "Ca", ChemicalGroup.ALKALINE_EARTH_METAL)
    SCANDIUM = _create_atom(21, 44.95591, "Sc", ChemicalGroup.TRANSITION_METAL)
    TITANIUM = _create_atom(22, 47.867, "Ti", ChemicalGroup.TRANSITION_METAL)
    VANADIUM = _create_atom(23, 50.9415, "V", ChemicalGroup.TRANSITION_METAL)
    CHROMIUM = _create_atom(24, 51.996, "Cr", ChemicalGroup.TRANSITION_METAL)
    MANGANESE = _create_atom(25, 54.93804, "Mn", ChemicalGroup.TRANSITION_METAL)
    IRON = _create_atom(26, 55.84, "Fe", ChemicalGroup.TRANSITION_METAL)
    COBALT = _create_atom(27, 58.93319, "Co", ChemicalGroup.TRANSITION_METAL)
    NICKEL = _create_atom(28, 58.693, "Ni", ChemicalGroup.TRANSITION_METAL)
    COPPER = _create_atom(29, 63.55, "Cu", ChemicalGroup.TRANSITION_METAL)
    ZINC = _create_atom(30, 65.4, "Zn", ChemicalGroup.TRANSITION_METAL)
    GALLIUM = _create_atom(31, 69.723, "Ga", ChemicalGroup.POST_TRANSITION_METAL)
    GERMANIUM = _create_atom(32, 72.63, "Ge", ChemicalGroup.METALLOID)
    ARSENIC = _create_atom(33, 74.92159, "As", ChemicalGroup.METALLOID)
    SELENIUM = _create_atom(34, 78.97, "Se", ChemicalGroup.NON_METAL)
    BROMINE = _create_atom(35, 79.90, "Br", ChemicalGroup.HALOGEN)
    KRYPTON = _create_atom(36, 83.80, "Kr", ChemicalGroup.NOBLE_GAS)
    RUBIDIUM = _create_atom(37, 85.468, "Rb", ChemicalGroup.ALKALI_METAL)
    STRONTIUM = _create_atom(38, 87.62, "Sr", ChemicalGroup.ALKALINE_EARTH_METAL)
    YTRIUM = _create_atom(39, 88.90584, "Y", ChemicalGroup.TRANSITION_METAL)
    ZITRONIUM = _create_atom(40, 91.22, "Zr", ChemicalGroup.TRANSITION_METAL)
    NIOBIUM = _create_atom(41, 92.90637, "Nb", ChemicalGroup.TRANSITION_METAL)
    MOLYBDENIUM = _create_atom(42, 95.95, "Mo", ChemicalGroup.TRANSITION_METAL)
    TECHNETIUM = _create_atom(43, 96.90636, "Tc", ChemicalGroup.TRANSITION_METAL)
    RUTHENIUM = _create_atom(44, 101.1, "Ru", ChemicalGroup.TRANSITION_METAL)
    RHODIUM = _create_atom(45, 102.9055, "Rh", ChemicalGroup.TRANSITION_METAL)
    PALLADIUM = _create_atom(46, 106.42, "Pd", ChemicalGroup.TRANSITION_METAL)
    SILVER = _create_atom(47, 107.868, "Ag", ChemicalGroup.TRANSITION_METAL)
    CADMIUM = _create_atom(48, 112.41, "Cd", ChemicalGroup.TRANSITION_METAL)
    INDIUM = _create_atom(49, 114.818, "In", ChemicalGroup.POST_TRANSITION_METAL)
    TIN = _create_atom(50, 118.71, "Sn", ChemicalGroup.POST_TRANSITION_METAL)
    ANTIMONY = _create_atom(51, 121.760, "Sb", ChemicalGroup.METALLOID)
    TELLURIUM = _create_atom(52, 127.6, "Te", ChemicalGroup.METALLOID)
    IODINE = _create_atom(53, 126.9045, "I", ChemicalGroup.HALOGEN)
    XENON = _create_atom(54, 131.29, "Xe", ChemicalGroup.NOBLE_GAS)
    CESIUM = _create_atom(55, 132.9054520, "Cs", ChemicalGroup.ALKALI_METAL)
    BARIUM = _create_atom(56, 137.33, "Ba", ChemicalGroup.ALKALINE_EARTH_METAL)
    HAFNIUM = _create_atom(72, 178.49, "Hf", ChemicalGroup.TRANSITION_METAL)
    TANTALUM = _create_atom(73, 180.9479, "Ta", ChemicalGroup.TRANSITION_METAL)


def _create_substance(
    substance: ChemicalSubstance,
    symbol: str,
    critical_temperature: Temperature,
    critical_pressure: Pressure,
    critical_volume: MolarVolume,
    standard_formation_enthalpy: FormationGibbsFreeEnergy,
    standard_formation_gibbs_free_energy: FormationGibbsFreeEnergy,
) -> ChemicalSubstance:
    substance.set_critical_properties(
        CriticalProperties(critical_temperature, critical_pressure, critical_volume)
    )
    substance.set_standard_formation_properties(
        StandardFormationProperties(
            standard_formation_enthalpy, standard_formation_gibbs_free_energy
        )
    )
    substance.set_symbol(symbol)
    _substance_map[symbol] = substance
    return substance


_substance_map: dict[str, ChemicalSubstance] = dict()


class ChemicalSubstancesMeta(EnumMeta):
    def __getitem__(self, name: str) -> ChemicalSubstance:  # type: ignore
        return _substance_map[name]


class ChemicalSubstances(Enum, metaclass=ChemicalSubstancesMeta):
    @staticmethod
    def create(
        substance: ChemicalSubstance,
        symbol: str,
        critical_temperature: Temperature,
        critical_pressure: Pressure,
        critical_volume: MolarVolume,
        standard_formation_enthalpy: FormationEnthalpy,
        standard_formation_gibbs_free_energy: FormationGibbsFreeEnergy,
    ) -> ChemicalSubstance:
        return _create_substance(
            substance,
            symbol,
            critical_temperature,
            critical_pressure,
            critical_volume,
            standard_formation_enthalpy,
            standard_formation_gibbs_free_energy,
        )

    @staticmethod
    def get(name: str) -> ChemicalSubstance:
        return ChemicalSubstances.__getitem__(name)

    HYDROGEN = _create_substance(
        ChemicalElement(Atoms.get("H"), 2),
        "H2",
        Temperature(33.19, TemperatureUnit.KELVIN),
        Pressure(13.13, PressureUnit.BAR),
        MolarVolume(0.064147, (LengthUnit.METER**3) / AmountUnit.KILO_MOL),
        FormationEnthalpy(0, EnergyUnit.KILO_JOULE / AmountUnit.MOL),
        FormationGibbsFreeEnergy(0, EnergyUnit.KILO_JOULE / AmountUnit.MOL),
    )
    WATER = _create_substance(
        ChemicalCompound([Atoms.get("H") * 2, Atoms.get("O")]),
        "H2O",
        Temperature(647.096, TemperatureUnit.KELVIN),
        Pressure(220.64, PressureUnit.BAR),
        MolarVolume(0.0559472, (LengthUnit.METER**3) / AmountUnit.KILO_MOL),
        FormationEnthalpy(-241.829, EnergyUnit.KILO_JOULE / AmountUnit.MOL),
        FormationGibbsFreeEnergy(-228.59, EnergyUnit.KILO_JOULE / AmountUnit.MOL),
    )
    METHANE = _create_substance(
        ChemicalCompound([Atoms.get("C"), Atoms.get("H") * 4]),
        "CH4",
        Temperature(190.564, TemperatureUnit.KELVIN),
        Pressure(45.99, PressureUnit.BAR),
        MolarVolume(0.09861, (LengthUnit.METER**3) / AmountUnit.KILO_MOL),
        FormationEnthalpy(-74.52, EnergyUnit.KILO_JOULE / AmountUnit.MOL),
        FormationGibbsFreeEnergy(-50.49, EnergyUnit.KILO_JOULE / AmountUnit.MOL),
    )
    CARBON_MONOXIDE = _create_substance(
        ChemicalCompound([Atoms.get("C"), Atoms.get("O")]),
        "CO",
        Temperature(132.92, TemperatureUnit.KELVIN),
        Pressure(34.99, PressureUnit.BAR),
        MolarVolume(0.0944, (LengthUnit.METER**3) / AmountUnit.KILO_MOL),
        FormationEnthalpy(-110.52, EnergyUnit.KILO_CALORIE / AmountUnit.MOL),
        FormationGibbsFreeEnergy(-137.27, EnergyUnit.KILO_JOULE / AmountUnit.MOL),
    )
    CARBON_DIOXIDE = _create_substance(
        ChemicalCompound([Atoms.get("C"), Atoms.get("O") * 2]),
        "CO2",
        Temperature(304.21, TemperatureUnit.KELVIN),
        Pressure(73.83, PressureUnit.BAR),
        MolarVolume(0.094, (LengthUnit.METER**3) / AmountUnit.KILO_MOL),
        FormationEnthalpy(-393.509, EnergyUnit.KILO_JOULE / AmountUnit.MOL),
        FormationGibbsFreeEnergy(-394.359, EnergyUnit.KILO_JOULE / AmountUnit.MOL),
    )
