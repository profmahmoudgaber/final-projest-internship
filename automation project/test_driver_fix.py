#!/usr/bin/env python3
"""
Test script to verify WebDriver fixes
"""

import os
import sys
import logging
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_driver_creation():
    """Test WebDriver creation with fixes"""
    
    print("=" * 60)
    print("TESTING WEBDRIVER FIXES")
    print("=" * 60)
    
    # Set credentials
    email = "prof.m.gaber@gmail.com"
    password = "123456789@Tt"
    
    print(f"\n[INFO] Testing with credentials:")
    print(f"  Email: {email}")
    print(f"  Password: {'*' * len(password)}")
    
    try:
        from utils.driver_factory import DriverFactory
        from config.config import Config
        
        print(f"\n[TEST] Attempting to create WebDriver...")
        print(f"  Preferred browser: {Config.BROWSER}")
        
        # Try to create driver
        driver = DriverFactory.create_driver()
        
        print(f"  [SUCCESS] WebDriver created successfully!")
        print(f"  [INFO] Driver type: {type(driver).__name__}")
        print(f"  [INFO] Current URL: {driver.current_url}")
        
        # Test basic navigation
        print(f"\n[TEST] Testing basic navigation...")
        driver.get("https://www.google.com")
        print(f"  [SUCCESS] Navigated to Google successfully!")
        print(f"  [INFO] Page title: {driver.title}")
        
        # Test Cartlow navigation
        print(f"\n[TEST] Testing Cartlow navigation...")
        driver.get("https://cartlow.com/uae/en")
        print(f"  [SUCCESS] Navigated to Cartlow successfully!")
        print(f"  [INFO] Page title: {driver.title}")
        
        # Close driver
        driver.quit()
        print(f"\n[SUCCESS] WebDriver closed successfully!")
        
        return True
        
    except Exception as e:
        print(f"\n[ERROR] WebDriver creation failed: {e}")
        return False

def test_framework_components():
    """Test framework components"""
    
    print(f"\n[TEST] Testing framework components...")
    
    try:
        from pages.login_page import LoginPage
        from pages.homepage import HomePage
        from pages.product_page import ProductPage
        from pages.cart_page import CartPage
        
        print(f"  [OK] All page objects imported successfully")
        
        from utils.test_helpers import TestHelpers
        print(f"  [OK] Test helpers imported successfully")
        
        from config.config import Config
        print(f"  [OK] Configuration loaded successfully")
        print(f"  [INFO] Base URL: {Config.BASE_URL}")
        print(f"  [INFO] Browser: {Config.BROWSER}")
        
        return True
        
    except Exception as e:
        print(f"  [ERROR] Framework component test failed: {e}")
        return False

def main():
    """Main test function"""
    
    print("WebDriver Fix Verification Test")
    print("This will test the fixes for WebDriver issues")
    
    # Test framework components first
    framework_ok = test_framework_components()
    
    if not framework_ok:
        print(f"\n[ERROR] Framework components test failed!")
        return False
    
    # Test driver creation
    driver_ok = test_driver_creation()
    
    if driver_ok:
        print(f"\n" + "=" * 60)
        print("ALL TESTS PASSED!")
        print("=" * 60)
        print(f"\n[SUCCESS] WebDriver fixes are working correctly!")
        print(f"[SUCCESS] Framework is ready for E2E test execution!")
        print(f"\n[READY] You can now run the complete E2E test:")
        print(f"  python run_when_online.py")
        return True
    else:
        print(f"\n" + "=" * 60)
        print("TESTS FAILED!")
        print("=" * 60)
        print(f"\n[ERROR] WebDriver issues still exist")
        print(f"[INFO] Check the error messages above for details")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
