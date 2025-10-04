from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    nombre: str
    correo: str
    contrasena: str

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    class Config:
        orm_mode = True

class PetBase(BaseModel):
    nombre: str
    especie: str
    raza: Optional[str]
    dueño_id: int

class PetCreate(PetBase):
    pass

class PetResponse(PetBase):
    id: int
    class Config:
        orm_mode = True