from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class RoleBase(BaseModel):
    name: str

class RoleCreate(RoleBase):
    pass

class RoleResponse(RoleBase):
    id: int
    class Config:
        orm_mode = True

class TypeDocumentBase(BaseModel):
    name: str

class TypeDocumentCreate(TypeDocumentBase):
    pass

class TypeDocumentResponse(TypeDocumentBase):
    id: int
    class Config:
        orm_mode = True

class UserBase(BaseModel):
    type_document_id: int
    num_document: str
    name: str
    lastname: str
    birth_date: date
    address: str
    num_cellphone: Optional[str] = None
    num_telephone: Optional[str] = None
    email: EmailStr
    role_id: int

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    lastname: Optional[str] = None
    address: Optional[str] = None
    num_cellphone: Optional[str] = None
    num_telephone: Optional[str] = None
    role_id: Optional[int] = None
    password: Optional[str] = None

class UserResponse(UserBase):
    id: int
    type_document: TypeDocumentResponse
    role: RoleResponse

    class Config:
        orm_mode = True