#!/usr/bin/env python3
"""
Test script to understand Cartlow's authentication flow
"""

import os
import sys
import logging
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_cartlow_authentication():
    """Test different authentication approaches for Cartlow"""
    
    print("=" * 60)
    print("TESTING CARTLOW AUTHENTICATION FLOW")
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
        
        # Try to click Account button and see what happens
        print(f"\n[TEST] Clicking Account button...")
        try:
            account_button = driver.find_element("xpath", "//span[contains(text(), 'Account')]")
            print(f"  [SUCCESS] Found Account button: {account_button.text}")
            
            # Click the Account button
            account_button.click()
            print(f"  [SUCCESS] Clicked Account button")
            
            # Wait for response
            time.sleep(3)
            
            # Check if login form appeared
            print(f"\n[TEST] Checking for login form...")
            
            # Look for various login form indicators
            login_indicators = [
                "//input[@type='email']",
                "//input[@type='password']",
                "//form[contains(@class, 'login')]",
                "//div[contains(@class, 'login')]",
                "//div[contains(@class, 'signin')]",
                "//div[contains(@class, 'auth')]",
                "//div[contains(@class, 'modal')]",
                "//div[contains(@class, 'popup')]",
                "//div[contains(@class, 'overlay')]"
            ]
            
            found_forms = []
            for indicator in login_indicators:
                try:
                    elements = driver.find_elements("xpath", indicator)
                    if elements:
                        for element in elements:
                            try:
                                if element.is_displayed():
                                    found_forms.append({
                                        "indicator": indicator,
                                        "tag": element.tag_name,
                                        "classes": element.get_attribute("class"),
                                        "visible": element.is_displayed()
                                    })
                            except:
                                continue
                except:
                    continue
            
            if found_forms:
                print(f"  [SUCCESS] Found {len(found_forms)} login form indicators:")
                for form in found_forms:
                    print(f"    - {form['indicator']}: {form['tag']}, Classes: '{form['classes']}'")
            else:
                print(f"  [INFO] No login form found after clicking Account button")
            
            # Check if we were redirected to a login page
            current_url = driver.current_url
            print(f"  [INFO] Current URL after clicking Account: {current_url}")
            
            if "login" in current_url.lower() or "signin" in current_url.lower() or "auth" in current_url.lower():
                print(f"  [SUCCESS] Redirected to login page!")
                
                # Look for email and password fields
                email_fields = driver.find_elements("xpath", "//input[@type='email' or @name='email' or @id='email']")
                password_fields = driver.find_elements("xpath", "//input[@type='password' or @name='password' or @id='password']")
                
                print(f"  [INFO] Found {len(email_fields)} email fields and {len(password_fields)} password fields")
                
                if email_fields and password_fields:
                    print(f"  [SUCCESS] Login form is available!")
                    
                    # Try to fill the form
                    email_field = email_fields[0]
                    password_field = password_fields[0]
                    
                    email_field.clear()
                    email_field.send_keys("prof.m.gaber@gmail.com")
                    print(f"  [SUCCESS] Entered email")
                    
                    password_field.clear()
                    password_field.send_keys("123456789@Tt")
                    print(f"  [SUCCESS] Entered password")
                    
                    # Look for submit button
                    submit_buttons = driver.find_elements("xpath", "//button[@type='submit' or contains(text(), 'Login') or contains(text(), 'Sign In')]")
                    if submit_buttons:
                        submit_button = submit_buttons[0]
                        submit_button.click()
                        print(f"  [SUCCESS] Clicked submit button")
                        
                        # Wait for response
                        time.sleep(5)
                        
                        # Check if login was successful
                        if "login" not in driver.current_url.lower() and "signin" not in driver.current_url.lower():
                            print(f"  [SUCCESS] Login appears to be successful!")
                        else:
                            print(f"  [INFO] Still on login page - credentials might be invalid")
                    else:
                        print(f"  [WARNING] No submit button found")
                else:
                    print(f"  [WARNING] Login form fields not found")
            else:
                print(f"  [INFO] Not redirected to login page")
                
        except Exception as e:
            print(f"  [ERROR] Failed to interact with Account button: {e}")
        
        # Take a screenshot
        screenshot_path = "cartlow_auth_test.png"
        driver.save_screenshot(screenshot_path)
        print(f"\n[INFO] Screenshot saved: {screenshot_path}")
        
        # Close driver
        driver.quit()
        print(f"\n[SUCCESS] WebDriver closed successfully!")
        
        return True
        
    except Exception as e:
        print(f"\n[ERROR] Authentication test failed: {e}")
        return False

def main():
    """Main test function"""
    
    print("Cartlow Authentication Flow Test")
    print("This will test different authentication approaches for Cartlow")
    
    # Test authentication flow
    success = test_cartlow_authentication()
    
    if success:
        print(f"\n" + "=" * 60)
        print("AUTHENTICATION TEST COMPLETED!")
        print("=" * 60)
        print(f"\n[SUCCESS] Authentication flow test completed!")
        print(f"[INFO] Check the results above to understand Cartlow's authentication flow")
        return True
    else:
        print(f"\n" + "=" * 60)
        print("AUTHENTICATION TEST FAILED!")
        print("=" * 60)
        print(f"\n[ERROR] Authentication flow test failed")
        print(f"[INFO] Check the error messages above for details")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
