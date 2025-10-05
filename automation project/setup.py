#!/usr/bin/env python3
"""
Setup script for Cartlow E2E automation test suite
"""

import os
import sys
import subprocess
from pathlib import Path

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to install requirements: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print("Creating directories...")
    directories = ['reports', 'logs', 'screenshots']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"   Created: {directory}/")
    print("Directories created successfully!")

def create_env_file():
    """Create .env file from template"""
    env_file = Path("config/.env")
    template_file = Path("config/env_template.txt")
    
    if env_file.exists():
        print(".env file already exists. Skipping creation.")
        return True
    
    if template_file.exists():
        print("Creating .env file from template...")
        try:
            with open(template_file, 'r') as template:
                content = template.read()
            
            with open(env_file, 'w') as env:
                env.write(content)
            
            print(".env file created successfully!")
            print("Please update config/.env with your actual Cartlow account credentials!")
            return True
        except Exception as e:
            print(f"Failed to create .env file: {e}")
            return False
    else:
        print("Template file not found!")
        return False

def check_python_version():
    """Check Python version"""
    print("Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"Python {version.major}.{version.minor}.{version.micro} is compatible!")
        return True
    else:
        print(f"Python {version.major}.{version.minor}.{version.micro} is not compatible!")
        print("   Please use Python 3.7 or higher.")
        return False

def main():
    """Main setup function"""
    print("Cartlow E2E Automation Test Suite Setup")
    print("=" * 50)
    
    success = True
    
    # Check Python version
    if not check_python_version():
        success = False
    
    # Create directories
    create_directories()
    
    # Install requirements
    if not install_requirements():
        success = False
    
    # Create .env file
    if not create_env_file():
        success = False
    
    print("\n" + "=" * 50)
    if success:
        print("Setup completed successfully!")
        print("\nNext steps:")
        print("1. Update config/.env with your Cartlow account credentials")
        print("2. Run tests using: python run_tests.py")
        print("3. Or run specific tests: python run_tests.py --test-type e2e")
    else:
        print("Setup completed with errors!")
        print("   Please check the error messages above and try again.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
