from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import usersModel
from schemes.userSchemes import RoleResponse, TypeDocumentResponse

router = APIRouter(
    prefix="/utils",
    tags=["Utils"]
)


@router.get("/role", response_model=List[RoleResponse])
def get_roles(db: Session = Depends(get_db)):
    roles = db.query(usersModel.Role).all()
    return roles

@router.get("/type-document", response_model=List[TypeDocumentResponse])
def get_type_document(db: Session = Depends(get_db)):
    type_document = db.query(usersModel.TypeDocument).all()
    return type_document