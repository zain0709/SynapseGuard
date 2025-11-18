# Auth Service

This service handles user authentication and security for Synapse Guard.

## Responsibilities
- User registration (signup)
- User login
- Password hashing (bcrypt)
- JWT creation and verification
- Protected endpoint `/auth/me`
- Managing user identity across microservices

## Technologies
- FastAPI
- SQLAlchemy
- PostgreSQL
- JWT (PyJWT)
- Alembic for database migrations

## Folder Structure
- `app/main.py` – FastAPI entrypoint
- `app/models.py` – SQLAlchemy User model
- `app/routes_auth.py` – Signup/login endpoints
- `app/security.py` – Hashing + JWT utilities
- `app/database.py` – Database connection
- `tests/` – Unit and integration tests
- `alembic/` – DB migrations
