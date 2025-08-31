from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime, timezone

# Database configuration
DB_PATH = "sqlite:///smartqueue.db"
engine = create_engine(DB_PATH, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


# Tables
class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=True)
    role = Column(String, nullable=False, default="manager")


class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)


class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    location_id = Column(Integer)
    patient_name = Column(String, nullable=False)
    priority = Column(String, default="normal")
    status = Column(String, default="waiting")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    message = Column(String, nullable=False)
    sent_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


# Initialize database tables
def init_db():
    Base.metadata.create_all(bind=engine)


# Seed default admin
def seed_admin():
    session = SessionLocal()
    admin = session.query(Admin).filter_by(username="Purity").first()
    if not admin:
        admin = Admin(username="Purity", role="manager")
        session.add(admin)
        session.commit()
    session.close()


# Seed default locations
def seed_locations():
    session = SessionLocal()
    default_locations = ["CityHospital", "GreenClinic", "MediCenter"]
    for loc_name in default_locations:
        if not session.query(Location).filter_by(name=loc_name).first():
            session.add(Location(name=loc_name))
    session.commit()
    session.close()
