from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship, Relationship
from database import Base

class User(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    correo = Column(String, nullable=False)
    contrasena = Column(String, nullable=False)

    mascotas = relationship("Pet", back_populates="dueño")


class Pet(Base):
    __tablename__ = 'mascotas'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    especie = Column(String, nullable=False)
    raza = Column(String, nullable=False)
    fecha_nac = Column(Date, nullable=True)
    dueño_id = Column(Integer, ForeignKey('usuarios.id'))

    dueño = relationship("User", back_populates="mascotas")