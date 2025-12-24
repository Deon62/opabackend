# Car Rental Backend - Development Guide

## Project Overview
**Objective**: Build a robust FastAPI backend for a car rental platform with server-side validation (zero trust in UI data) and a multi-step car listing workflow.

**Database**: SQLite (for now)

---

## ✅ Development Checklist

### 1. Project Setup & Configuration
- [x] Initialize FastAPI project structure
- [x] Set up virtual environment and dependencies
- [x] Configure SQLite database connection
- [x] Set up project dependencies (FastAPI, SQLAlchemy/SQLModel, Pydantic, bcrypt, python-jose for JWT, etc.)

### 2. Database Architecture
- [x] Create database models using SQLAlchemy or SQLModel
- [x] **Hosts Table**: Car owners with authentication fields
- [x] **Clients Table**: Renters with authentication fields
- [x] **Cars Table**: Vehicle details, pricing, and location data
- [x] Set up database migrations/initialization
- [x] Create database relationships (Cars → Hosts)

### 3. Authentication System - Hosts
- [x] Create Host authentication module
- [x] **Registration Endpoint**:
  - [x] Pydantic model: Full Name, Email, Password, Password Confirmation
  - [x] Server-side validation: password == confirm_password
  - [x] Email uniqueness check before DB write
  - [x] High-entropy password hashing (bcrypt)
  - [x] Save to database
- [x] **Login Endpoint**:
  - [x] JWT-based authentication
  - [x] Validate credentials
  - [x] Return JWT token
- [x] **Logout Endpoint**:
  - [x] Handle token invalidation/blacklisting (or client-side only)
- [x] **Social Auth Placeholders**:
  - [x] Commented route for "Continue with Google"
  - [x] Commented route for "Continue with Apple"
- [x] FastAPI tags: "Host Auth" for Swagger organization

### 4. Authentication System - Clients
- [x] Create Client authentication module
- [x] **Registration Endpoint**:
  - [x] Pydantic model: Full Name, Email, Password, Password Confirmation
  - [x] Server-side validation: password == confirm_password
  - [x] Email uniqueness check before DB write
  - [x] High-entropy password hashing (bcrypt)
  - [x] Save to database
- [x] **Login Endpoint**:
  - [x] JWT-based authentication
  - [x] Validate credentials
  - [x] Return JWT token
- [x] **Logout Endpoint**:
  - [x] Handle token invalidation/blacklisting (or client-side only)
- [x] **Social Auth Placeholders**:
  - [x] Commented route for "Continue with Google"
  - [x] Commented route for "Continue with Apple"
- [x] FastAPI tags: "Client Auth" for Swagger organization

### 5. Multi-Step Car Upload API
- [x] **Endpoint 1 - Car Basics**:
  - [x] Pydantic model: Car name, model, body type, year, long-form description
  - [x] Server-side validation
  - [x] Link to authenticated Host ID
  - [x] Create car record (incomplete state)
- [x] **Endpoint 2 - Technical Specs**:
  - [x] Pydantic model: Seats, fuel type, transmission, color, mileage, list of up to 12 optional features
  - [x] Server-side validation
  - [x] Update car record
- [x] **Endpoint 3 - Pricing & Rules**:
  - [x] Pydantic model: Daily rate, weekly rate, monthly rate, minimum rental days (mandatory), maximum rental days (optional), minimum age requirement, text-based car rules
  - [x] Server-side validation
  - [x] Update car record
- [x] **Endpoint 4 - Location**:
  - [x] Pydantic model: Support location name (string) OR geographic coordinates (Lat/Long)
  - [x] Server-side validation
  - [x] Update car record (mark as complete)
- [x] FastAPI tags: "Car Management" for Swagger organization

### 6. Technical Requirements
- [x] **Dependency Injection**:
  - [x] FastAPI dependency for database sessions
  - [x] FastAPI dependency for JWT user authentication
- [x] **Validation**:
  - [x] Use Pydantic for all request bodies
  - [x] Ensure data integrity on all endpoints
- [x] **Documentation**:
  - [x] Organize endpoints with FastAPI tags
  - [x] Verify Swagger UI (/docs) groups: "Host Auth", "Client Auth", "Car Management"
- [x] **Data Integrity**:
  - [x] Ensure car upload endpoints link vehicles to authenticated Host ID
  - [x] Validate Host ownership for car operations

---

## 📝 Notes
- All validation must be server-side (zero trust in UI data)
- Use bcrypt for password hashing
- JWT tokens for authentication
- SQLite database for now (can be migrated later)

## 🚀 Next Steps
_(Add future features and requirements here as the project evolves)_
