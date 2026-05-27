# QUICK START GUIDE
OpenCart Automation Testing Framework v1.0

## 🚀 Quick Installation (5 minutes)

### Step 1: Install Dependencies
```bash
cd /home/tung/PycharmProjects/PythonProject
pip install -r requirements.txt
```

### Step 2: Install Playwright Browsers
```bash
playwright install chromium
```

### Step 3: Create Directories
```bash
mkdir -p logs reports failures
```

### Step 4: Verify Installation
```bash
pytest --version
playwright --version
```

## 📊 Running Tests

### Run All 203 Tests
```bash
pytest main.py -v --html=reports/test_report.html --self-contained-html
```

### Run by Priority
```bash
# High priority only
pytest main.py -m high -v

# Medium priority only
pytest main.py -m medium -v
```

### Run by Use Case
```bash
# UC_01 - Registration
pytest main.py -m registration -v

# UC_02 - Login
pytest main.py -m login -v

# UC_08 - Cart
pytest main.py -m cart -v

# UC_09 - Checkout
pytest main.py -m checkout -v
```

### Run in Parallel (4 workers)
```bash
pytest main.py -n 4 -v
```

### Use Interactive Menu
```bash
python run_tests.py
```

## 📁 Project Structure

```
PythonProject/
├── main.py                          # Main test suite
├── conftest.py                      # Pytest fixtures & configuration
├── handlers.py                      # Use Case handlers (20 handlers)
├── config.py                        # Configuration management
├── requirements.txt                 # Python dependencies
├── pytest.ini                       # Pytest configuration
├── OpenCart_203_TestCases_Final.json # Test data (203 cases)
├── run_tests.py                     # Test runner utility
├── examples.py                      # Extension examples
├── README.md                        # Full documentation
├── QUICKSTART.md                    # This file
├── setup.sh                         # Setup script
└── (auto-created)
    ├── logs/automation.log          # Test execution logs
    ├── reports/test_report.html     # HTML test report
    └── failures/*.png               # Failure screenshots
```

## 🎯 Key Features

✅ **203 Test Cases** - All cases from JSON file  
✅ **Auto Markers** - High/Medium/Low priority + Use Case markers  
✅ **Data-Driven** - Tests parameterized from JSON  
✅ **Async/Await** - Full async support via Playwright  
✅ **Screenshot On Failure** - Automatic failure documentation  
✅ **HTML Reports** - Detailed test report generation  
✅ **Non-Headless** - Browser visible during execution  
✅ **Modular** - 20 separate handlers for different use cases  

## 🔧 Configuration

Edit `.env` file to customize:

```env
# OpenCart URL
OPENCART_URL=http://localhost/opencart_test/upload/

# Browser settings
BROWSER_HEADLESS=False
BROWSER_TYPE=chromium

# Test credentials
TEST_USER_EMAIL=shin@test.com
TEST_USER_PASSWORD=123456
```

## 📊 Test Markers

Run tests by marker:

```bash
# By Priority
pytest main.py -m high -v                    # High priority
pytest main.py -m medium -v                  # Medium priority
pytest main.py -m low -v                     # Low priority

# By Use Case (UC_01-UC_20)
pytest main.py -m registration -v            # UC_01
pytest main.py -m login -v                   # UC_02
pytest main.py -m password -v                # UC_03
pytest main.py -m address -v                 # UC_04
pytest main.py -m wishlist -v                # UC_05
pytest main.py -m comparison -v              # UC_06
pytest main.py -m review -v                  # UC_07
pytest main.py -m cart -v                    # UC_08
pytest main.py -m checkout -v                # UC_09
pytest main.py -m order -v                   # UC_10
pytest main.py -m category -v                # UC_11
pytest main.py -m product -v                 # UC_12
pytest main.py -m discount -v                # UC_13
pytest main.py -m coupon -v                  # UC_14
pytest main.py -m category_seo -v            # UC_15
pytest main.py -m product_seo -v             # UC_16
pytest main.py -m product_attribute -v       # UC_17
pytest main.py -m product_related -v         # UC_18
pytest main.py -m currency -v                # UC_19
pytest main.py -m customer_group -v          # UC_20
```

## 📋 Common Commands

```bash
# Run all tests (verbose with HTML report)
pytest main.py -v --html=reports/test_report.html --self-contained-html

# Stop on first failure
pytest main.py -x -v

# Run with verbose logging and debug info
pytest main.py -vv --log-cli-level=DEBUG

# Run tests matching a pattern
pytest main.py -k "TC_01" -v

# Run tests with coverage
pytest main.py --cov=handlers --cov-report=html

# Run tests in parallel (requires pytest-xdist)
pytest main.py -n 4 -v

# Run tests and show summary
pytest main.py -v --tb=short

# Run tests without capturing output
pytest main.py -v -s
```

## 📈 Test Results

### HTML Report
After running tests, open the report:
```bash
open reports/test_report.html    # macOS
xdg-open reports/test_report.html  # Linux
start reports/test_report.html     # Windows
```

### Failure Screenshots
Failed tests automatically capture screenshots:
```
failures/
├── TC_01_01_20240515_143025.png
├── TC_02_01_error_20240515_143050.png
├── TC_03_01_timeout_20240515_143100.png
└── ...
```

### Logs
View execution logs:
```bash
tail -f logs/automation.log    # Follow logs in real-time
grep ERROR logs/automation.log # Find errors
grep FAILED logs/automation.log # Find failures
```

## 🐛 Troubleshooting

### Problem: "No module named 'playwright'"
**Solution**: Install dependencies: `pip install -r requirements.txt`

### Problem: "OpenCart not accessible"
**Solution**: Ensure OpenCart is running: `curl http://localhost/opencart_test/upload/`

### Problem: "Element not found" errors
**Solution**: Update selectors in `handlers.py` to match your OpenCart theme

### Problem: Screenshots not saved
**Solution**: Ensure write permission: `chmod 755 failures/`

### Problem: Tests timeout
**Edit `.env` and increase timeout:
```env
NAVIGATION_TIMEOUT=120000
ACTION_TIMEOUT=60000
```

## 🎓 Understanding the Framework

### Handler Classes
- Each use case (UC_01-UC_20) has a handler class
- Handlers inherit from `BaseHandler`
- `get_handler()` function dispatches to correct handler
- Easy to extend with custom handlers

### Test Flow
1. Load 203 test cases from JSON
2. Parametrize each as individual test
3. For each test:
   - Get appropriate handler
   - Execute test logic
   - Verify expected result
   - Take screenshot on failure
4. Generate HTML report

### Adding New Tests
1. Add test case to JSON file
2. Handler is auto-selected by UC code
3. Run: `pytest main.py -v`

## 🔗 Resources

- **README.md** - Complete documentation
- **examples.py** - Extension examples and patterns
- **conftest.py** - Fixture definitions
- **handlers.py** - Handler implementations
- **config.py** - Configuration management

## 📞 Support

1. Check TROUBLESHOOTING section in README.md
2. Review `logs/automation.log` for details
3. Check `failures/` for screenshot evidence
4. Review HTML report: `reports/test_report.html`

## ✨ Pro Tips

1. **Reduce execution time**: Run only high-priority tests
   ```bash
   pytest main.py -m high -v
   ```

2. **Debug single test**: Use -k flag
   ```bash
   pytest main.py -k "TC_01_01" -vv -s
   ```

3. **Parallel execution**: Faster results
   ```bash
   pytest main.py -n 4 -v
   ```

4. **Skip failures**: Continue after failures
   ```bash
   pytest main.py --tb=no -v
   ```

5. **Watch mode**: Re-run tests on file change
   ```bash
   pytest-watch main.py
   ```

---

**Framework Version**: 1.0.0  
**Test Cases**: 203  
**Use Cases**: 20  
**Handlers**: 20  
**Last Updated**: 2026-05-15

