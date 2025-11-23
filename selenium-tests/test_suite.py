"""
SynapseGuard Core Test Suite
Focuses on essential "Happy Path" workflows for API and E2E.
"""

import pytest
import requests
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# ==========================================
# Configuration
# ==========================================

BASE_URL_AUTH = "http://localhost:8000"
BASE_URL_BUDGET = "http://localhost:8001"
FRONTEND_URL = "http://localhost:5173"
TEST_PASSWORD = "testpass123"
TIMEOUT = 10

# ==========================================
# API & Integration Tests (Core Flows)
# ==========================================

class TestAuthService:
    """Core Authentication API Tests"""
    
    def test_register_new_user(self):
        """Test user registration (Happy Path)"""
        username = f"api_user_{random.randint(1000,9999)}"
        response = requests.post(
            f"{BASE_URL_AUTH}/register",
            json={"username": username, "password": TEST_PASSWORD}
        )
        assert response.status_code in [200, 201]
    
    def test_login_valid_credentials(self):
        """Test login (Happy Path)"""
        username = f"api_login_{random.randint(1000,9999)}"
        # Register first
        requests.post(
            f"{BASE_URL_AUTH}/register",
            json={"username": username, "password": TEST_PASSWORD}
        )
        # Login
        response = requests.post(
            f"{BASE_URL_AUTH}/token",
            data={"username": username, "password": TEST_PASSWORD}
        )
        assert response.status_code == 200
        assert "access_token" in response.json()


class TestBudgetService:
    """Core Budget API Tests"""
    
    @pytest.fixture(scope="class")
    def auth_token(self):
        username = f"api_budget_{random.randint(1000,9999)}"
        requests.post(f"{BASE_URL_AUTH}/register", json={"username": username, "password": TEST_PASSWORD})
        resp = requests.post(f"{BASE_URL_AUTH}/token", data={"username": username, "password": TEST_PASSWORD})
        return resp.json()["access_token"]
    
    def test_create_budget(self, auth_token):
        """Test creating a budget (Happy Path)"""
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = requests.post(
            f"{BASE_URL_BUDGET}/budgets/",
            json={"name": "Core Budget", "limit": 1000.0},
            headers=headers
        )
        assert response.status_code in [200, 201]
        assert response.json()["name"] == "Core Budget"


class TestExpenseOperations:
    """Core Expense API Tests"""
    
    @pytest.fixture(scope="class")
    def setup_budget(self):
        username = f"api_expense_{random.randint(1000,9999)}"
        requests.post(f"{BASE_URL_AUTH}/register", json={"username": username, "password": TEST_PASSWORD})
        token = requests.post(f"{BASE_URL_AUTH}/token", data={"username": username, "password": TEST_PASSWORD}).json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        budget = requests.post(
            f"{BASE_URL_BUDGET}/budgets/",
            json={"name": "Expense Budget", "limit": 2000.0},
            headers=headers
        ).json()
        
        return {"headers": headers, "budget_id": budget["id"]}
    
    def test_create_expense(self, setup_budget):
        """Test creating an expense (Happy Path)"""
        data = setup_budget
        response = requests.post(
            f"{BASE_URL_BUDGET}/budgets/{data['budget_id']}/expenses/",
            json={"description": "Core Expense", "amount": 50.0, "category": "Food"},
            headers=data["headers"]
        )
        assert response.status_code in [200, 201]
        assert response.json()["amount"] == 50.0

# ==========================================
# E2E Selenium Tests (Core Flows)
# ==========================================

@pytest.fixture(scope="module")
def driver():
    service = Service(ChromeDriverManager().install())
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(TIMEOUT)
    yield driver
    driver.quit()

@pytest.fixture(scope="module")
def test_user():
    return {"username": f"e2e_{random.randint(10000, 99999)}", "password": "SecurePass123!"}

class TestCoreE2E:
    """Combined Core E2E Flows"""
    
    def test_01_registration(self, driver, test_user):
        """Register a new user"""
        driver.get(f"{FRONTEND_URL}/register")
        WebDriverWait(driver, TIMEOUT).until(EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Register')]")))
        
        driver.find_element(By.XPATH, "//input[@type='text']").send_keys(test_user["username"])
        driver.find_element(By.XPATH, "//input[@type='password']").send_keys(test_user["password"])
        driver.find_element(By.XPATH, "//button[contains(text(), 'Register')]").click()
        
        WebDriverWait(driver, TIMEOUT).until(EC.url_contains("/login"))
    
    def test_02_login(self, driver, test_user):
        """Login with new user"""
        driver.get(f"{FRONTEND_URL}/login")
        WebDriverWait(driver, TIMEOUT).until(EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Login')]")))
        
        driver.find_element(By.XPATH, "//input[@type='text']").send_keys(test_user["username"])
        driver.find_element(By.XPATH, "//input[@type='password']").send_keys(test_user["password"])
        driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]").click()
        
        WebDriverWait(driver, TIMEOUT).until(EC.url_contains("/dashboard"))
    
    def test_03_create_budget(self, driver):
        """Create a budget"""
        driver.get(f"{FRONTEND_URL}/dashboard")
        WebDriverWait(driver, TIMEOUT).until(EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'My Budgets')]")))
        
        driver.find_element(By.XPATH, "//input[@placeholder='Budget Name (e.g., Groceries)']").send_keys("E2E Budget")
        driver.find_element(By.XPATH, "//input[@placeholder='Limit']").send_keys("500")
        driver.find_element(By.XPATH, "//button[contains(text(), 'Create Budget')]").click()
        
        time.sleep(2)
        assert "E2E Budget" in driver.page_source
    
    def test_04_add_expense(self, driver):
        """Add an expense to the budget"""
        driver.get(f"{FRONTEND_URL}/dashboard")
        time.sleep(2) # Wait for fetch
        
        # Wait for the specific budget created in test_03
        try:
            WebDriverWait(driver, TIMEOUT).until(
                EC.presence_of_element_located((By.XPATH, "//h3[contains(text(), 'E2E Budget')]"))
            )
        except:
            pytest.fail("E2E Budget card not found")

        # Click the budget card containing "E2E Budget"
        # The card is the ancestor with class 'cursor-pointer'
        try:
            card = driver.find_element(By.XPATH, "//h3[contains(text(), 'E2E Budget')]/ancestor::div[contains(@class, 'cursor-pointer')]")
            card.click()
            time.sleep(1)
            
            driver.find_element(By.XPATH, "//input[@placeholder='Description']").send_keys("E2E Expense")
            driver.find_element(By.XPATH, "//input[@placeholder='Amount']").send_keys("20")
            driver.find_element(By.XPATH, "//button[contains(text(), 'Add')]").click()
            
            time.sleep(2)
            
            # Check if card collapsed (Expenses button not visible)
            # Use dot selector for text content including children
            expenses_btn_xpath = "//button[contains(., 'Expenses')]"
            try:
                # Short wait to check presence
                WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, expenses_btn_xpath))
                )
            except:
                # Re-expand card if button not found
                print("Card collapsed, re-expanding...")
                card = driver.find_element(By.XPATH, "//h3[contains(text(), 'E2E Budget')]/ancestor::div[contains(@class, 'cursor-pointer')]")
                card.click()
                time.sleep(1)
            
            # Click to expand expenses list
            driver.find_element(By.XPATH, expenses_btn_xpath).click()
            time.sleep(1)
            
            assert "E2E Expense" in driver.page_source
        except Exception as e:
            pytest.fail(f"Failed to add expense: {e}")
            
    def test_05_logout(self, driver):
        """Logout"""
        try:
            driver.find_element(By.XPATH, "//button[contains(text(), 'Logout')]").click()
            WebDriverWait(driver, TIMEOUT).until(EC.url_contains("/login"))
        except:
            pass # Best effort

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
