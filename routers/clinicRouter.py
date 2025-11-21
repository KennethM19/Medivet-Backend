from typing import Optional

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from models import clinicModel
from models.clinicModel import Clinic, Appointment, Schedules
from models.intemediateTables import ClinicServices
from schemes.clinicSchemes import SchedulesResponse, ClinicResponse, ClinicCreate, ServiceResponse, ServiceCreate, \
    ServiceUpdate, ClinicUpdate, AppointmentBase, AppointmentCreate, AppointmentUpdate, SchedulesCreate, SchedulesBase

router = APIRouter(prefix="/clinics", tags=["Clinics"])

#CREAR SERVICIOS
@router.post("", response_model=ServiceResponse)
def create_service(data: ServiceCreate, db: Session = Depends(get_db)):
    service = clinicModel.Services(**data.model_dump())
    db.add(service)
    db.commit()
    db.refresh(service)
    return service

#OBTENER SERVICIOS
@router.get("", response_model=list[ServiceResponse])
def get_services(service_id = Optional[int], db: Session = Depends(get_db)):
    if service_id is not None:
        service = (
            db.query(clinicModel.Services)
            .filter(clinicModel.Services.id == service_id)
            .first()
        )
        if not service:
            raise HTTPException(status_code=404, detail="Service not found")
        return service

    # Si no pasó service_id → devuelve todos
    return db.query(clinicModel.Services).all()

#ACTUALIZAR SERVICIOS
@router.put("", response_model=ServiceResponse)
def update_service(service_id: int, data: ServiceUpdate, db: Session = Depends(get_db)):
    service = db.query(clinicModel.Services).filter(clinicModel.Services.id == service_id).first()
    if not service:
        raise HTTPException(404, "Service not found")

    for key, value in data.model_dump().items():
        setattr(service, key, value)

    db.commit()
    db.refresh(service)
    return service

#ELIMINAR SERVICIOS
@router.delete("")
def delete_service(service_id: int, db: Session = Depends(get_db)):
    service = db.query(clinicModel.Services).filter(clinicModel.Services.id == service_id).first()
    if not service:
        raise HTTPException(404, "Service not found")

    db.delete(service)
    db.commit()
    return {"message": "Service deleted"}

#CREAR CLINICA
@router.post("", response_model=ClinicResponse, status_code=status.HTTP_201_CREATED)
def create_clinic(request: ClinicCreate, db: Session = Depends(get_db)):

    if request.ruc is not None:
        existing_clinic = db.query(Clinic).filter_by(ruc=request.ruc).first()

        if existing_clinic:
            raise HTTPException(status_code=400, detail="Clinic already exists")

    clinic_data = request.model_dump()

    db_clinics = clinicModel.Clinic(**clinic_data)
    db.add(db_clinics)
    db.commit()
    db.refresh(db_clinics)

    return db_clinics

#OBTENER CLINICA
@router.get("", response_model=list[ClinicResponse])
def get_clinics(clinic_id:Optional[int], db: Session = Depends(get_db)):

    if clinic_id is not None:
        clinic = (
            db.query(clinicModel.Clinic)
            .filter(clinicModel.Clinic.id == clinic_id)
            .first()
        )
        if not clinic:
            raise HTTPException(404, "Clinic not found")
        return clinic

    return db.query(clinicModel.Clinic).all()

#ACTUALZIAR CLÍNICA
@router.put("", response_model=ClinicResponse)
def update_clinic(clinic_id: int, data: ClinicUpdate, db: Session = Depends(get_db)):
    clinic = db.query(clinicModel.Clinic).filter(clinicModel.Clinic.id == clinic_id).first()
    if not clinic:
        raise HTTPException(404, "Clinic not found")

    for key, value in data.dict().items():
        setattr(clinic, key, value)

    db.commit()
    db.refresh(clinic)
    return clinic

#ELIMINAR CLINICA
@router.delete("")
def delete_clinic(clinic_id: int, db: Session = Depends(get_db)):
    clinic = db.query(clinicModel.Clinic).filter(clinicModel.Clinic.id == clinic_id).first()
    if not clinic:
        raise HTTPException(404, "Clinic not found")

    db.delete(clinic)
    db.commit()
    return {"message": "Clinic deleted"}

#OBTENER SERVICIOS DE CLINICA
@router.get("/{clinic_id}/services", response_model=list[ServiceResponse])
def get_clinic_services(clinic_id: int, db: Session = Depends(get_db)):
    clinic = db.query(clinicModel.Clinic).filter(clinicModel.Clinic.id == clinic_id).first()
    if not clinic:
        raise HTTPException(404, "Clinic not found")

    services = (
        db.query(clinicModel.Services)
        .join(ClinicServices, ClinicServices.service_id == clinicModel.Services.id)
        .filter(ClinicServices.clinic_id == clinic_id)
        .all()
    )
    return services

#ASIGNAR SERVICOS A CLINICA
@router.post("/{clinic_id}/services/{service_id}")
def add_service_to_clinic(clinic_id: int, service_id: int, db: Session = Depends(get_db)):
    exists = db.query(ClinicServices).filter_by(clinic_id=clinic_id, service_id=service_id).first()
    if exists:
        raise HTTPException(400, "Service already assigned to clinic")

    relation = ClinicServices(clinic_id=clinic_id, service_id=service_id)
    db.add(relation)
    db.commit()
    return {"message": "Service assigned to clinic"}

#ELIMINAR SERVICIOS DE CLINICA
@router.delete("/{clinic_id}/services/{service_id}")
def remove_service_from_clinic(clinic_id: int, service_id: int, db: Session = Depends(get_db)):
    relation = db.query(ClinicServices).filter_by(clinic_id=clinic_id, service_id=service_id).first()
    if not relation:
        raise HTTPException(404, "Service not assigned to clinic")

    db.delete(relation)
    db.commit()
    return {"message": "Service removed from clinic"}

#CREAR CITA
@router.post("", response_model=AppointmentBase)
def create_appointment(data: AppointmentCreate, db: Session = Depends(get_db)):
    appt = Appointment(**data.dict())
    db.add(appt)
    db.commit()
    db.refresh(appt)
    return appt

#OBTENER CITA
@router.get("", response_model=list[AppointmentBase])
def get_appointments(appointment_id: Optional[int], db: Session = Depends(get_db)):

    if appointment_id is not None:
        appointments = (
            db.query(Appointment)
            .filter(Appointment.id == appointment_id)
            .first()
        )

        if not appointments:
            raise HTTPException(404, "Appointment not found")
        return appointments

    return db.query(Appointment).all()

#ACTUALIZAR CITA
@router.put("", response_model=AppointmentBase)
def update_appointment(appointment_id: int, data: AppointmentUpdate, db: Session = Depends(get_db)):
    appt = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appt:
        raise HTTPException(404, "Appointment not found")

    for key, value in data.dict().items():
        setattr(appt, key, value)

    db.commit()
    db.refresh(appt)
    return appt

#ELIMINAR CITA
@router.delete("")
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appt = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appt:
        raise HTTPException(404, "Appointment not found")

    db.delete(appt)
    db.commit()
    return {"message": "Appointment deleted"}

#CREAR HORARIO
@router.post("", response_model=SchedulesResponse)
def create_schedule(data: SchedulesCreate, db: Session = Depends(get_db)):
    schedule = Schedules(**data.dict())
    db.add(schedule)
    db.commit()
    db.refresh(schedule)
    return schedule

#OBTENER HORARIO
@router.get("", response_model=list[SchedulesResponse])
def get_schedules(schedule_id: Optional[int] ,db: Session = Depends(get_db)):

    if schedule_id is not None:
        schedules = (
            db.query(Schedules)
            .filter(Schedules.id == schedule_id)
            .first()
        )

        if not schedules:
            raise HTTPException(404, "Schedule not found")
        return schedules

    return db.query(Schedules).all()

#ACTRUALIZAR HORARIO
@router.put("", response_model=SchedulesResponse)
def update_schedule(schedule_id: int, data: SchedulesBase, db: Session = Depends(get_db)):
    schedule = db.query(Schedules).filter(Schedules.id == schedule_id).first()
    if not schedule:
        raise HTTPException(404, "Schedule not found")

    for key, value in data.dict().items():
        setattr(schedule, key, value)

    db.commit()
    db.refresh(schedule)
    return schedule

#ELIMINAR HORARIO
@router.delete("")
def delete_schedule(schedule_id: int, db: Session = Depends(get_db)):
    schedule = db.query(Schedules).filter(Schedules.id == schedule_id).first()
    if not schedule:
        raise HTTPException(404, "Schedule not found")

    db.delete(schedule)
    db.commit()
    return {"message": "Schedule deleted"}
