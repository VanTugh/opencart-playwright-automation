# 📊 NON-FUNCTIONAL TESTING SUITE - Complete Reference Guide

## 🎯 Overview

A comprehensive **60-test non-functional testing suite** for OpenCart 4.1.0.3 covering three critical subsystems:

- ✅ **Performance Testing** (20 tests)
- ✅ **Security Testing** (20 tests)
- ✅ **Usability Testing** (20 tests)

**Total:** 5,000+ lines of production-grade Python code

**Status:** 🟢 Ready for execution

---

## 📋 Test Structure

### **Performance Testing (20 tests)**

#### Basic Tests (10)
| # | Test | Purpose | Threshold |
|---|------|---------|-----------|
| 01 | Homepage Load Time | Measure homepage load | < 3000ms |
| 02 | Product Page Load | Product detail page load | < 2500ms |
| 03 | Category Load Time | Category page load | < 2500ms |
| 04 | Cart Page Load | Shopping cart load | < 2000ms |
| 05 | Search Response | Simple keyword search | < 2000ms |
| 06 | Login Response | User authentication | < 2500ms |
| 07 | Add to Cart Response | Cart operation | < 1500ms |
| 08 | API Product List | REST API performance | < 1000ms |
| 09 | Database Aggregate Query | Multi-query performance | < 3000ms |
| 10 | Static Assets Load | CSS/JS/Image load | < 4000ms |

#### Advanced Tests (10)
| # | Test | Purpose | Finding |
|---|------|---------|---------|
| 01 | Heavy Search Stress | Complex keyword (500 chars) | Identify search bottleneck |
| 02 | Rapid API Requests | 10 simultaneous cart adds | Detect API overload |
| 03 | DB Connection Pool | 5 concurrent page loads | Connection pool limits |
| 04 | Memory Leak Detection | Page reload cycling | Memory degradation |
| 05 | Large Dataset Load | 100+ products on page | Rendering bottleneck |
| 06 | CSS Selector Performance | Complex selectors | DOM query efficiency |
| 07 | Concurrent Users (5) | Multi-user simulation | Degradation % |
| 08 | Pagination Consistency | Load time variance | Inconsistent performance |
| 09 | JSON Payload Size | API response size | Optimize transfer |
| 10 | API Rate Limiting | No protection check | DDoS vulnerability |

### **Security Testing (20 tests)**

#### Basic Tests (10)
| # | Test | Vulnerability | Attack Vector |
|---|------|---|---|
| 01 | SQL Injection - Email | Database escape bypass | `' OR '1'='1' -- ` |
| 02 | XSS - Profile Name | Script injection | `<script>alert()</script>` |
| 03 | Password Storage | Plaintext transmission | Response body check |
| 04 | CSRF Protection | Token missing | Form analysis |
| 05 | Error Disclosure | Information leakage | Path/stack trace exposure |
| 06 | IDOR - Address | Unauthorized access | arbitrary address_id |
| 07 | Session Entropy | Predictable tokens | Token pattern analysis |
| 08 | HTTPS Enforcement | Protocol downgrade | HTTP redirect check |
| 09 | Default Credentials | Admin/admin still valid | Direct admin login |
| 10 | Input Validation | Buffer overflow | 10,000 character input |

#### Advanced Tests (10)
| # | Test | Severity | Exploitation |
|---|------|---|---|
| 01 | Negative Price Tampering | CRITICAL | POST with price: -100 |
| 02 | IDOR Order Enumeration | CRITICAL | Increment order_id 1-20 |
| 03 | Address Modification IDOR | CRITICAL | PUT address of other user |
| 04 | Race Condition - Coupon | HARD | 10 concurrent applies |
| 05 | DB Corruption - Overflow | HARD | 65,000 char input |
| 06 | Email Header Injection | HARD | Newline in email field |
| 07 | Payment Amount Bypass | EXTREME | DOM manipulation |
| 08 | Admin Auth Bypass | EXTREME | No login direct access |
| 09 | Stored XSS - Product | HARD | Persistent XSS in DB |
| 10 | Unencrypted Transit | HARD | Plaintext data over HTTP |

### **Usability Testing (20 tests)**

#### Basic Tests (10)
| # | Test | Standard | Expectation |
|---|------|---|---|
| 01 | Mobile Responsive | 375px viewport | No horizontal scroll |
| 02 | Navigation Accessibility | WCAG 2.1 | All menus accessible |
| 03 | Form Label Association | Accessible names | 50%+ fields labeled |
| 04 | Button Text Clarity | Semantic HTML | No generic "Click" |
| 05 | Image Alt Text | WCAG AAA | 80%+ coverage |
| 06 | Color Contrast | WCAG AA | 4.5:1 minimum ratio |
| 07 | Page Title (SEO) | Meta tags | Unique, descriptive |
| 08 | Breadcrumb Nav | UX best practice | Location indicator |
| 09 | 404 Error Page | Error handling | Clear message + help |
| 10 | Loading Indicators | UX feedback | Visible progress |

#### Advanced Tests (10)
| # | Test | Missing Feature | Impact |
|---|------|---|---|
| 01 | Price Range Filter | Budget filter Min-Max | **CRITICAL** - Can't filter |
| 02 | Sort Options | Sort by price/popularity | User frustration |
| 03 | Pagination | Previous/Next controls | Navigation difficulty |
| 04 | Product Gallery | Image zoom/multiple | Limited product view |
| 05 | Quick Wishlist | Heart icon on list | Extra clicks required |
| 06 | Compare Products | Side-by-side comparison | Feature missing |
| 07 | Review/Rating | Star display | No social proof |
| 08 | Search Autocomplete | Dropdown suggestions | Search friction |
| 09 | Quick View Modal | Popup product preview | Full page required |
| 10 | Mobile Hamburger | Menu toggle | Poor mobile UX |

---

## 🚀 Quick Start

### Installation

```bash
cd /home/tung/PycharmProjects/PythonProject

# Install dependencies (if needed)
pip install -r requirements.txt
playwright install chromium
```

### Run All 60 Tests

```bash
pytest test_non_functional_suite.py -v
```

### Run by Subsystem

```bash
# Performance only (20 tests)
pytest test_non_functional_suite.py::TestPerformanceBasic -v
pytest test_non_functional_suite.py::TestPerformanceAdvanced -v

# Security only (20 tests)
pytest test_non_functional_suite.py::TestSecurityBasic -v
pytest test_non_functional_suite.py::TestSecurityAdvanced -v

# Usability only (20 tests)
pytest test_non_functional_suite.py::TestUsabilityBasic -v
pytest test_non_functional_suite.py::TestUsabilityAdvanced -v
```

### Run by Difficulty Level

```bash
# Basic tests only (30 tests)
pytest test_non_functional_suite.py -m basic -v

# Advanced tests only (30 tests)
pytest test_non_functional_suite.py -m advanced -v

# All security tests
pytest test_non_functional_suite.py -m security -v
```

### Individual Test Examples

```bash
# Single performance test
pytest test_non_functional_suite.py::TestPerformanceBasic::test_perf_basic_01_homepage_load_time -vv

# Single security test
pytest test_non_functional_suite.py::TestSecurityAdvanced::test_sec_advanced_01_negative_price_parameter_tampering -vv

# Single usability test
pytest test_non_functional_suite.py::TestUsabilityAdvanced::test_usab_advanced_01_price_filter_missing_minmax -vv
```

---

## 📊 Expected Results

### Performance Tests

**Healthy System** (No failures):
```
✅ PASSED: All 10 basic load time tests < thresholds
✅ PASSED: Advanced tests find NO bottlenecks
✅ PASSED: Connection pool handles 5 concurrent users
✅ PASSED: Memory stable across reload cycles
```

**Unhealthy System** (Failures):
```
❌ FAILED: Homepage > 3000ms
❌ FAILED: API overloaded at 10 concurrent requests
❌ FAILED: Memory leak detected (30% growth)
❌ FAILED: Large dataset (100+ products) > 5000ms
```

### Security Tests

**Secure System** (All pass):
```
✅ PASSED: SQL injection blocked
✅ PASSED: XSS escaped properly
✅ PASSED: CSRF tokens present on all forms
✅ PASSED: Default credentials disabled
✅ PASSED: IDOR protections in place
✅ PASSED: HTTPS required
✅ PASSED: No negative prices accepted
```

**Vulnerable System** (Failures):
```
❌ FAILED: SQL Injection vulnerability - email field
❌ FAILED: Parameter tampering - accepted negative price
❌ FAILED: IDOR - can view order #5 as non-owner
❌ FAILED: Race condition - coupon applied 5 times
❌ FAILED: Auth bypass - accessed admin without login
```

### Usability Tests

**Excellent UX** (Minor warnings only):
```
✅ PASSED: Mobile responsive at 375px
✅ PASSED: Navigation accessible
✅ PASSED: All forms have labels
✅ PASSED: Price filter available
✅ PASSED: Sort options present
⚠️ WARNING: No autocomplete (minor)
```

**Poor UX** (Critical failures):
```
❌ FAILED: NO PRICE FILTER - cannot filter by budget
❌ FAILED: Horizontal scroll on mobile (375px)
❌ FAILED: 404 page unclear
❌ FAILED: No breadcrumb navigation
```

---

## 📸 Automatic Evidence

### Screenshot Naming Convention

When tests fail (intentionally failing for vulnerability/UX issues):

```
failures/AUTO_FAIL_PERF_ADV_01_HEAVY_SEARCH.png
failures/AUTO_FAIL_SEC_ADV_01_NEGATIVE_PRICE.png
failures/AUTO_FAIL_SEC_ADV_02_IDOR_ORDER_5.png
failures/AUTO_FAIL_USAB_ADV_01_NO_PRICE_FILTER.png
```

### How It Works

1. Test detects vulnerability/issue
2. **Takes screenshot automatically** (full page)
3. Saves to `/failures/AUTO_FAIL_[CODE].png`
4. Logs detailed evidence
5. Calls `assert False` to mark FAILED
6. Screenshot provides exact state of bug

---

## 🔍 Test Output Example

```bash
$ pytest test_non_functional_suite.py::TestPerformanceBasic::test_perf_basic_01_homepage_load_time -vv

test_non_functional_suite.py::TestPerformanceBasic::test_perf_basic_01_homepage_load_time PASSED [100%]

🚀 [PERF_BASIC_01] Đang đo thời gian load Homepage...
✅ Homepage loaded in 2345.67ms
======================== 1 passed in 5.32s =========================
```

```bash
$ pytest test_non_functional_suite.py::TestSecurityAdvanced::test_sec_advanced_01_negative_price_parameter_tampering -vv

test_non_functional_suite.py::TestSecurityAdvanced::test_sec_advanced_01_negative_price_parameter_tampering FAILED [100%]

🔒 [SEC_ADV_01] Kiểm tra Parameter Tampering - Negative Price...
❌ PRICE TAMPERING VULNERABILITY: Negative price accepted!
📸 Saved screenshot: failures/AUTO_FAIL_SEC_ADV_01_NEGATIVE_PRICE.png
======================== 1 failed in 8.45s =========================
```

---

## 🎓 Code Structure

### Performance Testing Class

```python
class TestPerformanceBasic:
    """10 Basic performance tests"""
    
    @pytest.mark.asyncio
    @pytest.mark.performance
    @pytest.mark.basic
    async def test_perf_basic_01_homepage_load_time(self, page: Page):
        """Detailed docstring explaining purpose, threshold, expected result"""
        # 1. Navigate to page
        # 2. Measure time
        # 3. Assert time < threshold
        # 4. Log results
```

### Security Testing Class

```python
class TestSecurityAdvanced:
    """10 Advanced security tests"""
    
    @pytest.mark.asyncio
    @pytest.mark.security
    @pytest.mark.advanced
    async def test_sec_advanced_01_negative_price_parameter_tampering(self, page: Page):
        """Exploit logic flaw by tampering parameters"""
        # 1. Navigate to product
        # 2. Use page.request to send API with negative price
        # 3. Verify if accepted
        # 4. Take screenshot if vulnerability confirmed
        # 5. Assert False to mark as bug evidence
```

### Usability Testing Class

```python
class TestUsabilityAdvanced:
    """10 Advanced usability tests"""
    
    @pytest.mark.asyncio
    @pytest.mark.usability
    @pytest.mark.advanced
    async def test_usab_advanced_01_price_filter_missing_minmax(self, page: Page):
        """Check for missing price range filter"""
        # 1. Navigate to category page
        # 2. Look for min-max price input elements
        # 3. If missing, take screenshot
        # 4. Assert False with detailed message
```

---

## 🛠️ Advanced Usage

### Run with Performance Profiling

```bash
pytest test_non_functional_suite.py -v --tb=short --durations=10
# Shows slowest 10 tests
```

### Run Security Tests in Parallel

```bash
pytest test_non_functional_suite.py::TestSecurityAdvanced -v -n 4
# Requires pytest-xdist (pip install pytest-xdist)
```

### Custom Report Generation

```bash
pytest test_non_functional_suite.py -v \
    --html=reports/nonfunctional_report.html \
    --self-contained-html
```

### Filter by Severity

```bash
# Critical security tests only
pytest test_non_functional_suite.py -m "security and advanced" -v

# Basic tests (less strict)
pytest test_non_functional_suite.py -m "basic" -v
```

---

## 📋 Fixtures Used

All tests use standard conftest fixtures:

- `page: Page` - Playwright page object
- `BASE_URL` - From conftest.py
- `logger` - From conftest.py
- `browser: Browser` - For advanced concurrent testing

---

## 🔐 Security Test Details

### Critical Vulnerabilities Tested

1. **SQL Injection** - Database escape bypass
2. **XSS** - Script injection in forms
3. **Parameter Tampering** - Price manipulation
4. **IDOR** - Unauthorized object access
5. **Race Conditions** - Duplicate coupon apply
6. **Buffer Overflow** - 65k character input
7. **Email Injection** - Header manipulation
8. **Auth Bypass** - Direct admin access
9. **Stored XSS** - Persistent script in DB
10. **Unencrypted Transit** - HTTP plaintext data

Each test attempts exploitation before asserting failure.

---

## 📈 Performance Baseline

### Healthy System Targets

| Test | Expected | Threshold |
|------|----------|-----------|
| Homepage | 1.5s | < 3s |
| Product Page | 1.2s | < 2.5s |
| Search (simple) | 0.8s | < 2s |
| Add to Cart | 0.6s | < 1.5s |
| API Response | 0.3s | < 1s |

Adjust thresholds in code based on your infrastructure.

---

## ✨ Key Features

✅ **Playwright Async** - Non-blocking, parallel-friendly  
✅ **Data-Driven** - 60 independent test cases  
✅ **Modular** - Easy to extend with new tests  
✅ **Detailed Logging** - Every step logged  
✅ **Auto Screenshots** - Evidence on failure  
✅ **WCAG Compliance** - Accessibility checks  
✅ **Security Focused** - 20 vulnerability tests  
✅ **Performance Aware** - Load time analysis  
✅ **User-Centric** - Missing feature detection  

---

## 🐛 Troubleshooting

### Test Timeout

**Problem:** Test exceeds default timeout

**Solution:**
```python
await page.goto(URL, timeout=15000)  # Increase to 15s
```

### Cookie/Session Issues

**Problem:** Tests fail due to session/auth

**Solution:**
```bash
# Clear cookies between tests
pytest test_non_functional_suite.py --cache-clear
```

### Selector Not Found

**Problem:** Element selector doesn't exist

**Solution:**
- Tests use try/except for invalid selectors
- Check page.query_selector() returns None
- Use await page.wait_for_selector() for dynamic content

### Screenshot Fails

**Problem:** Screenshots not saved

**Solution:**
```bash
# Ensure failures/ directory exists
mkdir -p failures/

# Or tests create it automatically
```

---

## 👥 Integration with CI/CD

### GitHub Actions Example

```yaml
name: Non-Functional Tests
on: [push]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install -r requirements.txt
      - run: playwright install chromium
      - run: pytest test_non_functional_suite.py -v
      - uses: actions/upload-artifact@v2
        if: failure()
        with:
          name: failure-screenshots
          path: failures/
```

### Jenkins Example

```groovy
pipeline {
    stages {
        stage('Non-Functional Tests') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'pytest test_non_functional_suite.py --html=reports/nonfunctional.html'
            }
        }
        stage('Archive Reports') {
            steps {
                archiveArtifacts artifacts: 'failures/**/*.png'
                publishHTML([reportDir: 'reports', reportFiles: 'nonfunctional.html'])
            }
        }
    }
}
```

---

## 📊 Metrics & KPIs

Track these metrics across test runs:

| Metric | Target | Warning | Critical |
|--------|--------|---------|----------|
| Performance Pass Rate | 100% | < 95% | < 90% |
| Security Pass Rate | 100% | < 98% | < 95% |
| Usability Pass Rate | 95% | < 90% | < 80% |
| Avg Load Time | < 2s | > 2.5s | > 3s |
| API Response | < 1s | > 1.2s | > 1.5s |

---

## 📞 Support & Reporting

When reporting test failures:

1. **Include test name** - e.g., `test_perf_advanced_02_rapid_fire_cart_requests`
2. **Attach screenshot** - From `failures/` directory
3. **Provide log output** - From test run
4. **Note environment** - XAMPP version, OpenCart version

---

## 📞 Version

- **Framework Version:** 1.0.0
- **Python:** 3.8+
- **Playwright:** 1.40+
- **Pytest:** 7.0+
- **Created:** May 2026
- **Status:** Production Ready ✅

---

**End of Non-Functional Testing Guide**

