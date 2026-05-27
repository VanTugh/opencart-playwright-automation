"""
Advanced examples for extending OpenCart Automation Framework
"""

# ============================================================================
# EXAMPLE 1: Creating a Custom Handler for a New Use Case
# ============================================================================

from handlers import BaseHandler
import logging


logger = logging.getLogger(__name__)


class UC21_AdvancedFeatureHandler(BaseHandler):
    """
    Example handler for a hypothetical UC_21: Advanced Feature

    This demonstrates advanced handler patterns and techniques.
    """

    async def execute_test(self, test_data):
        """Execute advanced feature test"""
        logger.info(f"Executing UC_21 - {test_data.get('Tên kịch bản kiểm thử')}")

        # 1. Navigate to URL
        await self.navigate_to("index.php?route=custom/feature")

        # 2. Extract dynamic test data
        test_data_str = test_data.get('Dữ liệu kiểm thử', '')
        steps = test_data.get('Các bước thực hiện', '').split('. ')
        expected_result = test_data.get('Kết quả mong đợi', '')

        # 3. Wait for specific element
        try:
            await self.page.wait_for_selector('div.feature-container', timeout=10000)
            logger.info("Feature container loaded")
        except Exception as e:
            logger.error(f"Feature container not found: {e}")
            return False

        # 4. Interact with multiple elements
        elements = await self.page.query_selector_all('button.action')
        logger.info(f"Found {len(elements)} action buttons")

        # 5. Execute conditional logic
        if 'button.primary' in test_data_str:
            await self.click_button('button.primary')

        # 6. Handle multiple steps
        for i, step in enumerate(steps[1:], 1):  # Skip first as it's usually intro
            logger.info(f"Executing step {i}: {step}")
            # Step implementation here

        # 7. Verify result with multiple assertions
        result = (
            await self.verify_text('success') or
            await self.verify_text('completed') or
            await self.verify_text('accepted')
        )

        return result


# ============================================================================
# EXAMPLE 2: Advanced Test Data Parsing and Validation
# ============================================================================

def parse_test_data(test_data_string):
    """
    Parse complex test data from string format

    Example input: "Email: test@example.com, Pass: 123456, Phone: 0123456789"
    Returns: {"email": "test@example.com", "password": "123456", "phone": "0123456789"}
    """
    parsed = {}
    pairs = test_data_string.split(', ')

    for pair in pairs:
        if ':' in pair:
            key, value = pair.split(':', 1)
            key = key.strip().lower()
            value = value.strip()

            # Map common keys
            key_map = {
                'email': 'email',
                'pass': 'password',
                'password': 'password',
                'phone': 'phone',
                'name': 'name',
                'firstname': 'first_name',
                'lastname': 'last_name',
            }

            mapped_key = key_map.get(key, key)
            parsed[mapped_key] = value

    return parsed


def validate_test_data(test_data):
    """Validate test data before execution"""
    required_fields = ['TC ID', 'Tên kịch bản kiểm thử', 'Kết quả mong đợi']

    for field in required_fields:
        if field not in test_data or not test_data[field]:
            return False, f"Missing required field: {field}"

    return True, "Valid"


# ============================================================================
# EXAMPLE 3: Custom Assertion and Verification Methods
# ============================================================================

class AdvancedBaseHandler(BaseHandler):
    """Extended handler with advanced verification methods"""

    async def verify_multiple_texts(self, *texts):
        """Verify multiple text values exist on page"""
        content = await self.page.content()
        return all(text in content for text in texts)

    async def verify_element_visible(self, selector):
        """Verify element is visible"""
        try:
            element = await self.page.query_selector(selector)
            if not element:
                return False
            bounds = await element.bounding_box()
            return bounds is not None
        except:
            return False

    async def verify_element_enabled(self, selector):
        """Verify element is enabled (clickable)"""
        try:
            is_disabled = await self.page.is_disabled(selector)
            return not is_disabled
        except:
            return False

    async def verify_attribute_value(self, selector, attr, expected_value):
        """Verify element attribute value"""
        try:
            actual = await self.page.get_attribute(selector, attr)
            return actual == expected_value
        except:
            return False

    async def wait_for_text(self, text, timeout=30000):
        """Wait for specific text to appear"""
        try:
            await self.page.wait_for_function(
                f'() => document.body.textContent.includes("{text}")',
                timeout=timeout
            )
            return True
        except:
            return False


# ============================================================================
# EXAMPLE 4: Using Test Data for Dynamic Selectors
# ============================================================================

class DynamicSelectorHandler(BaseHandler):
    """Handler demonstrating dynamic selector usage"""

    async def fill_form_dynamically(self, form_data_dict):
        """Fill form fields based on dynamic mapping"""

        # Selector mapping - customize for your OpenCart version
        selector_map = {
            'email': 'input[name="email"]',
            'password': 'input[name="password"]',
            'first_name': 'input[name="firstname"]',
            'last_name': 'input[name="lastname"]',
            'phone': 'input[name="phone"]',
            'address': 'input[name="address_1"]',
            'city': 'input[name="city"]',
            'postcode': 'input[name="postcode"]',
            'country': 'select[name="country_id"]',
            'zone': 'select[name="zone_id"]',
        }

        for field_name, value in form_data_dict.items():
            selector = selector_map.get(field_name)
            if selector:
                await self.fill_field(selector, str(value))
            else:
                logger.warning(f"No selector mapping for field: {field_name}")


# ============================================================================
# EXAMPLE 5: Test Case Filtering and Organization
# ============================================================================

def filter_test_cases_by_priority(test_cases, priority='high'):
    """Filter test cases by priority level"""
    priority_map = {'high': 'High', 'medium': 'Medium', 'low': 'Low'}
    target_priority = priority_map.get(priority.lower(), 'High')

    return [
        tc for tc in test_cases
        if tc.get('Mức độ ưu tiên') == target_priority
    ]


def filter_test_cases_by_use_case(test_cases, use_case_code):
    """Filter test cases by use case"""
    return [
        tc for tc in test_cases
        if tc.get('Use Case', '').startswith(use_case_code)
    ]


def group_test_cases_by_use_case(test_cases):
    """Group test cases by their use case"""
    grouped = {}

    for tc in test_cases:
        use_case = tc.get('Use Case', 'Unknown')
        uc_code = use_case.split(':')[0].strip() if use_case else 'Unknown'

        if uc_code not in grouped:
            grouped[uc_code] = []

        grouped[uc_code].append(tc)

    return grouped


# ============================================================================
# EXAMPLE 6: Error Handling and Recovery
# ============================================================================

class RobustHandler(BaseHandler):
    """Handler with advanced error handling"""

    async def safe_fill_field(self, selector, value, max_retries=3):
        """Safely fill field with retry logic"""
        for attempt in range(max_retries):
            try:
                await self.fill_field(selector, str(value))
                return True
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    await self.page.wait_for_timeout(500)

        return False

    async def safe_click_button(self, selector, max_retries=3):
        """Safely click button with retry logic"""
        for attempt in range(max_retries):
            try:
                await self.page.wait_for_selector(selector, timeout=5000)
                await self.click_button(selector)
                return True
            except Exception as e:
                logger.warning(f"Click attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    await self.page.wait_for_timeout(500)

        return False


# ============================================================================
# EXAMPLE 7: Custom Pytest Fixtures
# ============================================================================

import pytest
from handlers import USE_CASE_HANDLERS


@pytest.fixture
def authenticated_page(page):
    """
    Fixture that provides an authenticated page (logged in)

    Usage:
        async def test_something(authenticated_page):
            # Already logged in
            await authenticated_page.goto('http://localhost...')
    """
    # Login implementation here
    return page


@pytest.fixture(params=['chromium', 'firefox', 'webkit'])
def cross_browser(request):
    """
    Fixture for cross-browser testing

    Usage:
        async def test_something(cross_browser):
            # Test runs on all three browsers
    """
    return request.param


# ============================================================================
# EXAMPLE 8: Report Generation Helpers
# ============================================================================

def generate_test_summary(test_results):
    """
    Generate a summary of test results

    Args:
        test_results: List of test result objects

    Returns:
        Dictionary with summary statistics
    """
    summary = {
        'total': len(test_results),
        'passed': sum(1 for r in test_results if r.get('status') == 'PASSED'),
        'failed': sum(1 for r in test_results if r.get('status') == 'FAILED'),
        'skipped': sum(1 for r in test_results if r.get('status') == 'SKIPPED'),
        'errors': sum(1 for r in test_results if r.get('status') == 'ERROR'),
    }

    if summary['total'] > 0:
        summary['pass_rate'] = (summary['passed'] / summary['total']) * 100

    return summary


# ============================================================================
# EXAMPLE 9: Integration with CI/CD
# ============================================================================

"""
For GitHub Actions (.github/workflows/test.yml):

name: OpenCart Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - run: pip install -r requirements.txt
      - run: playwright install chromium
      - run: pytest main.py -v --html=reports/test_report.html
      - uses: actions/upload-artifact@v2
        if: always()
        with:
          name: test-results
          path: reports/
"""

# ============================================================================
# EXAMPLE 10: Performance and Metrics Collection
# ============================================================================

import time
from datetime import datetime


class PerformanceTrackedHandler(BaseHandler):
    """Handler that tracks performance metrics"""

    def __init__(self, page):
        super().__init__(page)
        self.metrics = {
            'navigation_times': [],
            'action_times': [],
            'start_time': datetime.now(),
        }

    async def navigate_to_tracked(self, path=""):
        """Navigate with performance tracking"""
        start = time.time()
        await self.navigate_to(path)
        elapsed = time.time() - start
        self.metrics['navigation_times'].append(elapsed)
        logger.info(f"Navigation took {elapsed:.2f}s")

    async def click_button_tracked(self, selector):
        """Click button with performance tracking"""
        start = time.time()
        await self.click_button(selector)
        elapsed = time.time() - start
        self.metrics['action_times'].append(elapsed)
        logger.info(f"Click action took {elapsed:.2f}s")

    def get_performance_summary(self):
        """Get performance metrics summary"""
        return {
            'avg_navigation_time': sum(self.metrics['navigation_times']) / len(self.metrics['navigation_times']) if self.metrics['navigation_times'] else 0,
            'avg_action_time': sum(self.metrics['action_times']) / len(self.metrics['action_times']) if self.metrics['action_times'] else 0,
            'total_time': (datetime.now() - self.metrics['start_time']).total_seconds(),
        }


if __name__ == '__main__':
    print("This file contains examples for extending the OpenCart Automation Framework")
    print("See docstrings and comments above for detailed usage information")

