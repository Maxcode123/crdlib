from typing import TypeVar, Protocol


P = TypeVar("P")


def implements(protocol: Protocol):
    """
    Decorate a class to enable mypy to check if it implements the given protocol.
    """

    def wrapper(cls):
        cls._ = _protocol_implementation_check(protocol)
        return cls

    return wrapper


def _protocol_implementation_check(protocol: P):
    def wrapper(self) -> P:
        return self

    return wrapper
