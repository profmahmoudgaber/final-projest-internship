from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import logging

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)
        self.actions = ActionChains(driver)
        
    def find_element(self, locator):
        """Find element with explicit wait"""
        try:
            return self.wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            logging.error(f"Element not found: {locator}")
            raise
            
    def find_elements(self, locator):
        """Find multiple elements"""
        try:
            return self.wait.until(EC.presence_of_all_elements_located(locator))
        except TimeoutException:
            logging.error(f"Elements not found: {locator}")
            return []
            
    def click_element(self, locator):
        """Click element with explicit wait"""
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
            return True
        except TimeoutException:
            logging.error(f"Element not clickable: {locator}")
            return False
            
    def send_keys(self, locator, text):
        """Send keys to element"""
        try:
            element = self.find_element(locator)
            element.clear()
            element.send_keys(text)
            return True
        except TimeoutException:
            logging.error(f"Could not send keys to element: {locator}")
            return False
            
    def get_text(self, locator):
        """Get text from element"""
        try:
            element = self.find_element(locator)
            return element.text
        except TimeoutException:
            logging.error(f"Could not get text from element: {locator}")
            return ""
            
    def is_element_present(self, locator):
        """Check if element is present"""
        try:
            self.find_element(locator)
            return True
        except TimeoutException:
            return False
            
    def wait_for_element_visible(self, locator, timeout=10):
        """Wait for element to be visible"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
            
    def scroll_to_element(self, locator):
        """Scroll to element"""
        try:
            element = self.find_element(locator)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(1)
            return True
        except TimeoutException:
            return False
            
    def hover_element(self, locator):
        """Hover over element"""
        try:
            element = self.find_element(locator)
            self.actions.move_to_element(element).perform()
            return True
        except TimeoutException:
            return False
            
    def get_current_url(self):
        """Get current URL"""
        return self.driver.current_url
        
    def navigate_to(self, url):
        """Navigate to URL"""
        self.driver.get(url)
        
    def refresh_page(self):
        """Refresh current page"""
        self.driver.refresh()
        
    def go_back(self):
        """Go back to previous page"""
        self.driver.back()
        
    def switch_to_window(self, window_index):
        """Switch to window by index"""
        windows = self.driver.window_handles
        if window_index < len(windows):
            self.driver.switch_to.window(windows[window_index])
            return True
        return False
