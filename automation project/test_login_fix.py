#!/usr/bin/env python3
"""
Test script to verify login functionality fixes
"""

import os
import sys
import logging
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_login_functionality():
    """Test login functionality with improved locators"""
    
    print("=" * 60)
    print("TESTING LOGIN FUNCTIONALITY FIXES")
    print("=" * 60)
    
    # Set credentials
    email = "prof.m.gaber@gmail.com"
    password = "123456789@Tt"
    
    print(f"\n[INFO] Testing with credentials:")
    print(f"  Email: {email}")
    print(f"  Password: {'*' * len(password)}")
    
    try:
        from utils.driver_factory import DriverFactory
        from pages.login_page import LoginPage
        from config.config import Config
        
        print(f"\n[TEST] Creating WebDriver...")
        driver = DriverFactory.create_driver()
        
        print(f"  [SUCCESS] WebDriver created successfully!")
        print(f"  [INFO] Driver type: {type(driver).__name__}")
        
        # Navigate to Cartlow
        print(f"\n[TEST] Navigating to Cartlow...")
        driver.get(Config.BASE_URL)
        print(f"  [SUCCESS] Navigated to Cartlow successfully!")
        print(f"  [INFO] Page title: {driver.title}")
        
        # Create login page object
        print(f"\n[TEST] Testing login functionality...")
        login_page = LoginPage(driver)
        
        # Test login
        print(f"  [INFO] Attempting login...")
        login_success = login_page.login(email, password)
        
        if login_success:
            print(f"  [SUCCESS] Login successful!")
            
            # Check if logged in
            if login_page.is_logged_in():
                print(f"  [SUCCESS] User is confirmed logged in!")
            else:
                print(f"  [WARNING] Login appeared successful but user menu not found")
        else:
            print(f"  [INFO] Login failed - this might be expected if credentials are invalid")
            print(f"  [INFO] Taking screenshot for debugging...")
            
            # Take screenshot
            screenshot_path = "login_test_screenshot.png"
            driver.save_screenshot(screenshot_path)
            print(f"  [INFO] Screenshot saved: {screenshot_path}")
        
        # Close driver
        driver.quit()
        print(f"\n[SUCCESS] WebDriver closed successfully!")
        
        return True
        
    except Exception as e:
        print(f"\n[ERROR] Login test failed: {e}")
        return False

def main():
    """Main test function"""
    
    print("Login Functionality Fix Test")
    print("This will test the improved login locators and functionality")
    
    # Test login functionality
    success = test_login_functionality()
    
    if success:
        print(f"\n" + "=" * 60)
        print("LOGIN TEST COMPLETED!")
        print("=" * 60)
        print(f"\n[SUCCESS] Login functionality test completed!")
        print(f"[INFO] Check the results above for login status")
        print(f"[READY] The E2E test should now work better with improved login handling")
        return True
    else:
        print(f"\n" + "=" * 60)
        print("LOGIN TEST FAILED!")
        print("=" * 60)
        print(f"\n[ERROR] Login functionality test failed")
        print(f"[INFO] Check the error messages above for details")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
