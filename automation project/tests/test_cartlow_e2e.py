import pytest
import logging
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.driver_factory import DriverFactory
from utils.test_helpers import TestHelpers
from pages.login_page import LoginPage
from pages.homepage import HomePage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
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

class TestCartlowE2E:
    """End-to-End test for Cartlow website shopping flow"""
    
    @pytest.fixture(scope="class")
    def setup_driver(self):
        """Setup WebDriver for the test class"""
        driver = None
        try:
            driver = DriverFactory.create_driver()
            driver.get(Config.BASE_URL)
            TestHelpers.wait_for_page_load(driver)
            logging.info("Driver setup completed successfully")
            yield driver
        except Exception as e:
            logging.error(f"Driver setup failed: {e}")
            raise
        finally:
            if driver:
                driver.quit()
                logging.info("Driver closed")
    
    @pytest.fixture(scope="class")
    def page_objects(self, setup_driver):
        """Initialize page objects"""
        driver = setup_driver
        return {
            'login': LoginPage(driver),
            'homepage': HomePage(driver),
            'product': ProductPage(driver),
            'cart': CartPage(driver)
        }
    
    def test_complete_shopping_flow(self, setup_driver, page_objects):
        """Complete E2E shopping flow test"""
        driver = setup_driver
        login_page = page_objects['login']
        homepage = page_objects['homepage']
        product_page = page_objects['product']
        cart_page = page_objects['cart']
        
        try:
            # Step 1: Login with created account
            logging.info("Step 1: Logging in with created account")
            assert login_page.login(Config.EMAIL, Config.PASSWORD), "Login failed"
            time.sleep(3)
            
            # Verify login success
            assert login_page.is_logged_in(), "Login verification failed"
            logging.info("Login successful")
            
            # Step 2: Open the homepage
            logging.info("Step 2: Opening homepage")
            driver.get(Config.BASE_URL)
            TestHelpers.wait_for_page_load(driver)
            assert homepage.is_homepage_loaded(), "Homepage not loaded"
            logging.info("Homepage loaded successfully")
            
            # Step 3: Click on the Laptops tab
            logging.info("Step 3: Clicking on Laptops tab")
            assert homepage.click_laptops_tab(), "Failed to click Laptops tab"
            time.sleep(3)
            logging.info("Laptops tab clicked successfully")
            
            # Step 4: Select the Dell Latitude laptop
            logging.info("Step 4: Selecting Dell Latitude laptop")
            laptop_element = TestHelpers.find_product_by_name(driver, "Dell Latitude 7490")
            assert laptop_element is not None, "Dell Latitude laptop not found"
            
            TestHelpers.scroll_to_element(driver, laptop_element)
            laptop_element.click()
            time.sleep(3)
            logging.info("Dell Latitude laptop selected")
            
            # Step 5: Add 1 item to the cart
            logging.info("Step 5: Adding 1 Dell Latitude laptop to cart")
            assert product_page.configure_and_add_to_cart(quantity=1), "Failed to add laptop to cart"
            time.sleep(2)
            logging.info("Laptop added to cart successfully")
            
            # Step 6: Go to the Smartwatches tab
            logging.info("Step 6: Going to Smartwatches tab")
            driver.get(Config.BASE_URL)
            TestHelpers.wait_for_page_load(driver)
            assert homepage.click_smartwatches_tab(), "Failed to click Smartwatches tab"
            time.sleep(3)
            logging.info("Smartwatches tab clicked successfully")
            
            # Step 7: Select the Apple Watch Series 6
            logging.info("Step 7: Selecting Apple Watch Series 6")
            watch_element = TestHelpers.find_product_by_name(driver, "Apple Watch Series 6")
            assert watch_element is not None, "Apple Watch Series 6 not found"
            
            TestHelpers.scroll_to_element(driver, watch_element)
            watch_element.click()
            time.sleep(3)
            logging.info("Apple Watch Series 6 selected")
            
            # Step 8: Configure and add 2 items to the cart
            logging.info("Step 8: Configuring and adding 2 Apple Watches to cart")
            assert product_page.configure_and_add_to_cart(
                quantity=2, 
                color=Config.WATCH_COLOR, 
                size=Config.WATCH_SIZE, 
                connectivity=Config.WATCH_CONNECTIVITY
            ), "Failed to add watches to cart"
            time.sleep(2)
            logging.info("Apple Watches added to cart successfully")
            
            # Step 9: Open the cart → View cart
            logging.info("Step 9: Opening cart and viewing cart")
            assert homepage.click_cart_icon(), "Failed to click cart icon"
            time.sleep(2)
            
            # If there's a "View Cart" button, click it
            if cart_page.is_element_present(cart_page.VIEW_CART_BUTTON):
                assert cart_page.view_cart(), "Failed to view cart"
            time.sleep(3)
            logging.info("Cart opened successfully")
            
            # Verify items in cart
            cart_items = cart_page.get_cart_item_count()
            assert cart_items >= 2, f"Expected at least 2 items in cart, found {cart_items}"
            logging.info(f"Cart contains {cart_items} items")
            
            # Step 10: Remove the laptop
            logging.info("Step 10: Removing the laptop from cart")
            assert cart_page.remove_item_by_name("Dell Latitude"), "Failed to remove laptop"
            time.sleep(2)
            
            # Verify laptop removal
            remaining_items = cart_page.get_cart_item_count()
            assert remaining_items >= 1, "No items remaining after laptop removal"
            logging.info(f"Laptop removed. {remaining_items} items remaining in cart")
            
            # Step 11: Proceed to checkout
            logging.info("Step 11: Proceeding to checkout")
            assert cart_page.proceed_to_checkout(), "Failed to proceed to checkout"
            time.sleep(3)
            logging.info("Checkout process initiated successfully")
            
            # Verify we're on checkout page (URL should contain 'checkout' or similar)
            current_url = driver.current_url.lower()
            assert any(keyword in current_url for keyword in ['checkout', 'payment', 'billing']), \
                f"Not on checkout page. Current URL: {current_url}"
            logging.info("Successfully reached checkout page")
            
            logging.info("E2E test completed successfully!")
            
        except Exception as e:
            logging.error(f"Test failed: {e}")
            TestHelpers.take_screenshot(driver, f"test_failure_{int(time.time())}.png")
            raise
    
    def test_individual_components(self, setup_driver, page_objects):
        """Test individual components separately"""
        driver = setup_driver
        login_page = page_objects['login']
        homepage = page_objects['homepage']
        
        try:
            # Test homepage loading
            logging.info("Testing homepage loading")
            driver.get(Config.BASE_URL)
            TestHelpers.wait_for_page_load(driver)
            assert homepage.is_homepage_loaded(), "Homepage loading test failed"
            logging.info("Homepage loading test passed")
            
            # Test navigation to laptops
            logging.info("Testing navigation to laptops")
            assert homepage.click_laptops_tab(), "Laptops navigation test failed"
            time.sleep(2)
            logging.info("Laptops navigation test passed")
            
            # Test navigation to smartwatches
            logging.info("Testing navigation to smartwatches")
            driver.get(Config.BASE_URL)
            TestHelpers.wait_for_page_load(driver)
            assert homepage.click_smartwatches_tab(), "Smartwatches navigation test failed"
            time.sleep(2)
            logging.info("Smartwatches navigation test passed")
            
        except Exception as e:
            logging.error(f"Component test failed: {e}")
            TestHelpers.take_screenshot(driver, f"component_test_failure_{int(time.time())}.png")
            raise

if __name__ == "__main__":
    # Run the test
    pytest.main([__file__, "-v", "--tb=short"])
