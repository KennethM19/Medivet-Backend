from typing import List, Optional

from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.routing import APIRouter
from starlette import status

from sqlalchemy.orm import Session, Query, joinedload
from database import get_db
from models.intemediateTables import PetVaccine
from models.medicalRecodModel import VaccineType
from schemes.medicalRecordSchemes import VaccineTypeResponse, VaccineTypeCreate, PetVaccineCreate, PetVaccineResponse

router = APIRouter(
    prefix="/medical-record",
    tags=["medical-record"],
)

# Crear tipo de vacuna
@router.post("/vaccine-type", response_model=VaccineTypeResponse, status_code=status.HTTP_201_CREATED)
def create_vaccine_type(request: VaccineTypeCreate, db: Session = Depends(get_db)):
    new_vaccine_type = VaccineType(**request.model_dump())
    db.add(new_vaccine_type)
    db.commit()
    db.refresh(new_vaccine_type)
    return new_vaccine_type

# Obtener todos los tipos de vacuna
@router.get("/vaccine-type", response_model=List[VaccineTypeResponse])
def get_vaccine_types(db: Session = Depends(get_db)):
    return db.query(VaccineType).all()

# Eliminar tipo de vacuna por ID
@router.delete("/vaccine-type", response_model=VaccineTypeResponse)
def delete_vaccine_type(vaccine_type_id: int, db: Session = Depends(get_db)):
    vaccine_type = db.query(VaccineType).filter(VaccineType.id == vaccine_type_id).first()
    if not vaccine_type:
        raise HTTPException(status_code=404, detail="VaccineType not found")
    db.delete(vaccine_type)
    db.commit()
    return vaccine_type

# Crear aplicación de vacuna
@router.post("/pet-vaccine", response_model=PetVaccineResponse, status_code=status.HTTP_201_CREATED)
def create_pet_vaccine(request: PetVaccineCreate, db: Session = Depends(get_db)):
    new_pet_vaccine = PetVaccine(**request.model_dump())
    db.add(new_pet_vaccine)
    db.commit()
    db.refresh(new_pet_vaccine)
    return new_pet_vaccine

# Obtener todas las aplicaciones de vacunas
@router.get("/pet-vaccine", response_model=List[PetVaccineResponse])
def get_pet_vaccines(
        specie_id: Optional[int],
        db: Session = Depends(get_db)
):
    query = db.query(PetVaccine).options(joinedload(PetVaccine.vaccine_type))

    if specie_id:
        # join con VaccineType para filtrar por especie
        query = query.join(PetVaccine.vaccine_type).filter(VaccineType.specie_id == specie_id)

    return query.all()

# Eliminar aplicación de vacuna por ID
@router.delete("/pet-vaccine", response_model=PetVaccineResponse)
def delete_pet_vaccine(pet_vaccine_id: int, db: Session = Depends(get_db)):
    pet_vaccine = db.query(PetVaccine).filter(PetVaccine.id == pet_vaccine_id).first()
    if not pet_vaccine:
        raise HTTPException(status_code=404, detail="PetVaccine not found")
    db.delete(pet_vaccine)
    db.commit()
    return pet_vaccine