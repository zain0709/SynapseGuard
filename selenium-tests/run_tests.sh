#!/bin/bash
# Test Runner Script for SynapseGuard
# Runs all tests: Unit, Integration, and E2E

echo "========================================="
echo "SynapseGuard Test Suite"
echo "========================================="
echo ""

# Check if services are running
echo "Checking if services are running..."
if ! curl -s http://localhost:8000/docs > /dev/null; then
    echo "❌ Auth service not running on port 8000"
    echo "Please start services with: docker-compose up"
    exit 1
fi

if ! curl -s http://localhost:8001/docs > /dev/null; then
    echo "❌ Budget service not running on port 8001"
    echo "Please start services with: docker-compose up"
    exit 1
fi

if ! curl -s http://localhost:5173 > /dev/null; then
    echo "❌ Frontend not running on port 5173"
    echo "Please start frontend with: npm run dev"
    exit 1
fi

echo "✅ All services are running"
echo ""

# Install dependencies
echo "Installing test dependencies..."
pip install -r requirements.txt
echo ""

# Run Unit and Integration Tests
echo "========================================="
echo "Running Unit & Integration Tests..."
echo "========================================="
pytest test_unit_integration.py -v --tb=short --cov=. --cov-report=html --cov-report=term
UNIT_EXIT_CODE=$?
echo ""

# Run E2E Selenium Tests
echo "========================================="
echo "Running E2E Selenium Tests..."
echo "========================================="
pytest test_e2e_comprehensive.py -v --tb=short --html=test_report.html --self-contained-html
E2E_EXIT_CODE=$?
echo ""

# Summary
echo "========================================="
echo "Test Summary"
echo "========================================="
if [ $UNIT_EXIT_CODE -eq 0 ]; then
    echo "✅ Unit & Integration Tests: PASSED"
else
    echo "❌ Unit & Integration Tests: FAILED"
fi

if [ $E2E_EXIT_CODE -eq 0 ]; then
    echo "✅ E2E Selenium Tests: PASSED"
else
    echo "❌ E2E Selenium Tests: FAILED"
fi

echo ""
echo "Test reports generated:"
echo "  - HTML Report: test_report.html"
echo "  - Coverage Report: htmlcov/index.html"
echo ""

# Exit with failure if any tests failed
if [ $UNIT_EXIT_CODE -ne 0 ] || [ $E2E_EXIT_CODE -ne 0 ]; then
    exit 1
fi

exit 0
