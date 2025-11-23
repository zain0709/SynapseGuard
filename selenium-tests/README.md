   ```bash
   docker-compose up
   ```
   - Auth Service: http://localhost:8000
   - Budget Service: http://localhost:8001

2. **Frontend** (React + Vite):
   ```bash
   cd ../frontend
   npm install
   npm run dev
   ```
   - Frontend: http://localhost:5173

3. **Chrome Browser** (for Selenium tests)
   - ChromeDriver will be automatically installed via webdriver-manager

## 📦 Installation

Install test dependencies:

```bash
cd selenium-tests
pip install -r requirements.txt
```

## ▶️ Running Tests

### Option 1: Run All Tests (Recommended)

**Run everything:**
```bash
pytest test_suite.py -v
```

### Option 2: Run Individual Test Suites

**Specific Test Class:**
```bash
pytest test_suite.py::TestAuthService -v
```

**Specific Test Function:**
```bash
pytest test_suite.py::TestAuthenticationFlow::test_01_registration -v
```

### Option 3: Run with Coverage Report

```bash
pytest test_suite.py --cov=. --cov-report=html --cov-report=term
```

View coverage report:
```bash
# Open htmlcov/index.html in your browser
```

### Option 4: Run with HTML Report

```bash
pytest test_suite.py --html=test_report.html --self-contained-html
```

## 📊 Test Reports

After running tests, the following reports are generated:

1. **HTML Test Report**: `test_report.html`
   - Detailed test results with screenshots (for E2E tests)
   - Pass/fail status for each test
   - Execution time

2. **Coverage Report**: `htmlcov/index.html`
   - Code coverage percentage
   - Line-by-line coverage analysis
   - Uncovered code highlighting

## 🧪 Test Structure

### Unit & Integration Tests

```python
class TestAuthService:
    - test_register_new_user()
    - test_register_duplicate_user()
    - test_login_valid_credentials()
    - test_login_invalid_credentials()

class TestBudgetService:
    - test_create_budget()
    - test_get_budgets()
    - test_update_budget()
    - test_delete_budget()
    - test_create_budget_unauthorized()

class TestExpenseOperations:
    - test_create_expense()
    - test_update_expense()
    - test_delete_expense()

class TestExternalAPI:
    - test_exchange_rates_endpoint()
```

### E2E Selenium Tests

```python
class TestAuthenticationFlow:
    - test_01_registration()
    - test_02_login()
    - test_03_invalid_login()

class TestBudgetManagement:
    - test_04_create_budget()
    - test_05_expand_budget_card()
    - test_06_edit_budget()

class TestExpenseManagement:
    - test_07_add_expense()
    - test_08_view_expenses()
    - test_09_edit_expense()
    - test_10_delete_expense()

class TestNavigation:
    - test_11_navbar_navigation()
    - test_12_logout()


```

## 🐛 Troubleshooting

### Services Not Running
```
❌ Auth service not running on port 8000
```
**Solution:** Start Docker services:
```bash
docker-compose up
```

### Frontend Not Running
```
❌ Frontend not running on port 5173
```
**Solution:** Start the frontend:
```bash
cd ../frontend
npm run dev
```

### ChromeDriver Issues
```
selenium.common.exceptions.WebDriverException
```
**Solution:** Update webdriver-manager:
```bash
pip install --upgrade webdriver-manager
```

### Port Already in Use
```
Error: Port 8000 is already in use
```
**Solution:** Stop existing services or change ports in docker-compose.yml

### Test Failures Due to Timing
Some E2E tests may fail due to slow page loads. Increase timeout:
```python
TIMEOUT = 20  # Increase from 10 to 20 seconds
```

## 🎯 Best Practices

1. **Run tests before committing code**
2. **Ensure all services are running** before executing tests
3. **Review test reports** to identify failures
4. **Maintain test coverage** above 80%
5. **Update tests** when adding new features

## 📝 Writing New Tests

### Adding a Unit Test

```python
def test_new_feature(self, auth_token):
    """Test description"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.get(
        f"{BASE_URL_BUDGET}/new-endpoint",
        headers=headers
    )
    assert response.status_code == 200
```

### Adding an E2E Test

```python
def test_new_ui_feature(self, driver):
    """Test description"""
    driver.get(f"{FRONTEND_URL}/page")
    element = driver.find_element(By.ID, "element-id")
    element.click()
    assert "Expected Text" in driver.page_source
```

## 🔄 Continuous Integration

These tests are designed to run in CI/CD pipelines. For headless execution:

```python
# In test_e2e_comprehensive.py
options.add_argument("--headless")  # Uncomment this line
```

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review test output and error messages
3. Consult the main project README
4. Check Docker logs: `docker-compose logs`

## 📄 License

Part of the SynapseGuard Budget Tracker project.
