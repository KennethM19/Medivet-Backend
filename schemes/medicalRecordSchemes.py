from pydantic import BaseModel


class VaccineTypeBase(BaseModel):
    type: str

class VaccineTypeCreate(VaccineTypeBase):
    pass

class VaccineTypeResponse(BaseModel):
    id : int
    class Config:
        from_attributes = True

class VaccineBase(BaseModel):
    pet_id: int
    vaccine_type_id: int

class VaccineCreate(VaccineBase):
    pass

class VaccineResponse(VaccineBase):
    id: int
    vaccine_type: VaccineTypeResponse

    class Config:
        from_attributes = True
