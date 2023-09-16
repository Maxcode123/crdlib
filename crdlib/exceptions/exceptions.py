from typing import Optional


class CRDLibException(Exception):
    description: str

    def __init__(self, msg: Optional[str] = None) -> None:
        if msg is None:
            msg = self.description
        super().__init__(msg)


class PredefinedSetAttributeError(CRDLibException):
    description = "cannot set attribute of Predefined class. "


class PropertyUnitOperationError(CRDLibException):
    description = "invalid operation between units. "


class InvalidMeasurementUnit(CRDLibException):
    description = "invalid measurement unit"
