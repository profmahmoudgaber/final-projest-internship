from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import logging
import time

class ProductPage(BasePage):
    # Locators
    PRODUCT_TITLE = (By.XPATH, "//h1[contains(@class, 'product-title') or contains(@class, 'title')]")
    ADD_TO_CART_BUTTON = (By.XPATH, "//button[contains(text(), 'Add to Cart') or contains(@class, 'add-to-cart')]")
    QUANTITY_INPUT = (By.XPATH, "//input[@type='number' or contains(@class, 'quantity')]")
    QUANTITY_PLUS = (By.XPATH, "//button[contains(@class, 'plus') or contains(@class, 'increase')]")
    QUANTITY_MINUS = (By.XPATH, "//button[contains(@class, 'minus') or contains(@class, 'decrease')]")
    PRODUCT_OPTIONS = (By.XPATH, "//div[contains(@class, 'option') or contains(@class, 'variant')]")
    COLOR_OPTIONS = (By.XPATH, "//div[contains(@class, 'color')]//button")
    SIZE_OPTIONS = (By.XPATH, "//div[contains(@class, 'size')]//button")
    CONNECTIVITY_OPTIONS = (By.XPATH, "//div[contains(@class, 'connectivity')]//button")
    PRICE = (By.XPATH, "//span[contains(@class, 'price') or contains(@class, 'cost')]")
    CART_COUNT = (By.XPATH, "//span[contains(@class, 'cart-count') or contains(@class, 'badge')]")
    
    def __init__(self, driver):
        super().__init__(driver)
        
    def get_product_title(self):
        """Get product title"""
        try:
            return self.get_text(self.PRODUCT_TITLE)
        except Exception as e:
            logging.error(f"Failed to get product title: {e}")
            return ""
            
    def select_color(self, color):
        """Select product color"""
        try:
            color_buttons = self.find_elements(self.COLOR_OPTIONS)
            for button in color_buttons:
                if color.lower() in button.get_attribute("title").lower() or color.lower() in button.text.lower():
                    button.click()
                    time.sleep(1)
                    return True
            logging.warning(f"Color '{color}' not found")
            return False
        except Exception as e:
            logging.error(f"Failed to select color: {e}")
            return False
            
    def select_size(self, size):
        """Select product size"""
        try:
            size_buttons = self.find_elements(self.SIZE_OPTIONS)
            for button in size_buttons:
                if size in button.text or size in button.get_attribute("value"):
                    button.click()
                    time.sleep(1)
                    return True
            logging.warning(f"Size '{size}' not found")
            return False
        except Exception as e:
            logging.error(f"Failed to select size: {e}")
            return False
            
    def select_connectivity(self, connectivity):
        """Select connectivity option"""
        try:
            connectivity_buttons = self.find_elements(self.CONNECTIVITY_OPTIONS)
            for button in connectivity_buttons:
                if connectivity.lower() in button.text.lower():
                    button.click()
                    time.sleep(1)
                    return True
            logging.warning(f"Connectivity '{connectivity}' not found")
            return False
        except Exception as e:
            logging.error(f"Failed to select connectivity: {e}")
            return False
            
    def set_quantity(self, quantity):
        """Set product quantity"""
        try:
            # Try to find quantity input first
            if self.is_element_present(self.QUANTITY_INPUT):
                return self.send_keys(self.QUANTITY_INPUT, str(quantity))
            else:
                # Use plus/minus buttons
                current_qty = 1
                if quantity > current_qty:
                    for _ in range(quantity - current_qty):
                        self.click_element(self.QUANTITY_PLUS)
                        time.sleep(0.5)
                elif quantity < current_qty:
                    for _ in range(current_qty - quantity):
                        self.click_element(self.QUANTITY_MINUS)
                        time.sleep(0.5)
                return True
        except Exception as e:
            logging.error(f"Failed to set quantity: {e}")
            return False
            
    def add_to_cart(self):
        """Add product to cart"""
        try:
            if self.click_element(self.ADD_TO_CART_BUTTON):
                time.sleep(2)  # Wait for cart update
                return True
            return False
        except Exception as e:
            logging.error(f"Failed to add to cart: {e}")
            return False
            
    def get_cart_count(self):
        """Get current cart count"""
        try:
            count_text = self.get_text(self.CART_COUNT)
            return int(count_text) if count_text.isdigit() else 0
        except Exception as e:
            logging.error(f"Failed to get cart count: {e}")
            return 0
            
    def get_product_price(self):
        """Get product price"""
        try:
            return self.get_text(self.PRICE)
        except Exception as e:
            logging.error(f"Failed to get product price: {e}")
            return ""
            
    def configure_and_add_to_cart(self, quantity=1, color=None, size=None, connectivity=None):
        """Configure product options and add to cart"""
        try:
            # Select options if provided
            if color:
                self.select_color(color)
            if size:
                self.select_size(size)
            if connectivity:
                self.select_connectivity(connectivity)
                
            # Set quantity
            self.set_quantity(quantity)
            
            # Add to cart
            return self.add_to_cart()
        except Exception as e:
            logging.error(f"Failed to configure and add to cart: {e}")
            return False
