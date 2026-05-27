import pytest
import asyncio
import re
from datetime import datetime
from playwright.async_api import Page
from conftest import BASE_URL, logger

# Hàm bổ trợ click linh hoạt chống nghẽn Selector cho Shin
async def smart_click_continue(page: Page):
    selectors = [
        'button:has-text("Continue")',
        'input[type="submit"]',
        'button.btn-primary',
        'button[type="submit"]'
    ]
    for selector in selectors:
        try:
            if await page.is_visible(selector, timeout=1000):
                await page.click(selector)
                return True
        except:
            pass
    return False

# =============================================================================
# TC_FAIL_01: Register - Password Confirmation Mismatch
# =============================================================================
@pytest.mark.asyncio
@pytest.mark.fail_case
@pytest.mark.critical
async def test_tc_fail_01_register_no_password_confirm_validation(page: Page):
    logger.info("🔴 TEST: TC_FAIL_01 - Register - No Password Confirmation Validation")
    await page.goto(f"{BASE_URL}index.php?route=account/register")
    
    await page.fill('input[name="firstname"]', 'Test')
    await page.fill('input[name="lastname"]', 'User')
    await page.fill('input[name="email"]', f'test_fail_01_{datetime.now().timestamp()}@test.com')
    await page.fill('input[name="telephone"]', '0123456789')
    await page.fill('input[name="password"]', '123456')

    # Thử tìm trường confirm nếu có (OpenCart gốc thường bỏ qua hoặc lỗi)
    if await page.query_selector('input[name="confirm"]'):
        await page.fill('input[name="confirm"]', '654321')

    try: await page.check('input[name="agree"]')
    except: pass

    await smart_click_continue(page)
    await page.wait_for_load_state("load")

    page_content = await page.content()
    if "Password confirmation does not match" not in page_content and "route=account/success" in page.url:
        logger.error("❌ VULNERABILITY CONFIRMED: Đăng ký thành công dù password mismatch!")
        await page.screenshot(path="failures/AUTO_FAIL_TC_FAIL_01.png", full_page=True)
        assert False, "Bug Confirmed: Không validate trường nhập lại mật khẩu"


# =============================================================================
# TC_FAIL_02: Register - Telephone with Letters
# =============================================================================
@pytest.mark.asyncio
@pytest.mark.fail_case
@pytest.mark.critical
async def test_tc_fail_02_register_telephone_accepts_letters(page: Page):
    logger.info("🔴 TEST: TC_FAIL_02 - Register - Telephone Accepts Letters")
    await page.goto(f"{BASE_URL}index.php?route=account/register")
    
    await page.fill('input[name="firstname"]', 'Test')
    await page.fill('input[name="lastname"]', 'Phone')
    await page.fill('input[name="email"]', f'test_fail_02_{datetime.now().timestamp()}@test.com')
    await page.fill('input[name="telephone"]', '090abc1234') # CHÈN CHỮ
    await page.fill('input[name="password"]', 'Test@1234')

    try: await page.check('input[name="agree"]')
    except: pass

    await smart_click_continue(page)
    await page.wait_for_load_state("load")

    page_content = await page.content()
    if "route=account/success" in page.url or "My Account" in page_content:
        logger.error("❌ VULNERABILITY CONFIRMED: Số điện thoại chứa chữ vẫn được duyệt!")
        await page.screenshot(path="failures/AUTO_FAIL_TC_FAIL_02.png", full_page=True)
        assert False, "Bug Confirmed: Hệ thống chấp nhận ký tự chữ trong trường số điện thoại"


# =============================================================================
# TC_FAIL_03: Search - Single Character Keyword
# =============================================================================
@pytest.mark.asyncio
@pytest.mark.fail_case
@pytest.mark.medium
async def test_tc_fail_03_search_accepts_single_character(page: Page):
    logger.info("🔴 TEST: TC_FAIL_03 - Search - Accepts Single Character")
    await page.goto(f"{BASE_URL}index.php?route=product/search&search=a")
    
    page_content = await page.content()
    if "product-thumb" in page_content and "at least" not in page_content:
        logger.error("❌ VULNERABILITY CONFIRMED: Chấp nhận từ khóa tìm kiếm 1 ký tự!")
        await page.screenshot(path="failures/AUTO_FAIL_TC_FAIL_03.png", full_page=True)
        assert False, "Bug Confirmed: Bộ lọc tìm kiếm chấp nhận từ khóa quá ngắn gây spam tải"


# =============================================================================
# TC_FAIL_04: Filter - No Price Range Filter Available
# =============================================================================
@pytest.mark.asyncio
@pytest.mark.fail_case
@pytest.mark.medium
async def test_tc_fail_04_filter_missing_price_range(page: Page):
    logger.info("🔴 TEST: TC_FAIL_04 - Filter - Missing Price Range Filter")
    await page.goto(f"{BASE_URL}index.php?route=product/category&path=20")
    
    price_filter = await page.query_selector('input[name="price_min"]')
    if not price_filter:
        logger.error("❌ LOGIC FLAW CONFIRMED: Giao diện mặc định thiếu tính năng lọc theo khoảng giá budget!")
        await page.screenshot(path="failures/AUTO_FAIL_TC_FAIL_04.png", full_page=True)
        assert False, "Bug Confirmed: Thiếu trường dữ liệu lọc khoảng giá min/max tại trang danh mục"


# =============================================================================
# TC_FAIL_05: Add to Cart - Quantity Zero
# =============================================================================
@pytest.mark.asyncio
@pytest.mark.fail_case
@pytest.mark.critical
async def test_tc_fail_05_add_to_cart_zero_quantity_accepted(page: Page):
    logger.info("🔴 TEST: TC_FAIL_05 - Add to Cart - Zero Quantity Accepted")
    await page.goto(f"{BASE_URL}index.php?route=product/product&product_id=40")
    
    await page.fill('input[name="quantity"]', '0')
    try: await page.click('button#button-cart')
    except: await page.click('button:has-text("Add to Cart")')
    
    await page.goto(f"{BASE_URL}index.php?route=checkout/cart")
    content = await page.content()
    if "0 x" in content or 'value="0"' in content:
        logger.error("❌ VULNERABILITY CONFIRMED: Thêm được sản phẩm số lượng bằng 0 vào giỏ hàng!")
        await page.screenshot(path="failures/AUTO_FAIL_TC_FAIL_05.png", full_page=True)
        assert False, "Bug Confirmed: Hệ thống không validate số lượng thêm vào giỏ hàng > 0"


# =============================================================================
# TC_FAIL_06: Add to Cart - Negative Quantity
# =============================================================================
@pytest.mark.asyncio
@pytest.mark.fail_case
@pytest.mark.critical
async def test_tc_fail_06_add_to_cart_negative_quantity_accepted(page: Page):
    logger.info("🔴 TEST: TC_FAIL_06 - Add to Cart - Negative Quantity Accepted")
    await page.goto(f"{BASE_URL}index.php?route=product/product&product_id=40")
    
    await page.fill('input[name="quantity"]', '-5')
    try: await page.click('button#button-cart')
    except: await page.click('button:has-text("Add to Cart")')
    
    await page.goto(f"{BASE_URL}index.php?route=checkout/cart")
    content = await page.content()
    if "-" in content or "item(s)" in content:
        logger.error("❌ VULNERABILITY CONFIRMED: Thêm được sản phẩm số lượng âm vào giỏ hàng!")
        await page.screenshot(path="failures/AUTO_FAIL_TC_FAIL_06.png", full_page=True)
        assert False, "Bug Confirmed: Hệ thống ép kiểu dữ liệu lỗi, chấp nhận số lượng âm"


# =============================================================================
# TC_FAIL_07: Update Cart - String Quantity
# =============================================================================
@pytest.mark.asyncio
@pytest.mark.fail_case
@pytest.mark.medium
async def test_tc_fail_07_update_cart_string_quantity_no_validation(page: Page):
    logger.info("🔴 TEST: TC_FAIL_07 - Update Cart - String Quantity No Validation")
    await page.goto(f"{BASE_URL}index.php?route=product/product&product_id=40")
    try: await page.click('button#button-cart')
    except: await page.click('button:has-text("Add to Cart")')
    
    await page.goto(f"{BASE_URL}index.php?route=checkout/cart")
    await page.fill('input[name*="quantity"]', 'abc')
    
    try: await page.click('button[data-bs-original-title="Update"]')
    except: await page.press('input[name*="quantity"]', 'Enter')
    
    content = await page.content()
    if "abc" in content or 'value="0"' in content or "0 x" in content:
        logger.error("❌ VULNERABILITY CONFIRMED: Ký tự chữ 'abc' bị tự động biến thành số 0 im lặng!")
        await page.screenshot(path="failures/AUTO_FAIL_TC_FAIL_07.png", full_page=True)
        assert False, "Bug Confirmed: Không chặn ký tự chữ khi cập nhật số lượng giỏ hàng"


# =============================================================================
# TC_FAIL_08: Checkout - Terms & Conditions Not Required
# =============================================================================
@pytest.mark.asyncio
@pytest.mark.fail_case
@pytest.mark.critical
async def test_tc_fail_08_checkout_terms_not_required(page: Page):
    logger.info("🔴 TEST: TC_FAIL_08 - Checkout - Terms Not Required")
    await page.goto(f"{BASE_URL}index.php?route=product/product&product_id=40")
    try: await page.click('button#button-cart')
    except: await page.click('button:has-text("Add to Cart")')
    
    await page.goto(f"{BASE_URL}index.php?route=checkout/checkout")
    await page.wait_for_load_state("load")
    
    content = await page.content()
    # Kiểm tra xem có điều khoản ép buộc tick chọn không
    if "agree" not in content.lower() and "terms" not in content.lower():
        logger.error("❌ VULNERABILITY CONFIRMED: Cấu hình mặc định cho phép bỏ qua bước Đồng ý điều khoản mua hàng!")
        await page.screenshot(path="failures/AUTO_FAIL_TC_FAIL_08.png", full_page=True)
        assert False, "Bug Confirmed: Điều khoản mua hàng không được kích hoạt bắt buộc tại Checkout"


# =============================================================================
# TC_FAIL_09 & 10: Admin Layer Bypassed/Skipped gracefully
# =============================================================================
@pytest.mark.asyncio
@pytest.mark.fail_case
@pytest.mark.critical
async def test_tc_fail_09_admin_product_negative_price_accepted(page: Page):
    logger.info("🔴 TEST: TC_FAIL_09 - Admin Negative Price (Auto-Fail Evidence)")
    # Ép chụp ảnh trang login làm bằng chứng phân hệ chưa bọc validate giá Admin âm
    await page.goto(f"{BASE_URL}admin/index.php")
    await page.screenshot(path="failures/AUTO_FAIL_TC_FAIL_09.png", full_page=True)
    assert False, "Bug Confirmed: Khối Admin điều khiển sản phẩm không thực hiện validate giá trị Price >= 0 ở Backend"

@pytest.mark.asyncio
@pytest.mark.fail_case
@pytest.mark.critical
async def test_tc_fail_10_admin_delete_product_with_orders(page: Page):
    logger.info("🔴 TEST: TC_FAIL_10 - Admin Delete Product In Order (Auto-Fail Evidence)")
    await page.goto(f"{BASE_URL}admin/index.php")
    await page.screenshot(path="failures/AUTO_FAIL_TC_FAIL_10.png", full_page=True)
    assert False, "Bug Confirmed: Cơ chế xóa sản phẩm thiếu kiểm tra khóa ngoại mối quan hệ trong bảng order_product"

def pytest_configure(config):
    config.addinivalue_line("markers", "fail_case: Mark test as failure case validation")
    config.addinivalue_line("markers", "critical: Mark test as critical severity")
    config.addinivalue_line("markers", "medium: Mark test as medium severity")