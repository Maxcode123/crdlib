from crdlib.properties.properties import GasConstant
from crdlib.properties.units.units import (
    MassUnit,
    LengthUnit,
    TimeUnit,
    TemperatureUnit,
    AmountUnit,
)


GLOBAL_GAS_CONSTANT = GasConstant(
    8.31446261815324,
    MassUnit.KILO_GRAM
    * (LengthUnit.METER**2)
    / (TimeUnit.SECOND**2)
    / TemperatureUnit.KELVIN
    / AmountUnit.MOL,
)
