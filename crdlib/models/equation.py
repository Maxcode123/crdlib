from pydantic import BaseModel


class Equation(BaseModel):
    pass


class Balance(Equation):
    pass


class MassBalance(Balance):
    pass


class EnergyBalance(Balance):
    pass
