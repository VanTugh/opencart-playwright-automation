# OpenCart Automation Testing Framework
# Implementation Summary & Architecture Guide

## Project Overview

A production-ready automation testing framework for OpenCart using:
- **Playwright** - Modern browser automation
- **Python** - Test scripting language
- **Pytest** - Test execution framework
- **JSON** - Test data source with 203 test cases

## 📊 Statistics

- **Total Test Cases**: 203
- **Use Cases Covered**: 20 (UC_01 to UC_20)
- **Test Cases per UC**: 5-15 cases
- **Priority Levels**: High, Medium, Low
- **Handler Classes**: 20 + 2 generic (Security, Log check)
- **Async Methods**: 50+

## 🏗️ Architecture

### Layer 1: Configuration & Setup
```
config.py          - Configuration management
conftest.py        - Pytest fixtures & hooks
pytest.ini         - Pytest configuration
requirements.txt   - Dependencies
.env               - Environment variables
```

### Layer 2: Test Data
```
OpenCart_203_TestCases_Final.json
├── TC ID (e.g., TC_01_01)
├── Use Case (UC_01-UC_20)
├── Test Scenario Name (in Vietnamese)
├── Priority (High/Medium/Low)
├── Steps (Các bước thực hiện)
├── Test Data (Dữ liệu kiểm thử)
└── Expected Result (Kết quả mong đợi)
```

### Layer 3: Handler System
```
handlers.py
├── BaseHandler (common methods)
├── UC01_RegistrationHandler
├── UC02_LoginHandler
├── ... 18 more handlers ...
├── GenericSecurityHandler
├── GenericLogHandler
└── get_handler() - dispatching function
```

### Layer 4: Test Execution
```
main.py
├── TestOpenCartAutomation (main test class)
├── @pytest.mark.parametrize (203 test cases)
├── Error handling (screenshots on failure)
├── Dynamic markers (priority + use case)
└── Detailed logging
```

### Layer 5: Utilities
```
run_tests.py       - Interactive test runner menu
examples.py        - Extension examples
setup.sh           - Automated setup script
README.md          - Full documentation
QUICKSTART.md      - Quick start guide
```

## 🔄 Test Execution Flow

```
1. CLI: pytest main.py -v
   ↓
2. conftest.py: Initialize fixtures
   - Create browser instance
   - Create page context
   - Setup logging
   ↓
3. main.py: Load test data (203 cases from JSON)
   ↓
4. For each test case:
   a. Generate test ID
   b. Extract test data
   c. Get appropriate handler
   d. Execute handler.execute_test()
   e. Assert expected result
   f. Handle exceptions (screenshot on failure)
   g. Log results
   ↓
5. Generate HTML report
   ↓
6. Display summary
```

## 🎯 Handler Architecture

### Base Handler Pattern

```python
class BaseHandler(ABC):
    def __init__(self, page):
        self.page = page
        self.base_url = BASE_URL
    
    async def navigate_to(path)        # Navigate to URL
    async def fill_field(selector, value)  # Fill form
    async def click_button(selector)   # Click element
    async def check_element(selector)  # Check checkbox
    async def verify_text(text)        # Verify text
    async def execute_test(test_data)  # OVERRIDE ME
```

### Handler Dispatcher

```
get_handler(page, test_case)
    ↓
Extract Use Case from test_case
    ↓
Map Use Case to Handler Class
    ↓
Create Handler Instance
    ↓
Return handler ready to execute
```

## 📈 Test Markers System

### Priority Markers
- `@pytest.mark.high` - Critical functionality (40-50 tests)
- `@pytest.mark.medium` - Important (80-100 tests)
- `@pytest.mark.low` - Optional (30-50 tests)

### Use Case Markers
- `@pytest.mark.registration` - UC_01 tests
- `@pytest.mark.login` - UC_02 tests
- ... and so on for all 20 use cases

### How It Works
```
1. Each test_case has:
   - Mức độ ưu tiên (Priority)
   - Use Case field

2. get_priority_marker() -> pytest.mark.*
3. get_use_case_marker() -> pytest.mark.*

4. Can run by marker:
   pytest main.py -m high -v
   pytest main.py -m registration -v
   pytest main.py -m "high and cart" -v
```

## 🔐 Error Handling & Recovery

### Screenshot Capture
```
try:
    execute_test()
except Exception:
    → Take screenshot
    → Save to failures/{TC_ID}_{timestamp}.png
    → Log error details
    → Re-raise exception
```

### Test Status Tracking
- **PASSED**: Test executed successfully
- **FAILED**: Assertion failed
- **TIMEOUT**: Test exceeded timeout
- **ERROR**: Unexpected exception
- **SKIPPED**: Test skipped

## 📊 Data Flow

```
JSON File (203 test cases)
    ↓
main.py: load_test_cases()
    ↓
ALL_TEST_CASES = [...]
    ↓
@pytest.mark.parametrize(ALL_TEST_CASES)
    ↓
For each test_case:
    - Extract fields
    - Get handler
    - Execute handler
    - Assert result
    - Log outcome
    ↓
Generate report HTML
    ↓
Display summary
```

## 🛡️ Use Case Coverage

### E-commerce Core (UC_01-UC_10)
- UC_01: Registration
- UC_02: Login
- UC_03: Password Management
- UC_04: Address Management
- UC_05: Wishlist
- UC_06: Product Comparison
- UC_07: Product Review
- UC_08: Shopping Cart
- UC_09: Checkout Process
- UC_10: Order Management

### Product & Catalog (UC_11-UC_18)
- UC_11: Product Categories
- UC_12: Product Management
- UC_13: Discount Management
- UC_14: Coupon Management
- UC_15: Category SEO
- UC_16: Product SEO
- UC_17: Product Attributes
- UC_18: Related Products

### System Features (UC_19-UC_20)
- UC_19: Currency Management
- UC_20: Customer Groups

### Special Cases
- Security: XSS prevention tests
- Log check: Error handling tests

## 🔧 Configuration Hierarchy

```
Hard-coded defaults (conftest.py)
    ↓
Environment variables (.env)
    ↓
Config class (config.py)
    ↓
Runtime overrides (command line)
```

## 📊 Reporting System

### HTML Report Contents
- Test summary (passed/failed/skipped)
- Detailed test results
- Execution timeline
- Full logs for each test
- Test metadata

### Log Outputs
- **Console**: Real-time progress
- **File**: logs/automation.log - Complete history

### Artifacts
- **Screenshots**: failures/*.png - Failure evidence
- **Report**: reports/test_report.html - Full results

## 🚀 Performance Optimization

### Parallel Execution
```bash
pytest main.py -n 4 -v          # 4 workers
pytest main.py -n auto -v       # Auto-detect CPUs
```

### Selective Testing
```bash
pytest main.py -m high -v       # Only high priority
pytest main.py -k "cart" -v     # Only cart-related
pytest main.py -x -v            # Stop on first failure
```

### Resource Management
- Browser reused within test scope
- Page context closed after each test
- Memory automatically freed
- Timeout handling prevents hangs

## 🎓 Extension Points

### Add Custom Handler
```python
class UC21_CustomHandler(BaseHandler):
    async def execute_test(self, test_data):
        # Implementation here
        return True/False

USE_CASE_HANDLERS['UC_21'] = UC21_CustomHandler
```

### Add Custom Fixture
```python
@pytest.fixture
def my_fixture():
    # Setup
    yield value
    # Teardown
```

### Add Custom Assertion
```python
class AdvancedHandler(BaseHandler):
    async def verify_element_visible(self, selector):
        # Custom verification
        return True/False
```

## 🔍 Debugging

### Enable Debug Logging
```bash
pytest main.py -vv --log-cli-level=DEBUG
```

### Run Single Test
```bash
pytest main.py -k "TC_01_01" -vv
```

### View Failure Artifacts
```bash
ls -lt failures/                 # Latest screenshots
cat logs/automation.log | tail -50    # Latest logs
```

## 📦 Dependency Management

### Core Dependencies
- playwright: Browser automation
- pytest: Test framework
- pytest-playwright: Integration
- pytest-html: Report generation

### Optional Dependencies
- pytest-xdist: Parallel execution
- pytest-watch: Watch mode
- allure: Alternative reporting

## 🔐 Security Considerations

- No credentials in code (use .env)
- Test data isolated from production
- Headless mode disabled for visibility
- Screenshots sanitized of sensitive data
- Logs configurable for security

## 🎯 Testing Strategy

### Priority-Based Execution
1. **Critical (High)**: Must pass
2. **Important (Medium)**: Should pass
3. **Optional (Low)**: Nice to have

### Use Case-Based Organization
1. **Core Features**: Registration, Login, Cart, Checkout
2. **Secondary**: Category, Product, Review
3. **Advanced**: SEO, Currencies, Groups

### Data-Driven Approach
- Single handler method tests many scenarios
- Test data from external JSON
- Easy to add new cases without code changes
- Maintainable and scalable

## 📊 Metrics & Reporting

### Test Metrics
- Total executed
- Pass rate %
- Failure rate %
- Average execution time
- Success/failure breakdown by UC

### Failure Analysis
- Screenshot evidence
- Error messages
- Stack traces
- Detailed logs
- Timing information

## 🔄 CI/CD Integration

### GitHub Actions Example
```yaml
- Deploy code
- Install dependencies
- Run tests with pytest
- Upload artifacts (screenshots, reports)
- Notify on failure
```

### Jenkins Integration
```groovy
stage('Test') {
    steps {
        sh 'pytest main.py --junit-xml=results.xml'
    }
}
```

## 🎓 Best Practices Applied

✅ DRY (Don't Repeat Yourself) - Reusable handlers  
✅ SOLID Principles - Well-designed classes  
✅ Async/Await - Non-blocking execution  
✅ Error Handling - Graceful failure  
✅ Logging - Comprehensive audit trail  
✅ Configuration - Externalized settings  
✅ Modular - Easy to extend  
✅ Documented - Clear comments & examples  

## 📚 Files Created

```
Core Framework:
- main.py (267 lines) - Main test suite
- conftest.py - Pytest configuration
- handlers.py (497 lines) - 22 handler classes

Configuration:
- config.py - Configuration management
- pytest.ini - Pytest settings
- requirements.txt - Dependencies
- .env.example - Example env file
- .gitignore - Git exclusions

Utilities:
- run_tests.py - Interactive menu runner
- setup.sh - Auto setup script
- examples.py - Extension examples

Documentation:
- README.md - Complete guide
- QUICKSTART.md - Quick reference
- ARCHITECTURE.md - This file
```

## 🎯 Key Metrics

- **Code Coverage**: 203 test cases
- **Lines of Code**: ~1500
- **Handler Classes**: 22
- **Methods per Handler**: 1-5
- **Async Methods**: 50+
- **Markup Coverage**: 100% (all JSON test cases)
- **Documentation**: Comprehensive

## 🚀 Ready to Use

The framework is production-ready and can immediately:
- ✅ Load and execute all 203 test cases
- ✅ Generate HTML reports
- ✅ Capture failure evidence
- ✅ Provide detailed logging
- ✅ Run in parallel
- ✅ Filter by markers
- ✅ Extend with custom handlers
- ✅ Integrate with CI/CD

---

**Framework Version**: 1.0.0  
**Created**: 2026-05-15  
**Status**: Production Ready

