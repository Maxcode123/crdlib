from __future__ import annotations
from enum import Enum
from typing import Iterable

from pydantic import BaseModel


class BinaryOperation(Enum):
    ADDITION = "ADDITION"
    SUBTRACTION = "SUBTRACTION"
    DIVISION = "DIVISION"
    MULTIPLICATION = "MULTIPLICATION"


class Equation(BaseModel):
    lhs: Term
    rhs: Iterable[Term]


class Term:
    def __init__(self, factor: Factor) -> None:
        self.factor = factor


class Factor:
    pass


class BinaryFactor(Factor):
    def __init__(
        self,
        left: Factor,
        binary_operation: BinaryOperation,
        right: Factor,
            ) -> None:
        self.left = left
        self.right = right
        self.binary_operation = binary_operation


class Derivative(Factor):
    def __init__(self, variable: DependentVariable) -> None:
        self.variable = variable


class DependentVariable(Factor):
    def __init__(self, name: str, unit) -> None:
        self.name = name
        self.unit = unit


class Constant(Factor):
    pass
