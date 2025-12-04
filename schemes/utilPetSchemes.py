from datetime import datetime, time, date
from typing import Optional

from pydantic import BaseModel

# --------DIETA---------
class DietBase(BaseModel):
    food: str
    amount: int
    last_feeding: Optional[datetime] = None

class DietCreate(DietBase):
    pet_id: int

class DietUpdate(BaseModel):
    food: Optional[str] = None
    amount: Optional[int] = None
    last_feeding: Optional[datetime] = None

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
    time: Optional[time] = None

class DietScheduleResponse(DietScheduleBase):
    id: int
    diet_id: int

    class Config:
        from_attributes = True

#----------ACTIVIDAD--------------
class ActivityBase(BaseModel):
    name: str
    description: Optional[str] = None
    frequency_days: int
    last_done: Optional[date] = None
    next_due_date: Optional[date] = None
    notes: Optional[str] = None

class ActivityCreate(ActivityBase):
    pet_id: int

class ActivityUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    frequency_days: Optional[int] = None
    last_done: Optional[date] = None
    next_due_date: Optional[date] = None
    notes: Optional[str] = None

class ActivityResponse(ActivityBase):
    id: int
    pet_id: int

    class Config:
        from_attributes = True

#----------PRESCRIPCION------------
class PrescriptionBase(BaseModel):
    diagnosis: Optional[str] = None
    start_date: date
    end_date: date
    notes: Optional[str] = None

class PrescriptionCreate(PrescriptionBase):
    pet_id: int

class PrescriptionUpdate(BaseModel):
    diagnosis: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    notes: Optional[str] = None

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
    next_dose: Optional[datetime] = None
    taken: Optional[bool] = False

class PrescriptionDoseCreate(PrescriptionDoseBase):
    prescription_id: int

class PrescriptionDoseUpdate(BaseModel):
    medicine_name: Optional[str] = None
    dose_amount: Optional[str] = None
    frequency_hours: Optional[int] = None
    duration_days: Optional[int] = None
    first_dose: Optional[datetime] = None
    next_dose: Optional[datetime] = None
    taken: Optional[bool] = None

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
    type: Optional[str] = None
    title: Optional[str] = None
    message: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    sent: Optional[bool] = False

class NotificationResponse(NotificationBase):
    id: int
    pet_id: int
    sent: bool
    created_at: datetime

    class Config:
        from_attributes = True


