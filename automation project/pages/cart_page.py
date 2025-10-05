from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import logging
import time

class CartPage(BasePage):
    # Locators
    CART_ITEMS = (By.XPATH, "//div[contains(@class, 'cart-item') or contains(@class, 'item')]")
    REMOVE_BUTTON = (By.XPATH, "//button[contains(text(), 'Remove') or contains(@class, 'remove')]")
    QUANTITY_INPUT = (By.XPATH, "//input[@type='number' or contains(@class, 'quantity')]")
    UPDATE_QUANTITY_BUTTON = (By.XPATH, "//button[contains(text(), 'Update') or contains(@class, 'update')]")
    PROCEED_TO_CHECKOUT_BUTTON = (By.XPATH, "//button[contains(text(), 'Checkout') or contains(text(), 'Proceed')]")
    VIEW_CART_BUTTON = (By.XPATH, "//a[contains(text(), 'View Cart') or contains(@href, 'cart')]")
    CART_TOTAL = (By.XPATH, "//span[contains(@class, 'total') or contains(@class, 'subtotal')]")
    PRODUCT_NAME = (By.XPATH, "//a[contains(@class, 'product-name') or contains(@class, 'title')]")
    PRODUCT_PRICE = (By.XPATH, "//span[contains(@class, 'price')]")
    EMPTY_CART_MESSAGE = (By.XPATH, "//div[contains(text(), 'empty') or contains(text(), 'no items')]")
    
    def __init__(self, driver):
        super().__init__(driver)
        
    def get_cart_items(self):
        """Get all cart items"""
        try:
            return self.find_elements(self.CART_ITEMS)
        except Exception as e:
            logging.error(f"Failed to get cart items: {e}")
            return []
            
    def get_cart_item_count(self):
        """Get number of items in cart"""
        try:
            items = self.get_cart_items()
            return len(items)
        except Exception as e:
            logging.error(f"Failed to get cart item count: {e}")
            return 0
            
    def remove_item_by_name(self, product_name):
        """Remove item from cart by product name"""
        try:
            items = self.get_cart_items()
            for item in items:
                try:
                    item_name_element = item.find_element(*self.PRODUCT_NAME)
                    if product_name.lower() in item_name_element.text.lower():
                        remove_button = item.find_element(*self.REMOVE_BUTTON)
                        remove_button.click()
                        time.sleep(2)  # Wait for removal
                        return True
                except:
                    continue
            logging.warning(f"Product '{product_name}' not found in cart")
            return False
        except Exception as e:
            logging.error(f"Failed to remove item: {e}")
            return False
            
    def remove_first_item(self):
        """Remove first item from cart"""
        try:
            items = self.get_cart_items()
            if items:
                remove_button = items[0].find_element(*self.REMOVE_BUTTON)
                remove_button.click()
                time.sleep(2)  # Wait for removal
                return True
            return False
        except Exception as e:
            logging.error(f"Failed to remove first item: {e}")
            return False
            
    def update_item_quantity(self, item_index, new_quantity):
        """Update quantity of specific item"""
        try:
            items = self.get_cart_items()
            if item_index < len(items):
                quantity_input = items[item_index].find_element(*self.QUANTITY_INPUT)
                quantity_input.clear()
                quantity_input.send_keys(str(new_quantity))
                
                # Click update button if available
                try:
                    update_button = items[item_index].find_element(*self.UPDATE_QUANTITY_BUTTON)
                    update_button.click()
                except:
                    pass  # Some sites update automatically
                    
                time.sleep(1)
                return True
            return False
        except Exception as e:
            logging.error(f"Failed to update quantity: {e}")
            return False
            
    def proceed_to_checkout(self):
        """Proceed to checkout"""
        try:
            return self.click_element(self.PROCEED_TO_CHECKOUT_BUTTON)
        except Exception as e:
            logging.error(f"Failed to proceed to checkout: {e}")
            return False
            
    def view_cart(self):
        """Click view cart button"""
        try:
            return self.click_element(self.VIEW_CART_BUTTON)
        except Exception as e:
            logging.error(f"Failed to view cart: {e}")
            return False
            
    def get_cart_total(self):
        """Get cart total amount"""
        try:
            return self.get_text(self.CART_TOTAL)
        except Exception as e:
            logging.error(f"Failed to get cart total: {e}")
            return ""
            
    def is_cart_empty(self):
        """Check if cart is empty"""
        try:
            return self.is_element_present(self.EMPTY_CART_MESSAGE) or self.get_cart_item_count() == 0
        except Exception as e:
            logging.error(f"Failed to check if cart is empty: {e}")
            return False
            
    def get_item_details(self, item_index):
        """Get details of specific cart item"""
        try:
            items = self.get_cart_items()
            if item_index < len(items):
                item = items[item_index]
                name = item.find_element(*self.PRODUCT_NAME).text
                price = item.find_element(*self.PRODUCT_PRICE).text
                return {"name": name, "price": price}
            return None
        except Exception as e:
            logging.error(f"Failed to get item details: {e}")
            return None
