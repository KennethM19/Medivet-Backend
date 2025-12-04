from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import get_db
from models.utilPetsModel import Diet, DietSchedule, Activity, Prescription, PrescriptionDose, Notification
from schemes.utilPetSchemes import DietResponse, DietCreate, DietUpdate, DietScheduleResponse, DietScheduleCreate, \
    DietScheduleUpdate, ActivityResponse, ActivityCreate, PrescriptionResponse, PrescriptionCreate, PrescriptionUpdate, \
    PrescriptionDoseResponse, PrescriptionDoseCreate, PrescriptionDoseUpdate, NotificationResponse, NotificationCreate, \
    NotificationUpdate, ActivityUpdate

router = APIRouter(
    prefix="/utilPet",
    tags=["utilPet"],
)

#------DIETA--------
@router.get("/diet", response_model=list[DietResponse])
def get_diets(diet_id: Optional[int] = Query(None, description="Filer by diet ID") , db: Session = Depends(get_db)):

    if diet_id is not None:
        diet = (
            db.query(Diet)
            .filter(Diet.id == diet_id)
            .first()
        )

        if not diet:
            raise HTTPException(status_code=404, detail="Diet not found")
        return [diet]

    return db.query(Diet).all()

@router.post("/diet", response_model=DietResponse)
def create_diet(payload: DietCreate, db: Session = Depends(get_db)):
    diet = Diet(**payload.dict())
    db.add(diet)
    db.commit()
    db.refresh(diet)
    return diet


@router.put("/diet", response_model=DietResponse)
def update_diet(diet_id: int, payload: DietUpdate, db: Session = Depends(get_db)):
    diet = db.query(Diet).get(diet_id)
    if not diet:
        raise HTTPException(404, "Diet not found")
    for key, value in payload.dict(exclude_unset=True).items():
        setattr(diet, key, value)
    db.commit()
    db.refresh(diet)
    return diet


@router.delete("/diet")
def delete_diet(diet_id: int, db: Session = Depends(get_db)):
    diet = db.query(Diet).get(diet_id)
    if not diet:
        raise HTTPException(404, "Diet not found")
    db.delete(diet)
    db.commit()
    return {"message": "Diet deleted"}

#-----HORARIO DIETA----------
@router.post("/diet-schedule", response_model=DietScheduleResponse)
def create_schedule(payload: DietScheduleCreate, db: Session = Depends(get_db)):
    schedule = DietSchedule(**payload.dict())
    db.add(schedule)
    db.commit()
    db.refresh(schedule)
    return schedule

@router.post("/diet-schedule", response_model=DietScheduleResponse)
def create_schedule(payload: DietScheduleCreate, db: Session = Depends(get_db)):
    schedule = DietSchedule(**payload.dict())
    db.add(schedule)
    db.commit()
    db.refresh(schedule)
    return schedule


@router.put("/diet-schedule", response_model=DietScheduleResponse)
def update_schedule(schedule_id: int, payload: DietScheduleUpdate, db: Session = Depends(get_db)):
    schedule = db.query(DietSchedule).get(schedule_id)
    if not schedule:
        raise HTTPException(404, "Schedule not found")

    for key, value in payload.dict(exclude_unset=True).items():
        setattr(schedule, key, value)

    db.commit()
    db.refresh(schedule)
    return schedule


@router.delete("/diet-schedule")
def delete_schedule(schedule_id: int, db: Session = Depends(get_db)):
    schedule = db.query(DietSchedule).get(schedule_id)
    if not schedule:
        raise HTTPException(404, "Schedule not found")

    db.delete(schedule)
    db.commit()
    return {"message": "Schedule deleted successfully"}

#----------ACTIVIDADES-------------
@router.get("/activities", response_model=list[ActivityResponse])
def get_activities(db: Session = Depends(get_db)):
    return db.query(Activity).all()


@router.post("/activities", response_model=ActivityResponse)
def create_activity(payload: ActivityCreate, db: Session = Depends(get_db)):
    activity = Activity(**payload.dict())
    db.add(activity)
    db.commit()
    db.refresh(activity)
    return activity


@router.put("/activities", response_model=ActivityResponse)
def update_activity(activity_id: int, payload: ActivityUpdate, db: Session = Depends(get_db)):
    activity = db.query(Activity).get(activity_id)
    if not activity:
        raise HTTPException(404, "Activity not found")

    for key, value in payload.dict(exclude_unset=True).items():
        setattr(activity, key, value)

    db.commit()
    db.refresh(activity)
    return activity


@router.delete("/activities")
def delete_activity(activity_id: int, db: Session = Depends(get_db)):
    activity = db.query(Activity).get(activity_id)
    if not activity:
        raise HTTPException(404, "Activity not found")

    db.delete(activity)
    db.commit()
    return {"message": "Activity deleted successfully"}

#------------PRESCRIPCIÓN--------------
@router.get("/prescriptions", response_model=list[PrescriptionResponse])
def get_prescriptions(db: Session = Depends(get_db)):
    return db.query(Prescription).all()


@router.post("/prescriptions", response_model=PrescriptionResponse)
def create_prescription(payload: PrescriptionCreate, db: Session = Depends(get_db)):
    prescription = Prescription(**payload.dict())
    db.add(prescription)
    db.commit()
    db.refresh(prescription)
    return prescription


@router.put("/prescriptions", response_model=PrescriptionResponse)
def update_prescription(prescription_id: int, payload: PrescriptionUpdate, db: Session = Depends(get_db)):
    prescription = db.query(Prescription).get(prescription_id)
    if not prescription:
        raise HTTPException(404, "Prescription not found")

    for key, value in payload.dict(exclude_unset=True).items():
        setattr(prescription, key, value)

    db.commit()
    db.refresh(prescription)
    return prescription


@router.delete("/prescriptions")
def delete_prescription(prescription_id: int, db: Session = Depends(get_db)):
    prescription = db.query(Prescription).get(prescription_id)
    if not prescription:
        raise HTTPException(404, "Prescription not found")

    db.delete(prescription)
    db.commit()
    return {"message": "Prescription deleted successfully"}

#-----------------DOSIS DE PRESCRIPCIÓN-------------
@router.get("/doses", response_model=list[PrescriptionDoseResponse])
def get_doses(db: Session = Depends(get_db)):
    return db.query(PrescriptionDose).all()


@router.post("/doses", response_model=PrescriptionDoseResponse)
def create_dose(payload: PrescriptionDoseCreate, db: Session = Depends(get_db)):
    dose = PrescriptionDose(**payload.dict())
    db.add(dose)
    db.commit()
    db.refresh(dose)
    return dose


@router.put("/doses", response_model=PrescriptionDoseResponse)
def update_dose(dose_id: int, payload: PrescriptionDoseUpdate, db: Session = Depends(get_db)):
    dose = db.query(PrescriptionDose).get(dose_id)
    if not dose:
        raise HTTPException(404, "Dose not found")

    for key, value in payload.dict(exclude_unset=True).items():
        setattr(dose, key, value)

    db.commit()
    db.refresh(dose)
    return dose


@router.delete("/doses")
def delete_dose(dose_id: int, db: Session = Depends(get_db)):
    dose = db.query(PrescriptionDose).get(dose_id)
    if not dose:
        raise HTTPException(404, "Dose not found")

    db.delete(dose)
    db.commit()
    return {"message": "Dose deleted successfully"}

#--------NOTIFICACIÓN--------------
@router.get("/notifications", response_model=list[NotificationResponse])
def get_notifications(db: Session = Depends(get_db)):
    return db.query(Notification).all()


@router.post("/notifications", response_model=NotificationResponse)
def create_notification(payload: NotificationCreate, db: Session = Depends(get_db)):
    notification = Notification(**payload.dict())
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification


@router.put("/notifications", response_model=NotificationResponse)
def update_notification(notification_id: int, payload: NotificationUpdate, db: Session = Depends(get_db)):
    notification = db.query(Notification).get(notification_id)
    if not notification:
        raise HTTPException(404, "Notification not found")

    for key, value in payload.dict(exclude_unset=True).items():
        setattr(notification, key, value)

    db.commit()
    db.refresh(notification)
    return notification


@router.delete("/notifications")
def delete_notification(notification_id: int, db: Session = Depends(get_db)):
    notification = db.query(Notification).get(notification_id)
    if not notification:
        raise HTTPException(404, "Notification not found")

    db.delete(notification)
    db.commit()
    return {"message": "Notification deleted successfully"}


