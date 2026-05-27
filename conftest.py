"""
Pytest configuration and fixtures for OpenCart Automation Testing
"""
import os
import json
import logging
import asyncio
from pathlib import Path
from datetime import datetime
import pytest
from playwright.async_api import async_playwright

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/automation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Create necessary directories
Path('logs').mkdir(exist_ok=True)
Path('reports').mkdir(exist_ok=True)
Path('failures').mkdir(exist_ok=True)

BASE_URL = "http://localhost/opencart_test/upload/"

def pytest_configure(config):
    """Configure pytest"""
    logger.info("=" * 80)
    logger.info("OpenCart Automation Testing Framework")
    logger.info(f"Test Started: {datetime.now()}")
    logger.info("=" * 80)

def pytest_sessionfinish(session, exitstatus):
    """Called after the entire test session finished"""
    logger.info("=" * 80)
    logger.info(f"Test Finished: {datetime.now()}")
    logger.info(f"Exit Status: {exitstatus}")

@pytest.fixture(scope="session")
def test_data():
    """Load test data from JSON file"""
    try:
        with open('OpenCart_203_TestCases_Final.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.info(f"Loaded {len(data)} test cases from JSON")
        return data
    except Exception as e:
        logger.error(f"Error loading test data: {e}")
        raise

@pytest.fixture(scope="function")
async def browser():
    """Create a browser instance for each test"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        yield browser
        await browser.close()

@pytest.fixture(scope="function")
async def page(browser):
    """Create a page/context for each test"""
    context = await browser.new_context()
    page = await context.new_page()
    yield page
    await page.close()
    await context.close()

@pytest.fixture(scope="function")
def test_metadata(request):
    """Get metadata for current test"""
    return {
        'test_name': request.node.name,
        'timestamp': datetime.now().isoformat(),
        'status': None
    }

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook wrapper tự động chụp ảnh màn hình khi bất kỳ bài test nào thất bại"""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        # Tự động quét tìm fixture page hoặc authenticated_page trong hàm test
        page = item.funcargs.get("page") or item.funcargs.get("authenticated_page")

        if page:
            try:
                os.makedirs("failures", exist_ok=True)
                screenshot_path = f"failures/AUTO_FAIL_{item.name}.png"

                try:
                    loop = asyncio.get_event_loop()
                except RuntimeError:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)

                # Ép buộc hệ thống phải đợi chụp ảnh xong hoàn toàn trước khi đóng luồng
                if loop.is_running():
                    loop.create_task(page.screenshot(path=screenshot_path, full_page=True))
                else:
                    loop.run_until_complete(page.screenshot(path=screenshot_path, full_page=True))

                logger.info(f"📸 [AUTO SCREENSHOT] Đã lưu bằng chứng lỗi thành công: {screenshot_path}")
            except Exception as e:
                logger.error(f"⚠️ Không thể chụp ảnh tự động: {e}")