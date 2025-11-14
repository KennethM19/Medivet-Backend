from typing import List

from fastapi.params import Depends
from fastapi.routing import APIRouter
from starlette import status

from sqlalchemy.orm import Session
from database import get_db
from models.medicalRecodModel import VaccineType, Vaccine
from schemes.medicalRecordSchemes import VaccineTypeResponse, VaccineTypeCreate, VaccineResponse, VaccineCreate

router = APIRouter(
    prefix="/medical-record",
    tags=["medical-record"],
)

@router.post("/vaccine-type", response_model= VaccineTypeResponse, status_code=status.HTTP_201_CREATED )
def create_vaccine_type(request: VaccineTypeCreate, db: Session = Depends(get_db)):
    vaccine_type_data = request.model_dump()
    new_vaccine_type = VaccineTypeCreate(**vaccine_type_data)

    db.add(new_vaccine_type)
    db.commit()
    db.refresh(new_vaccine_type)

    return new_vaccine_type

@router.get("/vaccine-type", response_model=List[VaccineTypeResponse])
def get_vaccine_types(db: Session = Depends(get_db)):
    vaccine_types = db.query(VaccineType).all()

    return vaccine_types

@router.delete("/vaccine-type", response_model=VaccineTypeResponse)
def delete_vaccine_type(vaccine_type_id: int, db: Session = Depends(get_db)):
    vaccine_type = db.query(VaccineType).filter(VaccineType.id == vaccine_type_id).first()

    db.delete(vaccine_type)
    db.commit()

    return


@router.post("/vaccine", response_model=VaccineResponse)
def create_vaccine(request: VaccineCreate, db: Session = Depends(get_db)):
    vaccine_data = request.model_dump()
    new_vaccine = VaccineCreate(**vaccine_data)

    db.add(new_vaccine)
    db.commit()
    db.refresh(new_vaccine)

    return new_vaccine

@router.get("/vaccine", response_model=List[VaccineResponse])
def get_vaccine(db: Session = Depends(get_db)):
    vaccines = db.query(Vaccine).all()

    return vaccines

@router.delete("/vaccine", response_model=VaccineResponse)
def delete_vaccine(vaccine_id: int, db: Session = Depends(get_db)):
    vaccine = db.query(Vaccine).filter(Vaccine.id == vaccine_id).first()

    db.delete(vaccine)
    db.commit()

    return