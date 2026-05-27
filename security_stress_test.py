"""
RED TEAM SECURITY STRESS TEST - OpenCart Critical Logic Gaps
============================================================

This module implements 20 critical security vulnerabilities (one per Use Case UC_01 to UC_20)
using Playwright for browser automation and direct API attacks.

Each test demonstrates:
- State Transition Attacks
- Parameter Tampering  
- IDOR (Insecure Direct Object References)
- Race Conditions
- Database Corruption
- Authorization Bypass
- SQL Injection

Framework: Playwright + Python + Pytest + Asyncio
Target: OpenCart (Localhost XAMPP)

Usage:
    pytest security_stress_test.py -v --tb=short
    pytest security_stress_test.py::test_uc01_database_corruption -v -s
    pytest security_stress_test.py -k "sql_injection" -v
"""

import pytest
import asyncio
import logging
import re
import time
from typing import Optional, List, Dict, Any
from playwright.async_api import Page, Browser, async_playwright, expect


# ============================================================================
# CONFIGURATION & SETUP
# ============================================================================

# Base URL for OpenCart
BASE_URL = "http://localhost/opencart_test/upload/"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Test user credentials
# TEST_USER = {
#     "email": "shin@test.com",
#     "password": "123456"
# }
TEST_USER = {
    "email": "Shin@gmail.com",
    "password": "123456"
}

ADMIN_USER = {
    "email": "admin@test.com",
    "password": "admin123"
}


# ============================================================================
# PYTEST FIXTURES
# ============================================================================

@pytest.fixture
async def browser():
    """Create and return a Playwright browser instance"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        yield browser
        await browser.close()


@pytest.fixture
async def page(browser):
    """Create and return a Playwright page instance"""
    context = await browser.new_context()
    page = await context.new_page()
    
    # Set default timeout
    page.set_default_timeout(30000)
    page.set_default_navigation_timeout(30000)
    
    yield page
    
    await page.close()
    await context.close()


@pytest.fixture
async def authenticated_page(page):
    """Return a page already logged in as test user"""
    await page.goto(f"{BASE_URL}index.php?route=account/login")
    await page.fill('input[name="email"]', TEST_USER["email"])
    await page.fill('input[name="password"]', TEST_USER["password"])
    # Chỉ click vào nút submit NẰM TRONG form login của khách cũ
    await page.click('form[action*="login"] input[type="submit"], input[value="Login"]')
    await page.wait_for_load_state('networkidle')
    
    yield page


# ============================================================================
# TEST CASE 1: UC_01 - DATABASE CORRUPTION VIA OVERSIZED INPUT
# ============================================================================

@pytest.mark.security
@pytest.mark.extreme
async def test_uc01_database_corruption(page: Page):
    """
    VULNERABILITY: Database Overflow on Registration Field
    
    LOGIC FLAW:
    The registration form lacks input length validation on client AND server.
    An attacker can send firstname field with 65,000+ characters, causing:
    - Buffer overflow in database driver
    - Memory exhaustion leading to DoS
    - Data corruption in customer table
    - Potential SQL injection if not properly escaped
    
    EXPECTED BUG:
    ❌ Server Response: 500 Internal Server Error
    ❌ Database: Customer table corrupted with oversized record
    ❌ System: Memory exhausted, DoS
    """
    
    logger.info("🔴 TEST: UC_01 - Database Overflow Attack")
    
    await page.goto(f"{BASE_URL}index.php?route=account/register")
    await page.wait_for_load_state('networkidle')
    
    # Method 1: Send massive first name via API (POST bypass)
    oversized_firstname = "A" * 65000  # 65KB of data
    
    try:
        response = await page.request.post(
            f"{BASE_URL}index.php?route=account/register",
            data={
                "firstname": oversized_firstname,
                "lastname": "Doe",
                "email": f"overflow_test_{int(time.time())}@evil.com",
                "telephone": "1234567890",
                "password": "123456",
                "confirm": "123456",
                "agree": "on"
            }
        )
        
        logger.info(f"Response Status: {response.status}")
        resp_text = await response.text()
        
        # Check for error indicators
        if response.status >= 500 or "fatal" in resp_text.lower() or "memory" in resp_text.lower():
            logger.error("🔴 DATABASE CORRUPTION CONFIRMED: Server error on oversized input")
            assert False, "System crashed with oversized input"
        
        if response.status == 200 and len(oversized_firstname) in resp_text:
            logger.error("🔴 DATABASE CORRUPTION CONFIRMED: Oversized input was accepted!")
            assert False, "Oversized input was stored in database"
            
    except Exception as e:
        logger.error(f"Request failed (may indicate DoS): {e}")


# ============================================================================
# TEST CASE 2: UC_02 - SQL INJECTION IN LOGIN AUTHENTICATION
# ============================================================================

@pytest.mark.security
@pytest.mark.extreme
async def test_uc02_sql_injection_login(page: Page):
    """
    VULNERABILITY: SQL Injection in Login Form
    
    LOGIC FLAW:
    The login mechanism queries the customer table with email/password but may not 
    use parameterized queries. Without prepared statements, SQL injection is possible:
    
    Vulnerable query:
    SELECT * FROM oc_customer 
    WHERE email = '{user_input}' AND password = '{password}'
    
    ATTACK PAYLOADS:
    - Classic: admin@test.com' OR '1'='1
    - Union: admin@test.com' UNION SELECT ...
    - Blind: admin@test.com' AND SLEEP(5)--
    
    EXPECTED BUG:
    ❌ Authentication bypassed
    ❌ Able to login without valid credentials
    ❌ Time delay indicates SLEEP() execution (blind SQLi)
    """
    
    logger.info("🔴 TEST: UC_02 - SQL Injection in Login")
    
    await page.goto(f"{BASE_URL}index.php?route=account/login")
    await page.wait_for_load_state('networkidle')
    
    # Method 1: Classic OR-based bypass
    sql_injection_email = "admin@test.com' OR '1'='1"
    
    try:
        response = await page.request.post(
            f"{BASE_URL}index.php?route=account/login",
            data={
                "email": sql_injection_email,
                "password": "anything"
            }
        )
        
        resp_text = await response.text()
        
        # Check if we bypassed authentication
        if response.status == 200 and ("My Account" in resp_text or "logout" in resp_text.lower()):
            logger.error("🔴 SQL INJECTION CONFIRMED: Bypassed login with OR condition")
            assert False, "SQL injection bypassed authentication"
        
    except Exception as e:
        logger.warning(f"SQL injection request error (may be blocked): {e}")
    
    # Method 2: Time-based blind SQL injection
    logger.info("Testing time-based blind SQL injection...")
    
    time_payload = "shin@test.com' AND (SELECT * FROM (SELECT(SLEEP(5)))a)--"
    
    try:
        start_time = time.time()
        
        response = await page.request.post(
            f"{BASE_URL}index.php?route=account/login",
            data={
                "email": time_payload,
                "password": "x"
            },
            timeout=30000
        )
        
        elapsed = time.time() - start_time
        logger.info(f"Request took {elapsed:.2f} seconds")
        
        if elapsed > 4.5:  # Account for network latency
            logger.error(f"🔴 BLIND SQL INJECTION CONFIRMED: Query took {elapsed}s (SLEEP executed)")
            assert False, f"Database delay indicates SQL execution: {elapsed}s"
            
    except Exception as e:
        logger.info(f"Time-based SQLi test (timeout may indicate success): {e}")


# ============================================================================
# TEST CASE 3: UC_03 - SESSION FIXATION AFTER LOGOUT
# ============================================================================

@pytest.mark.security
@pytest.mark.hard
async def test_uc03_session_fixation(authenticated_page: Page):
    """
    VULNERABILITY: Session Token Reuse After Logout
    
    LOGIC FLAW:
    The logout process doesn't properly invalidate the session token.
    An attacker can:
    - Reuse old session token after target logs out
    - Access protected pages (My Account)
    - Perform actions on behalf of logged-out user
    
    EXPECTED BUG:
    ❌ Old session cookie still grants access after logout
    ❌ Can access /account/account without login
    ❌ Session destruction incomplete
    """
    
    logger.info("🔴 TEST: UC_03 - Session Fixation After Logout")
    
    page = authenticated_page
    
    # Verify logged in
    content = await page.content()
    assert "My Account" in content, "Not logged in at start"
    logger.info("✓ Confirmed logged in")
    
    # Capture session cookie BEFORE logout
    cookies = await page.context.cookies()
    session_cookie = None
    
    for cookie in cookies:
        if any(name in cookie['name'].lower() for name in ['phpsessid', 'ocsessid', 'session']):
            session_cookie = cookie
            logger.info(f"✓ Captured session cookie: {cookie['name']}")
            break
    
    if not session_cookie:
        logger.warning("No session cookie found, cannot test session fixation")
        return
    
    # Click logout button
    logout_buttons = await page.locator('a:has-text("Logout"), a[href*="logout"], button:has-text("Logout")').all()
    
    if logout_buttons:
        await logout_buttons[0].click()
        await page.wait_for_load_state('networkidle')
    else:
        logger.warning("Logout button not found, attempting manual logout")
        await page.goto(f"{BASE_URL}index.php?route=account/logout")
        await page.wait_for_load_state('networkidle')
    
    # Verify logged out
    content = await page.content()
    if "My Account" in content:
        logger.warning("Still showing My Account after logout - may not be truly logged out")
    
    logger.info("✓ Logout action completed")
    
    # Create NEW PAGE/CONTEXT with the OLD session cookie
    new_context = await page.context.browser.new_context()
    new_page = await new_context.new_page()
    
    # Set the captured session cookie in new context
    await new_context.add_cookies([{
        'name': session_cookie['name'],
        'value': session_cookie['value'],
        'domain': session_cookie.get('domain', 'localhost'),
        'path': session_cookie.get('path', '/'),
    }])
    
    logger.info(f"Set old session cookie: {session_cookie['name']}")
    
    # Try to access protected resource with old session
    try:
        await new_page.goto(f"{BASE_URL}index.php?route=account/account")
        await new_page.wait_for_load_state('networkidle')
        
        new_content = await new_page.content()
        
        if "My Account" in new_content or "Personal Information" in new_content or "Email" in new_content:
            logger.error("🔴 SESSION FIXATION CONFIRMED: Can access account with old session!")
            assert False, "Session fixation vulnerability confirmed"
        else:
            logger.info("✓ Old session properly invalidated")
            
    except Exception as e:
        logger.info(f"Cannot access account with old session (expected): {e}")
    
    finally:
        await new_page.close()
        await new_context.close()


# ============================================================================
# TEST CASE 4: UC_04 - IDOR: ACCESSING DISABLED/HIDDEN PRODUCTS
# ============================================================================

@pytest.mark.security
@pytest.mark.hard
async def test_uc04_idor_hidden_products(page: Page):
    """
    VULNERABILITY: IDOR - Direct Access to Disabled/Hidden Products
    
    LOGIC FLAW:
    The product detail endpoint doesn't check if a product is:
    - Disabled in admin panel
    - Out of stock
    - Scheduled for future release
    - Draft/unpublished
    
    An attacker can directly access:
    /product/product?product_id=999
    
    Even if disabled, the backend still returns full product data.
    
    EXPECTED BUG:
    ❌ GET /product?product_id=999 returns 200 OK
    ❌ Full product data visible (price, description, etc.)
    ❌ No authorization check on product status
    """
    
    logger.info("🔴 TEST: UC_04 - IDOR: Disabled Products")
    
    # First, get list of products that might be hidden
    await page.goto(f"{BASE_URL}")
    await page.wait_for_load_state('networkidle')
    
    # Try to enumerate product IDs and find disabled ones
    disabled_products_found = []
    
    for product_id in range(1, 50):
        try:
            response = await page.request.get(
                f"{BASE_URL}index.php?route=product/product&product_id={product_id}",
                timeout=5000
            )
            
            if response.status == 200:
                content = await response.text()
                
                # Check if product data is returned
                if "product_id" in content or "price" in content or "Add to Cart" in content:
                    logger.info(f"✓ Product {product_id} accessible")
                    
                    # Check if it's supposedly disabled
                    if any(disabled_marker in content for disabled_marker in 
                           ["disabled", "unavailable", "out of stock", "no longer available"]):
                        logger.error(f"🔴 IDOR CONFIRMED: Disabled product {product_id} accessible!")
                        disabled_products_found.append(product_id)
                        
        except Exception as e:
            logger.debug(f"Product {product_id} error: {e}")
            continue
    
    if disabled_products_found:
        logger.error(f"🔴 Found {len(disabled_products_found)} disabled products accessible: {disabled_products_found}")
        assert False, f"IDOR vulnerability - disabled products accessible"
    else:
        logger.info("✓ Disabled products properly protected")


# ============================================================================
# TEST CASE 5: UC_05 - SQL INJECTION IN SEARCH
# ============================================================================

@pytest.mark.security
@pytest.mark.extreme
async def test_uc05_sql_injection_search(page: Page):
    """
    VULNERABILITY: SQL Injection in Product Search
    
    LOGIC FLAW:
    The search function accepts user input without parameterization:
    SELECT * FROM oc_product WHERE name LIKE '%{search_term}%'
    
    An attacker can inject SQL to:
    - Extract customer data
    - Modify product prices
    - Delete products
    - Execute arbitrary SQL
    
    EXPECTED BUG:
    ❌ Search returns injected SQL output
    ❌ Database information disclosed via errors
    ❌ Time delay from SLEEP() query
    """
    
    logger.info("🔴 TEST: UC_05 - SQL Injection in Search")
    
    await page.goto(f"{BASE_URL}")
    await page.wait_for_load_state('networkidle')
    
    # Method 1: Union-based injection
    search_payload = "test' UNION SELECT customer_id, email, password, '1' FROM oc_customer LIMIT 1--"
    
    try:
        response = await page.request.get(
            f"{BASE_URL}index.php?route=product/search&search={search_payload}"
        )
        
        resp_text = await response.text()
        
        # Check if customer data leaked
        if any(email_pattern in resp_text for email_pattern in ["@test.com", "shin@", "admin@"]):
            logger.error("🔴 SQL INJECTION CONFIRMED: Customer data leaked via search!")
            assert False, "Search SQL injection allows data exfiltration"
            
    except Exception as e:
        logger.debug(f"Search request error: {e}")
    
    # Method 2: Time-based blind SQL injection
    logger.info("Testing time-based blind SQL injection in search...")
    
    time_payload = "test' AND (SELECT * FROM (SELECT(SLEEP(3)))a)--"
    
    try:
        start = time.time()
        response = await page.request.get(
            f"{BASE_URL}index.php?route=product/search&search={time_payload}",
            timeout=30000
        )
        elapsed = time.time() - start
        
        logger.info(f"Search request took {elapsed:.2f}s")
        
        if elapsed > 2.5:
            logger.error(f" BLIND SQL INJECTION CONFIRMED: Query delayed by {elapsed:.2f}s")
            assert False, "Time-based SQL injection detected"
            
    except asyncio.TimeoutError:
        logger.error(" BLIND SQL INJECTION LIKELY: Request timed out (SLEEP executed)")
        assert False, "SQL injection caused timeout"
    except Exception as e:
        logger.debug(f"Time-based SQLi result: {e}")


# ============================================================================
# TEST CASE 6: UC_06 - PARAMETER TAMPERING: NEGATIVE PRICE FILTERING
# ============================================================================

@pytest.mark.security
@pytest.mark.hard
async def test_uc06_negative_price_filter(page: Page):
    """
    VULNERABILITY: Negative Price Range Filter
    
    LOGIC FLAW:
    The product filter accepts price parameters with NO validation:
    - price_from = -1000 (negative!)
    - price_to = 0
    
    This can:
    - Return all products (invalid filter)
    - Confuse pricing logic
    - Expose inventory of products supposed to be hidden
    
    EXPECTED BUG:
    ❌ GET ?price_from=-1000&price_to=0 returns 200 OK
    ❌ Results include products not in price range
    ❌ No validation error
    """
    
    logger.info("🔴 TEST: UC_06 - Negative Price Filter")
    
    # Method 1: Direct URL parameter tampering
    try:
        response = await page.request.get(
            f"{BASE_URL}index.php?route=product/category&price_from=-1000&price_to=0"
        )
        
        if response.status == 200:
            content = await response.text()
            
            if "product" in content.lower() and "error" not in content.lower():
                logger.error("🔴 NEGATIVE PRICE FILTER ACCEPTED: No validation!")
                assert False, "Negative price filter was accepted"
        
    except Exception as e:
        logger.debug(f"Negative price filter request: {e}")
    
    # Method 2: Price filter via POST
    try:
        response = await page.request.post(
            f"{BASE_URL}index.php?route=product/category",
            data={
                "price": "-1000,0"
            }
        )
        
        if response.status == 200 and "error" not in await response.text():
            logger.error("🔴 POST: Negative price range accepted!")
            assert False, "Server accepted negative price in POST"
            
    except Exception as e:
        logger.debug(f"POST price filter: {e}")
    
    # Method 3: Very small decimal values
    try:
        response = await page.request.get(
            f"{BASE_URL}index.php?route=product/category&price_from=-999999.99&price_to=0.01"
        )
        
        if response.status == 200:
            logger.warning("Decimal price parameters accepted (may be valid)")
            
    except Exception as e:
        logger.info(f"Decimal price test: {e}")


# ============================================================================
# TEST CASE 7: UC_07 - IDOR: ACCESSING DELETED/DRAFT PRODUCTS
# ============================================================================

@pytest.mark.security
@pytest.mark.hard
async def test_uc07_idor_draft_products(page: Page):
    """
    VULNERABILITY: IDOR - Direct Access to Draft/Deleted Products
    
    LOGIC FLAW:
    There's no check that products are published/active before returning data.
    An attacker can:
    - Enumerate product IDs (1, 2, 3... 9999)
    - Access any product regardless of status
    - View draft products
    - See pricing of products not yet released
    
    EXPECTED BUG:
    ❌ Can access /product/product?product_id=9999
    ❌ Returns data for non-existent/deleted products
    ❌ Status check missing (should be 404)
    """
    
    logger.info("🔴 TEST: UC_07 - IDOR: Draft Products")
    
    # Try high product IDs that might be draft/deleted
    draft_products = []
    
    for product_id in [999, 1000, 1001, 9999, 99999]:
        try:
            response = await page.request.get(
                f"{BASE_URL}index.php?route=product/product&product_id={product_id}",
                timeout=5000
            )
            
            if response.status == 200:  # Should be 404!
                content = await response.text()
                
                if any(marker in content for marker in ["price", "product_id", "Add to Cart"]):
                    logger.warning(f"Product {product_id} returned 200 (may be IDOR)")
                    draft_products.append(product_id)
                    
            elif response.status == 404:
                logger.info(f"✓ Product {product_id} properly 404'd")
                
        except Exception as e:
            logger.debug(f"Product {product_id}: {e}")
    
    if draft_products:
        logger.error(f"🔴 IDOR: Can access non-existent products: {draft_products}")
        assert False, "IDOR vulnerability on draft products"
    else:
        logger.info("✓ Draft products properly protected")


# ============================================================================
# TEST CASE 8: UC_08 - NEGATIVE QUANTITY IN CART
# ============================================================================

@pytest.mark.security
@pytest.mark.hard
async def test_uc08_negative_quantity_cart(authenticated_page: Page):
    """
    VULNERABILITY: Negative Quantity in Shopping Cart
    
    LOGIC FLAW:
    Cart quantity validation only checks if quantity > 0 on frontend.
    A direct API call with negative quantity could:
    - Add item with -5 quantity
    - Result in negative cost (-$500 instead of +$500)
    - Create orders with negative prices (customer gets paid!)
    
    EXPECTED BUG:
    ❌ POST { "product_id": 43, "quantity": "-5" } returns 200
    ❌ Cart shows -5 items and -$500 total
    ❌ No backend validation
    """
    
    logger.info("🔴 TEST: UC_08 - Negative Quantity in Cart")
    
    page = authenticated_page
    product_id = 43  # Sample product
    
    # Method 1: Direct API POST with negative quantity
    try:
        response = await page.request.post(
            f"{BASE_URL}index.php?route=checkout/cart/add",
            data={
                "product_id": str(product_id),
                "quantity": "-5"  # NEGATIVE!
            }
        )
        
        resp_text = await response.text()
        
        if response.status == 200 and "added" in resp_text.lower():
            logger.error("🔴 NEGATIVE QUANTITY ACCEPTED: Item added with -5 quantity!")
            assert False, "Negative quantity was accepted"
        
    except Exception as e:
        logger.debug(f"Add negative quantity: {e}")
    
    # Method 2: Verify cart contents
    try:
        await page.goto(f"{BASE_URL}index.php?route=checkout/cart")
        await page.wait_for_load_state('networkidle')
        
        content = await page.content()
        
        # Check for negative quantities visible
        if re.search(r'Qty[:\s]*-\d+', content) or "Qty: -" in content:
            logger.error("🔴 NEGATIVE QUANTITY DETECTED IN CART!")
            assert False, "Negative quantity visible in cart"
        
    except Exception as e:
        logger.debug(f"Cart verification: {e}")
    
    # Method 3: Test various negative values
    for neg_qty in ["-1", "-0.5", "-999"]:
        try:
            response = await page.request.post(
                f"{BASE_URL}index.php?route=checkout/cart/add",
                data={
                    "product_id": str(product_id),
                    "quantity": neg_qty
                }
            )
            
            if response.status == 200:
                logger.warning(f"Negative quantity {neg_qty} accepted (may be stored)")
                
        except Exception as e:
            logger.debug(f"Negative qty {neg_qty}: {e}")


# ============================================================================
# TEST CASE 9: UC_09 - RACE CONDITION: CART ITEM REMOVAL
# ============================================================================

@pytest.mark.security
@pytest.mark.hard
async def test_uc09_race_condition_cart_removal(authenticated_page: Page):
    """
    VULNERABILITY: Race Condition in Cart Item Removal
    
    LOGIC FLAW:
    No atomic transaction protection when removing items from cart.
    Two concurrent DELETE requests can:
    - Both check if item exists (race condition)
    - Both delete the same item
    - Leave cart in inconsistent state
    - Duplicate inventory restoration
    
    EXPECTED BUG:
    ❌ Multiple concurrent DELETE succeed
    ❌ Item removed twice
    ❌ Inventory count wrong
    """

    logger.info("🔴 TEST: UC_09 - Race Condition: Cart Removal")
    
    page = authenticated_page
    # Thêm dòng này vào đầu hàm test_uc09 để làm sạch giỏ hàng trước khi bắt đầu
    await page.goto(f"{BASE_URL}index.php?route=checkout/cart")
    content = await page.content()
    # Nếu thấy nút xóa (remove), click liên tục để dọn sạch giỏ
    while "route=checkout/cart/remove" in content:
        await page.click('button[onclick*="cart.remove"]')
        await page.wait_for_timeout(1000)
        content = await page.content()
    # Add a product first
    product_id = 40
    
    response = await page.request.post(
        f"{BASE_URL}index.php?route=checkout/cart/add",
        data={
            "product_id": str(product_id),
            "quantity": "1"
        }
    )
    
    logger.info(f"Added product {product_id} to cart")
    
    # Get cart item key/ID
    await page.goto(f"{BASE_URL}index.php?route=checkout/cart")
    await page.wait_for_load_state('networkidle')
    
    content = await page.content()
    
    # Extract cart key if possible
    key_match = re.search(r'key=(\d+)', content)
    cart_key = key_match.group(1) if key_match else str(product_id)
    
    logger.info(f"Cart key: {cart_key}")
    
    # Send 5 concurrent DELETE requests
    logger.info("Sending 5 concurrent remove requests...")
    
    remove_tasks = []
    
    for i in range(5):
        task = page.request.post(
            f"{BASE_URL}index.php?route=checkout/cart/remove&key={cart_key}",
            data={"remove": "1"}
        )
        remove_tasks.append(task)
    
    # Execute concurrently
        # Execute concurrently
        # Chỉ bọc duy nhất lệnh bắn request vào try-except để bắt lỗi mạng nếu có
    try:
        responses = await asyncio.gather(*remove_tasks, return_exceptions=True)
    except Exception as e:
        logger.debug(f"Race condition network test error: {e}")
        responses = []

        # Tính toán số lượng request thành công
    success_count = sum(1 for r in responses
                        if isinstance(r, object) and hasattr(r, 'status') and r.status == 200)

    logger.info(f"Concurrent removes completed: {success_count} succeeded")

        # ĐƯA KHỐI NÀY RA NGOÀI: Để AssertionError bắn thẳng ra ngoài cho Pytest bắt được
    if success_count > 1:
        logger.error(f"🔴 RACE CONDITION CONFIRMED: {success_count} concurrent deletes succeeded!")
        assert False, f"Race condition - multiple concurrent deletes succeeded ({success_count} requests)"

    logger.info("✓ Cart removal properly protected against race conditions")

# ============================================================================
# TEST CASE 10: UC_10 - QUANTITY EXCEEDS STOCK
# ============================================================================

@pytest.mark.security
@pytest.mark.hard
async def test_uc10_quantity_exceed_stock(authenticated_page: Page):
    """
    VULNERABILITY: Cart Quantity Exceeds Available Stock
    
    LOGIC FLAW:
    Stock check only happens on form submission, not on API endpoints.
    An attacker can:
    - Set quantity to 999999 (way above stock)
    - Create order for items not in stock
    - Cause inventory issues
    
    EXPECTED BUG:
    ❌ POST { "quantity": "9999999" } accepted
    ❌ Order created with unavailable quantity
    ❌ No server-side inventory check
    """
    
    logger.info("🔴 TEST: UC_10 - Quantity Exceeds Stock")
    
    page = authenticated_page
    product_id = 40
    
    # Method 1: Direct API call with excessive quantity
    try:
        response = await page.request.post(
            f"{BASE_URL}index.php?route=checkout/cart/add",
            data={
                "product_id": str(product_id),
                "quantity": "9999999"  # Way over stock
            }
        )
        
        resp_text = await response.text()
        
        if response.status == 200 and "error" not in resp_text.lower():
            logger.error("🔴 EXCESSIVE QUANTITY ACCEPTED: No stock validation!")
            assert False, "Quantity exceeds stock but accepted"
        
    except Exception as e:
        logger.debug(f"Excessive quantity test: {e}")
    
    # Method 2: Try cart update with excessive quantity
    try:
        await page.goto(f"{BASE_URL}index.php?route=checkout/cart")
        await page.wait_for_load_state('networkidle')
        
        # Find quantity input and modify
        qty_inputs = await page.locator('input[name*="quantity"]').all()
        
        if qty_inputs:
            # Use page.evaluate to bypass client validation
            await page.evaluate("""
                document.querySelectorAll('input[name*="quantity"]').forEach(input => {
                    input.value = '9999999';
                    input.dispatchEvent(new Event('change'));
                });
            """)
            
            # Click update button
            update_buttons = await page.locator('button:has-text("Update")').all()
            
            if update_buttons:
                await update_buttons[0].click()
                await page.wait_for_load_state('networkidle')
                
                content = await page.content()
                
                if "9999999" in content:
                    logger.error("🔴 EXCESSIVE QUANTITY IN CART: Quantity accepted and stored!")
                    assert False, "Excessive quantity stored in cart"
        
    except Exception as e:
        logger.debug(f"Cart quantity update: {e}")


# ============================================================================
# TEST CASE 11: UC_11 - IDOR: OTHER CUSTOMERS' SHIPPING ADDRESSES
# ============================================================================

@pytest.mark.security
@pytest.mark.extreme
async def test_uc11_idor_shipping_addresses(authenticated_page: Page):
    """
    VULNERABILITY: IDOR - Access Other Customers' Addresses
    """
    logger.info("🔴 TEST: UC_11 - IDOR: Shipping Addresses")
    page = authenticated_page

    unauthorized_addresses = []

    # Rà quét các address_id từ 1 đến 50
    for address_id in range(1, 50):
        try:
            response = await page.request.get(
                f"{BASE_URL}index.php?route=account/address/edit&address_id={address_id}"
            )

            if response.status == 200:
                content = await response.text()

                # CHUẨN NGHIỆP VỤ: Nếu thực sự vào được trang EDIT của id đó,
                # URL hoặc nội dung phải chứa form chỉnh sửa chứ không phải trang danh sách bị văng về.
                # Kiểm tra các thuộc tính input đặc trưng của form sửa địa chỉ OpenCart
                if 'name="address_1"' in content and 'action Singapore' not in content:

                    # Để chắc chắn đây là địa chỉ của người khác chứ không phải của chính mình,
                    # Ta kiểm tra xem tiêu đề h2/bọc text có phải là "Edit Address" hay không
                    if "text-danger" not in content.lower():
                        logger.warning(f"⚠️ Phát hiện có thể truy cập form Address ID: {address_id}")
                        unauthorized_addresses.append(address_id)

        except Exception as e:
            logger.debug(f"Address {address_id}: {e}")

    # Chốt hạ kết quả kiểm thử
    if unauthorized_addresses:
        logger.error(
            f"🔴 IDOR CONFIRMED: Can access {len(unauthorized_addresses)} other addresses: {unauthorized_addresses}")

        # Tự động chụp ảnh màn hình trang lỗi làm bằng chứng đồ án
        import os
        os.makedirs("failures", exist_ok=True)
        await page.goto(f"{BASE_URL}index.php?route=account/address/edit&address_id={unauthorized_addresses[0]}")
        await page.screenshot(path="failures/IDOR_Address_Book_Confirmed.png")

        assert False, f"IDOR vulnerability on address book! Accessible IDs: {unauthorized_addresses}"
    else:
        logger.info("✓ Addresses properly protected (Redirected or Blocked successfully)")

# ============================================================================
# TEST CASE 12: UC_12 - SHIPPING COST MANIPULATION
# ============================================================================

@pytest.mark.security
@pytest.mark.extreme
async def test_uc12_shipping_cost_manipulation(authenticated_page: Page):
    """
    VULNERABILITY: Shipping Cost Manipulation (Parameter Tampering)
    """
    logger.info("🔴 TEST: UC_12 - Shipping Cost Manipulation")
    page = authenticated_page

    # BƯỚC 1: Phải thêm sản phẩm vào giỏ hàng thì mới vào được luồng Checkout
    logger.info("Thêm sản phẩm mồi vào giỏ hàng...")
    await page.request.post(
        f"{BASE_URL}index.php?route=checkout/cart/add",
        data={"product_id": "40", "quantity": "1"}
    )

    # BƯỚC 2: Điều hướng vào trang Checkout
    await page.goto(f"{BASE_URL}index.php?route=checkout/checkout")
    await page.wait_for_load_state('networkidle')

    # BƯỚC 3: Gửi request tấn công thay đổi phí Ship
    logger.info("Gửi request POST chèn phí vận chuyển âm (-999)...")

    # Đưa lệnh bắn request vào try-except để tránh sập luồng mạng
    try:
        response = await page.request.post(
            f"{BASE_URL}index.php?route=checkout/shipping_method/save",  # Endpoint chuẩn của OpenCart 3
            data={
                "shipping_method": "flat.flat",
                "shipping_cost": "-999"  # Payload tấn công giả định
            }
        )
        resp_text = await response.text()
        status_code = response.status
    except Exception as e:
        logger.error(f"Lỗi kết nối API: {e}")
        status_code = 500
        resp_text = ""
    logger.info(f"👉 SERVER RESP TEXT: {resp_text}")
    logger.info(f"Server response status: {status_code}")

    # BƯỚC 4: ĐƯA KHỐI KIỂM TRA RA NGOÀI (Tuyệt đối không bọc trong try-except)
    logger.info(f"Server response status: {status_code}")

    # Nếu hệ thống chấp nhận phí âm và trả về trạng thái không có lỗi
    if status_code == 200 and "error" not in resp_text.lower() and "warning" not in resp_text.lower():
        # Chúng ta cần kiểm tra lại giao diện xem tiền có bị trừ đi không
        await page.goto(f"{BASE_URL}index.php?route=checkout/cart")
        cart_content = await page.content()

        if "-$" in cart_content or "minus" in cart_content.lower():
            logger.error("🔴 CRITICAL BUG: Hệ thống chấp nhận phí vận chuyển âm và trừ vào tổng tiền!")
            assert False, "Vulnerability Confirmed: Negative shipping cost accepted and manipulated order total!"

    logger.info("✓ Hệ thống an toàn: Không cho phép thao túng chi phí vận chuyển từ Client.")
# ============================================================================
# TEST CASE 13: UC_13 - RACE CONDITION: COUPON DUPLICATION
# ============================================================================
@pytest.mark.security
@pytest.mark.hard
async def test_uc13_coupon_race_condition(authenticated_page: Page):
    """
    VULNERABILITY: Race Condition - Multiple Coupon Application
    """
    logger.info("🔴 TEST: UC_13 - Race Condition: Coupon Duplication")
    page = authenticated_page

    # BƯỚC 1: Tự động đi tới trang sản phẩm và thêm vào giỏ hàng (Bắt buộc phải có sản phẩm)
    logger.info("Điều hướng tới sản phẩm và thêm vào giỏ hàng...")
    await page.goto(f"{BASE_URL}index.php?route=product/product&product_id=40")  # ID 40 thường là iPhone
    await page.click("#button-cart")
    await page.wait_for_timeout(1500)  # Đợi 1.5 giây để giỏ hàng xử lý xong tầng Session

    coupon_code = "DISCOUNT10"  # Mã giảm giá giả định của bạn

    # BƯỚC 2: Gom 10 requests tấn công Race Condition dưới nền
    coupon_tasks = []
    for i in range(10):
        task = page.request.post(
            f"{BASE_URL}index.php?route=extension/total/coupon/coupon",
            data={"coupon": coupon_code}
        )
        coupon_tasks.append(task)

    logger.info("Sending 10 concurrent coupon requests...")
    responses = await asyncio.gather(*coupon_tasks, return_exceptions=True)

    # BƯỚC 3: Giải phóng màn hình treo - Chuyển hướng trình duyệt đến Giỏ hàng để xem kết quả
    logger.info("Chuyển hướng trình duyệt đến trang Giỏ hàng để kiểm tra...")
    await page.goto(f"{BASE_URL}index.php?route=checkout/cart")
    await page.wait_for_load_state('networkidle')

    # Kiểm tra log phản hồi
    success_count = sum(1 for r in responses
                        if isinstance(r, object) and hasattr(r, 'status') and r.status == 200)
    logger.info(f"Coupon applications: {success_count} requests completed.")

    # Chụp lại ảnh giỏ hàng sau khi bị tấn công đồng thời
    await page.screenshot(path="failures/coupon_race_condition_cart.png")


# ============================================================================
# TEST CASE 14: UC_14 - STATE TRANSITION: CONFIRM ORDER WITHOUT PAYMENT
# ============================================================================

@pytest.mark.security
@pytest.mark.extreme
async def test_uc14_state_transition_skip_payment(authenticated_page: Page):
    """
    VULNERABILITY: State Transition Attack - Skip Payment Step
    
    LOGIC FLAW:
    The checkout flow should enforce:
    1. Shipping Address → 2. Shipping Method → 3. Payment Method → 4. Confirm
    
    But if step 3 validation is missing, attacker can:
    - Jump directly to /checkout/confirm (skip payment selection)
    - Place order with NO payment method
    - Order created with "pending payment" status forever
    
    EXPECTED BUG:
    ❌ Can access /checkout/confirm without payment
    ❌ Order placed with no payment_method in session
    ❌ Order status: "pending payment" forever
    """
    
    logger.info("🔴 TEST: UC_14 - State Transition: Skip Payment")
    
    page = authenticated_page
    
    # Method 1: Try to jump directly to order confirmation
    try:
        response = await page.request.get(
            f"{BASE_URL}index.php?route=checkout/confirm"
        )
        
        if response.status == 200:
            content = await response.text()
            
            if "Confirm Order" in content:
                logger.warning("Can access confirm page directly (may be XSRF or state bypass)")
                
                # Try to submit without payment
                # This would need more session state manipulation
                
    except Exception as e:
        logger.debug(f"Direct confirm access: {e}")
    
    # Method 2: Try to access order history and see if order was placed without payment
    try:
        await page.goto(f"{BASE_URL}index.php?route=account/order")
        await page.wait_for_load_state('networkidle')
        
        content = await page.content()
        
        # Look for orders with "pending payment" status
        if "pending" in content.lower() or "awaiting payment" in content.lower():
            logger.warning("Found orders with pending payment status (vulnerability indicator)")
        
    except Exception as e:
        logger.debug(f"Order check: {e}")


# ============================================================================
# TEST CASE 15: UC_15 - IDOR: ACCESSING OTHER CUSTOMERS' ORDERS
# ============================================================================

@pytest.mark.security
@pytest.mark.extreme
async def test_uc15_idor_orders(page: Page):
    """
    VULNERABILITY: IDOR - Access Other Customers' Order Details
    
    LOGIC FLAW:
    The spec says: "Xác thực đơn hàng thuộc khách hàng hiện tại"
    But this might only be checked on frontend, not backend.
    
    An attacker can:
    - Enumerate order IDs: /account/order/info?order_id=1, 2, 3...
    - View any customer's order details
    - See shipping addresses, payment info, order total
    
    EXPECTED BUG:
    ❌ GET /account/order/info?order_id=1 returns 200 (not owned by user)
    ❌ Can see other customer emails, addresses
    ❌ No authorization check on order_id parameter
    """
    
    logger.info("🔴 TEST: UC_15 - IDOR: Order Details")
    
    # First, login as customer
    await page.goto(f"{BASE_URL}index.php?route=account/login")
    await page.fill('input[name="email"]', TEST_USER["email"])
    await page.fill('input[name="password"]', TEST_USER["password"])
    # Cho phép click cả thẻ input hoặc button có type submit, hoặc class btn-primary
    await page.click('input[type="submit"], button[type="submit"], .btn-primary')
    await page.wait_for_load_state('networkidle')
    
    # Enumerate order IDs
    exposed_orders = {}
    
    for order_id in range(1, 30):
        try:
            response = await page.request.get(
                f"{BASE_URL}index.php?route=account/order/info&order_id={order_id}"
            )
            
            if response.status == 200:
                content = await response.text()
                
                # Extract customer email to see if it's different from current user
                email_match = re.search(r'Email[:\s]+([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+)', content)
                
                if email_match:
                    email = email_match.group(1)
                    
                    if email != TEST_USER["email"]:
                        logger.error(f"🔴 IDOR CONFIRMED: Can see order {order_id} from {email}")
                        exposed_orders[order_id] = email
                    
        except Exception as e:
            logger.debug(f"Order {order_id}: {e}")
    
    if exposed_orders:
        logger.error(f"🔴 Can access {len(exposed_orders)} other customers' orders")
        assert False, f"IDOR vulnerability on orders: {exposed_orders}"
    else:
        logger.info("✓ Orders properly protected")


# ============================================================================
# TEST CASE 16: UC_16 - EMAIL TAKEOVER VIA PARAMETER TAMPERING
# ============================================================================

@pytest.mark.security
@pytest.mark.extreme
async def test_uc16_email_takeover(authenticated_page: Page):
    """
    VULNERABILITY: Email Takeover via Profile Update
    
    LOGIC FLAW:
    When updating profile, the system checks "if email exists" but might not check
    "if trying to change to someone else's email".
    
    An attacker can:
    - Try to change email to another user's email
    - If only duplicate check exists, might create issues
    - Or might successfully change to another user's email (IDOR)
    
    EXPECTED BUG:
    ❌ POST { email: "shin@test.com" } (someone else's) returns 200
    ❌ Email successfully changed to existing user's email
    ❌ Attacker can now login as that user
    """
    
    logger.info("🔴 TEST: UC_16 - Email Takeover")
    
    page = authenticated_page
    
    # Get current email
    await page.goto(f"{BASE_URL}index.php?route=account/edit")
    await page.wait_for_load_state('networkidle')
    
    current_email = TEST_USER["email"]
    
    # Try to change to another existing email
    other_emails = [
        "admin@test.com",
        "customer2@test.com",
        "shin@test.com"  # Even if it's our own, test the logic
    ]
    
    for target_email in other_emails:
        if target_email == current_email:
            continue
        
        try:
            response = await page.request.post(
                f"{BASE_URL}index.php?route=account/edit",
                data={
                    "firstname": "Attacker",
                    "lastname": "Hacker",
                    "email": target_email,
                    "telephone": "1234567890"
                }
            )
            
            resp_text = await response.text()
            
            if response.status == 200 and "error" not in resp_text.lower():
                logger.error(f"🔴 EMAIL TAKEOVER: Changed to {target_email} without error!")
                assert False, f"Successfully changed email to {target_email}"
            elif "already" in resp_text.lower() or "exists" in resp_text.lower():
                logger.info(f"✓ Email {target_email} properly rejected as duplicate")
            
        except Exception as e:
            logger.debug(f"Email change to {target_email}: {e}")


# ============================================================================
# TEST CASE 17: UC_17 - AUTHORIZATION BYPASS (CUSTOMER TO ADMIN)
# ============================================================================

@pytest.mark.security
@pytest.mark.extreme
async def test_uc17_admin_authorization_bypass(authenticated_page: Page):
    """
    VULNERABILITY: Authorization Bypass - Customer Accessing Admin
    """
    logger.info("🔴 TEST: UC_17 - Admin Authorization Bypass")
    page = authenticated_page

    # Try to access various admin paths
    admin_paths = [
        "/admin/",
        "/admin/index.php",
        "/administrator/",
        "/index.php?route=catalog/product",
        "/index.php?route=sale/order"
    ]

    bypassed_paths = []
    for path in admin_paths:
        try:
            response = await page.request.get(f"{BASE_URL}{path}")
            if response.status == 200:
                content = await response.text()
                # Kiểm tra dấu hiệu giao diện Admin lộ diện
                if any(admin_marker in content for admin_marker in
                       ["Dashboard", "Products", "Orders", "System", "Settings"]):
                    logger.error(f"🔴 AUTHORIZATION BYPASS: Can access {path} as customer!")
                    bypassed_paths.append(path)
        except Exception as e:
            logger.debug(f"Admin path {path} network test: {e}")

    # ĐƯA LỆNH ASSERT RA NGOÀI KHỐI TRY-EXCEPT ĐỂ CHỐT BUG ĐƯỜNG DẪN
    if bypassed_paths:
        assert False, f"IDOR Vulnerability Confirmed: Customer accessing admin paths: {bypassed_paths}"

    # Thử gọi API tạo sản phẩm trái phép dưới quyền khách hàng
    product_created = False
    try:
        response = await page.request.post(
            f"{BASE_URL}index.php?route=catalog/product/add",
            data={
                "name[0]": "Hacked Product",
                "price": "0.01",
                "status": "1"
            }
        )
        if response.status == 200 and "error" not in await response.text():
            logger.error("🔴 PRODUCT CREATION: Customer can create products!")
            product_created = True
    except Exception as e:
        logger.debug(f"Product creation attempt network error: {e}")

    # ĐƯA LỆNH ASSERT RA NGOÀI ĐỂ CHỐT BUG TẠO SẢN PHẨM
    if product_created:
        assert False, "Vulnerability Confirmed: Customer created product without admin role"

    logger.info("✓ Admin authorization properly protected against customer escalation")


# ============================================================================
# TEST CASE 18: UC_18 - CUSTOMER MODIFYING ORDER STATUS
# ============================================================================

@pytest.mark.security
@pytest.mark.extreme
async def test_uc18_order_status_modification(page: Page):
    """
    VULNERABILITY: Customer Modifying Order Status
    """
    logger.info("🔴 TEST: UC_18 - Order Status Modification")

    # Đăng nhập tài khoản kiểm thử
    await page.goto(f"{BASE_URL}index.php?route=account/login")
    await page.fill('input[name="email"]', TEST_USER["email"])
    await page.fill('input[name="password"]', TEST_USER["password"])

    # ĐÃ SỬA: Thay thế 'button' thành 'input' để triệt hạ lỗi treo máy TargetClosedError
    await page.click('input[type="submit"]')
    await page.wait_for_load_state('networkidle')

    # Di chuyển tới trang lịch sử đơn hàng
    await page.goto(f"{BASE_URL}index.php?route=account/order")
    await page.wait_for_load_state('networkidle')

    content = await page.content()
    order_match = re.search(r'Order[:\s]+#?(\d+)', content)

    if not order_match:
        logger.warning("⚠️ Không tìm thấy đơn hàng nào có sẵn của tài khoản này để thực hiện test!")
        return

    order_id = order_match.group(1)
    logger.info(f"Found order: {order_id}")

    status_manipulated = False
    try:
        response = await page.request.post(
            f"{BASE_URL}index.php?route=sale/order/edit&order_id={order_id}",
            data={
                "order_status_id": "5",  # Trạng thái Complete
                "notify": "0"
            }
        )
        if response.status == 200:
            logger.error(f"🔴 CUSTOMER CAN UPDATE ORDER STATUS for order {order_id}!")
            status_manipulated = True
    except Exception as e:
        logger.debug(f"Order status modification network error: {e}")

    # ĐƯA LỆNH ASSERT RA NGOÀI KHỐI TRY-EXCEPT ĐỂ CHỐT BUG ĐỔI TRẠNG THÁI ĐƠN HÀNG
    if status_manipulated:
        assert False, f"Vulnerability Confirmed: Customer modified order status for order {order_id}"

    logger.info("✓ Order status updates properly protected against customer tampering")


# ============================================================================
# TEST CASE 19: UC_19 - EXCHANGE RATE MANIPULATION
# ============================================================================

@pytest.mark.security
@pytest.mark.hard
async def test_uc19_exchange_rate_manipulation(page: Page):
    """
    VULNERABILITY: Exchange Rate Manipulation
    """
    logger.info("🔴 TEST: UC_19 - Exchange Rate Manipulation")

    zero_rate_accepted = False
    negative_rate_accepted = False

    # 1. Thử nghiệm ép tỷ giá hệ thống về bằng 0
    try:
        response = await page.request.post(
            f"{BASE_URL}index.php?route=localisation/currency/edit&currency_id=1",
            data={"value": "0"}
        )
        if response.status == 200 and "error" not in await response.text():
            logger.error("🔴 ZERO EXCHANGE RATE ACCEPTED!")
            zero_rate_accepted = True
    except Exception as e:
        logger.debug(f"Zero exchange rate network error: {e}")

    # 2. Thử nghiệm ép tỷ giá hệ thống xuống số âm
    try:
        response = await page.request.post(
            f"{BASE_URL}index.php?route=localisation/currency/edit&currency_id=1",
            data={"value": "-1.5"}
        )
        if response.status == 200 and "error" not in await response.text():
            logger.error("🔴 NEGATIVE EXCHANGE RATE ACCEPTED!")
            negative_rate_accepted = True
    except Exception as e:
        logger.debug(f"Negative exchange rate network error: {e}")

    # ĐƯA TOÀN BỘ KHỐI CHỐT LỖI RA NGOÀI ĐỂ PYTEST KHÔNG BỊ BẮT QUẢ TANG "FALSE PASS"
    if zero_rate_accepted:
        assert False, "Vulnerability Confirmed: Zero exchange rate was accepted by backend!"
    if negative_rate_accepted:
        assert False, "Vulnerability Confirmed: Negative exchange rate was accepted by backend!"

    logger.info("✓ Currency exchange rates properly protected against manipulation")


# ============================================================================
# TEST CASE 20: UC_20 - CUSTOMER GROUP PRIVILEGE ESCALATION
# ============================================================================

@pytest.mark.security
@pytest.mark.extreme
async def test_uc20_customer_group_escalation(authenticated_page: Page):
    """
    VULNERABILITY: IDOR - Customer Assigning Self to High-Discount Group
    """
    logger.info("🔴 TEST: UC_20 - Customer Group Escalation")
    page = authenticated_page

    # Trích xuất mã ID khách hàng hiện tại
    await page.goto(f"{BASE_URL}index.php?route=account/account")
    await page.wait_for_load_state('networkidle')

    content = await page.content()
    customer_id_match = re.search(r'customer[_-]?id["\']?\s*:\s*["\']?(\d+)', content)
    customer_id = customer_id_match.group(1) if customer_id_match else "1"
    logger.info(f"Customer ID: {customer_id}")

    api_escalation_accepted = False
    profile_form_accepted = False

    # 1. Thử thay đổi nhóm thành VIP qua Endpoint API
    try:
        response = await page.request.post(
            f"{BASE_URL}api/customer/{customer_id}/group",
            data={"group_id": "2"}  # Mã nhóm VIP chiết khấu cao
        )
        if response.status == 200:
            logger.error(f"🔴 CUSTOMER GROUP ESCALATION: Changed to VIP group!")
            api_escalation_accepted = True
    except Exception as e:
        logger.debug(f"Group change via API network error: {e}")

    # 2. Thử chèn trường dữ liệu nhóm VIP vào Form chỉnh sửa thông tin cá nhân công khai
    try:
        response = await page.request.post(
            f"{BASE_URL}index.php?route=account/edit",
            data={
                "customer_group_id": "2",
                "firstname": "John",
                "lastname": "Doe",
                "email": TEST_USER["email"]
            }
        )
        if response.status == 200 and "error" not in await response.text():
            logger.error("🔴 CUSTOMER GROUP FIELD in profile edit accepted!")
            profile_form_accepted = True
    except Exception as e:
        logger.debug(f"Profile group change network error: {e}")

    # ĐƯA LỆNH ASSERT ĐÁNH GIÁ LỖI RA NGOÀI HOÀN TOÀN KHỐI TRY-EXCEPT
    if api_escalation_accepted:
        assert False, "Vulnerability Confirmed: Customer changed own group to higher discount via API"
    if profile_form_accepted:
        assert False, "Vulnerability Confirmed: Customer group field maliciously accepted in profile update form"

    # Đo lường mảng hiển thị giá sản phẩm ngoài trang chủ để verify tính toàn vẹn
    try:
        await page.goto(f"{BASE_URL}")
        await page.wait_for_load_state('networkidle')

        before_prices = await page.evaluate("""
                                            Array.from(document.querySelectorAll('.price, [class*="price"]'))
                                                .map(el => parseFloat(el.textContent.replace(/[^0-9.]/g, '')))
                                                .filter(p => p > 0)
                                            """)
        logger.info(f"Product prices visible: {before_prices[:5]}")
    except Exception as e:
        logger.debug(f"Price integrity check: {e}")

    logger.info("✓ Customer group privileges properly protected against unauthorized escalation")

# ============================================================================
# PYTEST MARKER CONFIGURATION
# ============================================================================

def pytest_configure(config):
    """Register custom markers"""
    config.addinivalue_line("markers", "security: Security vulnerability tests")
    config.addinivalue_line("markers", "extreme: Extreme difficulty tests")
    config.addinivalue_line("markers", "hard: Hard difficulty tests")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    """
    Run security stress tests
    
    Examples:
        python security_stress_test.py                    # Run all
        pytest security_stress_test.py -v                 # Verbose
        pytest security_stress_test.py -k "sql_injection"  # Select by name
        pytest security_stress_test.py -m extreme          # By marker
        pytest security_stress_test.py::test_uc01_*        # Specific test
    """
    
    pytest.main([
        __file__,
        "-v",
        "--tb=short",
        "--disable-warnings"
    ])

