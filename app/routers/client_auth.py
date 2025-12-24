from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Client
from app.schemas import (
    ClientRegisterRequest,
    ClientRegisterResponse,
    ClientLoginRequest,
    ClientLoginResponse
)
from app.auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_client_by_email,
    get_current_client,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter()


@router.post("/client/auth/register", response_model=ClientRegisterResponse, status_code=status.HTTP_201_CREATED)
async def register_client(
    request: ClientRegisterRequest,
    db: Session = Depends(get_db)
):
    """
    Register a new client (car renter)
    
    - **full_name**: Full name of the client
    - **email**: Email address (must be unique)
    - **password**: Password (minimum 8 characters)
    - **password_confirmation**: Password confirmation (must match password)
    """
    # Check if email already exists
    existing_client = get_client_by_email(db, request.email)
    if existing_client:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new client
    hashed_password = get_password_hash(request.password)
    db_client = Client(
        full_name=request.full_name,
        email=request.email,
        hashed_password=hashed_password
    )
    
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    
    return db_client


@router.post("/client/auth/login", response_model=ClientLoginResponse)
async def login_client(
    request: ClientLoginRequest,
    db: Session = Depends(get_db)
):
    """
    Login for clients
    
    - **email**: Registered email address
    - **password**: Password
    """
    # Get client by email
    client = get_client_by_email(db, request.email)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify password
    if not verify_password(request.password, client.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token with role
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(client.id), "role": "client"}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "client": client
    }


@router.post("/client/auth/logout")
async def logout_client(current_client: Client = Depends(get_current_client)):
    """
    Logout endpoint for clients
    
    Note: JWT tokens are stateless. In a production environment, you might want to
    implement token blacklisting. For now, this endpoint is provided for API
    consistency. The client should discard the token.
    """
    return {"message": "Successfully logged out"}


@router.get("/client/me", response_model=ClientRegisterResponse)
async def get_current_client_info(current_client: Client = Depends(get_current_client)):
    """
    Get current authenticated client information
    
    Requires Bearer token authentication.
    """
    return current_client


# Social Auth Placeholders
# TODO: Implement "Continue with Google" integration
# @router.post("/client/auth/google")
# async def client_google_auth():
#     """Continue with Google authentication for clients"""
#     pass


# TODO: Implement "Continue with Apple" integration
# @router.post("/client/auth/apple")
# async def client_apple_auth():
#     """Continue with Apple authentication for clients"""
#     pass

