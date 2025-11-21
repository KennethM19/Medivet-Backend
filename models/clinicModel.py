from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Clinic(Base):
    __tablename__ = 'clinic'
    id = Column(Integer, primary_key=True)
    ruc = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    district = Column(String, nullable=False)
    province = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    latitude = Column(String, nullable=False)
    longitude = Column(String, nullable=False)
    webPage = Column(String, nullable=True)

    services = relationship("ClinicServices", back_populates="clinics")
    schedules = relationship("Schedules", back_populates="clinics")
    appointments = relationship("Appointments", back_populates="clinics")

class Services(Base):
    __tablename__ = 'service'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)

    clinics = relationship("ClinicServices", back_populates="services")
    appointments = relationship("Appointments", back_populates="services")

class Appointment(Base):
    __tablename__ = 'appointment'
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    reason = Column(String, nullable=False)

    clinic_id = Column(Integer, ForeignKey('clinic.id'), nullable=False)
    service_id = Column(Integer, ForeignKey('service.id'), nullable=False)
    status_id = Column(Integer, ForeignKey('appointment_status.id'), nullable=False)
    pet_id = Column(Integer, ForeignKey('pet.id'), nullable=False)

    status = relationship("AppointmentStatus", back_populates="appointments")
    clinics = relationship("Clinic", back_populates="appointments")
    services = relationship("Services", back_populates="appointments")
    pets = relationship("Pets", back_populates="appointments")

class AppointmentStatus(Base):
    __tablename__ = 'appointment_status'
    id = Column(Integer, primary_key=True)
    status = Column(String, nullable=False)

    appointments = relationship("Appointment", back_populates="status")

class Schedules(Base):
    __tablename__ = 'schedules'
    id = Column(Integer, primary_key=True)
    clinic_id = Column(Integer, ForeignKey("clinic.id"), nullable=False)
    day = Column(String, nullable=False)
    open_time = Column(Time, nullable=False)
    close_time = Column(Time, nullable=False)

    clinics = relationship("Clinic", back_populates="schedules")
