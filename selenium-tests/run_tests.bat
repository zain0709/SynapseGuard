@echo off
REM Test Runner Script for SynapseGuard (Windows)
REM Runs all tests: Unit, Integration, and E2E

echo =========================================
echo SynapseGuard Test Suite
echo =========================================
echo.

REM Check if services are running
echo Checking if services are running...
curl -s http://localhost:8000/docs >nul 2>&1
if errorlevel 1 (
    echo X Auth service not running on port 8000
    echo Please start services with: docker-compose up
    exit /b 1
)

curl -s http://localhost:8001/docs >nul 2>&1
if errorlevel 1 (
    echo X Budget service not running on port 8001
    echo Please start services with: docker-compose up
    exit /b 1
)

curl -s http://localhost:5173 >nul 2>&1
if errorlevel 1 (
    echo X Frontend not running on port 5173
    echo Please start frontend with: npm run dev
    exit /b 1
)

echo √ All services are running
echo.

REM Install dependencies
echo Installing test dependencies...
pip install -r requirements.txt
echo.

REM Run Unit and Integration Tests
echo =========================================
echo Running Unit and Integration Tests...
echo =========================================
pytest test_unit_integration.py -v --tb=short --cov=. --cov-report=html --cov-report=term
set UNIT_EXIT_CODE=%errorlevel%
echo.

REM Run E2E Selenium Tests
echo =========================================
echo Running E2E Selenium Tests...
echo =========================================
pytest test_e2e_comprehensive.py -v --tb=short --html=test_report.html --self-contained-html
set E2E_EXIT_CODE=%errorlevel%
echo.

REM Summary
echo =========================================
echo Test Summary
echo =========================================
if %UNIT_EXIT_CODE%==0 (
    echo √ Unit and Integration Tests: PASSED
) else (
    echo X Unit and Integration Tests: FAILED
)

if %E2E_EXIT_CODE%==0 (
    echo √ E2E Selenium Tests: PASSED
) else (
    echo X E2E Selenium Tests: FAILED
)

echo.
echo Test reports generated:
echo   - HTML Report: test_report.html
echo   - Coverage Report: htmlcov\index.html
echo.

REM Exit with failure if any tests failed
if not %UNIT_EXIT_CODE%==0 exit /b 1
if not %E2E_EXIT_CODE%==0 exit /b 1

exit /b 0
