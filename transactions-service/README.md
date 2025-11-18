# Transactions Service

This service manages user financial transactions and interacts with the risk scoring service.

## Responsibilities
- CRUD operations for user transactions
- Linking transactions to users
- Triggering fraud scoring via risk-service
- Validating JWT tokens for protected routes

## Technologies
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic migrations

## Folder Structure
- `app/models.py` – Transaction model
- `app/routes_transactions.py` – CRUD endpoints
- `app/utils.py` – Helper functions
- `tests/` – Unit tests
- `alembic/` – Database migrations
