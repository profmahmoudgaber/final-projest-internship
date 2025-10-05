import pytest
import logging
from utils.driver_factory import DriverFactory
from config.config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test_execution.log'),
        logging.StreamHandler()
    ]
)

@pytest.fixture(scope="session")
def driver_session():
    """Session-scoped driver fixture"""
    driver = None
    try:
        driver = DriverFactory.create_driver()
        yield driver
    finally:
        if driver:
            driver.quit()

@pytest.fixture(scope="function")
def driver():
    """Function-scoped driver fixture"""
    driver = None
    try:
        driver = DriverFactory.create_driver()
        driver.get(Config.BASE_URL)
        yield driver
    finally:
        if driver:
            driver.quit()

@pytest.fixture(autouse=True)
def setup_test_environment():
    """Setup test environment before each test"""
    logging.info("Setting up test environment")
    yield
    logging.info("Cleaning up test environment")
