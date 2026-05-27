# Quick Start Guide - Test Fail Cases Execution

## ⚡ TL;DR - 30 Seconds to First Test

```bash
# 1. Install dependencies (if not already done)
pip install pytest-asyncio playwright
playwright install chromium

# 2. Run all 10 fail case tests
pytest test_fail_cases.py -v

# 3. Check evidence
ls -la failures/AUTO_FAIL_*.png
```

---

## 📖 What You'll Get

Running the tests will show:

```
test_fail_cases.py::test_tc_fail_01_register_no_password_confirm_validation FAILED [ 10%]
test_fail_cases.py::test_tc_fail_02_register_telephone_accepts_letters FAILED [ 20%]
test_fail_cases.py::test_tc_fail_03_search_accepts_single_character FAILED [ 30%]
test_fail_cases.py::test_tc_fail_04_filter_missing_price_range FAILED [ 40%]
test_fail_cases.py::test_tc_fail_05_add_to_cart_zero_quantity_accepted FAILED [ 50%]
test_fail_cases.py::test_tc_fail_06_add_to_cart_negative_quantity_accepted FAILED [ 60%]
test_fail_cases.py::test_tc_fail_07_update_cart_string_quantity_no_validation FAILED [ 70%]
test_fail_cases.py::test_tc_fail_08_checkout_terms_not_required FAILED [ 80%]
test_fail_cases.py::test_tc_fail_09_admin_product_negative_price_accepted FAILED [ 90%]
test_fail_cases.py::test_tc_fail_10_admin_delete_product_with_orders FAILED [100%]

10 FAILED in 45.23s
```

✅ **All FAILED = Expected** (means vulnerabilities confirmed)

---

## 🎯 Run Variants

### **Run Only Critical Tests (7 tests)**
```bash
pytest test_fail_cases.py -m critical -v
```

### **Run Only Medium Priority (3 tests)**
```bash
pytest test_fail_cases.py -m medium -v
```

### **Run Single Test with Full Debug**
```bash
pytest test_fail_cases.py::test_tc_fail_05_add_to_cart_zero_quantity_accepted -vv --tb=long
```

### **Run and Stop on First Failure**
```bash
pytest test_fail_cases.py -x -v
```

### **Run with Timeout (30 seconds per test)**
```bash
pytest test_fail_cases.py -v --timeout=30
```

---

## 📁 Output Structure

After running tests:

```
PythonProject/
├── test_fail_cases.py                  # Test file (950 lines)
├── failures/                            # Test evidence
│   ├── AUTO_FAIL_TC_FAIL_01.png       # Registration vulnerability
│   ├── AUTO_FAIL_TC_FAIL_02.png       # Telephone validation
│   ├── AUTO_FAIL_TC_FAIL_03.png       # Search validation
│   ├── AUTO_FAIL_TC_FAIL_04.png       # Missing filter
│   ├── AUTO_FAIL_TC_FAIL_05.png       # Zero quantity
│   ├── AUTO_FAIL_TC_FAIL_06.png       # Negative quantity
│   ├── AUTO_FAIL_TC_FAIL_07.png       # String quantity
│   ├── AUTO_FAIL_TC_FAIL_08.png       # Terms validation
│   ├── AUTO_FAIL_TC_FAIL_09.png       # Admin price
│   └── AUTO_FAIL_TC_FAIL_10.png       # Admin delete
└── logs/
    └── automation.log                   # Detailed execution log
```

---

## 🔍 Analyzing Evidence

### **View Screenshot of Failed Test**
```bash
# Linux - view in image viewer
eog failures/AUTO_FAIL_TC_FAIL_05.png

# Or open in IDE
cat failures/AUTO_FAIL_TC_FAIL_05.png | base64 -d | display
```

### **Read Detailed Logs**
```bash
# Show last 50 lines
tail -50 logs/automation.log

# Show specific test logs
grep "TC_FAIL_05" logs/automation.log

# Follow logs in real-time
tail -f logs/automation.log
```

### **Count Failures**
```bash
ls -1 failures/AUTO_FAIL_*.png | wc -l
# Expected output: 10
```

---

## 🛠️ Troubleshooting

### **"Connection refused" Error**
```
Error: Page.goto: net::ERR_CONNECTION_REFUSED
```
**Fix:** Ensure OpenCart is running on `http://localhost/opencart_test/upload/`

### **"Element not found" Error**
```
TimeoutError: Waiting for selector 'input[name="quantity"]'
```
**Fix:** Test selectors may need adjustment for your OpenCart version

### **"Tests hang" Issue**
```bash
# Kill hanging browser processes
pkill -f chromium
pkill -f pytest
```

### **"Screenshots not saving" Problem**
```bash
# Ensure failures directory exists
mkdir -p failures
chmod 777 failures
```

---

## 📊 Interpretation Guide

### **If ALL 10 Tests FAIL** ✅
This is **GOOD** - means OpenCart has the vulnerabilities documented in `10_testcase_chac_chan_fail.md`

### **If SOME Tests PASS** ⚠️
This means those features have been partially patched

### **If ALL Tests PASS** ✨
OpenCart has been hardened - vulnerabilities are fixed!

---

## 🎓 Understanding Test Names

```
test_tc_fail_01_register_no_password_confirm_validation
├── tc_fail_01        → Test ID from specification
├── register          → Feature being tested
├── no_password...    → The specific vulnerability
└── validation        → Type of check (validation bypass)
```

---

## 💡 Quick Facts

| Aspect | Details |
|--------|---------|
| **Test Count** | 10 tests |
| **Critical** | 7 tests (High severity) |
| **Medium** | 3 tests (Medium severity) |
| **Framework** | Pytest + Playwright Async |
| **Duration** | ~45-60 seconds for all tests |
| **Evidence** | Full page screenshots |
| **Logging** | Detailed step-by-step logs |

---

## 🚀 Integration Examples

### **GitHub Actions CI/CD**
```yaml
- name: Run Fail Case Tests
  run: pytest test_fail_cases.py -v --tb=short
```

### **Jenkins Pipeline**
```groovy
stage('Security Tests') {
    steps {
        sh 'pytest test_fail_cases.py -v --junitxml=results.xml'
    }
}
```

### **Pre-Commit Hook**
```bash
#!/bin/bash
pytest test_fail_cases.py -m critical -q
```

---

## 📝 Test Documentation

For detailed documentation on each test, read:
- **Primary:** `TEST_FAIL_CASES_README.md` (comprehensive guide)
- **Specification:** `10_testcase_chac_chan_fail.md` (original requirements)
- **Security:** `RED_TEAM_SECURITY_TEST_CASES.md` (attack methodology)

---

## ✅ Pre-Flight Checklist

Before running tests:

```bash
# Check OpenCart is running
curl -s http://localhost/opencart_test/upload/ | grep -q "<!DOCTYPE" && echo "✓ OpenCart running" || echo "✗ OpenCart not found"

# Check Python version
python --version  # Needs 3.7+

# Check Pytest installed
pytest --version  # Needs pytest 7.4+

# Check Playwright installed
python -c "import playwright; print('✓ Playwright installed')"

# Check failures directory
mkdir -p failures && echo "✓ Directory ready"
```

---

## 🎯 Sample Output

```
==== 10 FAILED in 45.23s ====

FAILURES:
____ test_tc_fail_01_register_no_password_confirm_validation ____
AssertionError: TC_FAIL_01 CONFIRMED: Register form has no password confirmation field

____ test_tc_fail_02_register_telephone_accepts_letters ____
AssertionError: TC_FAIL_02 CONFIRMED: Telephone field validates only length, not format

____ test_tc_fail_03_search_accepts_single_character ____
AssertionError: TC_FAIL_03 CONFIRMED: Search accepts single character keywords

... (7 more) ...

EVIDENCE CAPTURED:
✓ failures/AUTO_FAIL_TC_FAIL_01.png (45 KB)
✓ failures/AUTO_FAIL_TC_FAIL_02.png (42 KB)
✓ failures/AUTO_FAIL_TC_FAIL_03.png (38 KB)
✓ failures/AUTO_FAIL_TC_FAIL_04.png (40 KB)
✓ failures/AUTO_FAIL_TC_FAIL_05.png (50 KB)
✓ failures/AUTO_FAIL_TC_FAIL_06.png (51 KB)
✓ failures/AUTO_FAIL_TC_FAIL_07.png (43 KB)
✓ failures/AUTO_FAIL_TC_FAIL_08.png (55 KB)
✓ failures/AUTO_FAIL_TC_FAIL_09.png (48 KB) [Admin test]
✓ failures/AUTO_FAIL_TC_FAIL_10.png (49 KB) [Admin test]
```

---

## 📚 Test Data

Tests use real OpenCart product IDs and pages:
- **Product Page:** `product_id=28` (iPhone product)
- **Category:** `path=20` (Sample category)
- **Dynamic Data:** Unique emails with timestamps

---

## 🔐 Security Notes

- ✅ Tests use real OpenCart instance
- ✅ No data destruction (no actual product deletion)
- ✅ Admin tests gracefully skip if auth needed
- ✅ All evidence captured automatically
- ✅ Logs contain detailed execution trace

---

## 💾 Saving Results

```bash
# Save test output to file
pytest test_fail_cases.py -v > test_results.txt

# Generate XML report (for CI/CD)
pytest test_fail_cases.py -v --junit-xml=results.xml

# Generate detailed HTML report
pytest test_fail_cases.py -v --html=report.html --self-contained-html
```

---

## 🎯 Next Actions

1. ✅ Run: `pytest test_fail_cases.py -v`
2. ✅ Review: Screenshots in `failures/` directory
3. ✅ Analyze: Check `logs/automation.log`
4. ✅ Report: Document findings for development team
5. ✅ Fix: Patch vulnerabilities in OpenCart
6. ✅ Retest: Run again to verify patches

---

**Status:** Ready to Execute ✅  
**Last Updated:** 2026-05-16  

🚀 **Run your tests now!**
```bash
pytest test_fail_cases.py -v
```

