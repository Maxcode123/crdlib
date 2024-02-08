from unittest import TestCase, main

from parameterized import parameterized

from crdlib.chemical_substances.predefined import Atoms
from crdlib.chemical_substances.substance import (
    ChemicalCompound,
    ChemicalElement,
    ChemicalReactionFactors,
    ChemicalReactionParticipant,
)
from crdlib.chemical_substances.exceptions import (
    InvalidChemicalCompoundComponentBinaryOperation,
    InvalidChemicalReactionFactorBinaryOperation,
)


class TestChemicalCompound(TestCase):
    def test_init_compound_from_atoms(self):
        compound = ChemicalCompound({Atoms["Al"], Atoms["Sb"]})
        self.assertEqual(
            compound.molecular_weight,
            Atoms["Al"].atomic_mass + Atoms["Sb"].atomic_mass,
        )

    def test_init_compound_from_elements(self):
        compound = ChemicalCompound(
            (
                ChemicalElement(Atoms["H"], 2),
                ChemicalElement(Atoms["O"], 1),
            )
        )
        self.assertEqual(
            compound.molecular_weight,
            Atoms["H"].atomic_mass * 2 + Atoms["O"].atomic_mass,
        )

    def test_init_compound_from_mix(self):
        compound = ChemicalCompound([Atoms["C"], ChemicalElement(Atoms["O"], 2)])
        self.assertEqual(
            compound.molecular_weight,
            Atoms["C"].atomic_mass + Atoms["O"].atomic_mass * 2,
        )


invalid_factors = [
    ("float", 1.2),
    ("str", "smth"),
    ("negative_int", -2),
    ("none", None),
    ("list", [1, 2]),
]


class TestChemicalCompoundComponents(TestCase):
    def test_create_element_from_atom(self):
        elem = Atoms["S"] * 2
        self.assertEqual(elem.atom, Atoms["S"])
        self.assertEqual(elem.number_of_atoms, 2)

    @parameterized.expand(invalid_factors)
    def test_create_invalid_element_from_atom_raises(self, _, factor):
        with self.assertRaises(InvalidChemicalCompoundComponentBinaryOperation):
            Atoms["K"] * factor

    @parameterized.expand(invalid_factors)
    def test_invalid_atom_shift_raises(self, _, factor):
        with self.assertRaises(InvalidChemicalCompoundComponentBinaryOperation):
            Atoms["Ca"] << factor

    @parameterized.expand(invalid_factors)
    def test_invalid_element_shift_raises(self, _, factor):
        with self.assertRaises(InvalidChemicalCompoundComponentBinaryOperation):
            ChemicalElement(Atoms["Br"]) << factor

    @parameterized.expand(invalid_factors)
    def test_invalid_compound_shift_raises(self, _, factor):
        compound = ChemicalCompound(
            [ChemicalElement(Atoms["H"]), ChemicalElement(Atoms["Cl"])]
        )
        with self.assertRaises(InvalidChemicalCompoundComponentBinaryOperation):
            compound << factor

    def test_create_compound_from_atoms(self):
        compound = Atoms["H"] << Atoms["Cl"]
        self.assertEqual(len(compound.elements), 2)
        self.assertTrue(ChemicalElement(Atoms["H"]) in compound.elements)
        self.assertTrue(ChemicalElement(Atoms["Cl"]) in compound.elements)

    def test_create_compound_from_elements(self):
        compound = ChemicalElement(Atoms["H"]) << ChemicalElement(Atoms["Cl"])
        self.assertEqual(len(compound.elements), 2)
        self.assertTrue(ChemicalElement(Atoms["H"]) in compound.elements)
        self.assertTrue(ChemicalElement(Atoms["Cl"]) in compound.elements)

    def test_create_compound_from_element_and_atom(self):
        compound = ChemicalElement(Atoms["H"], 2) << Atoms["O"]
        self.assertEqual(len(compound.elements), 2)
        self.assertTrue(ChemicalElement(Atoms["H"], 2) in compound.elements)
        self.assertTrue(ChemicalElement(Atoms["O"]) in compound.elements)

    def test_create_compound_from_atom_and_element(self):
        compound = Atoms["O"] << ChemicalElement(Atoms["H"], 2)
        self.assertEqual(len(compound.elements), 2)
        self.assertTrue(ChemicalElement(Atoms["H"], 2) in compound.elements)
        self.assertTrue(ChemicalElement(Atoms["O"]) in compound.elements)

    def test_create_compound_from_compound_and_atom(self):
        compound = ChemicalCompound([Atoms["Na"], Atoms["O"]]) << Atoms["Cl"]
        self.assertEqual(len(compound.elements), 3)
        self.assertTrue(ChemicalElement(Atoms["Na"]) in compound.elements)
        self.assertTrue(ChemicalElement(Atoms["O"]) in compound.elements)
        self.assertTrue(ChemicalElement(Atoms["Cl"]) in compound.elements)

    def test_create_compound_from_atom_and_compound(self):
        compound = Atoms["Cl"] << ChemicalCompound([Atoms["Na"], Atoms["O"]])
        self.assertEqual(len(compound.elements), 3)
        self.assertTrue(ChemicalElement(Atoms["Na"]) in compound.elements)
        self.assertTrue(ChemicalElement(Atoms["O"]) in compound.elements)
        self.assertTrue(ChemicalElement(Atoms["Cl"]) in compound.elements)

    def test_create_compound_from_compound_and_element(self):
        compound = ChemicalCompound([Atoms["Na"], Atoms["O"]]) << ChemicalElement(
            Atoms["Cl"]
        )
        self.assertEqual(len(compound.elements), 3)
        self.assertTrue(ChemicalElement(Atoms["Na"]) in compound.elements)
        self.assertTrue(ChemicalElement(Atoms["O"]) in compound.elements)
        self.assertTrue(ChemicalElement(Atoms["Cl"]) in compound.elements)

    def test_create_compound_from_element_and_compound(self):
        compound = ChemicalElement(Atoms["Cl"]) << ChemicalCompound(
            [Atoms["Na"], Atoms["O"]]
        )
        self.assertEqual(len(compound.elements), 3)
        self.assertTrue(ChemicalElement(Atoms["Na"]) in compound.elements)
        self.assertTrue(ChemicalElement(Atoms["O"]) in compound.elements)
        self.assertTrue(ChemicalElement(Atoms["Cl"]) in compound.elements)

    def test_create_compound_from_compound_and_compound(self):
        compound = ChemicalCompound([Atoms["Na"], Atoms["O"]]) << ChemicalCompound(
            [Atoms["Cl"], Atoms["H"]]
        )
        self.assertEqual(len(compound.elements), 4)
        self.assertTrue(ChemicalElement(Atoms["Na"]) in compound.elements)
        self.assertTrue(ChemicalElement(Atoms["O"]) in compound.elements)
        self.assertTrue(ChemicalElement(Atoms["Cl"]) in compound.elements)
        self.assertTrue(ChemicalElement(Atoms["H"]) in compound.elements)


class TestChemicalReactionFactors(TestCase):
    def test_element_addition_creates_factors(self):
        factors = ChemicalElement(Atoms["H"]) + ChemicalElement(Atoms["O"])
        self.assertTrue(isinstance(factors, ChemicalReactionFactors))
        self.assertEqual(len(factors.participants), 2)

    @parameterized.expand(invalid_factors)
    def test_invalid_element_addition_raises(self, _, factor):
        with self.assertRaises(InvalidChemicalReactionFactorBinaryOperation):
            ChemicalElement(Atoms["P"]) + factor

    def test_element_multiplication_creates_participant(self):
        participant = ChemicalElement(Atoms["O"]) * 3
        self.assertEqual(participant.stoichiometric_coefficient, 3)

    def test_element_right_multiplication_creates_participant(self):
        participant = 3 * ChemicalElement(Atoms["Na"])
        self.assertEqual(participant.stoichiometric_coefficient, 3)

    @parameterized.expand(invalid_factors)
    def test_invalid_element_multiplication_raises(self, _, factor):
        with self.assertRaises(InvalidChemicalReactionFactorBinaryOperation):
            ChemicalElement(Atoms["F"]) * factor

    def test_factors_multiplication_creates_factors(self):
        factors = ChemicalReactionFactors([ChemicalElement(Atoms["C"])]) * 2
        self.assertTrue(isinstance(factors, ChemicalReactionFactors))
        self.assertEqual(factors.participants[0].stoichiometric_coefficient, 2)

    @parameterized.expand(invalid_factors)
    def test_invalid_factors_multiplication_raises(self, _, factor):
        with self.assertRaises(InvalidChemicalReactionFactorBinaryOperation):
            ChemicalReactionFactors([ChemicalElement(Atoms["C"])]) * factor

    @parameterized.expand(
        [
            ("participant", ChemicalReactionParticipant(ChemicalElement(Atoms["H"]))),
            ("compound", ChemicalCompound([Atoms["C"], Atoms["H"]])),
            ("element", ChemicalElement(Atoms["Li"])),
        ]
    )
    def test_factors_addition_creates_factors(self, _, factor):
        factors = ChemicalReactionFactors([ChemicalElement(Atoms["Si"])]) + factor
        self.assertTrue(factors, ChemicalReactionFactors)
        self.assertEqual(len(factors.participants), 2)

    @parameterized.expand(invalid_factors)
    def test_invalid_factors_addition_raises(self, _, factor):
        with self.assertRaises(InvalidChemicalReactionFactorBinaryOperation):
            ChemicalReactionFactors([ChemicalElement(Atoms["Si"])]) + factor


if __name__ == "__main__":
    main()
