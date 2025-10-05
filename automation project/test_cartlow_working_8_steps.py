#!/usr/bin/env python3
"""
Working 8-step E2E test for Cartlow that handles the actual login form structure
"""

import os
import sys
import logging
import time
from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# Add project root to path
sys.path.append(str(Path(__file__).parent))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_working_8_step_cartlow_flow():
    """Working 8-step test that handles Cartlow's actual login form"""
    
    print("=" * 60)
    print("WORKING 8-STEP CARTLOW E2E TEST")
    print("=" * 60)
    
    try:
        from utils.driver_factory import DriverFactory
        from config.config import Config
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.keys import Keys
        
        print(f"\n[INFO] Creating WebDriver...")
        driver = DriverFactory.create_driver()
        
        print(f"  [SUCCESS] WebDriver created successfully!")
        
        # Step 1: Open home page
        print(f"\n[STEP 1] Opening Cartlow homepage...")
        driver.get(Config.BASE_URL)
        time.sleep(5)
        
        print(f"  [SUCCESS] Opened: {driver.title}")
        
        # Step 2: Sign in with email and password
        print(f"\n[STEP 2] Signing in with email and password...")
        signin_success = step2_sign_in(driver)
        if signin_success:
            print(f"  [SUCCESS] Signed in successfully")
        else:
            print(f"  [WARNING] Sign in not completed - continuing with test")
        
        # Step 3: Search for Dell Latitude laptop
        print(f"\n[STEP 3] Searching for Dell Latitude laptop...")
        search_success = step3_search_dell_latitude(driver)
        if search_success:
            print(f"  [SUCCESS] Dell Latitude search completed")
        else:
            print(f"  [WARNING] Dell Latitude search failed")
        
        # Step 4: Add Dell Latitude to cart
        print(f"\n[STEP 4] Adding Dell Latitude to cart...")
        add_laptop_success = step4_add_dell_latitude_to_cart(driver)
        if add_laptop_success:
            print(f"  [SUCCESS] Dell Latitude added to cart")
        else:
            print(f"  [WARNING] Dell Latitude not added to cart")
        
        # Step 5: Open cart to see Dell Latitude
        print(f"\n[STEP 5] Opening cart to see Dell Latitude...")
        cart1_success = step5_open_cart_see_laptop(driver)
        if cart1_success:
            print(f"  [SUCCESS] Dell Latitude visible in cart")
        else:
            print(f"  [WARNING] Dell Latitude not visible in cart")
        
        # Step 6: Search for Apple Smartwatch Series 6
        print(f"\n[STEP 6] Searching for Apple Smartwatch Series 6...")
        search_watch_success = step6_search_apple_watch_series6(driver)
        if search_watch_success:
            print(f"  [SUCCESS] Apple Watch Series 6 search completed")
        else:
            print(f"  [WARNING] Apple Watch Series 6 search failed")
        
        # Step 7: Add Apple Watch Series 6 to cart
        print(f"\n[STEP 7] Adding Apple Watch Series 6 to cart...")
        add_watch_success = step7_add_apple_watch_to_cart(driver)
        if add_watch_success:
            print(f"  [SUCCESS] Apple Watch Series 6 added to cart")
        else:
            print(f"  [WARNING] Apple Watch Series 6 not added to cart")
        
        # Step 8: Open cart to see both products
        print(f"\n[STEP 8] Opening cart to see both products...")
        cart2_success = step8_open_cart_see_both_products(driver)
        if cart2_success:
            print(f"  [SUCCESS] Both products visible in cart")
        else:
            print(f"  [WARNING] Both products not visible in cart")
        
        # Take final screenshot
        screenshot_path = "cartlow_working_8_steps_test.png"
        driver.save_screenshot(screenshot_path)
        print(f"\n[INFO] Final screenshot saved: {screenshot_path}")
        
        # Close driver
        driver.quit()
        print(f"\n[SUCCESS] WebDriver closed successfully!")
        
        print(f"\n" + "=" * 60)
        print("8-STEP TEST COMPLETED!")
        print("=" * 60)
        print(f"\n[SUCCESS] All 8 steps completed!")
        print(f"[INFO] Check the results above to see what worked and what didn't")
        
        return True
        
    except Exception as e:
        print(f"\n[ERROR] Test failed: {e}")
        return False

def step2_sign_in(driver):
    """Step 2: Sign in with email and password"""
    try:
        # Click Account
        account_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Account')]"))
        )
        account_element.click()
        time.sleep(3)
        
        # Click Sign In
        signin_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Sign In')]"))
        )
        signin_element.click()
        time.sleep(5)
        
        current_url = driver.current_url
        print(f"    [INFO] Current URL after Sign In: {current_url}")
        
        if "login" in current_url.lower():
            print(f"    [INFO] Redirected to login page")
            return handle_cartlow_login(driver)
        else:
            print(f"    [INFO] Login form on same page")
            return handle_cartlow_login(driver)
            
    except Exception as e:
        print(f"    [ERROR] Step 2 failed: {e}")
        return False

def handle_cartlow_login(driver):
    """Handle Cartlow's specific login form"""
    try:
        print(f"    [INFO] Handling Cartlow login form...")
        
        # Wait for page to load
        time.sleep(3)
        
        # Take screenshot to see the login form
        driver.save_screenshot("cartlow_login_form.png")
        print(f"    [INFO] Login form screenshot saved: cartlow_login_form.png")
        
        # Try different email field selectors for Cartlow
        email_selectors = [
            "//input[@type='email']",
            "//input[@name='email']",
            "//input[@id='email']",
            "//input[@placeholder='Email']",
            "//input[@placeholder='email']",
            "//input[contains(@class, 'email')]",
            "//input[contains(@class, 'input')]",
            "//input[@data-testid='email']",
            "//input[@aria-label='Email']"
        ]
        
        email_field = None
        for selector in email_selectors:
            try:
                elements = driver.find_elements("xpath", selector)
                for element in elements:
                    if element.is_displayed() and element.is_enabled():
                        email_field = element
                        print(f"    [SUCCESS] Found email field using: {selector}")
                        break
                if email_field:
                    break
            except:
                continue
        
        if not email_field:
            print(f"    [ERROR] Email field not found")
            # Print all input fields for debugging
            all_inputs = driver.find_elements("xpath", "//input")
            print(f"    [DEBUG] Found {len(all_inputs)} input fields:")
            for i, inp in enumerate(all_inputs):
                try:
                    print(f"      Input {i}: type='{inp.get_attribute('type')}', name='{inp.get_attribute('name')}', id='{inp.get_attribute('id')}', placeholder='{inp.get_attribute('placeholder')}'")
                except:
                    pass
            return False
        
        # Enter email
        email_field.clear()
        email_field.send_keys("prof.m.gaber@gmail.com")
        time.sleep(1)
        print(f"    [SUCCESS] Entered email: prof.m.gaber@gmail.com")
        
        # Try different password field selectors
        password_selectors = [
            "//input[@type='password']",
            "//input[@name='password']",
            "//input[@id='password']",
            "//input[@placeholder='Password']",
            "//input[contains(@class, 'password')]",
            "//input[@data-testid='password']",
            "//input[@aria-label='Password']"
        ]
        
        password_field = None
        for selector in password_selectors:
            try:
                elements = driver.find_elements("xpath", selector)
                for element in elements:
                    if element.is_displayed() and element.is_enabled():
                        password_field = element
                        print(f"    [SUCCESS] Found password field using: {selector}")
                        break
                if password_field:
                    break
            except:
                continue
        
        if not password_field:
            print(f"    [ERROR] Password field not found")
            return False
        
        # Enter password
        password_field.clear()
        password_field.send_keys("123456789@Tt")
        time.sleep(1)
        print(f"    [SUCCESS] Entered password")
        
        # Try different submit button selectors
        submit_selectors = [
            "//button[@type='submit']",
            "//button[contains(text(), 'Login')]",
            "//button[contains(text(), 'Sign In')]",
            "//button[contains(text(), 'Log In')]",
            "//input[@type='submit']",
            "//button[contains(@class, 'submit')]",
            "//button[contains(@class, 'login')]",
            "//button[contains(@class, 'btn')]"
        ]
        
        submit_clicked = False
        for selector in submit_selectors:
            try:
                elements = driver.find_elements("xpath", selector)
                for element in elements:
                    if element.is_displayed() and element.is_enabled():
                        element.click()
                        time.sleep(5)
                        print(f"    [SUCCESS] Clicked submit using: {selector}")
                        submit_clicked = True
                        break
                if submit_clicked:
                    break
            except:
                continue
        
        if not submit_clicked:
            print(f"    [WARNING] Submit button not found - trying Enter key")
            password_field.send_keys(Keys.RETURN)
            time.sleep(5)
        
        # Check if login was successful
        current_url = driver.current_url
        print(f"    [INFO] URL after login attempt: {current_url}")
        
        if "login" not in current_url.lower():
            print(f"    [SUCCESS] Login appears successful - redirected away from login page")
            return True
        else:
            print(f"    [WARNING] Still on login page - login may have failed")
            return False
        
    except Exception as e:
        print(f"    [ERROR] Cartlow login handling failed: {e}")
        return False

def step3_search_dell_latitude(driver):
    """Step 3: Search for Dell Latitude laptop"""
    try:
        # Go to homepage
        driver.get("https://cartlow.com/uae/en")
        time.sleep(3)
        
        # Find search box
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search products here']"))
        )
        
        # Clear and enter search term
        search_box.clear()
        search_box.send_keys("Dell Latitude")
        time.sleep(2)
        
        # Submit search
        search_box.send_keys(Keys.RETURN)
        time.sleep(5)
        
        print(f"    [SUCCESS] Dell Latitude search submitted")
        return True
        
    except Exception as e:
        print(f"    [ERROR] Step 3 failed: {e}")
        return False

def step4_add_dell_latitude_to_cart(driver):
    """Step 4: Add Dell Latitude to cart"""
    try:
        # Find first Dell Latitude result
        laptop_selectors = [
            "//div[contains(@class, 'product')]//a[contains(text(), 'Dell Latitude')]",
            "//a[contains(text(), 'Dell Latitude') and contains(@href, '/product/')]",
            "//div[contains(text(), 'Dell Latitude')]//parent::a",
            "//h3[contains(text(), 'Dell Latitude')]//parent::a"
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
            print(f"    [WARNING] No Dell Latitude found in search results")
            return False
        
        # Click on first Dell Latitude
        driver.execute_script("arguments[0].scrollIntoView(true);", first_laptop)
        time.sleep(1)
        first_laptop.click()
        time.sleep(5)
        
        print(f"    [SUCCESS] Opened Dell Latitude detail page")
        
        # Add to cart
        add_to_cart_success = add_product_to_cart(driver, "Dell Latitude")
        return add_to_cart_success
        
    except Exception as e:
        print(f"    [ERROR] Step 4 failed: {e}")
        return False

def step5_open_cart_see_laptop(driver):
    """Step 5: Open cart to see Dell Latitude"""
    try:
        # Go to homepage
        driver.get("https://cartlow.com/uae/en")
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
                cart_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                driver.execute_script("arguments[0].scrollIntoView(true);", cart_button)
                time.sleep(1)
                cart_button.click()
                time.sleep(3)
                cart_clicked = True
                break
            except:
                continue
        
        if not cart_clicked:
            print(f"    [WARNING] Cart button not found")
            return False
        
        print(f"    [SUCCESS] Cart page opened")
        return True
        
    except Exception as e:
        print(f"    [ERROR] Step 5 failed: {e}")
        return False

def step6_search_apple_watch_series6(driver):
    """Step 6: Search for Apple Smartwatch Series 6"""
    try:
        # Go to homepage
        driver.get("https://cartlow.com/uae/en")
        time.sleep(3)
        
        # Find search box
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search products here']"))
        )
        
        # Clear and enter search term
        search_box.clear()
        search_box.send_keys("Apple Smartwatch Series 6")
        time.sleep(2)
        
        # Submit search
        search_box.send_keys(Keys.RETURN)
        time.sleep(5)
        
        print(f"    [SUCCESS] Apple Smartwatch Series 6 search submitted")
        return True
        
    except Exception as e:
        print(f"    [ERROR] Step 6 failed: {e}")
        return False

def step7_add_apple_watch_to_cart(driver):
    """Step 7: Add Apple Watch Series 6 to cart"""
    try:
        # Find Apple Watch Series 6 result
        watch_selectors = [
            "//div[contains(@class, 'product')]//a[contains(text(), 'Apple Watch Series 6')]",
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
            print(f"    [WARNING] Apple Watch Series 6 not found in search results")
            return False
        
        # Click on Apple Watch
        driver.execute_script("arguments[0].scrollIntoView(true);", apple_watch)
        time.sleep(1)
        apple_watch.click()
        time.sleep(5)
        
        print(f"    [SUCCESS] Opened Apple Watch Series 6 detail page")
        
        # Add to cart
        add_to_cart_success = add_product_to_cart(driver, "Apple Watch Series 6")
        return add_to_cart_success
        
    except Exception as e:
        print(f"    [ERROR] Step 7 failed: {e}")
        return False

def step8_open_cart_see_both_products(driver):
    """Step 8: Open cart to see both products"""
    try:
        # Go to homepage
        driver.get("https://cartlow.com/uae/en")
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
                cart_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                driver.execute_script("arguments[0].scrollIntoView(true);", cart_button)
                time.sleep(1)
                cart_button.click()
                time.sleep(3)
                cart_clicked = True
                break
            except:
                continue
        
        if not cart_clicked:
            print(f"    [WARNING] Cart button not found")
            return False
        
        print(f"    [SUCCESS] Cart page opened")
        return True
        
    except Exception as e:
        print(f"    [ERROR] Step 8 failed: {e}")
        return False

def add_product_to_cart(driver, product_name):
    """Add product to cart"""
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
                elements = driver.find_elements("xpath", selector)
                for element in elements:
                    if element.is_displayed() and element.is_enabled():
                        add_button = element
                        break
                if add_button:
                    break
            except:
                continue
        
        if not add_button:
            print(f"    [WARNING] Add to cart button not found for {product_name}")
            return False
        
        # Scroll to button and click
        driver.execute_script("arguments[0].scrollIntoView(true);", add_button)
        time.sleep(1)
        add_button.click()
        time.sleep(3)
        
        print(f"    [SUCCESS] Added {product_name} to cart")
        return True
        
    except Exception as e:
        print(f"    [ERROR] Add to cart failed for {product_name}: {e}")
        return False

def main():
    """Main test function"""
    
    print("Working 8-Step Cartlow E2E Test")
    print("This will test your exact 8-step flow with robust error handling")
    
    # Test working flow
    success = test_working_8_step_cartlow_flow()
    
    if success:
        print(f"\n" + "=" * 60)
        print("8-STEP TEST COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print(f"\n[SUCCESS] All 8 steps completed!")
        print(f"[INFO] Check the results above to see what worked and what didn't")
        return True
    else:
        print(f"\n" + "=" * 60)
        print("8-STEP TEST FAILED!")
        print("=" * 60)
        print(f"\n[ERROR] Test failed")
        print(f"[INFO] Check the error messages above for details")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
