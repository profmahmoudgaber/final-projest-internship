import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class TestHelpers:
    @staticmethod
    def wait_for_page_load(driver, timeout=30):
        """Wait for page to fully load"""
        try:
            WebDriverWait(driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            time.sleep(2)  # Additional wait for dynamic content
            return True
        except TimeoutException:
            logging.warning("Page load timeout")
            return False
    
    @staticmethod
    def find_product_by_name(driver, product_name, timeout=10):
        """Find product by name on the page"""
        try:
            # Try different selectors for product links
            selectors = [
                f"//a[contains(text(), '{product_name}')]",
                f"//h3[contains(text(), '{product_name}')]//parent::a",
                f"//div[contains(@class, 'product')]//a[contains(text(), '{product_name}')]",
                f"//*[contains(text(), '{product_name}')]//ancestor::a"
            ]
            
            for selector in selectors:
                try:
                    element = WebDriverWait(driver, timeout).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    return element
                except TimeoutException:
                    continue
            
            logging.warning(f"Product '{product_name}' not found")
            return None
            
        except Exception as e:
            logging.error(f"Error finding product: {e}")
            return None
    
    @staticmethod
    def scroll_to_element(driver, element):
        """Scroll to element"""
        try:
            driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(1)
            return True
        except Exception as e:
            logging.error(f"Failed to scroll to element: {e}")
            return False
    
    @staticmethod
    def take_screenshot(driver, filename):
        """Take screenshot"""
        try:
            driver.save_screenshot(filename)
            logging.info(f"Screenshot saved: {filename}")
            return True
        except Exception as e:
            logging.error(f"Failed to take screenshot: {e}")
            return False
    
    @staticmethod
    def wait_for_element_clickable(driver, locator, timeout=10):
        """Wait for element to be clickable"""
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            return element
        except TimeoutException:
            logging.error(f"Element not clickable: {locator}")
            return None
    
    @staticmethod
    def wait_for_text_in_element(driver, locator, text, timeout=10):
        """Wait for specific text in element"""
        try:
            WebDriverWait(driver, timeout).until(
                EC.text_to_be_present_in_element(locator, text)
            )
            return True
        except TimeoutException:
            logging.error(f"Text '{text}' not found in element: {locator}")
            return False
    
    @staticmethod
    def handle_popup(driver):
        """Handle common popups"""
        try:
            # Common popup selectors
            popup_selectors = [
                "//button[contains(text(), 'Close')]",
                "//button[contains(@class, 'close')]",
                "//div[contains(@class, 'popup')]//button",
                "//div[contains(@class, 'modal')]//button"
            ]
            
            for selector in popup_selectors:
                try:
                    popup = driver.find_element(By.XPATH, selector)
                    if popup.is_displayed():
                        popup.click()
                        time.sleep(1)
                        break
                except:
                    continue
                    
        except Exception as e:
            logging.warning(f"Error handling popup: {e}")
    
    @staticmethod
    def retry_action(action, max_retries=3, delay=2):
        """Retry an action multiple times"""
        for attempt in range(max_retries):
            try:
                result = action()
                if result:
                    return True
            except Exception as e:
                logging.warning(f"Attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(delay)
        
        logging.error(f"Action failed after {max_retries} attempts")
        return False
