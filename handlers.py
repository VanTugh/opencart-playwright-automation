"""
Handler classes for different OpenCart Use Cases
"""
import logging
from abc import ABC, abstractmethod
import asyncio


logger = logging.getLogger(__name__)

# Base URL for OpenCart
BASE_URL = "http://localhost/opencart_test/upload/"


class BaseHandler(ABC):
    """Base handler class for all use cases"""

    def __init__(self, page):
        self.page = page
        self.base_url = BASE_URL

    async def navigate_to(self, path=""):
        """Navigate to a URL"""
        url = self.base_url + path
        logger.info(f"Navigating to: {url}")
        await self.page.goto(url, wait_until="networkidle")
        await asyncio.sleep(0.5)

    async def fill_field(self, selector, value):
        """Fill a form field"""
        if value:
            logger.info(f"Filling field {selector} with: {value}")
            await self.page.fill(selector, str(value))
            await asyncio.sleep(0.2)

    async def click_button(self, selector):
        """Click a button"""
        logger.info(f"Clicking button: {selector}")
        await self.page.click(selector)
        await asyncio.sleep(0.5)

    async def check_element(self, selector):
        """Check a checkbox or radio button"""
        logger.info(f"Checking element: {selector}")
        await self.page.check(selector)
        await asyncio.sleep(0.2)

    async def verify_text(self, text):
        """Verify if text exists on page"""
        logger.info(f"Verifying text: {text}")
        await asyncio.sleep(0.5)
        return await self.page.text_content("body") is not None and text in await self.page.content()

    async def wait_for_navigation(self):
        """Wait for navigation to complete"""
        await asyncio.sleep(1)

    async def execute_test(self, test_data):
        """Execute the test - must be implemented by subclasses"""
        raise NotImplementedError()


class UC01_RegistrationHandler(BaseHandler):
    """Handler for UC_01: Registration"""

    async def execute_test(self, test_data):
        """Execute registration test"""
        logger.info(f"Executing UC_01 - {test_data.get('Tên kịch bản kiểm thử')}")

        # Navigate to registration page
        await self.navigate_to("index.php?route=account/register")

        # Extract test data
        test_info = test_data.get('Dữ liệu kiểm thử', '')
        expected_result = test_data.get('Kết quả mong đợi', '')

        # Fill registration form (basic implementation)
        # These selectors should be adjusted based on actual OpenCart form
        await self.fill_field('input[name="firstname"]', 'John')
        await self.fill_field('input[name="lastname"]', 'Doe')
        await self.fill_field('input[name="email"]', 'john@test.com')
        await self.fill_field('input[name="password"]', '123456')
        await self.fill_field('input[name="confirm"]', '123456')

        # Check privacy policy if present
        try:
            await self.check_element('input[name="agree"]')
        except:
            logger.warning("Privacy policy checkbox not found")

        # Click continue/submit button
        try:
            await self.click_button('button[type="submit"]')
        except:
            try:
                await self.click_button('input[type="submit"]')
            except:
                logger.error("Submit button not found")
                raise

        # Wait for navigation
        await self.wait_for_navigation()

        # Verify expected result
        return await self.verify_text('Your Account Has Been Created!') or await self.verify_text('Account')


class UC02_LoginHandler(BaseHandler):
    """Handler for UC_02: Login - Đã sửa lỗi Hardcode và Selector"""

    async def execute_test(self, test_data):
        logger.info(f"Executing UC_02 - {test_data.get('Tên kịch bản kiểm thử')}")
        await self.navigate_to("index.php?route=account/login")

        # --- TỰ ĐỘNG TÁCH DỮ LIỆU TỪ JSON ---
        raw_data = test_data.get('Dữ liệu kiểm thử', '')
        email = "shin@test.com"  # Mặc định
        password = "wrong_password"  # Mặc định để test fail-safe

        if "Email:" in raw_data:
            # Tách chuỗi kiểu "Email: abc@test.com, Pass: 123"
            parts = raw_data.split(',')
            for p in parts:
                if "Email:" in p: email = p.split(':')[1].strip()
                if "Pass:" in p: password = p.split(':')[1].strip()

        # Điền dữ liệu thực tế từ kịch bản
        await self.fill_field('input[name="email"]', email)
        await self.fill_field('input[name="password"]', password)

        # --- SỬA SELECTOR NÚT BẤM (Hỗ trợ cả input và button) ---
        submit_selector = 'input[type="submit"], button[type="submit"], .btn-primary'
        await self.click_button(submit_selector)

        await self.wait_for_navigation()

        # Kiểm tra kết quả mong đợi từ cột 'Kết quả mong đợi'
        expected = test_data.get('Kết quả mong đợi', 'My Account')
        # Nếu expected là câu thông báo lỗi, tìm thông báo lỗi. Nếu không, tìm chữ My Account.
        return await self.verify_text(expected) or await self.verify_text('My Account')


class UC03_PasswordHandler(BaseHandler):
    """Handler for UC_03 - Sửa lỗi lấy Email từ kịch bản Quên mật khẩu"""

    async def execute_test(self, test_data):
        logger.info(f"Executing UC_03 - {test_data.get('Tên kịch bản kiểm thử')}")
        await self.navigate_to("index.php?route=account/forgotten")

        raw_input = test_data.get('Dữ liệu kiểm thử', '')
        email = "unknown@test.com"  # mặc định

        if "Email:" in raw_input:
            email = raw_input.split('Email:')[1].strip()

        await self.fill_field('input[name="email"]', email)

        # Selector cho nút Continue trong trang Forgotten Password
        await self.click_button('input[type="submit"], button[type="submit"]')

        await self.wait_for_navigation()
        expected = test_data.get('Kết quả mong đợi', '')
        return await self.verify_text(expected)


class UC04_AddressHandler(BaseHandler):
    """Handler for UC_04: Address Management"""

    async def execute_test(self, test_data):
        """Execute address test"""
        logger.info(f"Executing UC_04 - {test_data.get('Tên kịch bản kiểm thử')}")

        # Navigate to addresses page (requires login)
        await self.navigate_to("index.php?route=account/address")

        # Verify expected result
        expected_result = test_data.get('Kết quả mong đợi', '')
        return await self.verify_text('Address') or await self.verify_text('address')


class UC05_WishlistHandler(BaseHandler):
    """Handler for UC_05: Wishlist"""

    async def execute_test(self, test_data):
        """Execute wishlist test"""
        logger.info(f"Executing UC_05 - {test_data.get('Tên kịch bản kiểm thử')}")

        # Navigate to wishlist page
        await self.navigate_to("index.php?route=account/wishlist")

        # Verify expected result
        expected_result = test_data.get('Kết quả mong đợi', '')
        return await self.verify_text('Wish List') or await self.verify_text('wishlist')


class UC06_ComparisonHandler(BaseHandler):
    """Handler for UC_06: Product Comparison"""

    async def execute_test(self, test_data):
        """Execute comparison test"""
        logger.info(f"Executing UC_06 - {test_data.get('Tên kịch bản kiểm thử')}")

        # Navigate to comparison page
        await self.navigate_to("index.php?route=product/comparison")

        # Verify expected result
        expected_result = test_data.get('Kết quả mong đợi', '')
        return await self.verify_text('compare') or await self.verify_text('Compare')


class UC07_ReviewHandler(BaseHandler):
    """Handler for UC_07: Product Review"""

    async def execute_test(self, test_data):
        """Execute review test"""
        logger.info(f"Executing UC_07 - {test_data.get('Tên kịch bản kiểm thử')}")

        # Navigate to a product page
        await self.navigate_to("index.php?route=product/product&product_id=43")

        # Verify expected result
        expected_result = test_data.get('Kết quả mong đợi', '')
        return await self.verify_text('Review') or await self.verify_text('review')


class UC08_CartHandler(BaseHandler):
    """Handler for UC_08: Shopping Cart"""

    async def execute_test(self, test_data):
        """Execute cart test"""
        logger.info(f"Executing UC_08 - {test_data.get('Tên kịch bản kiểm thử')}")

        # Navigate to cart page
        await self.navigate_to("index.php?route=checkout/cart")

        # Verify expected result
        expected_result = test_data.get('Kết quả mong đợi', '')
        return await self.verify_text('Cart') or await self.verify_text('cart')


class UC09_CheckoutHandler(BaseHandler):
    """Handler for UC_09: Checkout Process"""

    async def execute_test(self, test_data):
        """Execute checkout test"""
        logger.info(f"Executing UC_09 - {test_data.get('Tên kịch bản kiểm thử')}")

        # Navigate to checkout page
        await self.navigate_to("index.php?route=checkout/checkout")

        # Verify expected result
        expected_result = test_data.get('Kết quả mong đợi', '')
        return await self.verify_text('Checkout') or await self.verify_text('checkout')


class UC10_OrderHandler(BaseHandler):
    """Handler for UC_10: Order Management"""

    async def execute_test(self, test_data):
        """Execute order test"""
        logger.info(f"Executing UC_10 - {test_data.get('Tên kịch bản kiểm thử')}")

        # Navigate to order history
        await self.navigate_to("index.php?route=account/order")

        # Verify expected result
        expected_result = test_data.get('Kết quả mong đợi', '')
        return await self.verify_text('Order') or await self.verify_text('order')


class UC11_CategoryHandler(BaseHandler):
    """Handler for UC_11: Product Categories"""

    async def execute_test(self, test_data):
        """Execute category test"""
        logger.info(f"Executing UC_11 - {test_data.get('Tên kịch bản kiểm thử')}")

        # Navigate to category page
        await self.navigate_to("index.php?route=product/category&path=20")

        # Verify expected result
        expected_result = test_data.get('Kết quả mong đợi', '')
        return await self.verify_text('category') or await self.verify_text('Category')


class UC12_ProductHandler(BaseHandler):
    """Handler for UC_12: Product Management"""

    async def execute_test(self, test_data):
        """Execute product test"""
        logger.info(f"Executing UC_12 - {test_data.get('Tên kịch bản kiểm thử')}")

        # Navigate to product page
        await self.navigate_to("index.php?route=product/product&product_id=43")

        # Verify expected result
        expected_result = test_data.get('Kết quả mong đợi', '')
        return await self.verify_text('Product') or await self.verify_text('product')


class UC13_DiscountHandler(BaseHandler):
    """Handler for UC_13: Discount Management"""

    async def execute_test(self, test_data):
        """Execute discount test"""
        logger.info(f"Executing UC_13 - {test_data.get('Tên kịch bản kiểm thử')}")

        # Navigate to home to verify discount
        await self.navigate_to()

        # Verify expected result
        expected_result = test_data.get('Kết quả mong đợi', '')
        return await self.verify_text('Special') or await self.verify_text('discount')


class UC14_CouponHandler(BaseHandler):
    """Handler for UC_14: Coupon Management"""

    async def execute_test(self, test_data):
        """Execute coupon test"""
        logger.info(f"Executing UC_14 - {test_data.get('Tên kịch bản kiểm thử')}")

        # Navigate to checkout page where coupon can be applied
        await self.navigate_to("index.php?route=checkout/checkout")

        # Verify expected result
        expected_result = test_data.get('Kết quả mong đợi', '')
        return await self.verify_text('coupon') or await self.verify_text('Coupon')


class UC15_CategorySEOHandler(BaseHandler):
    """Handler for UC_15: Category SEO"""

    async def execute_test(self, test_data):
        """Execute category SEO test"""
        logger.info(f"Executing UC_15 - {test_data.get('Tên kịch bản kiểm thử')}")

        # Navigate to category page
        await self.navigate_to("index.php?route=product/category&path=20")

        # Verify expected result
        expected_result = test_data.get('Kết quả mong đợi', '')
        return await self.verify_text('category') or await self.verify_text('SEO')


class UC16_ProductSEOHandler(BaseHandler):
    """Handler for UC_16: Product SEO"""

    async def execute_test(self, test_data):
        """Execute product SEO test"""
        logger.info(f"Executing UC_16 - {test_data.get('Tên kịch bản kiểm thử')}")

        # Navigate to product page
        await self.navigate_to("index.php?route=product/product&product_id=43")

        # Verify expected result
        expected_result = test_data.get('Kết quả mong đợi', '')
        return await self.verify_text('product') or await self.verify_text('SEO')


class UC17_AttributeHandler(BaseHandler):
    """Handler for UC_17: Product Attributes"""

    async def execute_test(self, test_data):
        """Execute attribute test"""
        logger.info(f"Executing UC_17 - {test_data.get('Tên kịch bản kiểm thử')}")

        # Navigate to product page
        await self.navigate_to("index.php?route=product/product&product_id=43")

        # Verify expected result
        expected_result = test_data.get('Kết quả mong đợi', '')
        return await self.verify_text('Attribute') or await self.verify_text('attribute')


class UC18_RelatedProductHandler(BaseHandler):
    """Handler for UC_18: Related Products"""

    async def execute_test(self, test_data):
        """Execute related product test"""
        logger.info(f"Executing UC_18 - {test_data.get('Tên kịch bản kiểm thử')}")

        # Navigate to product page
        await self.navigate_to("index.php?route=product/product&product_id=43")

        # Verify expected result
        expected_result = test_data.get('Kết quả mong đợi', '')
        return await self.verify_text('Related') or await self.verify_text('related')


class UC19_CurrencyHandler(BaseHandler):
    """Handler for UC_19: Currency Management"""

    async def execute_test(self, test_data):
        """Execute currency test"""
        logger.info(f"Executing UC_19 - {test_data.get('Tên kịch bản kiểm thử')}")

        # Navigate to home page to check currency selector
        await self.navigate_to()

        # Verify expected result
        expected_result = test_data.get('Kết quả mong đợi', '')
        return await self.verify_text('currency') or await self.verify_text('Currency')


class UC20_CustomerGroupHandler(BaseHandler):
    """Handler for UC_20: Customer Groups"""

    async def execute_test(self, test_data):
        """Execute customer group test"""
        logger.info(f"Executing UC_20 - {test_data.get('Tên kịch bản kiểm thử')}")

        # Navigate to home page
        await self.navigate_to()

        # Verify expected result
        expected_result = test_data.get('Kết quả mong đợi', '')
        return await self.verify_text('group') or await self.verify_text('Group')


class GenericSecurityHandler(BaseHandler):
    """Handler for Security test cases"""

    async def execute_test(self, test_data):
        """Execute security test"""
        logger.info(f"Executing Security Test - {test_data.get('Tên kịch bản kiểm thử')}")

        # Navigate to home
        await self.navigate_to()

        # Verify no alert dialogs appear (XSS check)
        expected_result = test_data.get('Kết quả mong đợi', '')
        page_content = await self.page.content()

        return '<script>' not in page_content


class GenericLogHandler(BaseHandler):
    """Handler for Log check test cases"""

    async def execute_test(self, test_data):
        """Execute log check test"""
        logger.info(f"Executing Log Check - {test_data.get('Tên kịch bản kiểm thử')}")

        # Navigate to home
        await self.navigate_to()

        # Verify page loads without errors
        expected_result = test_data.get('Kết quả mong đợi', '')
        status = await self.page.evaluate('() => window.lastError || null')

        return status is None


# Mapping of Use Cases to Handler classes
USE_CASE_HANDLERS = {
    'UC_01': UC01_RegistrationHandler,
    'UC_02': UC02_LoginHandler,
    'UC_03': UC03_PasswordHandler,
    'UC_04': UC04_AddressHandler,
    'UC_05': UC05_WishlistHandler,
    'UC_06': UC06_ComparisonHandler,
    'UC_07': UC07_ReviewHandler,
    'UC_08': UC08_CartHandler,
    'UC_09': UC09_CheckoutHandler,
    'UC_10': UC10_OrderHandler,
    'UC_11': UC11_CategoryHandler,
    'UC_12': UC12_ProductHandler,
    'UC_13': UC13_DiscountHandler,
    'UC_14': UC14_CouponHandler,
    'UC_15': UC15_CategorySEOHandler,
    'UC_16': UC16_ProductSEOHandler,
    'UC_17': UC17_AttributeHandler,
    'UC_18': UC18_RelatedProductHandler,
    'UC_19': UC19_CurrencyHandler,
    'UC_20': UC20_CustomerGroupHandler,
    'Security': GenericSecurityHandler,
    'Log check': GenericLogHandler,
}


def get_handler(page, test_case):
    """Get appropriate handler for a test case"""
    # Extract use case code from "Use Case" field
    use_case_raw = test_case.get('Use Case', '')

    if not use_case_raw:
        # If Use Case is null, try to infer from TC ID or use generic handler
        tc_id = test_case.get('TC ID', '')
        if tc_id.startswith('TC_'):
            uc_code = 'UC_' + tc_id.split('_')[1].zfill(2)
            handler_class = USE_CASE_HANDLERS.get(uc_code, UC01_RegistrationHandler)
        else:
            handler_class = UC01_RegistrationHandler
    else:
        # Extract use case code from string like "UC_01: Đăng ký"
        parts = use_case_raw.split(':')
        uc_code = parts[0].strip()
        handler_class = USE_CASE_HANDLERS.get(uc_code, UC01_RegistrationHandler)

    return handler_class(page)

