from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import usersModel, petsModel
from schemes.petSchemes import SexResponse, SpeciesResponse, BreedResponse
from schemes.userSchemes import RoleResponse, TypeDocumentResponse, UserResponse

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

@router.get("/sex", response_model=List[SexResponse])
def get_sex(db: Session = Depends(get_db)):
    sex = db.query(petsModel.Sex).all()
    return sex

@router.get("/species", response_model=List[SpeciesResponse])
def get_species(db: Session = Depends(get_db)):
    species = db.query(petsModel.Species).all()
    return species

@router.get("/breed", response_model=List[BreedResponse])
def get_breed(db: Session = Depends(get_db)):
    breed = db.query(petsModel.Breed).all()
    return breed