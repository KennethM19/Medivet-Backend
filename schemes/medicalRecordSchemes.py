from datetime import date
from typing import Optional

from pydantic import BaseModel


class VaccineTypeBase(BaseModel):
    type: str

class VaccineTypeCreate(VaccineTypeBase):
    specie_id: int

class VaccineTypeResponse(VaccineTypeBase):
    id: int
    specie_id: int

    class Config:
        from_attributes = True

class PetVaccineBase(BaseModel):
    pet_id: int
    vaccine_type_id: int
    date_applied: Optional[date] = None
    dose: Optional[str] = None
    batch: Optional[str] = None
    veterinarian: Optional[str] = None

class PetVaccineCreate(PetVaccineBase):
    pass

class PetVaccineResponse(PetVaccineBase):
    id: int
    vaccine_type: VaccineTypeResponse

    class Config:
        from_attributes = True
