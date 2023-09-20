from crdlib.exceptions.exceptions import CRDLibException


class InvalidUnitDescriptorBinaryOperation(CRDLibException):
    description = "invalid binary operation between unit descriptors. "


class WrongUnitDescriptorType(CRDLibException):
    description = "got a wrong unit descriptor type. "


class InvalidUnitConversion(CRDLibException):
    description = (
        "conversion to invalid physical property unit (e.g. from m^2 to cm^3 or from K"
        " to bar). "
    )


class UndefinedConverter(CRDLibException):
    description = "a converter has not been defined for a given generic descriptor. "
