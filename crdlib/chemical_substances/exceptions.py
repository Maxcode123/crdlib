from crdlib.exceptions.exceptions import CRDLibException


class PredefinedSetAttributeError(CRDLibException):
    description = "cannot set attribute of Predefined class. "
