from dataclasses import dataclass


@dataclass
class ThermalCapacityCoefficient:
    """
    Coefficients of the equation
    ``
    Cp = A + B*T + C*T^2 + D/(T^2)
    ``
    used to calculate thermal capacity in cal/mol/K.
    """

    A: float
    B: float
    C: float
    D: float
