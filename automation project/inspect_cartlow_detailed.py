#!/usr/bin/env python3
"""
Detailed inspection of Cartlow website to understand login and search flow
"""

import os
import sys
import logging
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def inspect_cartlow_detailed():
    """Detailed inspection of Cartlow website structure"""
    
    print("=" * 60)
    print("DETAILED CARTLOW WEBSITE INSPECTION")
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
        
        # Step 1: Inspect login/account elements
        print(f"\n[STEP 1] Inspecting login/account elements...")
        
        # Look for account/login related elements
        account_elements = [
            "//span[contains(text(), 'Account')]",
            "//button[contains(text(), 'Account')]",
            "//a[contains(text(), 'Account')]",
            "//div[contains(@class, 'account')]",
            "//*[contains(@class, 'user')]",
            "//*[contains(@class, 'login')]",
            "//*[contains(@class, 'signin')]"
        ]
        
        found_account_elements = []
        for element_xpath in account_elements:
            try:
                elements = driver.find_elements("xpath", element_xpath)
                for element in elements:
                    try:
                        if element.is_displayed():
                            found_account_elements.append({
                                "xpath": element_xpath,
                                "tag": element.tag_name,
                                "text": element.text,
                                "classes": element.get_attribute("class"),
                                "clickable": element.is_enabled()
                            })
                    except:
                        continue
            except:
                continue
        
        print(f"  [RESULTS] Found {len(found_account_elements)} account elements:")
        for i, element in enumerate(found_account_elements, 1):
            print(f"    {i}. {element['tag']}: '{element['text']}' - Classes: '{element['classes']}' - Clickable: {element['clickable']}")
        
        # Step 2: Try to click account and see what happens
        if found_account_elements:
            print(f"\n[STEP 2] Testing account element click...")
            try:
                account_element = driver.find_element("xpath", found_account_elements[0]['xpath'])
                account_element.click()
                time.sleep(3)
                
                # Check if login form appeared
                print(f"  [INFO] Checking for login form after click...")
                
                login_form_indicators = [
                    "//input[@type='email']",
                    "//input[@type='password']",
                    "//form[contains(@class, 'login')]",
                    "//div[contains(@class, 'login')]",
                    "//div[contains(@class, 'signin')]",
                    "//div[contains(@class, 'auth')]",
                    "//div[contains(@class, 'modal')]",
                    "//div[contains(@class, 'popup')]"
                ]
                
                login_form_found = False
                for indicator in login_form_indicators:
                    try:
                        elements = driver.find_elements("xpath", indicator)
                        for element in elements:
                            if element.is_displayed():
                                print(f"    [FOUND] Login form indicator: {indicator}")
                                login_form_found = True
                                break
                        if login_form_found:
                            break
                    except:
                        continue
                
                if not login_form_found:
                    print(f"    [INFO] No login form found - checking for redirect...")
                    current_url = driver.current_url
                    print(f"    [INFO] Current URL: {current_url}")
                    
                    if "login" in current_url.lower() or "signin" in current_url.lower():
                        print(f"    [SUCCESS] Redirected to login page!")
                        
                        # Look for email and password fields
                        email_fields = driver.find_elements("xpath", "//input[@type='email' or @name='email' or @id='email']")
                        password_fields = driver.find_elements("xpath", "//input[@type='password' or @name='password' or @id='password']")
                        
                        print(f"    [INFO] Found {len(email_fields)} email fields and {len(password_fields)} password fields")
                        
                        if email_fields and password_fields:
                            print(f"    [SUCCESS] Login form is available!")
                            
                            # Try to fill the form
                            email_field = email_fields[0]
                            password_field = password_fields[0]
                            
                            email_field.clear()
                            email_field.send_keys("prof.m.gaber@gmail.com")
                            print(f"    [SUCCESS] Entered email")
                            
                            password_field.clear()
                            password_field.send_keys("123456789@Tt")
                            print(f"    [SUCCESS] Entered password")
                            
                            # Look for submit button
                            submit_buttons = driver.find_elements("xpath", "//button[@type='submit' or contains(text(), 'Login') or contains(text(), 'Sign In')]")
                            if submit_buttons:
                                submit_button = submit_buttons[0]
                                submit_button.click()
                                print(f"    [SUCCESS] Clicked submit button")
                                
                                # Wait for response
                                time.sleep(5)
                                
                                # Check if login was successful
                                if "login" not in driver.current_url.lower() and "signin" not in driver.current_url.lower():
                                    print(f"    [SUCCESS] Login appears to be successful!")
                                else:
                                    print(f"    [INFO] Still on login page - credentials might be invalid")
                            else:
                                print(f"    [WARNING] No submit button found")
                        else:
                            print(f"    [WARNING] Login form fields not found")
                    else:
                        print(f"    [INFO] Not redirected to login page")
                        
            except Exception as e:
                print(f"    [ERROR] Failed to interact with account element: {e}")
        
        # Step 3: Inspect search functionality
        print(f"\n[STEP 3] Inspecting search functionality...")
        
        # Look for search elements
        search_elements = [
            "//input[@type='search']",
            "//input[@name='search']",
            "//input[@id='search']",
            "//input[contains(@placeholder, 'Search')]",
            "//input[contains(@placeholder, 'search')]",
            "//input[contains(@class, 'search')]"
        ]
        
        found_search_elements = []
        for element_xpath in search_elements:
            try:
                elements = driver.find_elements("xpath", element_xpath)
                for element in elements:
                    try:
                        if element.is_displayed():
                            found_search_elements.append({
                                "xpath": element_xpath,
                                "tag": element.tag_name,
                                "placeholder": element.get_attribute("placeholder"),
                                "classes": element.get_attribute("class"),
                                "clickable": element.is_enabled()
                            })
                    except:
                        continue
            except:
                continue
        
        print(f"  [RESULTS] Found {len(found_search_elements)} search elements:")
        for i, element in enumerate(found_search_elements, 1):
            print(f"    {i}. {element['tag']}: Placeholder='{element['placeholder']}' - Classes: '{element['classes']}' - Clickable: {element['clickable']}")
        
        # Step 4: Test search functionality
        if found_search_elements:
            print(f"\n[STEP 4] Testing search functionality...")
            try:
                search_element = driver.find_element("xpath", found_search_elements[0]['xpath'])
                search_element.clear()
                search_element.send_keys("Dell Latitude 7490")
                time.sleep(2)
                
                # Try to submit search
                search_buttons = driver.find_elements("xpath", "//button[@type='submit' or contains(@class, 'search') or contains(text(), 'Search')]")
                if search_buttons:
                    search_buttons[0].click()
                    print(f"    [SUCCESS] Clicked search button")
                else:
                    search_element.send_keys("\n")  # Press Enter
                    print(f"    [SUCCESS] Pressed Enter to search")
                
                time.sleep(5)
                
                # Check search results
                current_url = driver.current_url
                print(f"    [INFO] Current URL after search: {current_url}")
                
                # Look for product results
                product_elements = driver.find_elements("xpath", "//div[contains(@class, 'product') or contains(@class, 'item')]")
                print(f"    [INFO] Found {len(product_elements)} potential product elements")
                
            except Exception as e:
                print(f"    [ERROR] Failed to test search: {e}")
        
        # Step 5: Inspect category navigation
        print(f"\n[STEP 5] Inspecting category navigation...")
        
        # Look for category elements
        category_elements = [
            "//a[contains(text(), 'Laptops')]",
            "//button[contains(text(), 'Laptops')]",
            "//span[contains(text(), 'Laptops')]",
            "//a[contains(text(), 'Smartwatches')]",
            "//button[contains(text(), 'Smartwatches')]",
            "//span[contains(text(), 'Smartwatches')]"
        ]
        
        found_category_elements = []
        for element_xpath in category_elements:
            try:
                elements = driver.find_elements("xpath", element_xpath)
                for element in elements:
                    try:
                        if element.is_displayed():
                            found_category_elements.append({
                                "xpath": element_xpath,
                                "tag": element.tag_name,
                                "text": element.text,
                                "classes": element.get_attribute("class"),
                                "clickable": element.is_enabled()
                            })
                    except:
                        continue
            except:
                continue
        
        print(f"  [RESULTS] Found {len(found_category_elements)} category elements:")
        for i, element in enumerate(found_category_elements, 1):
            print(f"    {i}. {element['tag']}: '{element['text']}' - Classes: '{element['classes']}' - Clickable: {element['clickable']}")
        
        # Take a screenshot
        screenshot_path = "cartlow_detailed_inspection.png"
        driver.save_screenshot(screenshot_path)
        print(f"\n[INFO] Screenshot saved: {screenshot_path}")
        
        # Close driver
        driver.quit()
        print(f"\n[SUCCESS] WebDriver closed successfully!")
        
        return True
        
    except Exception as e:
        print(f"\n[ERROR] Detailed inspection failed: {e}")
        return False

def main():
    """Main inspection function"""
    
    print("Cartlow Detailed Website Inspection")
    print("This will inspect the Cartlow website to understand login and search flow")
    
    # Inspect the website
    success = inspect_cartlow_detailed()
    
    if success:
        print(f"\n" + "=" * 60)
        print("DETAILED INSPECTION COMPLETED!")
        print("=" * 60)
        print(f"\n[SUCCESS] Detailed inspection completed!")
        print(f"[INFO] Check the results above to understand Cartlow's actual structure")
        return True
    else:
        print(f"\n" + "=" * 60)
        print("DETAILED INSPECTION FAILED!")
        print("=" * 60)
        print(f"\n[ERROR] Detailed inspection failed")
        print(f"[INFO] Check the error messages above for details")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
