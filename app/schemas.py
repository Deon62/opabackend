from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import Optional, List
from datetime import datetime
import json


# Host Auth Schemas
class HostRegisterRequest(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    password: str = Field(..., min_length=8)
    password_confirmation: str = Field(..., min_length=8)

    @model_validator(mode='after')
    def passwords_match(self):
        if self.password != self.password_confirmation:
            raise ValueError('Passwords do not match')
        return self


class HostRegisterResponse(BaseModel):
    id: int
    full_name: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


class HostLoginRequest(BaseModel):
    email: EmailStr
    password: str


class HostLoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    host: HostRegisterResponse


class TokenData(BaseModel):
    host_id: Optional[int] = None


# Client Auth Schemas
class ClientRegisterRequest(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    password: str = Field(..., min_length=8)
    password_confirmation: str = Field(..., min_length=8)

    @model_validator(mode='after')
    def passwords_match(self):
        if self.password != self.password_confirmation:
            raise ValueError('Passwords do not match')
        return self


class ClientRegisterResponse(BaseModel):
    id: int
    full_name: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


class ClientLoginRequest(BaseModel):
    email: EmailStr
    password: str


class ClientLoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    client: ClientRegisterResponse


# Car Upload Schemas
class CarBasicsRequest(BaseModel):
    """Endpoint 1: Car Basics"""
    name: str = Field(..., min_length=1, max_length=255)
    model: str = Field(..., min_length=1, max_length=100)
    body_type: str = Field(..., min_length=1, max_length=50)
    year: int = Field(..., ge=1900, le=2100)
    description: str = Field(..., min_length=1)


class CarTechnicalSpecsRequest(BaseModel):
    """Endpoint 2: Technical Specs"""
    seats: int = Field(..., ge=1, le=50)
    fuel_type: str = Field(..., min_length=1, max_length=50)
    transmission: str = Field(..., min_length=1, max_length=50)
    color: str = Field(..., min_length=1, max_length=50)
    mileage: int = Field(..., ge=0)
    features: List[str] = Field(default_factory=list, max_length=12)


class CarPricingRulesRequest(BaseModel):
    """Endpoint 3: Pricing & Rules"""
    daily_rate: float = Field(..., gt=0)
    weekly_rate: float = Field(..., gt=0)
    monthly_rate: float = Field(..., gt=0)
    min_rental_days: int = Field(..., ge=1)
    max_rental_days: Optional[int] = Field(None)
    min_age_requirement: int = Field(..., ge=18, le=100)
    rules: str = Field(..., min_length=1)

    @model_validator(mode='after')
    def validate_max_rental_days(self):
        """Validate max_rental_days: 0 or None means no maximum, otherwise must be >= 1"""
        if self.max_rental_days is not None:
            if self.max_rental_days == 0:
                # Convert 0 to None (no maximum)
                self.max_rental_days = None
            elif self.max_rental_days < 1:
                raise ValueError('max_rental_days must be greater than or equal to 1 if provided')
        return self


class CarLocationRequest(BaseModel):
    """Endpoint 4: Location"""
    location_name: Optional[str] = Field(None, max_length=255)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)

    @model_validator(mode='after')
    def location_provided(self):
        """Ensure either location_name OR coordinates are provided"""
        if not self.location_name and (self.latitude is None or self.longitude is None):
            raise ValueError('Either location_name or both latitude and longitude must be provided')
        if self.location_name and (self.latitude is not None or self.longitude is not None):
            raise ValueError('Provide either location_name OR coordinates, not both')
        if (self.latitude is not None and self.longitude is None) or (self.latitude is None and self.longitude is not None):
            raise ValueError('Both latitude and longitude must be provided together')
        return self


class CarResponse(BaseModel):
    """Car response schema"""
    id: int
    host_id: int
    name: Optional[str] = None
    model: Optional[str] = None
    body_type: Optional[str] = None
    year: Optional[int] = None
    description: Optional[str] = None
    seats: Optional[int] = None
    fuel_type: Optional[str] = None
    transmission: Optional[str] = None
    color: Optional[str] = None
    mileage: Optional[int] = None
    features: Optional[List[str]] = None
    daily_rate: Optional[float] = None
    weekly_rate: Optional[float] = None
    monthly_rate: Optional[float] = None
    min_rental_days: Optional[int] = None
    max_rental_days: Optional[int] = None
    min_age_requirement: Optional[int] = None
    rules: Optional[str] = None
    location_name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_complete: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

