from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import json

from app.database import get_db
from app.models import Car, Host
from app.schemas import (
    CarBasicsRequest,
    CarTechnicalSpecsRequest,
    CarPricingRulesRequest,
    CarLocationRequest,
    CarResponse
)
from app.auth import get_current_host

router = APIRouter()


def _car_to_response(db_car: Car) -> CarResponse:
    """Helper function to convert Car model to CarResponse"""
    features = None
    if db_car.features:
        try:
            features = json.loads(db_car.features)
        except (json.JSONDecodeError, TypeError):
            features = None
    
    return CarResponse(
        id=db_car.id,
        host_id=db_car.host_id,
        name=db_car.name,
        model=db_car.model,
        body_type=db_car.body_type,
        year=db_car.year,
        description=db_car.description,
        seats=db_car.seats,
        fuel_type=db_car.fuel_type,
        transmission=db_car.transmission,
        color=db_car.color,
        mileage=db_car.mileage,
        features=features,
        daily_rate=db_car.daily_rate,
        weekly_rate=db_car.weekly_rate,
        monthly_rate=db_car.monthly_rate,
        min_rental_days=db_car.min_rental_days,
        max_rental_days=db_car.max_rental_days,
        min_age_requirement=db_car.min_age_requirement,
        rules=db_car.rules,
        location_name=db_car.location_name,
        latitude=db_car.latitude,
        longitude=db_car.longitude,
        is_complete=db_car.is_complete,
        created_at=db_car.created_at,
        updated_at=db_car.updated_at
    )


@router.post("/cars/basics", response_model=CarResponse, status_code=status.HTTP_201_CREATED)
async def create_car_basics(
    request: CarBasicsRequest,
    current_host: Host = Depends(get_current_host),
    db: Session = Depends(get_db)
):
    """
    Endpoint 1: Create car with basic information
    
    - **name**: Car name
    - **model**: Car model
    - **body_type**: Body type (e.g., Sedan, SUV, Hatchback)
    - **year**: Manufacturing year
    - **description**: Long-form description of the car
    
    Creates a new car listing in incomplete state, linked to the authenticated host.
    """
    # Create new car record
    db_car = Car(
        host_id=current_host.id,
        name=request.name,
        model=request.model,
        body_type=request.body_type,
        year=request.year,
        description=request.description,
        is_complete=False
    )
    
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    
    return _car_to_response(db_car)


@router.put("/cars/{car_id}/specs", response_model=CarResponse)
async def update_car_specs(
    car_id: int,
    request: CarTechnicalSpecsRequest,
    current_host: Host = Depends(get_current_host),
    db: Session = Depends(get_db)
):
    """
    Endpoint 2: Update car with technical specifications
    
    - **seats**: Number of seats (1-50)
    - **fuel_type**: Fuel type (e.g., Gasoline, Diesel, Electric)
    - **transmission**: Transmission type (e.g., Manual, Automatic)
    - **color**: Car color
    - **mileage**: Current mileage
    - **features**: List of up to 12 optional features
    
    Updates an existing car record with technical specifications.
    """
    # Get car and verify ownership
    db_car = db.query(Car).filter(Car.id == car_id).first()
    if not db_car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Car not found"
        )
    
    if db_car.host_id != current_host.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this car"
        )
    
    # Update car specs
    db_car.seats = request.seats
    db_car.fuel_type = request.fuel_type
    db_car.transmission = request.transmission
    db_car.color = request.color
    db_car.mileage = request.mileage
    db_car.features = json.dumps(request.features) if request.features else None
    
    db.commit()
    db.refresh(db_car)
    
    return _car_to_response(db_car)


def _car_to_response(db_car: Car) -> CarResponse:
    """Helper function to convert Car model to CarResponse"""
    features = None
    if db_car.features:
        try:
            features = json.loads(db_car.features)
        except (json.JSONDecodeError, TypeError):
            features = None
    
    return CarResponse(
        id=db_car.id,
        host_id=db_car.host_id,
        name=db_car.name,
        model=db_car.model,
        body_type=db_car.body_type,
        year=db_car.year,
        description=db_car.description,
        seats=db_car.seats,
        fuel_type=db_car.fuel_type,
        transmission=db_car.transmission,
        color=db_car.color,
        mileage=db_car.mileage,
        features=features,
        daily_rate=db_car.daily_rate,
        weekly_rate=db_car.weekly_rate,
        monthly_rate=db_car.monthly_rate,
        min_rental_days=db_car.min_rental_days,
        max_rental_days=db_car.max_rental_days,
        min_age_requirement=db_car.min_age_requirement,
        rules=db_car.rules,
        location_name=db_car.location_name,
        latitude=db_car.latitude,
        longitude=db_car.longitude,
        is_complete=db_car.is_complete,
        created_at=db_car.created_at,
        updated_at=db_car.updated_at
    )


@router.put("/cars/{car_id}/pricing", response_model=CarResponse)
async def update_car_pricing(
    car_id: int,
    request: CarPricingRulesRequest,
    current_host: Host = Depends(get_current_host),
    db: Session = Depends(get_db)
):
    """
    Endpoint 3: Update car with pricing and rules
    
    - **daily_rate**: Daily rental rate (required, > 0)
    - **weekly_rate**: Weekly rental rate (required, > 0)
    - **monthly_rate**: Monthly rental rate (required, > 0)
    - **min_rental_days**: Minimum rental days (required, >= 1)
    - **max_rental_days**: Maximum rental days (optional, >= 1)
    - **min_age_requirement**: Minimum age requirement (required, 18-100)
    - **rules**: Text-based car rules
    
    Updates an existing car record with pricing and rental rules.
    """
    # Get car and verify ownership
    db_car = db.query(Car).filter(Car.id == car_id).first()
    if not db_car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Car not found"
        )
    
    if db_car.host_id != current_host.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this car"
        )
    
    # Update pricing and rules
    db_car.daily_rate = request.daily_rate
    db_car.weekly_rate = request.weekly_rate
    db_car.monthly_rate = request.monthly_rate
    db_car.min_rental_days = request.min_rental_days
    db_car.max_rental_days = request.max_rental_days
    db_car.min_age_requirement = request.min_age_requirement
    db_car.rules = request.rules
    
    db.commit()
    db.refresh(db_car)
    
    return _car_to_response(db_car)


@router.put("/cars/{car_id}/location", response_model=CarResponse)
async def update_car_location(
    car_id: int,
    request: CarLocationRequest,
    current_host: Host = Depends(get_current_host),
    db: Session = Depends(get_db)
):
    """
    Endpoint 4: Update car location and mark as complete
    
    - **location_name**: Location name as string (e.g., "Downtown Parking")
    OR
    - **latitude**: Geographic latitude (-90 to 90)
    - **longitude**: Geographic longitude (-180 to 180)
    
    Updates an existing car record with location information and marks it as complete.
    """
    # Get car and verify ownership
    db_car = db.query(Car).filter(Car.id == car_id).first()
    if not db_car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Car not found"
        )
    
    if db_car.host_id != current_host.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this car"
        )
    
    # Update location
    if request.location_name:
        db_car.location_name = request.location_name
        db_car.latitude = None
        db_car.longitude = None
    else:
        db_car.location_name = None
        db_car.latitude = request.latitude
        db_car.longitude = request.longitude
    
    # Mark car as complete
    db_car.is_complete = True
    
    db.commit()
    db.refresh(db_car)
    
    return _car_to_response(db_car)


@router.get("/cars/{car_id}", response_model=CarResponse)
async def get_car(
    car_id: int,
    db: Session = Depends(get_db)
):
    """
    Get car details by ID
    """
    db_car = db.query(Car).filter(Car.id == car_id).first()
    if not db_car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Car not found"
        )
    
    return _car_to_response(db_car)


@router.get("/cars", response_model=List[CarResponse])
async def list_cars(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    List all cars (with pagination)
    """
    cars = db.query(Car).offset(skip).limit(limit).all()
    return [_car_to_response(car) for car in cars]


@router.get("/host/cars", response_model=List[CarResponse])
async def list_my_cars(
    current_host: Host = Depends(get_current_host),
    db: Session = Depends(get_db)
):
    """
    List all cars belonging to the authenticated host
    """
    cars = db.query(Car).filter(Car.host_id == current_host.id).all()
    return [_car_to_response(car) for car in cars]

