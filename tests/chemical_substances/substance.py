from unittest import TestCase, main

from crdlib.chemical_substances.predefined import PredefinedAtoms
from crdlib.chemical_substances.substance import ChemicalCompound, ChemicalElement


class TestChemicalCompound(TestCase):
    def test_init_compound_from_atoms(self):
        compound = ChemicalCompound(
            {PredefinedAtoms.ALUMINUM, PredefinedAtoms.ANTIMONY}
        )
        self.assertEqual(
            compound.molecular_weight,
            PredefinedAtoms.ALUMINUM.atomic_mass + PredefinedAtoms.ANTIMONY.atomic_mass,
        )

    def test_init_compound_from_elements(self):
        compound = ChemicalCompound(
            (
                ChemicalElement(PredefinedAtoms.HYDROGEN, 2),
                ChemicalElement(PredefinedAtoms.OXYGEN, 1),
            )
        )
        self.assertEqual(
            compound.molecular_weight,
            PredefinedAtoms.HYDROGEN.atomic_mass * 2
            + PredefinedAtoms.OXYGEN.atomic_mass,
        )

    def test_init_compound_from_mix(self):
        compound = ChemicalCompound(
            [PredefinedAtoms.CARBON, ChemicalElement(PredefinedAtoms.OXYGEN, 2)]
        )
        self.assertEqual(
            compound.molecular_weight,
            PredefinedAtoms.CARBON.atomic_mass + PredefinedAtoms.OXYGEN.atomic_mass * 2,
        )


if __name__ == "__main__":
    main()
