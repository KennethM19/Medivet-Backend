from sqlalchemy import Column, Integer, ForeignKey, Date, String
from sqlalchemy.orm import relationship

from database import Base

class PetVaccine(Base):
    __tablename__ = "pet_vaccine"
    id = Column(Integer, primary_key=True)
    pet_id = Column(Integer, ForeignKey("pet.id"), nullable=False)
    vaccine_type_id = Column(Integer, ForeignKey("vaccine_type.id"), nullable=False)

    date_applied = Column(Date, nullable=True)
    dose = Column(String, nullable=True)
    batch = Column(String, nullable=True)
    veterinarian = Column(String, nullable=True)

    pet = relationship("Pets", back_populates="vaccines")
    vaccine_type = relationship("VaccineType", back_populates="pets")

class ClinicServices(Base):
    __tablename__ = 'clinic_services'
    id = Column(Integer, primary_key=True)
    clinic_id = Column(Integer, ForeignKey("clinic.id"), nullable=False)
    service_id = Column(Integer, ForeignKey("service.id"), nullable=False)

    clinics = relationship("Clinic", back_populates="services")
    services = relationship("Service", back_populates="clinics")