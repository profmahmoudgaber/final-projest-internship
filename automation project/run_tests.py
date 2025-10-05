#!/usr/bin/env python3
"""
Test runner script for Cartlow E2E automation tests
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def create_directories():
    """Create necessary directories"""
    directories = ['reports', 'logs', 'screenshots']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"Created directory: {directory}")

def run_tests(test_type="all", browser="chrome", headless=False, verbose=True):
    """Run tests with specified parameters"""
    
    # Create necessary directories
    create_directories()
    
    # Set environment variables
    env = os.environ.copy()
    env['BROWSER'] = browser
    env['HEADLESS'] = str(headless).lower()
    
    # Build pytest command
    cmd = ['python', '-m', 'pytest']
    
    if test_type == "e2e":
        cmd.append('tests/test_cartlow_e2e.py::TestCartlowE2E::test_complete_shopping_flow')
    elif test_type == "components":
        cmd.append('tests/test_cartlow_e2e.py::TestCartlowE2E::test_individual_components')
    else:
        cmd.append('tests/')
    
    if verbose:
        cmd.append('-v')
    
    # Add HTML report
    cmd.extend(['--html=reports/report.html', '--self-contained-html'])
    
    # Add markers
    if test_type == "e2e":
        cmd.extend(['-m', 'e2e'])
    
    print(f"Running command: {' '.join(cmd)}")
    print(f"Browser: {browser}")
    print(f"Headless: {headless}")
    print("-" * 50)
    
    try:
        result = subprocess.run(cmd, env=env, check=True)
        print("\n" + "=" * 50)
        print("✅ Tests completed successfully!")
        print("📊 Check reports/report.html for detailed results")
        return True
    except subprocess.CalledProcessError as e:
        print("\n" + "=" * 50)
        print("❌ Tests failed!")
        print(f"Exit code: {e.returncode}")
        return False
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Run Cartlow E2E automation tests')
    parser.add_argument('--test-type', choices=['all', 'e2e', 'components'], 
                       default='all', help='Type of tests to run')
    parser.add_argument('--browser', choices=['chrome', 'firefox'], 
                       default='chrome', help='Browser to use')
    parser.add_argument('--headless', action='store_true', 
                       help='Run in headless mode')
    parser.add_argument('--quiet', action='store_true', 
                       help='Run in quiet mode (less verbose)')
    
    args = parser.parse_args()
    
    print("🚀 Cartlow E2E Automation Test Runner")
    print("=" * 50)
    
    success = run_tests(
        test_type=args.test_type,
        browser=args.browser,
        headless=args.headless,
        verbose=not args.quiet
    )
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
