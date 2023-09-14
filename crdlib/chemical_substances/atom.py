from typing import Any

from pydantic import BaseModel

class Atom(BaseModel):
    number_of_protons: int
    number_of_neutrons: int
    number_of_electrons: int
    properties: dict[str, Any]

    @property
    def electric_charge(self) -> int:
        return self.number_of_protons - self.number_of_electrons
