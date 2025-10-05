from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import logging

class HomePage(BasePage):
    # Locators
    LAPTOPS_TAB = (By.XPATH, "//a[contains(text(), 'Laptops') or contains(@href, 'laptop')]")
    SMARTWATCHES_TAB = (By.XPATH, "//a[contains(text(), 'Smartwatches') or contains(text(), 'Smart Watch') or contains(@href, 'smartwatch')]")
    CART_ICON = (By.XPATH, "//a[contains(@href, 'cart') or contains(@class, 'cart')]")
    SEARCH_BOX = (By.XPATH, "//input[@type='search' or @placeholder='Search']")
    SEARCH_BUTTON = (By.XPATH, "//button[contains(@class, 'search') or @type='submit']")
    CATEGORY_MENU = (By.XPATH, "//div[contains(@class, 'category') or contains(@class, 'menu')]")
    
    def __init__(self, driver):
        super().__init__(driver)
        
    def click_laptops_tab(self):
        """Click on Laptops tab"""
        try:
            return self.click_element(self.LAPTOPS_TAB)
        except Exception as e:
            logging.error(f"Failed to click laptops tab: {e}")
            return False
            
    def click_smartwatches_tab(self):
        """Click on Smartwatches tab"""
        try:
            return self.click_element(self.SMARTWATCHES_TAB)
        except Exception as e:
            logging.error(f"Failed to click smartwatches tab: {e}")
            return False
            
    def click_cart_icon(self):
        """Click on cart icon"""
        try:
            return self.click_element(self.CART_ICON)
        except Exception as e:
            logging.error(f"Failed to click cart icon: {e}")
            return False
            
    def search_product(self, product_name):
        """Search for a product"""
        try:
            if self.send_keys(self.SEARCH_BOX, product_name):
                return self.click_element(self.SEARCH_BUTTON)
            return False
        except Exception as e:
            logging.error(f"Failed to search product: {e}")
            return False
            
    def is_homepage_loaded(self):
        """Check if homepage is loaded"""
        try:
            return self.is_element_present(self.CATEGORY_MENU)
        except Exception as e:
            logging.error(f"Failed to verify homepage load: {e}")
            return False
