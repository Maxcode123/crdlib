from dataclasses import dataclass
from enum import Enum, EnumMeta


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


def _create_coefficient(
    symbol: str, A: float, B: float, C: float, D: float
) -> ThermalCapacityCoefficient:
    _coefficient_map[symbol] = ThermalCapacityCoefficient(A, B, C, D)
    return _coefficient_map[symbol]


_coefficient_map: dict[str, ThermalCapacityCoefficient] = dict()


class ThermalCapacityCoefficientMeta(EnumMeta):
    def __getitem__(self, name: str) -> ThermalCapacityCoefficient:  # type: ignore
        return _coefficient_map[name]


class ThermalCapacityCoefficients(Enum, metaclass=ThermalCapacityCoefficientMeta):
    @staticmethod
    def get(name: str) -> ThermalCapacityCoefficient:
        return ThermalCapacityCoefficients.__getitem__(name)

    HYDROGEN = _create_coefficient("H2", 6.62, 0.0081, 0, 0)
    WATER = _create_coefficient("H20", 8.22, 0.00015, 0.00000134, 0)
    METHANE = _create_coefficient("CH4", 5.34, 0.0115, 0, 0)
    CARBON_MONOXIDE = _create_coefficient("CO", 6.60, 0.00120, 0, 0)
    CARBON_DIOXIDE = _create_coefficient("CO2", 10.34, 0.00274, 0, -195500)
    NICKEL = _create_coefficient("Ni", 6.99, 0.000905, 0, 0)
    NICKEL_OXIDE = _create_coefficient("NiO", 11.3, 0.00215, 0, 0)
    CALCIUM_OXIDE = _create_coefficient("CaO", 10, 0.00484, 0, -108000)
    CALCIUM_CARBONATE = _create_coefficient("CaCO3", 19.68, 0.01189, 0, -307600)
