# OpenCart Automation Testing Framework

A robust, scalable automation testing framework for OpenCart using Playwright, Python, and Pytest. This framework executes **203 test cases** across **20 Use Cases** in a data-driven, modular approach.

## Features

✅ **Data-Driven Testing**: All 203 test cases are loaded from JSON  
✅ **Modular Architecture**: Separate handler classes for each use case (UC_01 to UC_20)  
✅ **Parametrized Tests**: Uses `@pytest.mark.parametrize` for clean, scalable test execution  
✅ **Async/Await Support**: Full async support via Playwright  
✅ **Screenshot Management**: Automatic screenshots on test failures (saved in `/failures`)  
✅ **HTML Reports**: Generated test reports via `pytest-html`  
✅ **Logging**: Comprehensive logging to both console and file (`logs/automation.log`)  
✅ **Test Markers**: Tests can be run by use case, priority level (High/Medium/Low)  
✅ **Non-Headless Browser**: Full visibility of test execution (headless=False)  

## Project Structure

```
PythonProject/
├── main.py                              # Main test suite with parametrized tests
├── conftest.py                          # Pytest configuration and fixtures
├── handlers.py                          # Use Case handler classes
├── requirements.txt                     # Python dependencies
├── pytest.ini                           # Pytest configuration
├── OpenCart_203_TestCases_Final.json   # Test data (203 test cases)
├── run_tests.py                         # Utility script to run tests
├── logs/                                # Logging directory (auto-created)
├── failures/                            # Failed test screenshots (auto-created)
└── reports/                             # HTML test reports (auto-created)
```

## Installation & Setup

### 1. Install Dependencies

```bash
cd /home/tung/PycharmProjects/PythonProject
pip install -r requirements.txt
```

### 2. Install Playwright Browsers

```bash
playwright install chromium
```

### 3. Configuration

Update the `BASE_URL` in `handlers.py` if your OpenCart instance is at a different location:

```python
BASE_URL = "http://localhost/opencart_test/upload/"
```

## Running Tests

### Run All Tests

```bash
pytest main.py -v --html=reports/test_report.html --self-contained-html
```

### Run Tests by Priority

```bash
# High priority tests only
pytest main.py -m high -v

# Medium priority tests only
pytest main.py -m medium -v

# Low priority tests only
pytest main.py -m low -v
```

### Run Tests by Use Case

```bash
# Registration tests (UC_01)
pytest main.py -m registration -v

# Login tests (UC_02)
pytest main.py -m login -v

# Cart tests (UC_08)
pytest main.py -m cart -v

# Checkout tests (UC_09)
pytest main.py -m checkout -v

# All use case markers:
# registration, login, password, address, wishlist, comparison, review,
# cart, checkout, order, category, product, discount, coupon, 
# category_seo, product_seo, product_attribute, product_related, currency, customer_group
```

### Run Specific Test Case

```bash
pytest main.py::TestOpenCartAutomation::test_opencart_scenario[TC_01_01_Đăng_ký_thành_công...] -v
```

### Run Tests in Parallel

```bash
# Run with 4 workers (requires pytest-xdist)
pytest main.py -n 4 -v
```

### Run Tests with Verbose Logging

```bash
pytest main.py -vv --log-cli-level=DEBUG
```

### Stop on First Failure

```bash
pytest main.py -x -v
```

### Quick Run Script

```bash
python run_tests.py
```

This will run all tests with a nice formatted output.

## Test Case Structure

Each test case in the JSON file contains:

- **TC ID**: Unique test case identifier (e.g., TC_01_01)
- **Use Case**: The feature/module being tested (UC_01 to UC_20)
- **Tên kịch bản kiểm thử**: Test scenario name (in Vietnamese)
- **Mức độ ưu tiên**: Priority level (High/Medium/Low)
- **Các bước thực hiện**: Steps to execute
- **Dữ liệu kiểm thử**: Test data to use
- **Kết quả mong đợi**: Expected result to verify

## Understanding the Handler System

Handlers are Python classes that implement the test logic for each use case. The framework automatically selects the appropriate handler based on the test case's Use Case field.

### Base Handler

All handlers inherit from `BaseHandler` with common methods:

```python
class BaseHandler:
    async def navigate_to(path)        # Navigate to URL
    async def fill_field(selector, value)  # Fill form field
    async def click_button(selector)   # Click button
    async def check_element(selector)  # Check checkbox
    async def verify_text(text)        # Verify text on page
    async def execute_test(test_data)  # Execute test (implemented by subclass)
```

### Example Handler: UC_01 Registration

```python
class UC01_RegistrationHandler(BaseHandler):
    async def execute_test(self, test_data):
        # Navigate to registration page
        await self.navigate_to("index.php?route=account/register")
        
        # Fill form fields
        await self.fill_field('input[name="firstname"]', 'John')
        
        # Verify result
        return await self.verify_text('Your Account Has Been Created!')
```

## Adding New Handlers

To add a handler for a new use case:

1. Create a new class in `handlers.py`:

```python
class UC21_CustomFeatureHandler(BaseHandler):
    async def execute_test(self, test_data):
        await self.navigate_to("index.php?route=custom/feature")
        # Test logic here
        return await self.verify_text('Expected text')
```

2. Register it in `USE_CASE_HANDLERS` dictionary:

```python
USE_CASE_HANDLERS = {
    # ... existing entries ...
    'UC_21': UC21_CustomFeatureHandler,
}
```

## Output & Results

### Logs

Test execution logs are saved to:
- **Console**: Real-time test progress
- **File**: `logs/automation.log` - Complete execution history

### Screenshots

Failed tests automatically capture screenshots:
- **Location**: `failures/` directory
- **Naming**: `{TC_ID}_{timestamp}.png`
- **Types**: failure, timeout, error

Example:
```
failures/TC_01_01_20240515_143025.png
failures/TC_02_01_error_20240515_143050.png
```

### HTML Reports

A comprehensive HTML report is generated after test execution:
- **Location**: `reports/test_report.html`
- **Contents**: 
  - Test summary (passed/failed/skipped)
  - Detailed test results
  - Execution timeline
  - Logs for each test

## Test Markers Reference

### Priority Markers
- `@pytest.mark.high` - Critical functionality
- `@pytest.mark.medium` - Important functionality
- `@pytest.mark.low` - Optional feature

### Use Case Markers (UC_01 to UC_20)
- `@pytest.mark.registration` - UC_01
- `@pytest.mark.login` - UC_02
- `@pytest.mark.password` - UC_03
- `@pytest.mark.address` - UC_04
- `@pytest.mark.wishlist` - UC_05
- `@pytest.mark.comparison` - UC_06
- `@pytest.mark.review` - UC_07
- `@pytest.mark.cart` - UC_08
- `@pytest.mark.checkout` - UC_09
- `@pytest.mark.order` - UC_10
- `@pytest.mark.category` - UC_11
- `@pytest.mark.product` - UC_12
- `@pytest.mark.discount` - UC_13
- `@pytest.mark.coupon` - UC_14
- `@pytest.mark.category_seo` - UC_15
- `@pytest.mark.product_seo` - UC_16
- `@pytest.mark.product_attribute` - UC_17
- `@pytest.mark.product_related` - UC_18
- `@pytest.mark.currency` - UC_19
- `@pytest.mark.customer_group` - UC_20

## Troubleshooting

### Tests Not Finding OpenCart

**Issue**: Tests fail with connection error  
**Solution**: Verify OpenCart is running on `http://localhost/opencart_test/upload/`

```bash
# Check if service is running
curl http://localhost/opencart_test/upload/
```

### Selector Issues

**Issue**: "Element not found" errors  
**Solution**: Update CSS selectors in handler classes to match your OpenCart theme

### Screenshot Not Saved

**Issue**: Screenshot creation fails  
**Solution**: Ensure `/failures` directory has write permissions

```bash
chmod 755 failures/
```

### Async Errors

**Issue**: "RuntimeError: asyncio.run() cannot be called from a running event loop"  
**Solution**: This is handled by Pytest fixtures. Ensure you're using async fixtures properly.

## Best Practices

1. **Organize Tests by Priority**: Run high-priority tests first
2. **Use Parallel Execution**: Run independent tests in parallel with `-n` flag
3. **Review Screenshots**: Check failure screenshots for debugging
4. **Update Selectors**: Keep element selectors updated with UI changes
5. **Maintain Handlers**: Add new handlers instead of modifying existing ones
6. **Monitor Logs**: Review `logs/automation.log` for execution details
7. **CI/CD Integration**: Use in continuous integration pipelines

## Advanced Usage

### Custom Test Execution

```bash
# Run tests with custom pytest plugins
pytest main.py -v -p no:warnings

# Run tests with allurereport
pytest main.py --alluredir=allure-results

# Run tests with coverage
pytest main.py --cov=handlers --cov-report=html
```

### Environment Variables

Add environment-specific configuration:

```bash
# .env file
OPENCART_URL=http://localhost/opencart_test/upload/
BROWSER_HEADLESS=False
TIMEOUT=30
```

## Dependencies

- **playwright**: 1.48.0 - Browser automation
- **pytest**: 7.4.3 - Test framework
- **pytest-playwright**: 0.4.2 - Pytest integration
- **pytest-html**: 4.1.1 - HTML report generation
- **pytest-xdist**: 3.5.0 - Parallel test execution
- **python-dotenv**: 1.0.0 - Environment variable management

## Contributing

To add more test scenarios:

1. Update `OpenCart_203_TestCases_Final.json` with new cases
2. Create corresponding handler class if needed
3. Register handler in `USE_CASE_HANDLERS`
4. Run tests to verify: `pytest main.py -v`

## License

This automation framework is proprietary to the OpenCart project.

## Support

For issues or questions:
1. Check the Troubleshooting section
2. Review test logs in `logs/automation.log`
3. Examine failure screenshots in `failures/`
4. Check HTML report in `reports/test_report.html`

## Version History

- **v1.0.0** - Initial framework with 203 test cases across 20 use cases
  - Data-driven testing with Playwright
  - Modular handler architecture
  - Automatic screenshot capture
  - HTML report generation
  - Comprehensive logging

---

**Framework Created**: 2026-05-15  
**Test Cases**: 203  
**Use Cases**: 20 (UC_01 to UC_20)  
**Technology**: Playwright + Python + Pytest

