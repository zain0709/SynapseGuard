# Budget Tracker

A full-stack Budget Tracker application built with Microservices architecture.

## Features
- User Authentication (JWT)
- Budget Management (Create, Read)
- Expense Tracking (Add expenses to budgets)
- Real-time Currency Exchange Rates
- Responsive Dashboard

## Architecture
- **Auth Service**: FastAPI, SQLite, JWT
- **Budget Service**: FastAPI, SQLite, External API Integration
- **Frontend**: React, Vite, Tailwind CSS
- **Infrastructure**: Docker, Docker Compose

## Prerequisites
- Docker & Docker Compose
- Python 3.9+ (for local testing)
- Node.js 18+ (for local testing)

## How to Run
1. Clone the repository.
2. Build and start the services:
   ```bash
   docker-compose up --build
   ```
3. Access the application at `http://localhost:5173`.

## API Documentation
- Auth Service: `http://localhost:8000/docs`
- Budget Service: `http://localhost:8001/docs`

## Testing
To run E2E tests:
1. Ensure the app is running.
2. Install test dependencies:
   ```bash
   cd selenium-tests
   pip install -r requirements.txt
   ```
3. Run tests:
   ```bash
   pytest test_e2e.py
   ```
