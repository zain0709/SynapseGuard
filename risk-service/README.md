# Risk Service

This service evaluates transactions for potential fraud by integrating with an external ML or anomaly-detection API.

## Responsibilities
- Receive transaction payloads from transactions-service
- Call external fraud/anomaly API (e.g., OpenAI or another ML provider)
- Return probability score and risk label

## Technologies
- FastAPI
- External API (OpenAI / anomaly detection)
- Python HTTP clients (httpx/requests)

## Folder Structure
- `app/external_api.py` – External API integration
- `app/routes_risk.py` – Risk scoring route
- `tests/` – Unit tests
