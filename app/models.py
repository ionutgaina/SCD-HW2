from pydantic import BaseModel
from typing import Optional


class Country(BaseModel):
    nume: str
    lat: float
    lon: float


class City(BaseModel):
    idTara: str
    nume: str
    lat: float
    lon: float


class Temperature(BaseModel):
    idOras: str
    valoare: float
    timestamp: Optional[str] = None
