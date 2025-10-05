#!/usr/bin/env python3
"""
Script to inspect Cartlow website and find correct login elements
"""

import os
import sys
import logging
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def inspect_cartlow_website():
    """Inspect Cartlow website to find login elements"""
    
    print("=" * 60)
    print("INSPECTING CARTLOW WEBSITE STRUCTURE")
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
        
        # Look for various login-related elements
        print(f"\n[INFO] Inspecting page for login elements...")
        
        # Common login element patterns
        login_patterns = [
            "//button[contains(text(), 'Login')]",
            "//a[contains(text(), 'Login')]",
            "//button[contains(text(), 'Sign In')]",
            "//a[contains(text(), 'Sign In')]",
            "//button[contains(text(), 'Log In')]",
            "//a[contains(text(), 'Log In')]",
            "//button[contains(@class, 'login')]",
            "//a[contains(@class, 'login')]",
            "//button[contains(@class, 'signin')]",
            "//a[contains(@class, 'signin')]",
            "//button[contains(@class, 'account')]",
            "//a[contains(@class, 'account')]",
            "//button[contains(@class, 'user')]",
            "//a[contains(@class, 'user')]",
            "//*[contains(text(), 'Account')]",
            "//*[contains(text(), 'Profile')]",
            "//*[contains(text(), 'My Account')]"
        ]
        
        found_elements = []
        for pattern in login_patterns:
            try:
                elements = driver.find_elements("xpath", pattern)
                if elements:
                    for element in elements:
                        try:
                            text = element.text
                            tag = element.tag_name
                            classes = element.get_attribute("class")
                            found_elements.append({
                                "pattern": pattern,
                                "tag": tag,
                                "text": text,
                                "classes": classes,
                                "visible": element.is_displayed(),
                                "enabled": element.is_enabled()
                            })
                        except:
                            continue
            except:
                continue
        
        print(f"\n[RESULTS] Found {len(found_elements)} potential login elements:")
        for i, element in enumerate(found_elements, 1):
            print(f"  {i}. Tag: {element['tag']}, Text: '{element['text']}', Classes: '{element['classes']}', Visible: {element['visible']}, Enabled: {element['enabled']}")
            print(f"     XPath: {element['pattern']}")
        
        # Look for email/password inputs
        print(f"\n[INFO] Looking for email/password input fields...")
        
        email_inputs = driver.find_elements("xpath", "//input[@type='email' or @name='email' or @id='email' or contains(@placeholder, 'email') or contains(@placeholder, 'Email')]")
        password_inputs = driver.find_elements("xpath", "//input[@type='password' or @name='password' or @id='password']")
        
        print(f"  [INFO] Found {len(email_inputs)} email input fields")
        for i, input_field in enumerate(email_inputs, 1):
            try:
                name = input_field.get_attribute("name")
                id_attr = input_field.get_attribute("id")
                placeholder = input_field.get_attribute("placeholder")
                print(f"    {i}. Name: '{name}', ID: '{id_attr}', Placeholder: '{placeholder}'")
            except:
                pass
        
        print(f"  [INFO] Found {len(password_inputs)} password input fields")
        for i, input_field in enumerate(password_inputs, 1):
            try:
                name = input_field.get_attribute("name")
                id_attr = input_field.get_attribute("id")
                placeholder = input_field.get_attribute("placeholder")
                print(f"    {i}. Name: '{name}', ID: '{id_attr}', Placeholder: '{placeholder}'")
            except:
                pass
        
        # Take a screenshot
        screenshot_path = "cartlow_inspection.png"
        driver.save_screenshot(screenshot_path)
        print(f"\n[INFO] Screenshot saved: {screenshot_path}")
        
        # Get page source for analysis
        page_source_path = "cartlow_page_source.html"
        with open(page_source_path, 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        print(f"[INFO] Page source saved: {page_source_path}")
        
        # Close driver
        driver.quit()
        print(f"\n[SUCCESS] WebDriver closed successfully!")
        
        return found_elements
        
    except Exception as e:
        print(f"\n[ERROR] Inspection failed: {e}")
        return []

def main():
    """Main inspection function"""
    
    print("Cartlow Website Inspection")
    print("This will inspect the Cartlow website to find correct login elements")
    
    # Inspect the website
    elements = inspect_cartlow_website()
    
    if elements:
        print(f"\n" + "=" * 60)
        print("INSPECTION COMPLETED!")
        print("=" * 60)
        print(f"\n[SUCCESS] Found {len(elements)} potential login elements!")
        print(f"[INFO] Check the results above to identify the correct login elements")
        print(f"[INFO] Screenshot and page source saved for manual inspection")
        return True
    else:
        print(f"\n" + "=" * 60)
        print("INSPECTION FAILED!")
        print("=" * 60)
        print(f"\n[ERROR] No login elements found")
        print(f"[INFO] Check the error messages above for details")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
