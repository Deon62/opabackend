from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Host(Base):
    """Car owners/rental hosts"""
    __tablename__ = "hosts"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship to cars
    cars = relationship("Car", back_populates="host")


class Client(Base):
    """Car renters/clients"""
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    
    # Profile fields
    bio = Column(Text, nullable=True)
    fun_fact = Column(Text, nullable=True)
    mobile_number = Column(String(50), nullable=True)
    id_number = Column(String(100), nullable=True)  # Driver's licence/passport number
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Car(Base):
    """Car listings"""
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    host_id = Column(Integer, ForeignKey("hosts.id"), nullable=False)
    
    # Endpoint 1: Basics
    name = Column(String(255))
    model = Column(String(100))
    body_type = Column(String(50))
    year = Column(Integer)
    description = Column(Text)
    
    # Endpoint 2: Technical Specs
    seats = Column(Integer)
    fuel_type = Column(String(50))
    transmission = Column(String(50))
    color = Column(String(50))
    mileage = Column(Integer)
    features = Column(Text)  # JSON string for up to 12 features
    
    # Endpoint 3: Pricing & Rules
    daily_rate = Column(Float)
    weekly_rate = Column(Float)
    monthly_rate = Column(Float)
    min_rental_days = Column(Integer)
    max_rental_days = Column(Integer, nullable=True)
    min_age_requirement = Column(Integer)
    rules = Column(Text)
    
    # Endpoint 4: Location
    location_name = Column(String(255), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    
    # Status tracking
    is_complete = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship to host
    host = relationship("Host", back_populates="cars")


