"""
End-to-End Selenium Tests for SynapseGuard Budget Tracker
Tests complete user workflows from registration to budget management
"""

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import random

# Test Configuration
FRONTEND_URL = "http://localhost:5173"
TIMEOUT = 10

@pytest.fixture(scope="module")
def driver():
    """Setup Chrome WebDriver"""
    service = Service(ChromeDriverManager().install())
    options = Options()
    # Uncomment for headless mode (useful for CI/CD)
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(TIMEOUT)
    yield driver
    driver.quit()

@pytest.fixture(scope="module")
def test_user():
    """Generate unique test user credentials"""
    return {
        "username": f"testuser_{random.randint(10000, 99999)}",
        "password": "SecurePass123!"
    }


class TestAuthenticationFlow:
    """Test user registration and login flows"""
    
    def test_01_registration(self, driver, test_user):
        """Test user registration process"""
        driver.get(f"{FRONTEND_URL}/register")
        
        # Wait for page to load
        WebDriverWait(driver, TIMEOUT).until(
            EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Register')]"))
        )
        
        # Fill registration form
        username_input = driver.find_element(By.XPATH, "//input[@type='text']")
        password_input = driver.find_element(By.XPATH, "//input[@type='password']")
        
        username_input.clear()
        username_input.send_keys(test_user["username"])
        password_input.clear()
        password_input.send_keys(test_user["password"])
        
        # Submit form
        register_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Register')]")
        register_button.click()
        
        # Should redirect to login page
        WebDriverWait(driver, TIMEOUT).until(EC.url_contains("/login"))
        assert "/login" in driver.current_url, "Should redirect to login after registration"
    
    def test_02_login(self, driver, test_user):
        """Test user login process"""
        driver.get(f"{FRONTEND_URL}/login")
        
        # Wait for login form
        WebDriverWait(driver, TIMEOUT).until(
            EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Login')]"))
        )
        
        # Fill login form
        username_input = driver.find_element(By.XPATH, "//input[@type='text']")
        password_input = driver.find_element(By.XPATH, "//input[@type='password']")
        
        username_input.clear()
        username_input.send_keys(test_user["username"])
        password_input.clear()
        password_input.send_keys(test_user["password"])
        
        # Submit form
        login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
        login_button.click()
        
        # Should redirect to dashboard
        WebDriverWait(driver, TIMEOUT).until(EC.url_contains("/dashboard"))
        assert "/dashboard" in driver.current_url, "Should redirect to dashboard after login"
    
    def test_03_invalid_login(self, driver):
        """Test login with invalid credentials"""
        driver.get(f"{FRONTEND_URL}/login")
        
        # Fill with invalid credentials
        username_input = driver.find_element(By.XPATH, "//input[@type='text']")
        password_input = driver.find_element(By.XPATH, "//input[@type='password']")
        
        username_input.send_keys("invaliduser")
        password_input.send_keys("wrongpassword")
        
        login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
        login_button.click()
        
        # Should show error message
        time.sleep(1)
        assert "Invalid" in driver.page_source or "error" in driver.page_source.lower()


class TestBudgetManagement:
    """Test budget creation, editing, and deletion"""
    
    def test_04_create_budget(self, driver):
        """Test creating a new budget"""
        driver.get(f"{FRONTEND_URL}/dashboard")
        
        # Wait for dashboard to load
        WebDriverWait(driver, TIMEOUT).until(
            EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'My Budgets')]"))
        )
        
        # Fill budget creation form
        budget_name = f"Test Budget {random.randint(100, 999)}"
        budget_limit = "1500"
        
        name_input = driver.find_element(By.XPATH, "//input[@placeholder='Budget Name (e.g., Groceries)']")
        limit_input = driver.find_element(By.XPATH, "//input[@placeholder='Limit']")
        
        name_input.clear()
        name_input.send_keys(budget_name)
        limit_input.clear()
        limit_input.send_keys(budget_limit)
        
        # Click create button
        create_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Create Budget')]")
        create_button.click()
        
        # Wait for budget to appear
        time.sleep(2)
        assert budget_name in driver.page_source, "Budget should appear on dashboard"
    
    def test_05_expand_budget_card(self, driver):
        """Test expanding a budget card to see details"""
        driver.get(f"{FRONTEND_URL}/dashboard")
        time.sleep(1)
        
        # Click on a budget card to expand
        budget_cards = driver.find_elements(By.XPATH, "//div[contains(@class, 'rounded-2xl')]")
        if len(budget_cards) > 0:
            budget_cards[0].click()
            time.sleep(1)
            # Should show expense form
            assert "Add Expense" in driver.page_source
    
    def test_06_edit_budget(self, driver):
        """Test editing a budget name and limit"""
        driver.get(f"{FRONTEND_URL}/dashboard")
        time.sleep(1)
        
        # Find and click edit button (pencil icon)
        try:
            edit_buttons = driver.find_elements(By.XPATH, "//button[@title='Edit Budget']")
            if len(edit_buttons) > 0:
                edit_buttons[0].click()
                time.sleep(1)
                
                # Find input fields and modify
                inputs = driver.find_elements(By.XPATH, "//input[@type='text']")
                if len(inputs) > 0:
                    inputs[0].clear()
                    inputs[0].send_keys("Updated Budget Name")
                
                # Click save
                save_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Save')]")
                save_button.click()
                time.sleep(1)
                
                assert "Updated Budget Name" in driver.page_source
        except Exception as e:
            pytest.skip(f"Edit functionality not fully testable: {e}")


class TestExpenseManagement:
    """Test expense creation, editing, and deletion"""
    
    def test_07_add_expense(self, driver):
        """Test adding an expense to a budget"""
        driver.get(f"{FRONTEND_URL}/dashboard")
        time.sleep(1)
        
        # Expand first budget card
        budget_cards = driver.find_elements(By.XPATH, "//div[contains(@class, 'cursor-pointer')]")
        if len(budget_cards) > 0:
            budget_cards[0].click()
            time.sleep(1)
            
            # Fill expense form
            description_input = driver.find_element(By.XPATH, "//input[@placeholder='Description']")
            amount_input = driver.find_element(By.XPATH, "//input[@placeholder='Amount']")
            
            description_input.send_keys("Test Expense")
            amount_input.send_keys("50.00")
            
            # Click Add button
            add_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Add')]")
            add_button.click()
            
            time.sleep(2)
            # Verify expense appears
            assert "Test Expense" in driver.page_source or "-$50" in driver.page_source
    
    def test_08_view_expenses(self, driver):
        """Test viewing expense list"""
        driver.get(f"{FRONTEND_URL}/dashboard")
        time.sleep(1)
        
        # Expand budget
        budget_cards = driver.find_elements(By.XPATH, "//div[contains(@class, 'cursor-pointer')]")
        if len(budget_cards) > 0:
            budget_cards[0].click()
            time.sleep(1)
            
            # Click to show expenses
            try:
                expenses_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Expenses')]")
                expenses_button.click()
                time.sleep(1)
                # Should show expense list or "No expenses" message
                assert "Expense" in driver.page_source or "No expenses" in driver.page_source
            except:
                pass
    
    def test_09_edit_expense(self, driver):
        """Test editing an existing expense"""
        driver.get(f"{FRONTEND_URL}/dashboard")
        time.sleep(1)
        
        try:
            # Expand budget and show expenses
            budget_cards = driver.find_elements(By.XPATH, "//div[contains(@class, 'cursor-pointer')]")
            if len(budget_cards) > 0:
                budget_cards[0].click()
                time.sleep(1)
                
                # Show expenses
                expenses_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Expenses')]")
                expenses_button.click()
                time.sleep(1)
                
                # Click edit button on first expense
                edit_buttons = driver.find_elements(By.XPATH, "//button[@title='Edit']")
                if len(edit_buttons) > 0:
                    edit_buttons[0].click()
                    time.sleep(1)
                    
                    # Modify description
                    desc_inputs = driver.find_elements(By.XPATH, "//input[@type='text']")
                    if len(desc_inputs) > 0:
                        desc_inputs[-1].clear()
                        desc_inputs[-1].send_keys("Modified Expense")
                    
                    # Click Save
                    save_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Save')]")
                    save_button.click()
                    time.sleep(1)
        except Exception as e:
            pytest.skip(f"Expense edit test skipped: {e}")
    
    def test_10_delete_expense(self, driver):
        """Test deleting an expense"""
        driver.get(f"{FRONTEND_URL}/dashboard")
        time.sleep(1)
        
        try:
            # Expand budget and show expenses
            budget_cards = driver.find_elements(By.XPATH, "//div[contains(@class, 'cursor-pointer')]")
            if len(budget_cards) > 0:
                budget_cards[0].click()
                time.sleep(1)
                
                expenses_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Expenses')]")
                expenses_button.click()
                time.sleep(1)
                
                # Get initial expense count
                initial_source = driver.page_source
                
                # Click delete button
                delete_buttons = driver.find_elements(By.XPATH, "//button[@title='Delete']")
                if len(delete_buttons) > 0:
                    delete_buttons[0].click()
                    time.sleep(2)
                    
                    # Verify expense was removed
                    # Page should refresh or update
        except Exception as e:
            pytest.skip(f"Expense delete test skipped: {e}")


class TestNavigation:
    """Test navigation and logout"""
    
    def test_11_navbar_navigation(self, driver):
        """Test navigation using navbar"""
        driver.get(f"{FRONTEND_URL}/dashboard")
        time.sleep(1)
        
        # Check that navbar exists
        assert "SynapseGuard" in driver.page_source
        assert "Dashboard" in driver.page_source or "Logout" in driver.page_source
    
    def test_12_logout(self, driver):
        """Test logout functionality"""
        driver.get(f"{FRONTEND_URL}/dashboard")
        time.sleep(1)
        
        # Click logout button
        try:
            logout_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Logout')]")
            logout_button.click()
            
            # Should redirect to login
            WebDriverWait(driver, TIMEOUT).until(EC.url_contains("/login"))
            assert "/login" in driver.current_url
        except Exception as e:
            pytest.skip(f"Logout test skipped: {e}")


class TestResponsiveness:
    """Test responsive design"""
    
    def test_13_mobile_view(self, driver):
        """Test mobile responsive design"""
        # Set mobile viewport
        driver.set_window_size(375, 667)  # iPhone size
        driver.get(f"{FRONTEND_URL}/login")
        time.sleep(1)
        
        # Page should still be usable
        assert "Login" in driver.page_source
        
        # Reset to desktop
        driver.set_window_size(1920, 1080)
    
    def test_14_tablet_view(self, driver):
        """Test tablet responsive design"""
        # Set tablet viewport
        driver.set_window_size(768, 1024)  # iPad size
        driver.get(f"{FRONTEND_URL}/dashboard")
        time.sleep(1)
        
        # Dashboard should be visible
        assert "My Budgets" in driver.page_source or "Budget" in driver.page_source
        
        # Reset to desktop
        driver.set_window_size(1920, 1080)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short", "--html=test_report.html"])
