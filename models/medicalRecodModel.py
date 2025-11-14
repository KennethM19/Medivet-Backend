from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from database import Base

class VaccineType(Base):
    __tablename__ = 'vaccine_type'
    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)

    vaccine = relationship('Vaccine', back_populates='type')

class Vaccine(Base):
    __tablename__ = 'vaccine'
    id = Column(Integer, primary_key=True)
    pet_id = Column(Integer, ForeignKey('pet.id'))
    vaccine_type_id = Column(Integer, ForeignKey('vaccine_type.id'))

    pets = relationship('Pets', back_populates='vaccine')
    type = relationship('VaccineType', back_populates='vaccine')
