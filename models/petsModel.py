from sqlalchemy import Column, Integer, ForeignKey, String, Double, Boolean
from sqlalchemy.orm import relationship

from database import Base

class Sex(Base):
    __tablename__ = 'sex'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Species(Base):
    __tablename__ = 'species'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    races = relationship('Race', back_populates='specie')
    pets = relationship('Pet', back_populates='specie')

class Race(Base):
    __tablename__ = 'race'
    id = Column(Integer, primary_key=True)
    species_id = Column(Integer, ForeignKey('species.id'))
    name = Column(String)

    specie = relationship('Species', back_populates='races')
    pets = relationship('Pet', back_populates='race')

class Pets(Base):
    __tablename__ = 'pet'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    num_doc = Column(String, nullable=True)
    name = Column(String, nullable=False)
    photo = Column(String, nullable=True)
    sex_id = Column(Integer, ForeignKey('sex.id'), nullable=False)
    specie_id = Column(Integer, ForeignKey('species.id'), nullable=False)
    race_id = Column(Integer, ForeignKey('race.id'), nullable=False)
    year_birth = Column(Integer, nullable=True)
    month_birth = Column(Integer, nullable=True)
    weight = Column(Double, nullable=True)
    neutered = Column(Boolean, nullable=False, default=False)

    specie = relationship('Species', back_populates='pets')
    race = relationship('Race', back_populates='pets')
    user = relationship('User', back_populates='pets')