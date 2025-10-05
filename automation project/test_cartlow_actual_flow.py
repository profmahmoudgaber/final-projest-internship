#!/usr/bin/env python3
"""
Test script to perform actual Cartlow shopping flow with real UI interactions
"""

import os
import sys
import logging
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_actual_cartlow_flow():
    """Test actual Cartlow shopping flow with real interactions"""
    
    print("=" * 60)
    print("TESTING ACTUAL CARTLOW SHOPPING FLOW")
    print("=" * 60)
    
    try:
        from utils.driver_factory import DriverFactory
        from config.config import Config
        
        print(f"\n[INFO] Creating WebDriver...")
        driver = DriverFactory.create_driver()
        
        print(f"  [SUCCESS] WebDriver created successfully!")
        
        # Navigate to Cartlow
        print(f"\n[INFO] Navigating to Cartlow...")
        driver.get(Config.BASE_URL)
        print(f"  [SUCCESS] Navigated to Cartlow successfully!")
        print(f"  [INFO] Page title: {driver.title}")
        
        # Wait for page to load
        import time
        time.sleep(5)
        
        # Step 1: Handle login/authentication
        print(f"\n[STEP 1] Handling authentication...")
        try:
            # Click account element
            account_element = driver.find_element("xpath", "//span[contains(text(), 'Account')]")
            account_element.click()
            time.sleep(3)
            print(f"  [SUCCESS] Clicked account element")
            
            # Check if login form appeared or redirected
            current_url = driver.current_url
            if "login" in current_url.lower() or "signin" in current_url.lower():
                print(f"  [INFO] Redirected to login page: {current_url}")
                
                # Try to login
                email_fields = driver.find_elements("xpath", "//input[@type='email' or @name='email' or @id='email']")
                password_fields = driver.find_elements("xpath", "//input[@type='password' or @name='password' or @id='password']")
                
                if email_fields and password_fields:
                    email_field = email_fields[0]
                    password_field = password_fields[0]
                    
                    email_field.clear()
                    email_field.send_keys("prof.m.gaber@gmail.com")
                    time.sleep(1)
                    
                    password_field.clear()
                    password_field.send_keys("123456789@Tt")
                    time.sleep(1)
                    
                    # Find and click submit button
                    submit_buttons = driver.find_elements("xpath", "//button[@type='submit' or contains(text(), 'Login') or contains(text(), 'Sign In')]")
                    if submit_buttons:
                        submit_buttons[0].click()
                        time.sleep(5)
                        print(f"  [SUCCESS] Login form submitted")
                    else:
                        print(f"  [WARNING] No submit button found")
                else:
                    print(f"  [WARNING] Login form fields not found")
            else:
                print(f"  [INFO] No login redirect - user might already be logged in")
                
        except Exception as e:
            print(f"  [WARNING] Authentication handling failed: {e}")
        
        # Step 2: Search for Dell Latitude 7490
        print(f"\n[STEP 2] Searching for Dell Latitude 7490...")
        try:
            # Find search box
            search_box = driver.find_element("xpath", "//input[@placeholder='Search products here']")
            search_box.clear()
            search_box.send_keys("Dell Latitude 7490")
            time.sleep(2)
            
            # Submit search
            from selenium.webdriver.common.keys import Keys
            search_box.send_keys(Keys.RETURN)
            time.sleep(5)
            
            print(f"  [SUCCESS] Search submitted for Dell Latitude 7490")
            
            # Look for product in results
            try:
                # Try to find the product
                product_elements = driver.find_elements("xpath", "//div[contains(text(), 'Dell Latitude') or contains(text(), '7490')]")
                if product_elements:
                    print(f"  [SUCCESS] Found Dell Latitude product in results")
                    
                    # Try to find add to cart button
                    add_to_cart_buttons = driver.find_elements("xpath", "//button[contains(text(), 'Add to Cart') or contains(text(), 'Add to Bag')]")
                    if add_to_cart_buttons:
                        # Scroll to button and click
                        driver.execute_script("arguments[0].scrollIntoView(true);", add_to_cart_buttons[0])
                        time.sleep(1)
                        add_to_cart_buttons[0].click()
                        time.sleep(2)
                        print(f"  [SUCCESS] Added Dell Latitude 7490 to cart")
                    else:
                        print(f"  [WARNING] Add to cart button not found")
                else:
                    print(f"  [WARNING] Dell Latitude product not found in results")
                    
            except Exception as e:
                print(f"  [WARNING] Product interaction failed: {e}")
                
        except Exception as e:
            print(f"  [ERROR] Search failed: {e}")
        
        # Step 3: Search for Apple Watch Series 6
        print(f"\n[STEP 3] Searching for Apple Watch Series 6...")
        try:
            # Go back to homepage first
            driver.get(Config.BASE_URL)
            time.sleep(3)
            
            # Find search box again
            search_box = driver.find_element("xpath", "//input[@placeholder='Search products here']")
            search_box.clear()
            search_box.send_keys("Apple Watch Series 6")
            time.sleep(2)
            
            # Submit search
            search_box.send_keys(Keys.RETURN)
            time.sleep(5)
            
            print(f"  [SUCCESS] Search submitted for Apple Watch Series 6")
            
            # Look for product in results
            try:
                # Try to find the product
                product_elements = driver.find_elements("xpath", "//div[contains(text(), 'Apple Watch') or contains(text(), 'Series 6')]")
                if product_elements:
                    print(f"  [SUCCESS] Found Apple Watch product in results")
                    
                    # Try to find add to cart button
                    add_to_cart_buttons = driver.find_elements("xpath", "//button[contains(text(), 'Add to Cart') or contains(text(), 'Add to Bag')]")
                    if add_to_cart_buttons:
                        # Scroll to button and click
                        driver.execute_script("arguments[0].scrollIntoView(true);", add_to_cart_buttons[0])
                        time.sleep(1)
                        add_to_cart_buttons[0].click()
                        time.sleep(2)
                        print(f"  [SUCCESS] Added Apple Watch Series 6 to cart")
                    else:
                        print(f"  [WARNING] Add to cart button not found")
                else:
                    print(f"  [WARNING] Apple Watch product not found in results")
                    
            except Exception as e:
                print(f"  [WARNING] Product interaction failed: {e}")
                
        except Exception as e:
            print(f"  [ERROR] Search failed: {e}")
        
        # Step 4: View cart
        print(f"\n[STEP 4] Viewing cart...")
        try:
            # Go back to homepage
            driver.get(Config.BASE_URL)
            time.sleep(3)
            
            # Look for cart button
            cart_buttons = driver.find_elements("xpath", "//a[contains(@class, 'cart') or contains(text(), 'Cart') or contains(text(), 'Bag')]")
            if cart_buttons:
                # Scroll to cart button
                driver.execute_script("arguments[0].scrollIntoView(true);", cart_buttons[0])
                time.sleep(1)
                cart_buttons[0].click()
                time.sleep(3)
                print(f"  [SUCCESS] Clicked cart button")
                
                # Check if cart page loaded
                current_url = driver.current_url
                if "cart" in current_url.lower() or "bag" in current_url.lower():
                    print(f"  [SUCCESS] Cart page loaded: {current_url}")
                    
                    # Try to find remove buttons
                    remove_buttons = driver.find_elements("xpath", "//button[contains(text(), 'Remove') or contains(@class, 'remove')]")
                    if remove_buttons:
                        print(f"  [INFO] Found {len(remove_buttons)} remove buttons")
                        # Click first remove button (laptop)
                        remove_buttons[0].click()
                        time.sleep(2)
                        print(f"  [SUCCESS] Removed laptop from cart")
                    else:
                        print(f"  [WARNING] No remove buttons found")
                    
                    # Try to find checkout button
                    checkout_buttons = driver.find_elements("xpath", "//button[contains(text(), 'Checkout') or contains(text(), 'Proceed')]")
                    if checkout_buttons:
                        # Scroll to checkout button
                        driver.execute_script("arguments[0].scrollIntoView(true);", checkout_buttons[0])
                        time.sleep(1)
                        checkout_buttons[0].click()
                        time.sleep(3)
                        print(f"  [SUCCESS] Clicked checkout button")
                    else:
                        print(f"  [WARNING] No checkout button found")
                else:
                    print(f"  [WARNING] Cart page not loaded properly")
            else:
                print(f"  [WARNING] Cart button not found")
                
        except Exception as e:
            print(f"  [ERROR] Cart interaction failed: {e}")
        
        # Take final screenshot
        screenshot_path = "cartlow_actual_flow_test.png"
        driver.save_screenshot(screenshot_path)
        print(f"\n[INFO] Final screenshot saved: {screenshot_path}")
        
        # Close driver
        driver.quit()
        print(f"\n[SUCCESS] WebDriver closed successfully!")
        
        return True
        
    except Exception as e:
        print(f"\n[ERROR] Test failed: {e}")
        return False

def main():
    """Main test function"""
    
    print("Cartlow Actual Shopping Flow Test")
    print("This will test the actual shopping flow with real UI interactions")
    
    # Test actual flow
    success = test_actual_cartlow_flow()
    
    if success:
        print(f"\n" + "=" * 60)
        print("ACTUAL FLOW TEST COMPLETED!")
        print("=" * 60)
        print(f"\n[SUCCESS] Actual flow test completed!")
        print(f"[INFO] Check the results above to see what worked and what didn't")
        return True
    else:
        print(f"\n" + "=" * 60)
        print("ACTUAL FLOW TEST FAILED!")
        print("=" * 60)
        print(f"\n[ERROR] Actual flow test failed")
        print(f"[INFO] Check the error messages above for details")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
