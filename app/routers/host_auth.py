from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Host
from app.schemas import (
    HostRegisterRequest,
    HostRegisterResponse,
    HostLoginRequest,
    HostLoginResponse
)
from app.auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_host_by_email,
    get_current_host,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter()


@router.post("/host/auth/register", response_model=HostRegisterResponse, status_code=status.HTTP_201_CREATED)
async def register_host(
    request: HostRegisterRequest,
    db: Session = Depends(get_db)
):
    """
    Register a new host (car owner)
    
    - **full_name**: Full name of the host
    - **email**: Email address (must be unique)
    - **password**: Password (minimum 8 characters)
    - **password_confirmation**: Password confirmation (must match password)
    """
    # Check if email already exists
    existing_host = get_host_by_email(db, request.email)
    if existing_host:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new host
    hashed_password = get_password_hash(request.password)
    db_host = Host(
        full_name=request.full_name,
        email=request.email,
        hashed_password=hashed_password
    )
    
    db.add(db_host)
    db.commit()
    db.refresh(db_host)
    
    return db_host


@router.post("/host/auth/login", response_model=HostLoginResponse)
async def login_host(
    request: HostLoginRequest,
    db: Session = Depends(get_db)
):
    """
    Login for hosts
    
    - **email**: Registered email address
    - **password**: Password
    """
    # Get host by email
    host = get_host_by_email(db, request.email)
    if not host:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify password
    if not verify_password(request.password, host.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token with role
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(host.id), "role": "host"}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "host": host
    }


@router.post("/host/auth/logout")
async def logout_host(current_host: Host = Depends(get_current_host)):
    """
    Logout endpoint for hosts
    
    Note: JWT tokens are stateless. In a production environment, you might want to
    implement token blacklisting. For now, this endpoint is provided for API
    consistency. The client should discard the token.
    """
    return {"message": "Successfully logged out"}


@router.get("/host/me", response_model=HostRegisterResponse)
async def get_current_host_info(current_host: Host = Depends(get_current_host)):
    """
    Get current authenticated host information
    
    Requires Bearer token authentication.
    """
    return current_host


# Social Auth Placeholders
# TODO: Implement "Continue with Google" integration
# @router.post("/host/auth/google")
# async def host_google_auth():
#     """Continue with Google authentication for hosts"""
#     pass


# TODO: Implement "Continue with Apple" integration
# @router.post("/host/auth/apple")
# async def host_apple_auth():
#     """Continue with Apple authentication for hosts"""
#     pass


