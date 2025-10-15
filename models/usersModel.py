from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from database import Base

class Role(Base):
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    users = relationship('Users', back_populates='role')

class TypeDocument(Base):
    __tablename__ = 'typedocument'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    users = relationship('Users', back_populates='type_document')

class Users(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    type_document_id = Column(Integer, ForeignKey('typedocument.id'), nullable=False)
    num_document = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)
    address = Column(String, nullable=False)
    num_cellphone = Column(String, nullable=True)
    num_telephone = Column(String, nullable=True)
    email = Column(String, unique=True)
    password = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey('role.id'), nullable=False)

    type_document = relationship('TypeDocument', back_populates='users')
    role = relationship('Role', back_populates='users')
    pets = relationship('Pets', back_populates='user')
