from sqlalchemy import Column, Integer, String, Date, Time

from database import Base


class Clinic(Base):
    __tablename__ = 'clinic'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    district = Column(String, nullable=False)
    province = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    latitude = Column(String, nullable=False)
    longitude = Column(String, nullable=False)
    schedules = Column(String, nullable=False)
    webPage = Column(String, nullable=False)

class Services(Base):
    __tablename__ = 'services'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)

class ClinicServices(Base):
    __tablename__ = 'clinic_services'
    id = Column(Integer, primary_key=True)

class Appointment(Base):
    __tablename__ = 'appointment'
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    reason = Column(String, nullable=False)

class AppointmentStatus(Base):
    __tablename__ = 'appointment_status'
    id = Column(Integer, primary_key=True)
    status = Column(String, nullable=False)

class Schedules(Base):
    __tablename__ = 'schedules'
    id = Column(Integer, primary_key=True)
