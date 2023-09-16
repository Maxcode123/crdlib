from enum import Enum


class Regime(Enum):
    pass


class TemporalRegime(Regime):
    STEADY_STATE = "STEADY_STATE"
    DYNAMIC = "DYNAMIC"


class FluidPhaseRegime(Regime):
    HETEROGENEOUS = "HETEROGENEOUS"
    PSEUDO_HOMOGENEOUS = "PSEUDO_HOMOGENEOUS"


class ThermalRegime(Regime):
    ISOTHERMAL = "ISOTHERMAL"
    NON_ISOTHERMAL = "NON_ISOTHERMAL"
