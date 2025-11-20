from sqlalchemy import Column, Integer, ForeignKey, String, Double, Boolean
from sqlalchemy.orm import relationship

from database import Base

class Sex(Base):
    __tablename__ = 'sex'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    pets = relationship('Pets', back_populates='sex')

class Species(Base):
    __tablename__ = 'species'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    breeds = relationship('Breed', back_populates='specie')
    pets = relationship('Pets', back_populates='specie')
    vaccine_type = relationship('VaccineType', back_populates='specie')

class Breed(Base):
    __tablename__ = 'breed'
    id = Column(Integer, primary_key=True)
    species_id = Column(Integer, ForeignKey('species.id'))
    name = Column(String)

    specie = relationship('Species', back_populates='breeds')
    pets = relationship('Pets', back_populates='breed')

class Pets(Base):
    __tablename__ = 'pet'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    num_doc = Column(String, nullable=True)
    name = Column(String, nullable=False)
    photo = Column(String, nullable=True)
    sex_id = Column(Integer, ForeignKey('sex.id'), nullable=False)
    specie_id = Column(Integer, ForeignKey('species.id'), nullable=False)
    breed_id = Column(Integer, ForeignKey('breed.id'), nullable=False)
    year_birth = Column(Integer, nullable=True)
    month_birth = Column(Integer, nullable=True)
    weight = Column(Double, nullable=True)
    neutered = Column(Boolean, nullable=False, default=False)

    specie = relationship('Species', back_populates='pets')
    breed = relationship('Breed', back_populates='pets')
    user = relationship('Users', back_populates='pets')
    sex = relationship('Sex', back_populates='pets')

    vaccines = relationship("PetVaccine", back_populates="pet")