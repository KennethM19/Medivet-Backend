from sqlalchemy import Table, Column, Integer, ForeignKey, Date, String
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