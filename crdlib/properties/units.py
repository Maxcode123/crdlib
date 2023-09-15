from enum import Enum


class TemperatureUnit(Enum):
    CELCIUS = "CELCIUS"
    KELVIN = "KELVIN"
    FAHRENHEIT = "FAHRENHEIT"
    RANKINE = "RANKINE"


class PressureUnit(Enum):
    MILLI_BAR = "MILLI_BAR"
    BAR = "BAR"
    PSI = "PSI"
    PASCAL = "PASCAL"
    KILO_PASCAL =  "KILO_PASCAL"
