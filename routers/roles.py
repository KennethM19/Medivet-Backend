from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import models
from database import get_db
from schemas import RoleResponse, TypeDocumentResponse

router = APIRouter(
    prefix="/utils",
    tags=["Utils"]
)


@router.get("/role", response_model=List[RoleResponse])
def get_roles(db: Session = Depends(get_db)):
    roles = db.query(models.Role).all()
    return roles

@router.get("/type-document", response_model=List[TypeDocumentResponse])
def get_type_document(db: Session = Depends(get_db)):
    type_document = db.query(models.TypeDocument).all()
    return type_document