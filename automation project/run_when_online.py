#!/usr/bin/env python3
"""
Script to run the Cartlow E2E test when internet connectivity is available
"""

import os
import sys
import subprocess
from pathlib import Path

def run_cartlow_test():
    """Run the Cartlow E2E test with proper credentials"""
    
    print("=" * 60)
    print("CARTLOW E2E AUTOMATION TEST RUNNER")
    print("=" * 60)
    
    # Set credentials
    email = "prof.m.gaber@gmail.com"
    password = "123456789@Tt"
    
    print(f"\n[INFO] Test Configuration:")
    print(f"  Email: {email}")
    print(f"  Password: {'*' * len(password)}")
    print(f"  Website: https://cartlow.com/uae/en")
    print(f"  Browser: Edge (default)")
    
    # Set environment variables
    env = os.environ.copy()
    env['EMAIL'] = email
    env['PASSWORD'] = password
    env['BROWSER'] = 'edge'
    env['HEADLESS'] = 'false'
    
    print(f"\n[INFO] Starting E2E test execution...")
    print(f"  This will:")
    print(f"  1. Download Edge WebDriver (if needed)")
    print(f"  2. Launch Edge browser")
    print(f"  3. Navigate to Cartlow website")
    print(f"  4. Execute the complete shopping scenario")
    print(f"  5. Generate HTML test report")
    
    # Run the test
    try:
        cmd = [
            sys.executable, '-m', 'pytest',
            'tests/test_cartlow_e2e.py::TestCartlowE2E::test_complete_shopping_flow',
            '-v',
            '--html=reports/cartlow_e2e_report.html',
            '--self-contained-html',
            '--tb=short'
        ]
        
        print(f"\n[EXECUTING] Command: {' '.join(cmd)}")
        print(f"[EXECUTING] Environment: EMAIL={email}, PASSWORD={'*' * len(password)}")
        
        result = subprocess.run(cmd, env=env, check=True)
        
        print(f"\n" + "=" * 60)
        print("TEST EXECUTION COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print(f"\n[RESULTS]")
        print(f"  [OK] E2E test passed")
        print(f"  [OK] HTML report generated: reports/cartlow_e2e_report.html")
        print(f"  [OK] Screenshots saved (if any failures)")
        print(f"  [OK] Logs available: test_execution.log")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n" + "=" * 60)
        print("TEST EXECUTION FAILED!")
        print("=" * 60)
        print(f"\n[ERROR] Exit code: {e.returncode}")
        print(f"[ERROR] Check the logs for details")
        print(f"[ERROR] Screenshots may be available in screenshots/ folder")
        
        return False
        
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        return False

def show_test_scenario():
    """Show the test scenario that will be executed"""
    
    print(f"\n[TEST SCENARIO] The following E2E test will be executed:")
    print(f"  Step 1:  Login with prof.m.gaber@gmail.com")
    print(f"  Step 2:  Open Cartlow homepage")
    print(f"  Step 3:  Click on Laptops tab")
    print(f"  Step 4:  Select Dell Latitude 7490 laptop")
    print(f"  Step 5:  Add 1 laptop to cart")
    print(f"  Step 6:  Navigate to Smartwatches tab")
    print(f"  Step 7:  Select Apple Watch Series 6")
    print(f"  Step 8:  Configure: GPS+Cellular, Silver, 44mm")
    print(f"  Step 9:  Add 2 watches to cart")
    print(f"  Step 10: Open cart and view items")
    print(f"  Step 11: Remove laptop from cart")
    print(f"  Step 12: Proceed to checkout")

def main():
    """Main function"""
    
    print("Cartlow E2E Automation Test Runner")
    print("This script will run the complete E2E test scenario")
    
    # Show test scenario
    show_test_scenario()
    
    # Ask for confirmation
    response = input(f"\n[CONFIRM] Do you want to proceed with the test? (y/n): ")
    if response.lower() != 'y':
        print(f"[CANCELLED] Test execution cancelled by user")
        return
    
    # Run the test
    success = run_cartlow_test()
    
    if success:
        print(f"\n[SUCCESS] Test completed successfully!")
        print(f"[NEXT] Check reports/cartlow_e2e_report.html for detailed results")
    else:
        print(f"\n[FAILED] Test execution failed!")
        print(f"[DEBUG] Check logs and screenshots for troubleshooting")

if __name__ == "__main__":
    main()
