from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
# REMOVE: from sqlalchemy.ext.declarative import declarative_base
# REMOVE: Base = declarative_base()
from app.database.database import Base  # ADD THIS INSTEAD

class Doctor(Base):
    __tablename__ = "doctors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    specialty = Column(String)

class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String)
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    appointment_time = Column(DateTime)
    status = Column(String) 
    language = Column(String)