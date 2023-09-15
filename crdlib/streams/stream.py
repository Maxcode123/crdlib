from pydantic import BaseModel


class Stream(BaseModel):
    temperature: object
    pressure: object
    composition: object
    mass_rate: object
