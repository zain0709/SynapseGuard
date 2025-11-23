"""
Unit and Integration Tests for SynapseGuard Budget Tracker
Tests API endpoints, authentication, and core business logic
"""

import pytest
import requests
from requests.auth import HTTPBasicAuth
import json

# Test Configuration
BASE_URL_AUTH = "http://localhost:8000"
BASE_URL_BUDGET = "http://localhost:8001"
TEST_USERNAME = "testuser_integration"
TEST_PASSWORD = "testpass123"

class TestAuthService:
    """Unit tests for Authentication Service"""
    
    def test_register_new_user(self):
        """Test user registration"""
        response = requests.post(
            f"{BASE_URL_AUTH}/register",
            json={"username": f"{TEST_USERNAME}_new", "password": TEST_PASSWORD}
        )
        assert response.status_code in [200, 201], f"Registration failed: {response.text}"
    
    def test_register_duplicate_user(self):
        """Test that duplicate registration fails"""
        # Register once
        requests.post(
            f"{BASE_URL_AUTH}/register",
            json={"username": f"{TEST_USERNAME}_dup", "password": TEST_PASSWORD}
        )
        # Try to register again
        response = requests.post(
            f"{BASE_URL_AUTH}/register",
            json={"username": f"{TEST_USERNAME}_dup", "password": TEST_PASSWORD}
        )
        assert response.status_code == 400, "Duplicate registration should fail"
    
    def test_login_valid_credentials(self):
        """Test login with valid credentials"""
        # First register
        requests.post(
            f"{BASE_URL_AUTH}/register",
            json={"username": TEST_USERNAME, "password": TEST_PASSWORD}
        )
        # Then login
        response = requests.post(
            f"{BASE_URL_AUTH}/token",
            data={"username": TEST_USERNAME, "password": TEST_PASSWORD}
        )
        assert response.status_code == 200
        assert "access_token" in response.json()
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        response = requests.post(
            f"{BASE_URL_AUTH}/token",
            data={"username": "nonexistent", "password": "wrongpass"}
        )
        assert response.status_code == 401


class TestBudgetService:
    """Integration tests for Budget Service API"""
    
    @pytest.fixture(scope="class")
    def auth_token(self):
        """Get authentication token for tests"""
        # Register and login
        requests.post(
            f"{BASE_URL_AUTH}/register",
            json={"username": TEST_USERNAME, "password": TEST_PASSWORD}
        )
        response = requests.post(
            f"{BASE_URL_AUTH}/token",
            data={"username": TEST_USERNAME, "password": TEST_PASSWORD}
        )
        return response.json()["access_token"]
    
    def test_create_budget(self, auth_token):
        """Test creating a new budget"""
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = requests.post(
            f"{BASE_URL_BUDGET}/budgets/",
            json={"name": "Test Budget", "limit": 1000.0},
            headers=headers
        )
        assert response.status_code in [200, 201]
        data = response.json()
        assert data["name"] == "Test Budget"
        assert data["limit"] == 1000.0
    
    def test_get_budgets(self, auth_token):
        """Test retrieving all budgets"""
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = requests.get(
            f"{BASE_URL_BUDGET}/budgets/",
            headers=headers
        )
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_create_budget_unauthorized(self):
        """Test that creating budget without auth fails"""
        response = requests.post(
            f"{BASE_URL_BUDGET}/budgets/",
            json={"name": "Unauthorized Budget", "limit": 500.0}
        )
        assert response.status_code == 401
    
    def test_update_budget(self, auth_token):
        """Test updating an existing budget"""
        headers = {"Authorization": f"Bearer {auth_token}"}
        
        # Create a budget first
        create_response = requests.post(
            f"{BASE_URL_BUDGET}/budgets/",
            json={"name": "Original Budget", "limit": 500.0},
            headers=headers
        )
        budget_id = create_response.json()["id"]
        
        # Update it
        update_response = requests.put(
            f"{BASE_URL_BUDGET}/budgets/{budget_id}",
            json={"name": "Updated Budget", "limit": 750.0},
            headers=headers
        )
        assert update_response.status_code == 200
        data = update_response.json()
        assert data["name"] == "Updated Budget"
        assert data["limit"] == 750.0
    
    def test_delete_budget(self, auth_token):
        """Test deleting a budget"""
        headers = {"Authorization": f"Bearer {auth_token}"}
        
        # Create a budget first
        create_response = requests.post(
            f"{BASE_URL_BUDGET}/budgets/",
            json={"name": "Budget to Delete", "limit": 300.0},
            headers=headers
        )
        budget_id = create_response.json()["id"]
        
        # Delete it
        delete_response = requests.delete(
            f"{BASE_URL_BUDGET}/budgets/{budget_id}",
            headers=headers
        )
        assert delete_response.status_code == 200


class TestExpenseOperations:
    """Integration tests for Expense operations"""
    
    @pytest.fixture(scope="class")
    def setup_budget(self):
        """Create a budget and return auth token and budget ID"""
        # Register and login
        requests.post(
            f"{BASE_URL_AUTH}/register",
            json={"username": f"{TEST_USERNAME}_expense", "password": TEST_PASSWORD}
        )
        token_response = requests.post(
            f"{BASE_URL_AUTH}/token",
            data={"username": f"{TEST_USERNAME}_expense", "password": TEST_PASSWORD}
        )
        token = token_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Create a budget
        budget_response = requests.post(
            f"{BASE_URL_BUDGET}/budgets/",
            json={"name": "Expense Test Budget", "limit": 2000.0},
            headers=headers
        )
        budget_id = budget_response.json()["id"]
        
        return {"token": token, "budget_id": budget_id, "headers": headers}
    
    def test_create_expense(self, setup_budget):
        """Test creating an expense"""
        data = setup_budget
        response = requests.post(
            f"{BASE_URL_BUDGET}/budgets/{data['budget_id']}/expenses/",
            json={"description": "Test Expense", "amount": 50.0, "category": "Food"},
            headers=data["headers"]
        )
        assert response.status_code in [200, 201]
        expense_data = response.json()
        assert expense_data["description"] == "Test Expense"
        assert expense_data["amount"] == 50.0
    
    def test_update_expense(self, setup_budget):
        """Test updating an expense"""
        data = setup_budget
        
        # Create expense first
        create_response = requests.post(
            f"{BASE_URL_BUDGET}/budgets/{data['budget_id']}/expenses/",
            json={"description": "Original Expense", "amount": 25.0, "category": "General"},
            headers=data["headers"]
        )
        expense_id = create_response.json()["id"]
        
        # Update it
        update_response = requests.put(
            f"{BASE_URL_BUDGET}/budgets/{data['budget_id']}/expenses/{expense_id}",
            json={"description": "Updated Expense", "amount": 35.0, "category": "Transport"},
            headers=data["headers"]
        )
        assert update_response.status_code == 200
        updated_data = update_response.json()
        assert updated_data["description"] == "Updated Expense"
        assert updated_data["amount"] == 35.0
    
    def test_delete_expense(self, setup_budget):
        """Test deleting an expense"""
        data = setup_budget
        
        # Create expense first
        create_response = requests.post(
            f"{BASE_URL_BUDGET}/budgets/{data['budget_id']}/expenses/",
            json={"description": "Expense to Delete", "amount": 15.0, "category": "General"},
            headers=data["headers"]
        )
        expense_id = create_response.json()["id"]
        
        # Delete it
        delete_response = requests.delete(
            f"{BASE_URL_BUDGET}/budgets/{data['budget_id']}/expenses/{expense_id}",
            headers=data["headers"]
        )
        assert delete_response.status_code == 200


class TestExternalAPI:
    """Test external API integration"""
    
    def test_exchange_rates_endpoint(self):
        """Test that exchange rates endpoint works"""
        response = requests.get(f"{BASE_URL_BUDGET}/rates/USD")
        assert response.status_code == 200
        # Should return exchange rate data
        data = response.json()
        assert data is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
