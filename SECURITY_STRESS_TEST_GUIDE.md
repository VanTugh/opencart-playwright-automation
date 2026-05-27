# 🔴 SECURITY STRESS TEST GUIDE

**File:** `security_stress_test.py`  
**Lines:** 1600  
**Test Cases:** 20 (one per Use Case UC_01 to UC_20)  
**Framework:** Pytest + Playwright + Asyncio  
**Status:** ✅ PRODUCTION READY  

---

## 📋 OVERVIEW

The `security_stress_test.py` file is a **comprehensive red team security testing suite** that implements all 20 critical vulnerabilities identified in the RED_TEAM_SECURITY_TEST_CASES.md document.

Each test case:
- ✅ Uses **async/await** for Playwright automation
- ✅ Implements both **UI-level** and **API-level** attacks
- ✅ Uses `page.evaluate()` for JavaScript manipulation
- ✅ Uses `page.request` for direct API calls
- ✅ Includes detailed logging
- ✅ Has comprehensive docstrings

---

## 🚀 INSTALLATION & SETUP

### 1. Ensure Dependencies Are Installed

```bash
pip install pytest pytest-asyncio playwright asyncio
playwright install chromium
```

### 2. Verify File Location

```bash
ls -lh ~/PycharmProjects/PythonProject/security_stress_test.py
```

Expected output: **1600 lines**, ~45KB

---

## 🧪 RUNNING THE TESTS

### Run All 20 Security Tests

```bash
pytest security_stress_test.py -v --tb=short
```

**Output Example:**
```
test_uc01_database_corruption PASSED                      [5%]
test_uc02_sql_injection_login PASSED                       [10%]
test_uc03_session_fixation PASSED                          [15%]
test_uc04_idor_hidden_products PASSED                      [20%]
...
test_uc20_customer_group_escalation PASSED                [100%]

======================== 20 passed in 45.23s ========================
```

### Run Specific Test Case

```bash
# Run only UC_01 (Database Overflow)
pytest security_stress_test.py::test_uc01_database_corruption -v -s

# Run only UC_02 (SQL Injection)
pytest security_stress_test.py::test_uc02_sql_injection_login -v -s

# Run only UC_14 (State Transition)
pytest security_stress_test.py::test_uc14_state_transition_skip_payment -v -s
```

### Run Tests by Marker

```bash
# Run only EXTREME difficulty tests
pytest security_stress_test.py -m extreme -v

# Run only HARD difficulty tests
pytest security_stress_test.py -m hard -v

# Run all security tests
pytest security_stress_test.py -m security -v
```

### Run Tests by Keyword

```bash
# Run all SQL injection tests
pytest security_stress_test.py -k "sql_injection" -v

# Run all IDOR tests
pytest security_stress_test.py -k "idor" -v

# Run all state/race condition tests
pytest security_stress_test.py -k "state_transition or race_condition" -v
```

### Run with Verbose Output and Screenshots

```bash
pytest security_stress_test.py -v -s --tb=long

# With custom timeout
pytest security_stress_test.py -v --timeout=300

# With detailed logging
pytest security_stress_test.py -v --log-cli-level=DEBUG
```

---

## 📊 TEST CASE BREAKDOWN

### Category 1: Database/Input Attacks

| Test | UC | Vulnerability | Attack Vector |
|------|-----|---|---|
| `test_uc01_database_corruption` | UC_01 | Buffer Overflow | 65KB firstname input |
| `test_uc05_sql_injection_search` | UC_05 | SQL Injection | `' UNION SELECT ...` |

### Category 2: Authentication/Authorization

| Test | UC | Vulnerability | Attack Vector |
|------|-----|---|---|
| `test_uc02_sql_injection_login` | UC_02 | SQL Injection Auth | `' OR '1'='1` |
| `test_uc17_admin_authorization_bypass` | UC_17 | Auth Bypass | Direct /admin/ access |
| `test_uc18_order_status_modification` | UC_18 | Auth Bypass | Status updates as customer |

### Category 3: IDOR (Insecure Direct Object References)

| Test | UC | Vulnerability | Attack Vector |
|------|-----|---|---|
| `test_uc04_idor_hidden_products` | UC_04 | IDOR | Enumerate product_id=1,2,3... |
| `test_uc07_idor_draft_products` | UC_07 | IDOR | Access draft product details |
| `test_uc11_idor_shipping_addresses` | UC_11 | IDOR | Access other customer addresses |
| `test_uc15_idor_orders` | UC_15 | IDOR | Enumerate order IDs, view all |
| `test_uc20_customer_group_escalation` | UC_20 | IDOR | Assign self to VIP group |

### Category 4: Parameter Tampering

| Test | UC | Vulnerability | Attack Vector |
|------|-----|---|---|
| `test_uc06_negative_price_filter` | UC_06 | Tampering | Negative price range |
| `test_uc08_negative_quantity_cart` | UC_08 | Tampering | Negative quantity -5 |
| `test_uc10_quantity_exceed_stock` | UC_10 | Tampering | Qty > stock (9999999) |
| `test_uc12_shipping_cost_manipulation` | UC_12 | Tampering | Negative shipping -$99 |
| `test_uc16_email_takeover` | UC_16 | Tampering | Change email to other user |
| `test_uc19_exchange_rate_manipulation` | UC_19 | Tampering | Rate = 0 or negative |

### Category 5: Race Conditions & Timing

| Test | UC | Vulnerability | Attack Vector |
|------|-----|---|---|
| `test_uc03_session_fixation` | UC_03 | Session Reuse | Reuse session after logout |
| `test_uc09_race_condition_cart_removal` | UC_09 | Race Condition | 5 concurrent deletes |
| `test_uc13_coupon_race_condition` | UC_13 | Race Condition | 10 concurrent coupon applies |

### Category 6: State Transition

| Test | UC | Vulnerability | Attack Vector |
|------|-----|---|---|
| `test_uc14_state_transition_skip_payment` | UC_14 | State Bypass | Jump to confirm without payment |

---

## 🔍 TEST EXECUTION FLOW

### Example: Test UC_02 (SQL Injection in Login)

```python
@pytest.mark.security
@pytest.mark.extreme
async def test_uc02_sql_injection_login(page: Page):
    """
    Step 1: Navigate to login page
    Step 2: Inject SQL payload: admin@test.com' OR '1'='1
    Step 3: Check if authentication is bypassed
    Step 4: Try time-based blind SQL injection (SLEEP)
    Step 5: Measure response time to detect query execution
    Step 6: Assert vulnerability or pass
    """
    
    logger.info("Testing SQL injection...")
    
    # 1. Setup
    await page.goto(f"{BASE_URL}index.php?route=account/login")
    
    # 2. Inject malicious email
    sql_injection_email = "admin@test.com' OR '1'='1"
    
    # 3. Send via direct API (bypass UI validation)
    response = await page.request.post(
        f"{BASE_URL}index.php?route=account/login",
        data={"email": sql_injection_email, "password": "anything"}
    )
    
    # 4. Check result
    if "My Account" in await response.text():
        assert False, "SQL injection successful - auth bypassed!"
```

---

## 🎯 KEY FEATURES

### 1. Async/Await Support
All tests are async for performance:
```python
async def test_uc09_race_condition_cart_removal(authenticated_page):
    # Send 5 concurrent DELETE requests
    delete_tasks = [
        page.request.post(...),
        page.request.post(...),
        # ... 5 times
    ]
    responses = await asyncio.gather(*delete_tasks)
```

### 2. Direct API Attack Capability
Uses `page.request` to bypass UI validation:
```python
response = await page.request.post(
    f"{BASE_URL}index.php?route=checkout/cart/add",
    data={"product_id": "43", "quantity": "-5"}  # Negative!
)
```

### 3. JavaScript Evaluation
Uses `page.evaluate()` to manipulate DOM:
```python
await page.evaluate("""
    document.querySelector('input[name="quantity"]').value = '9999999';
    document.querySelector('button[onclick*="cart.add"]').click();
""")
```

### 4. Comprehensive Logging
Every test logs detailed information:
```
2026-05-15 10:30:45 - security_stress_test - INFO - 🔴 TEST: UC_02 - SQL Injection
2026-05-15 10:30:46 - security_stress_test - ERROR - 🔴 SQL INJECTION CONFIRMED
```

### 5. Multiple Attack Vectors Per Test
Each test tries multiple exploitation methods:
```python
# Method 1: Classic OR-based bypass
# Method 2: Union-based injection  
# Method 3: Time-based blind SQL injection
```

---

## 📈 EXPECTED RESULTS

### If System is SECURE ✅
```
test_uc01_database_corruption PASSED
test_uc02_sql_injection_login PASSED
test_uc03_session_fixation PASSED
...
======================== 20 PASSED ========================
```

### If System is VULNERABLE ❌
```
FAILED security_stress_test.py::test_uc02_sql_injection_login
AssertionError: SQL injection successful - auth bypassed!

FAILED security_stress_test.py::test_uc14_state_transition_skip_payment
AssertionError: Order placed without payment method selected!
```

---

## 🔧 CUSTOMIZATION

### Modify Target URL
```python
# In security_stress_test.py, line ~35
BASE_URL = "http://localhost/opencart_test/upload/"

# Change to:
BASE_URL = "http://your-site.com/opencart/"
```

### Modify Test Credentials
```python
# Line ~48-54
TEST_USER = {
    "email": "shin@test.com",
    "password": "123456"
}

# Change to your test user
```

### Add Custom Test
```python
@pytest.mark.security
async def test_custom_vulnerability(page: Page):
    """Test custom vulnerability"""
    logger.info("Testing custom flaw...")
    
    response = await page.request.post(
        f"{BASE_URL}custom/endpoint",
        data={"param": "malicious_value"}
    )
    
    if response.status == 200:
        assert False, "Custom vulnerability confirmed!"
```

---

## 📝 INTEGRATION WITH CI/CD

### GitHub Actions Example

```yaml
name: Security Tests

on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - run: pip install -r requirements.txt
      - run: pytest security_stress_test.py -v --tb=short
```

### GitLab CI Example

```yaml
security_tests:
  stage: test
  script:
    - pip install -r requirements.txt
    - pytest security_stress_test.py -v --timeout=300
  artifacts:
    reports:
      junit: test-results.xml
```

---

## 🐛 TROUBLESHOOTING

### Issue: Tests Timeout
**Solution:** Increase timeout or check if server is running
```bash
pytest security_stress_test.py --timeout=600
```

### Issue: Browser Not Starting
**Solution:** Install Chromium
```bash
playwright install chromium
```

### Issue: Tests Fail with ConnectionError
**Solution:** Verify OpenCart is running
```bash
# Check if server is responsive
curl http://localhost/opencart_test/upload/
```

### Issue: Some Tests Skipped
**Solution:** Check fixtures and dependencies
```bash
pytest security_stress_test.py -v --setup-show
```

---

## 📊 REPORTING RESULTS

### Generate HTML Report
```bash
pytest security_stress_test.py -v --html=security_report.html --self-contained-html
```

### Generate JUnit XML
```bash
pytest security_stress_test.py -v --junit-xml=security_results.xml
```

### Generate Detailed Log
```bash
pytest security_stress_test.py -v --log-file=security_test.log --log-cli-level=INFO
```

---

## ✅ SECURITY TESTING CHECKLIST

Before deploying your OpenCart system to production:

- [ ] Run all 20 security tests: `pytest security_stress_test.py -v`
- [ ] Verify 0 failures: Look for "20 PASSED"
- [ ] Check for EXTREME vulnerabilities: Run with `-m extreme`
- [ ] Review logs for warnings: `pytest security_stress_test.py -v -s`
- [ ] Test with real user data: Modify TEST_USER credentials
- [ ] Run against production-like environment
- [ ] Document any findings: Create issue tickets
- [ ] Fix vulnerabilities: Implement security patches
- [ ] Re-test after fixes: Run tests again

---

## 🎓 LEARNING OUTCOMES

After running these tests, you'll understand:

1. **SQL Injection** - How to detect and prevent
2. **IDOR Vulnerabilities** - Authorization bypass techniques
3. **Parameter Tampering** - Input validation importance
4. **Race Conditions** - Concurrency issues
5. **Session Management** - Proper invalidation
6. **API Security** - Endpoint authorization
7. **State Machines** - Workflow enforcement

---

## 📞 SUPPORT & DOCUMENTATION

**See also:**
- `RED_TEAM_SECURITY_TEST_CASES.md` - Detailed vulnerability analysis
- `IMPLEMENTATION.md` - Framework overview
- `README.md` - General documentation
- `handlers.py` - Handler implementations

---

## ⚖️ LEGAL & ETHICAL

This test suite is designed for:
- ✅ Testing your own systems
- ✅ Authorized penetration testing
- ✅ Security research and education
- ✅ Finding and fixing vulnerabilities

Not for:
- ❌ Unauthorized access
- ❌ Testing systems you don't own
- ❌ Malicious purposes

---

## 📈 SUMMARY

| Aspect | Details |
|--------|---------|
| **Lines of Code** | 1,600 |
| **Test Cases** | 20 |
| **Async Functions** | 20 |
| **Attack Types** | 6 categories |
| **Framework** | Pytest + Playwright |
| **Difficulty** | Hard - Extreme |
| **Status** | ✅ Production Ready |
| **Documentation** | Comprehensive |

---

## 🚀 QUICK START

```bash
# 1. Install dependencies
pip install pytest pytest-asyncio playwright

# 2. Install browser
playwright install chromium

# 3. Start OpenCart (make sure it's running)
# Open XAMPP and start Apache/MySQL

# 4. Run all security tests
pytest security_stress_test.py -v

# 5. Check results
# All 20 tests should PASS if system is secure
# Any FAILED tests indicate vulnerabilities
```

---

**Generated:** May 15, 2026  
**Status:** ✅ READY FOR PRODUCTION TESTING  
**Maintainer:** Security Team  
**Version:** 1.0


