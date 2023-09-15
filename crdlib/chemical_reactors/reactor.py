from pydantic import BaseModel


class ChemicalReactor(BaseModel):
    pass


class BedReactor(ChemicalReactor):
    length: float
    radius: float


class FixedBedReactor(BedReactor):
    pass
