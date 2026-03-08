import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.database import Base
from app.database.models import Doctor

# 1. Connect to the EXACT same database file the app uses
DB_PATH = "sqlite:///./2care_ai.db"
engine = create_engine(DB_PATH)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def force_populate():
    # 2. Force create tables if they don't exist
    print("Initializing Database...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # 3. Clear any existing partial data to start fresh
        db.query(Doctor).delete()
        
        # 4. List of 10 Doctors
        doctors_data = [
            {"name": "Arjun Sharma", "specialty": "Cardiologist"},
            {"name": "Priya Nair", "specialty": "Dermatologist"},
            {"name": "Suresh Iyer", "specialty": "Neurologist"},
            {"name": "Kavita Reddy", "specialty": "Pediatrician"},
            {"name": "Anjali Gupta", "specialty": "Gynecologist"},
            {"name": "Vikram Singh", "specialty": "Orthopedic Surgeon"},
            {"name": "Meenakshi Sundaram", "specialty": "Ophthalmologist"},
            {"name": "Rahul Verma", "specialty": "General Physician"},
            {"name": "Deepa Lakshmi", "specialty": "Psychiatrist"},
            {"name": "Karthik Raja", "specialty": "ENT Specialist"}
        ]

        print("Inserting 10 doctors...")
        for doc in doctors_data:
            new_doc = Doctor(name=doc["name"], specialty=doc["specialty"])
            db.add(new_doc)
        
        db.commit()
        
        # 5. FINAL VERIFICATION
        count = db.query(Doctor).count()
        print(f"✅ DONE! Database verified. Total doctors found: {count}")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    force_populate()