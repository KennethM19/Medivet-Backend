from datetime import datetime, time, date

from pydantic import BaseModel

# --------DIETA---------
class DietBase(BaseModel):
    food: str
    amount: int
    last_feeding: datetime | None = None

class DietCreate(DietBase):
    pet_id: int

class DietUpdate(BaseModel):
    food: str | None = None
    amount: int | None = None
    last_feeding: datetime | None = None

class DietResponse(DietBase):
    id: int
    pet_id: int

    class Config:
        from_attributes = True

#-------HORARIO DIETA -----------
class DietScheduleBase(BaseModel):
    time: time

class DietScheduleCreate(DietScheduleBase):
    diet_id: int

class DietScheduleUpdate(BaseModel):
    time: time | None = None

class DietScheduleResponse(DietScheduleBase):
    id: int
    diet_id: int

    class Config:
        from_attributes = True

#----------ACTIVIDAD--------------
class ActivityBase(BaseModel):
    name: str
    description: str | None = None
    frequency_days: int
    last_done: date | None = None
    next_due_date: date | None = None
    notes: str | None = None

class ActivityCreate(ActivityBase):
    pet_id: int

class ActivityUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    frequency_days: int | None = None
    last_done: date | None = None
    next_due_date: date | None = None
    notes: str | None = None

class ActivityResponse(ActivityBase):
    id: int
    pet_id: int

    class Config:
        from_attributes = True

#----------PRESCRIPCION------------
class PrescriptionBase(BaseModel):
    diagnosis: str | None = None
    start_date: date
    end_date: date
    notes: str | None = None

class PrescriptionCreate(PrescriptionBase):
    pet_id: int

class PrescriptionUpdate(BaseModel):
    diagnosis: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    notes: str | None = None

class PrescriptionResponse(PrescriptionBase):
    id: int
    pet_id: int

    class Config:
        from_attributes = True

#------------DOSIS-------------
class PrescriptionDoseBase(BaseModel):
    medicine_name: str
    dose_amount: str
    frequency_hours: int
    duration_days: int
    first_dose: datetime
    next_dose: datetime | None = None
    taken: bool | None = False

class PrescriptionDoseCreate(PrescriptionDoseBase):
    prescription_id: int

class PrescriptionDoseUpdate(BaseModel):
    medicine_name: str | None = None
    dose_amount: str | None = None
    frequency_hours: int | None = None
    duration_days: int | None = None
    first_dose: datetime | None = None
    next_dose: datetime | None = None
    taken: bool | None = None

class PrescriptionDoseResponse(PrescriptionDoseBase):
    id: int
    prescription_id: int

    class Config:
        from_attributes = True

#-------------NOTIFICACIONES-----------
class NotificationBase(BaseModel):
    type: str
    title: str
    message: str
    scheduled_at: datetime

class NotificationCreate(NotificationBase):
    pet_id: int

class NotificationUpdate(BaseModel):
    type: str | None = None
    title: str | None = None
    message: str | None = None
    scheduled_at: datetime | None = None
    sent: bool | None = None

class NotificationResponse(NotificationBase):
    id: int
    pet_id: int
    sent: bool
    created_at: datetime

    class Config:
        from_attributes = True


