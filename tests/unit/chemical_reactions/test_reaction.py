from unittest import main

from crdlib.chemical_reactions.reaction import (
    ChemicalReaction,
    ChemicalSubstance,
    ChemicalReactionParticipant,
)
from tests.factories.substance import SubstanceFactory

from unittest_extensions import TestCase, args

A = SubstanceFactory.build()
B = SubstanceFactory.build()
C = SubstanceFactory.build()
D = SubstanceFactory.build()


class TestInit(TestCase):
    def subject(self, reactants, products) -> ChemicalReaction:
        return ChemicalReaction(reactants, products)

    def assertReactants(self, reactants):
        if isinstance(reactants, ChemicalSubstance):
            self.assertEqual(self.result().reactants.participants[0], 1 * reactants)
        elif isinstance(reactants, ChemicalReactionParticipant):
            self.assertListEqual(self.result().reactants.participants, [reactants])
        else:
            self.assertEqual(self.result().reactants, reactants)

    def assertProducts(self, products):
        if isinstance(products, ChemicalSubstance):
            self.assertEqual(self.cachedResult().products.participants[0], 1 * products)
        elif isinstance(products, ChemicalReactionParticipant):
            self.assertListEqual(self.cachedResult().products.participants, [products])
        else:
            self.assertEqual(self.cachedResult().products, products)

    @args({"reactants": A, "products": B})
    def test_participant_to_participant(self):
        self.assertReactants(A)
        self.assertProducts(B)

    @args({"reactants": 2 * A, "products": B})
    def test_multimol_participant_to_participant(self):
        self.assertReactants(2 * A)
        self.assertProducts(B)

    @args({"reactants": A, "products": 3 * B})
    def test_participant_to_multimol_participant(self):
        self.assertReactants(A)
        self.assertProducts(3 * B)

    @args({"reactants": A + B, "products": C})
    def test_participants_to_participant(self):
        self.assertReactants(A + B)
        self.assertProducts(C)

    @args({"reactants": A + B + C, "products": 4 * D})
    def test_participants_to_multimol_participant(self):
        self.assertReactants(A + B + C)
        self.assertProducts(4 * D)

    @args({"reactants": A + 2 * B, "products": C})
    def test_multimol_participants_to_participant(self):
        self.assertReactants(A + 2 * B)
        self.assertProducts(C)

    @args({"reactants": A, "products": B + C})
    def test_participant_to_participants(self):
        self.assertReactants(A)
        self.assertProducts(B + C)

    @args({"reactants": 5 * A, "products": B + C})
    def test_multimol_participant_to_participants(self):
        self.assertReactants(5 * A)
        self.assertProducts(B + C)

    @args({"reactants": A + B, "products": C + D})
    def test_participants_to_participants(self):
        self.assertReactants(A + B)
        self.assertProducts(C + D)

    @args({"reactants": A + 3 * B, "products": (2 * C) + D})
    def test_multimol_participants_to_multimol_participants(self):
        self.assertReactants(A + 3 * B)
        self.assertProducts((2 * C) + D)


if __name__ == "__main__":
    main()
