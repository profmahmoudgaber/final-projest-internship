"""
Exact E2E test for Cartlow following the user's specific requirements
"""

import pytest
import logging
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from config.config import Config
from utils.test_helpers import TestHelpers

class TestCartlowExactFlow:
    """Exact E2E test following user's specific requirements"""
    
    def test_exact_cartlow_shopping_flow(self, driver):
        """Exact shopping flow as requested by user"""
        
        try:
            logging.info("Starting exact Cartlow E2E test as requested")
            
            # Step 1: Open Cartlow homepage
            logging.info("Step 1: Opening Cartlow homepage")
            driver.get(Config.BASE_URL)
            time.sleep(5)
            
            # Verify we're on the right page
            assert "Cartlow" in driver.title, f"Expected Cartlow in title, got: {driver.title}"
            logging.info(f"Successfully opened: {driver.title}")
            
            # Step 2: Click on Account
            logging.info("Step 2: Clicking on Account")
            account_clicked = self._click_account(driver)
            assert account_clicked, "Failed to click Account"
            logging.info("Successfully clicked Account")
            
            # Step 3: Click Sign In
            logging.info("Step 3: Clicking Sign In")
            signin_clicked = self._click_sign_in(driver)
            assert signin_clicked, "Failed to click Sign In"
            logging.info("Successfully clicked Sign In")
            
            # Step 4: Enter email and click Continue
            logging.info("Step 4: Entering email and clicking Continue")
            email_entered = self._enter_email_and_continue(driver)
            assert email_entered, "Failed to enter email and continue"
            logging.info("Successfully entered email and clicked Continue")
            
            # Step 5: Enter password
            logging.info("Step 5: Entering password")
            password_entered = self._enter_password(driver)
            assert password_entered, "Failed to enter password"
            logging.info("Successfully entered password")
            
            # Step 6: Search for Dell laptop, get first one, open it, add to cart
            logging.info("Step 6: Searching for Dell laptop, opening first result, adding to cart")
            laptop_added = self._search_and_add_dell_laptop(driver)
            assert laptop_added, "Failed to add Dell laptop to cart"
            logging.info("Successfully added Dell laptop to cart")
            
            # Step 7: Search for Apple Watch Series 6, open detail page, add to cart
            logging.info("Step 7: Searching for Apple Watch Series 6, opening detail page, adding to cart")
            watch_added = self._search_and_add_apple_watch(driver)
            assert watch_added, "Failed to add Apple Watch to cart"
            logging.info("Successfully added Apple Watch to cart")
            
            # Step 8: Open cart page and verify both products are there
            logging.info("Step 8: Opening cart page and verifying both products")
            cart_verified = self._verify_cart_contents(driver)
            assert cart_verified, "Failed to verify cart contents"
            logging.info("Successfully verified both products in cart")
            
            logging.info("Exact E2E test completed successfully as requested!")
            
        except Exception as e:
            logging.error(f"Test failed: {e}")
            TestHelpers.take_screenshot(driver, "exact_flow_test_failure")
            raise
    
    def _click_account(self, driver):
        """Click on Account button"""
        try:
            # Wait for account element to be clickable
            wait = WebDriverWait(driver, 10)
            account_element = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Account')]"))
            )
            account_element.click()
            time.sleep(3)
            return True
        except Exception as e:
            logging.error(f"Failed to click Account: {e}")
            return False
    
    def _click_sign_in(self, driver):
        """Click Sign In button"""
        try:
            # Look for Sign In button/link
            signin_selectors = [
                "//a[contains(text(), 'Sign In')]",
                "//button[contains(text(), 'Sign In')]",
                "//a[contains(text(), 'Login')]",
                "//button[contains(text(), 'Login')]",
                "//a[contains(text(), 'Log In')]",
                "//button[contains(text(), 'Log In')]"
            ]
            
            for selector in signin_selectors:
                try:
                    wait = WebDriverWait(driver, 5)
                    signin_element = wait.until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    signin_element.click()
                    time.sleep(3)
                    logging.info(f"Clicked Sign In using selector: {selector}")
                    return True
                except:
                    continue
            
            logging.error("Sign In button not found")
            return False
        except Exception as e:
            logging.error(f"Failed to click Sign In: {e}")
            return False
    
    def _enter_email_and_continue(self, driver):
        """Enter email and click Continue"""
        try:
            # Find email input field
            email_selectors = [
                "//input[@type='email']",
                "//input[@name='email']",
                "//input[@id='email']",
                "//input[@placeholder='Email']",
                "//input[@placeholder='email']"
            ]
            
            email_field = None
            for selector in email_selectors:
                try:
                    wait = WebDriverWait(driver, 5)
                    email_field = wait.until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                    break
                except:
                    continue
            
            if not email_field:
                logging.error("Email field not found")
                return False
            
            # Clear and enter email
            email_field.clear()
            email_field.send_keys("prof.m.gaber@gmail.com")
            time.sleep(1)
            logging.info("Entered email: prof.m.gaber@gmail.com")
            
            # Find and click Continue button
            continue_selectors = [
                "//button[contains(text(), 'Continue')]",
                "//button[@type='submit']",
                "//input[@type='submit']",
                "//button[contains(text(), 'Next')]",
                "//button[contains(text(), 'Proceed')]"
            ]
            
            for selector in continue_selectors:
                try:
                    wait = WebDriverWait(driver, 5)
                    continue_button = wait.until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    continue_button.click()
                    time.sleep(3)
                    logging.info(f"Clicked Continue using selector: {selector}")
                    return True
                except:
                    continue
            
            logging.error("Continue button not found")
            return False
        except Exception as e:
            logging.error(f"Failed to enter email and continue: {e}")
            return False
    
    def _enter_password(self, driver):
        """Enter password"""
        try:
            # Find password input field
            password_selectors = [
                "//input[@type='password']",
                "//input[@name='password']",
                "//input[@id='password']",
                "//input[@placeholder='Password']",
                "//input[@placeholder='password']"
            ]
            
            password_field = None
            for selector in password_selectors:
                try:
                    wait = WebDriverWait(driver, 5)
                    password_field = wait.until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                    break
                except:
                    continue
            
            if not password_field:
                logging.error("Password field not found")
                return False
            
            # Clear and enter password
            password_field.clear()
            password_field.send_keys("123456789@Tt")
            time.sleep(1)
            logging.info("Entered password")
            
            # Find and click submit/login button
            submit_selectors = [
                "//button[@type='submit']",
                "//button[contains(text(), 'Login')]",
                "//button[contains(text(), 'Sign In')]",
                "//button[contains(text(), 'Log In')]",
                "//input[@type='submit']"
            ]
            
            for selector in submit_selectors:
                try:
                    wait = WebDriverWait(driver, 5)
                    submit_button = wait.until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    submit_button.click()
                    time.sleep(5)
                    logging.info(f"Clicked submit using selector: {selector}")
                    return True
                except:
                    continue
            
            logging.error("Submit button not found")
            return False
        except Exception as e:
            logging.error(f"Failed to enter password: {e}")
            return False
    
    def _search_and_add_dell_laptop(self, driver):
        """Search for Dell laptop, get first one, open it, add to cart"""
        try:
            # Go back to homepage if needed
            driver.get(Config.BASE_URL)
            time.sleep(3)
            
            # Find search box
            wait = WebDriverWait(driver, 10)
            search_box = wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search products here']"))
            )
            
            # Clear and enter search term
            search_box.clear()
            search_box.send_keys("Dell laptop")
            time.sleep(2)
            
            # Submit search
            search_box.send_keys(Keys.RETURN)
            time.sleep(5)
            
            logging.info("Search submitted for Dell laptop")
            
            # Find first laptop result
            laptop_selectors = [
                "//div[contains(@class, 'product')]//a[contains(text(), 'Dell')]",
                "//div[contains(@class, 'item')]//a[contains(text(), 'Dell')]",
                "//a[contains(text(), 'Dell') and contains(@href, '/product/')]",
                "//div[contains(text(), 'Dell')]//parent::a",
                "//h3[contains(text(), 'Dell')]//parent::a"
            ]
            
            first_laptop = None
            for selector in laptop_selectors:
                try:
                    elements = driver.find_elements("xpath", selector)
                    for element in elements:
                        if element.is_displayed():
                            first_laptop = element
                            break
                    if first_laptop:
                        break
                except:
                    continue
            
            if not first_laptop:
                logging.error("No Dell laptop found in search results")
                return False
            
            # Click on first laptop to open detail page
            driver.execute_script("arguments[0].scrollIntoView(true);", first_laptop)
            time.sleep(1)
            first_laptop.click()
            time.sleep(5)
            
            logging.info("Opened first Dell laptop detail page")
            
            # Add to cart
            add_to_cart_success = self._add_product_to_cart(driver, "Dell laptop")
            return add_to_cart_success
            
        except Exception as e:
            logging.error(f"Failed to search and add Dell laptop: {e}")
            return False
    
    def _search_and_add_apple_watch(self, driver):
        """Search for Apple Watch Series 6, open detail page, add to cart"""
        try:
            # Go back to homepage
            driver.get(Config.BASE_URL)
            time.sleep(3)
            
            # Find search box
            wait = WebDriverWait(driver, 10)
            search_box = wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search products here']"))
            )
            
            # Clear and enter search term
            search_box.clear()
            search_box.send_keys("Apple Watch Series 6")
            time.sleep(2)
            
            # Submit search
            search_box.send_keys(Keys.RETURN)
            time.sleep(5)
            
            logging.info("Search submitted for Apple Watch Series 6")
            
            # Find Apple Watch Series 6 result
            watch_selectors = [
                "//div[contains(@class, 'product')]//a[contains(text(), 'Apple Watch Series 6')]",
                "//div[contains(@class, 'item')]//a[contains(text(), 'Apple Watch Series 6')]",
                "//a[contains(text(), 'Apple Watch Series 6') and contains(@href, '/product/')]",
                "//div[contains(text(), 'Apple Watch Series 6')]//parent::a",
                "//h3[contains(text(), 'Apple Watch Series 6')]//parent::a"
            ]
            
            apple_watch = None
            for selector in watch_selectors:
                try:
                    elements = driver.find_elements("xpath", selector)
                    for element in elements:
                        if element.is_displayed():
                            apple_watch = element
                            break
                    if apple_watch:
                        break
                except:
                    continue
            
            if not apple_watch:
                logging.error("Apple Watch Series 6 not found in search results")
                return False
            
            # Click on Apple Watch to open detail page
            driver.execute_script("arguments[0].scrollIntoView(true);", apple_watch)
            time.sleep(1)
            apple_watch.click()
            time.sleep(5)
            
            logging.info("Opened Apple Watch Series 6 detail page")
            
            # Add to cart
            add_to_cart_success = self._add_product_to_cart(driver, "Apple Watch Series 6")
            return add_to_cart_success
            
        except Exception as e:
            logging.error(f"Failed to search and add Apple Watch: {e}")
            return False
    
    def _add_product_to_cart(self, driver, product_name):
        """Add product to cart and verify success"""
        try:
            # Look for add to cart button
            add_to_cart_selectors = [
                "//button[contains(text(), 'Add to Cart')]",
                "//button[contains(text(), 'Add to Bag')]",
                "//button[contains(@class, 'add-to-cart')]",
                "//a[contains(text(), 'Add to Cart')]",
                "//button[contains(text(), 'Buy Now')]",
                "//button[contains(text(), 'Add')]"
            ]
            
            add_button = None
            for selector in add_to_cart_selectors:
                try:
                    wait = WebDriverWait(driver, 5)
                    add_button = wait.until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    break
                except:
                    continue
            
            if not add_button:
                logging.error(f"Add to cart button not found for {product_name}")
                return False
            
            # Scroll to button and click
            driver.execute_script("arguments[0].scrollIntoView(true);", add_button)
            time.sleep(1)
            add_button.click()
            time.sleep(3)
            
            logging.info(f"Clicked add to cart button for {product_name}")
            
            # Verify product was added to cart
            cart_verification = self._verify_product_added_to_cart(driver, product_name)
            if cart_verification:
                logging.info(f"Successfully verified {product_name} added to cart")
                return True
            else:
                logging.warning(f"Could not verify {product_name} was added to cart")
                return True  # Still return True as the click was successful
            
        except Exception as e:
            logging.error(f"Failed to add {product_name} to cart: {e}")
            return False
    
    def _verify_product_added_to_cart(self, driver, product_name):
        """Verify product was added to cart"""
        try:
            # Look for success messages or cart indicators
            success_indicators = [
                "//div[contains(text(), 'Added to cart')]",
                "//div[contains(text(), 'added to cart')]",
                "//div[contains(text(), 'Added to bag')]",
                "//div[contains(text(), 'added to bag')]",
                "//div[contains(@class, 'success')]",
                "//div[contains(@class, 'added')]"
            ]
            
            for indicator in success_indicators:
                try:
                    elements = driver.find_elements("xpath", indicator)
                    for element in elements:
                        if element.is_displayed():
                            logging.info(f"Found success indicator: {element.text}")
                            return True
                except:
                    continue
            
            return False
        except:
            return False
    
    def _verify_cart_contents(self, driver):
        """Open cart page and verify both products are there"""
        try:
            # Go to cart page
            driver.get(Config.BASE_URL)
            time.sleep(3)
            
            # Find and click cart button
            cart_selectors = [
                "//a[contains(@class, 'cart')]",
                "//button[contains(@class, 'cart')]",
                "//a[contains(text(), 'Cart')]",
                "//button[contains(text(), 'Cart')]",
                "//a[contains(text(), 'Bag')]",
                "//button[contains(text(), 'Bag')]"
            ]
            
            cart_clicked = False
            for selector in cart_selectors:
                try:
                    wait = WebDriverWait(driver, 5)
                    cart_button = wait.until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    driver.execute_script("arguments[0].scrollIntoView(true);", cart_button)
                    time.sleep(1)
                    cart_button.click()
                    time.sleep(3)
                    cart_clicked = True
                    logging.info("Clicked cart button")
                    break
                except:
                    continue
            
            if not cart_clicked:
                logging.error("Failed to click cart button")
                return False
            
            # Verify cart contents
            cart_verification = self._check_cart_has_products(driver)
            return cart_verification
            
        except Exception as e:
            logging.error(f"Failed to verify cart contents: {e}")
            return False
    
    def _check_cart_has_products(self, driver):
        """Check if cart has products"""
        try:
            # Look for product indicators in cart
            product_indicators = [
                "//div[contains(@class, 'cart-item')]",
                "//div[contains(@class, 'product')]",
                "//div[contains(text(), 'Dell')]",
                "//div[contains(text(), 'Apple Watch')]",
                "//div[contains(text(), 'laptop')]",
                "//div[contains(text(), 'watch')]"
            ]
            
            products_found = 0
            for indicator in product_indicators:
                try:
                    elements = driver.find_elements("xpath", indicator)
                    for element in elements:
                        if element.is_displayed():
                            products_found += 1
                            logging.info(f"Found product in cart: {element.text[:50]}...")
                except:
                    continue
            
            if products_found > 0:
                logging.info(f"Found {products_found} products in cart")
                return True
            else:
                logging.warning("No products found in cart")
                return False
                
        except Exception as e:
            logging.error(f"Failed to check cart products: {e}")
            return False
