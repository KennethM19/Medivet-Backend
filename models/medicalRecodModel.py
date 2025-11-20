from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from database import Base

class VaccineType(Base):
    __tablename__ = 'vaccine_type'
    id = Column(Integer, primary_key=True)
    specie_id = Column(Integer, ForeignKey('species.id'))
    type = Column(String, nullable=False)

    specie = relationship('Species', back_populates='vaccine_type')

    pets = relationship("PetVaccine", back_populates="vaccine_type")
