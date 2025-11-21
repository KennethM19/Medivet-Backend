from typing import Optional
from datetime import date, time

from pydantic import BaseModel

class ServiceBase(BaseModel):
    name: str
    description: str

class ServiceCreate(ServiceBase):
    pass

class ServiceUpdate(ServiceBase):
    pass

class ServiceResponse(ServiceBase):
    id: int
    name: str
    description: str


class ClinicBase(BaseModel):
    ruc: str
    name: str
    address: str
    district: str
    province: str
    phone: str
    latitude: str
    longitude: str
    webPage: Optional[str] = None

class ClinicCreate(ClinicBase):
    pass

class ClinicUpdate(ClinicBase):
    pass

class ClinicResponse(ClinicBase):
    id: int
    ruc: str
    name: str
    address: str
    district: str
    province: str
    phone: str
    latitude: str
    longitude: str
    webPage: Optional[str] = None

    service: Optional[ServiceResponse] = None


class AppointmentBase(BaseModel):
    date: date
    time: time
    reason: str
    clinic_id: int
    service_id: int
    status_id: int

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentUpdate(AppointmentBase):
    status_id: int

    services: ServiceResponse
    clinics: ClinicResponse

class SchedulesBase(BaseModel):
    clinic_id: int
    day: str
    open_time: str
    close_time: str

class SchedulesCreate(SchedulesBase):
    pass

class SchedulesResponse(SchedulesBase):
    id: int
    clinic_id: int
    day: str
    open_time: str
    close_time: str
    clinics: ClinicResponse


