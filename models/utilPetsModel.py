from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Time, Date, Boolean
from sqlalchemy.orm import relationship

from database import Base


class Diet(Base):
    __tablename__ = "diet"
    id = Column(Integer, primary_key=True)
    pet_id = Column(Integer, ForeignKey("pet.id"))
    food = Column(String)
    amount = Column(Integer)

    last_feeding = Column(DateTime, nullable=True)

    pet = relationship("Pets", back_populates="diets")
    schedules = relationship("DietSchedule", back_populates="diet")

class DietSchedule(Base):
    __tablename__ = "diet_schedule"
    id = Column(Integer, primary_key=True)
    diet_id = Column(Integer, ForeignKey("diet.id"))
    time = Column(Time)

    diet = relationship("Diet", back_populates="schedules")

class Activity(Base):
    __tablename__ = "activities"
    id = Column(Integer, primary_key=True)
    pet_id = Column(Integer, ForeignKey("pet.id"))

    name = Column(String)
    description = Column(String)

    frequency_days = Column(Integer)
    last_done = Column(Date)

    next_due_date = Column(Date)
    notes = Column(String)

    pet = relationship("Pets", back_populates="activities")

class Prescription(Base):
    __tablename__ = "prescriptions"
    id = Column(Integer, primary_key=True)

    pet_id = Column(Integer, ForeignKey("pet.id"))
    diagnosis = Column(String)

    start_date = Column(Date)
    end_date = Column(Date)

    notes = Column(String)

    pet = relationship("Pets", back_populates="prescriptions")
    doses = relationship("PrescriptionDose", back_populates="prescription")


class PrescriptionDose(Base):
    __tablename__ = "prescription_doses"
    id = Column(Integer, primary_key=True)

    prescription_id = Column(Integer, ForeignKey("prescriptions.id"))

    medicine_name = Column(String)
    dose_amount = Column(String)

    frequency_hours = Column(Integer)
    duration_days = Column(Integer)

    first_dose = Column(DateTime)

    next_dose = Column(DateTime)

    taken = Column(Boolean, default=False)

    prescription = relationship("Prescription", back_populates="doses")


class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True)
    pet_id = Column(Integer, ForeignKey("pet.id"))

    type = Column(String)
    title = Column(String)
    message = Column(String)
    scheduled_at = Column(DateTime)

    sent = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

