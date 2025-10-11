from typing import Optional

from pydantic import BaseModel

from schemes.userSchemes import UserResponse


class SexBase(BaseModel):
    name: str

class SexCreate(SexBase):
    pass

class SexResponse(SexBase):
    id: int

    class Config:
        orm_mode = True

class SpeciesBase(BaseModel):
    name: str

class SpeciesCreate(SpeciesBase):
    pass

class SpeciesResponse(SpeciesBase):
    id: int

    class Config:
        orm_mode = True

class BreedBase(BaseModel):
    name: str

class BreedCreate(BreedBase):
    pass

class BreedResponse(BreedBase):
    id: int

    class Config:
        orm_mode = True

class PetBase(BaseModel):
    num_doc: Optional[str] = None
    name: str
    photo: Optional[str] = None
    sex_id: int
    specie_id: int
    breed_id: int
    year_birth: Optional[int] = None
    month_birth: Optional[int] = None
    weight: Optional[float] = None
    neutered: bool

class PetCreate(PetBase):
    pass

class PetUpdate(BaseModel):
    name: str
    photo: Optional[str] = None
    weight: Optional[float] = None
    neutered: bool

class PetResponse(PetBase):
    id: int
    user: Optional[UserResponse] = None
    breed: Optional[BreedResponse] = None
    species: Optional[SpeciesResponse] = None
    sex: Optional[SexResponse] = None

    class Config:
        orm_mode = True