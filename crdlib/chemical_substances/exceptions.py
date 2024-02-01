from crdlib.exceptions.exceptions import CRDLibException


class InvalidChemicalReactionFactorBinaryOperation(CRDLibException):
    description = "invalid (wrong data type) multiplication or addition with chemical reaction factor. "


class InvalidChemicalCompoundComponentBinaryOperation(CRDLibException):
    description = "invalid (wrong data type) multiplication or addition with chemical compound component. "


class WrongChemicalReactionFactorType(CRDLibException):
    description = "got a wrong chemical reaction factor type. "
