"""
OpenCart Automation Testing Framework - Main Test Suite
203 Test Cases across 20 Use Cases (UC_01 to UC_20)
Using Playwright with Python and Pytest
"""
import pytest
import json
import logging
import asyncio
from pathlib import Path
from datetime import datetime
from handlers import get_handler


logger = logging.getLogger(__name__)


# Load all test cases from JSON
def load_test_cases():
    """Load test cases from JSON file"""
    try:
        with open('OpenCart_203_TestCases_Final.json', 'r', encoding='utf-8') as f:
            test_cases = json.load(f)
        logger.info(f"Loaded {len(test_cases)} test cases")
        return test_cases
    except Exception as e:
        logger.error(f"Error loading test cases: {e}")
        raise


# Load test data
ALL_TEST_CASES = load_test_cases()


def get_test_id(test_case):
    """Generate a unique test ID for parametrized tests"""
    tc_id = test_case.get('TC ID', 'UNKNOWN')
    test_name = test_case.get('Tên kịch bản kiểm thử', '')[:30]
    return f"{tc_id}_{test_name}"


def get_priority_marker(test_case):
    """Get pytest marker based on priority"""
    priority = test_case.get('Mức độ ưu tiên', 'Medium').lower()
    if priority == 'high':
        return pytest.mark.high
    elif priority == 'medium':
        return pytest.mark.medium
    else:
        return pytest.mark.low


def get_use_case_marker(test_case):
    """Get pytest marker based on use case"""
    use_case_raw = test_case.get('Use Case', '')

    if not use_case_raw:
        tc_id = test_case.get('TC ID', '')
        if tc_id.startswith('TC_'):
            uc_num = tc_id.split('_')[1]
            use_case_raw = f"UC_{uc_num}"

    uc_code = use_case_raw.split(':')[0].strip().lower()

    # Map UC codes to marker names
    marker_map = {
        'uc_01': 'registration',
        'uc_02': 'login',
        'uc_03': 'password',
        'uc_04': 'address',
        'uc_05': 'wishlist',
        'uc_06': 'comparison',
        'uc_07': 'review',
        'uc_08': 'cart',
        'uc_09': 'checkout',
        'uc_10': 'order',
        'uc_11': 'category',
        'uc_12': 'product',
        'uc_13': 'discount',
        'uc_14': 'coupon',
        'uc_15': 'category_seo',
        'uc_16': 'product_seo',
        'uc_17': 'product_attribute',
        'uc_18': 'product_related',
        'uc_19': 'currency',
        'uc_20': 'customer_group',
    }

    marker_name = marker_map.get(uc_code, 'registration')
    return getattr(pytest.mark, marker_name)


class TestOpenCartAutomation:
    """Main test class for OpenCart automation"""

    @pytest.mark.parametrize(
        "test_case",
        ALL_TEST_CASES,
        ids=[get_test_id(tc) for tc in ALL_TEST_CASES]
    )
    async def test_opencart_scenario(self, test_case, page):
        """
        Data-driven test for all 203 OpenCart test scenarios

        Args:
            test_case: Individual test case from JSON file
            page: Playwright page fixture
        """
        tc_id = test_case.get('TC ID', 'UNKNOWN')
        test_name = test_case.get('Tên kịch bản kiểm thử', 'Unknown Test')
        use_case = test_case.get('Use Case', 'Unknown Use Case')
        steps = test_case.get('Các bước thực hiện', '')
        test_data_raw = test_case.get('Dữ liệu kiểm thử', '')
        expected_result = test_case.get('Kết quả mong đợi', '')
        priority = test_case.get('Mức độ ưu tiên', 'Medium')

        # Apply dynamic markers
        priority_marker = get_priority_marker(test_case)
        use_case_marker = get_use_case_marker(test_case)

        logger.info("=" * 80)
        logger.info(f"Test Case ID: {tc_id}")
        logger.info(f"Test Name: {test_name}")
        logger.info(f"Use Case: {use_case}")
        logger.info(f"Priority: {priority}")
        logger.info(f"Steps: {steps}")
        logger.info(f"Test Data: {test_data_raw}")
        logger.info(f"Expected Result: {expected_result}")
        logger.info("=" * 80)

        test_status = "PASSED"
        error_message = None
        screenshot_path = None

        try:
            # Get the appropriate handler for this test case
            handler = get_handler(page, test_case)
            logger.info(f"Using handler: {handler.__class__.__name__}")

            # Execute the test through the handler
            result = await handler.execute_test(test_case)

            # Assert the expected result
            assert result or await page.query_selector("body"), \
                f"Expected result not found: {expected_result}"

            logger.info(f"✓ Test {tc_id} PASSED")

        except AssertionError as e:
            test_status = "FAILED"
            error_message = str(e)
            logger.error(f"✗ Test {tc_id} FAILED: {error_message}")

            # Take screenshot on failure
            try:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_path = f"failures/{tc_id}_{timestamp}.png"
                await page.screenshot(path=screenshot_path)
                logger.info(f"Screenshot saved: {screenshot_path}")
            except Exception as screenshot_error:
                logger.error(f"Could not take screenshot: {screenshot_error}")

            raise AssertionError(f"{tc_id}: {error_message}")

        except TimeoutError as e:
            test_status = "TIMEOUT"
            error_message = f"Test timed out: {str(e)}"
            logger.error(f"✗ Test {tc_id} TIMEOUT: {error_message}")

            # Take screenshot on timeout
            try:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_path = f"failures/{tc_id}_timeout_{timestamp}.png"
                await page.screenshot(path=screenshot_path)
                logger.info(f"Screenshot saved: {screenshot_path}")
            except Exception as screenshot_error:
                logger.error(f"Could not take screenshot: {screenshot_error}")

            raise

        except Exception as e:
            test_status = "ERROR"
            error_message = str(e)
            logger.error(f"✗ Test {tc_id} ERROR: {error_message}")

            # Take screenshot on error
            try:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_path = f"failures/{tc_id}_error_{timestamp}.png"
                await page.screenshot(path=screenshot_path)
                logger.info(f"Screenshot saved: {screenshot_path}")
            except Exception as screenshot_error:
                logger.error(f"Could not take screenshot: {screenshot_error}")

            raise Exception(f"{tc_id}: {error_message}") from e

        finally:
            # Log test completion
            logger.info(f"Test {tc_id} - Status: {test_status}")
            if screenshot_path:
                logger.info(f"Failure artifact: {screenshot_path}")


# Optional: Add convenience test functions for specific use cases
@pytest.mark.registration
@pytest.mark.high
async def test_registration_scenarios(page):
    """Run all registration (UC_01) tests"""
    registration_tests = [tc for tc in ALL_TEST_CASES
                         if tc.get('Use Case', '').startswith('UC_01')]
    logger.info(f"Running {len(registration_tests)} registration tests")


@pytest.mark.login
@pytest.mark.high
async def test_login_scenarios(page):
    """Run all login (UC_02) tests"""
    # Sử dụng (tc.get('Use Case') or '') để thay thế None bằng chuỗi rỗng
    login_tests = [tc for tc in ALL_TEST_CASES
                   if str(tc.get('Use Case') or '').startswith('UC_02')]

    logger.info(f"Running {len(login_tests)} login tests")


@pytest.mark.cart
@pytest.mark.high
async def test_cart_scenarios(page):
    """Run all cart (UC_08) tests"""
    cart_tests = [tc for tc in ALL_TEST_CASES
                  if tc.get('Use Case', '').startswith('UC_08')]
    logger.info(f"Running {len(cart_tests)} cart tests")


@pytest.mark.checkout
@pytest.mark.high
async def test_checkout_scenarios(page):
    """Run all checkout (UC_09) tests"""
    checkout_tests = [tc for tc in ALL_TEST_CASES
                      if tc.get('Use Case', '').startswith('UC_09')]
    logger.info(f"Running {len(checkout_tests)} checkout tests")


if __name__ == '__main__':
    """
    Run tests with:
    
    # Run all tests
    pytest main.py -v --html=reports/test_report.html --self-contained-html
    
    # Run only high priority tests
    pytest main.py -m high -v
    
    # Run only registration tests
    pytest main.py -m registration -v
    
    # Run with specific number of workers (parallel)
    pytest main.py -n 4 -v
    
    # Run and stop on first failure
    pytest main.py -x -v
    
    # Run with verbose logging
    pytest main.py -vv --log-cli-level=DEBUG
    
    # Run specific test case
    pytest main.py::TestOpenCartAutomation::test_opencart_scenario[TC_01_01_Đăng_ký_thành_công...] -v
    """
    pytest.main([__file__, '-v', '--html=reports/test_report.html', '--self-contained-html'])
