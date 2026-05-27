"""
Configuration module for OpenCart Automation Framework
"""
import os
from pathlib import Path
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()


class Config:
    """Base configuration class"""
    
    # Application Settings
    APP_NAME = "OpenCart Automation Testing Framework"
    VERSION = "1.0.0"
    
    # Base URL
    BASE_URL = os.getenv('OPENCART_URL', 'http://localhost/opencart_test/upload/')
    
    # Browser Settings
    HEADLESS = os.getenv('BROWSER_HEADLESS', 'False').lower() == 'true'
    BROWSER_TYPE = os.getenv('BROWSER_TYPE', 'chromium')  # chromium, firefox, webkit
    
    # Timeout Settings (in seconds)
    NAVIGATION_TIMEOUT = int(os.getenv('NAVIGATION_TIMEOUT', '60000'))
    ACTION_TIMEOUT = int(os.getenv('ACTION_TIMEOUT', '30000'))
    ELEMENT_TIMEOUT = int(os.getenv('ELEMENT_TIMEOUT', '10000'))
    
    # Screenshot Settings
    SCREENSHOT_ON_FAILURE = os.getenv('SCREENSHOT_ON_FAILURE', 'True').lower() == 'true'
    SCREENSHOT_ON_SUCCESS = os.getenv('SCREENSHOT_ON_SUCCESS', 'False').lower() == 'true'
    SCREENSHOT_DIR = os.getenv('SCREENSHOT_DIR', 'failures')
    
    # Logging Settings
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_DIR = os.getenv('LOG_DIR', 'logs')
    LOG_FILE = os.path.join(LOG_DIR, 'automation.log')
    
    # Report Settings
    REPORT_DIR = os.getenv('REPORT_DIR', 'reports')
    REPORT_FILE = os.path.join(REPORT_DIR, 'test_report.html')
    
    # Parallel Execution
    NUM_WORKERS = int(os.getenv('NUM_WORKERS', '1'))
    
    # Test Data
    TEST_DATA_FILE = os.getenv('TEST_DATA_FILE', 'OpenCart_203_TestCases_Final.json')
    
    # Retry Settings
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', '0'))
    RETRY_DELAY = int(os.getenv('RETRY_DELAY', '1'))  # seconds
    
    # Test User Credentials (Example)
    TEST_USER_EMAIL = os.getenv('TEST_USER_EMAIL', 'shin@test.com')
    TEST_USER_PASSWORD = os.getenv('TEST_USER_PASSWORD', '123456')
    TEST_USER_NEW_EMAIL = os.getenv('TEST_USER_NEW_EMAIL', 'new@test.com')
    
    # Create necessary directories
    @staticmethod
    def init():
        """Initialize configuration directories"""
        dirs = [Config.LOG_DIR, Config.REPORT_DIR, Config.SCREENSHOT_DIR]
        for dir_name in dirs:
            Path(dir_name).mkdir(exist_ok=True)


# Initialize config on import
Config.init()

