"""
Robust WebDriver factory that can handle various scenarios
"""

import os
import sys
import logging
import subprocess
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from config.config import Config

class RobustDriverFactory:
    @staticmethod
    def create_driver(browser_name=None):
        """Create and return a WebDriver instance with fallback options"""
        browser = browser_name or Config.BROWSER.lower()
        
        # Try different approaches in order
        approaches = [
            RobustDriverFactory._try_system_driver,
            RobustDriverFactory._try_webdriver_manager,
            RobustDriverFactory._try_manual_driver
        ]
        
        for approach in approaches:
            try:
                logging.info(f"Trying approach: {approach.__name__}")
                driver = approach(browser)
                if driver:
                    logging.info(f"Successfully created {browser} driver using {approach.__name__}")
                    return driver
            except Exception as e:
                logging.warning(f"Approach {approach.__name__} failed: {e}")
                continue
        
        raise Exception(f"Failed to create any {browser} driver with all approaches")
    
    @staticmethod
    def _try_system_driver(browser):
        """Try to use system-installed driver"""
        try:
            if browser == "chrome":
                options = ChromeOptions()
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-gpu")
                options.add_argument("--window-size=1920,1080")
                
                # Try to find Chrome driver in system PATH
                driver = webdriver.Chrome(options=options)
                return driver
                
            elif browser == "firefox":
                options = FirefoxOptions()
                options.add_argument("--width=1920")
                options.add_argument("--height=1080")
                
                driver = webdriver.Firefox(options=options)
                return driver
                
            elif browser == "edge":
                options = EdgeOptions()
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-gpu")
                options.add_argument("--window-size=1920,1080")
                
                driver = webdriver.Edge(options=options)
                return driver
                
        except Exception as e:
            logging.warning(f"System driver approach failed: {e}")
            return None
    
    @staticmethod
    def _try_webdriver_manager(browser):
        """Try to use webdriver-manager with better error handling"""
        try:
            if browser == "chrome":
                from webdriver_manager.chrome import ChromeDriverManager
                
                # Try to get driver path
                driver_path = ChromeDriverManager().install()
                
                # Fix common path issues
                if "THIRD_PARTY_NOTICES" in driver_path:
                    # Find the actual chromedriver.exe
                    driver_dir = Path(driver_path).parent
                    actual_driver = driver_dir / "chromedriver.exe"
                    if actual_driver.exists():
                        driver_path = str(actual_driver)
                    else:
                        # Look for chromedriver in the directory
                        for file in driver_dir.glob("*chromedriver*"):
                            if file.suffix == ".exe":
                                driver_path = str(file)
                                break
                
                options = ChromeOptions()
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-gpu")
                options.add_argument("--window-size=1920,1080")
                
                service = ChromeService(driver_path)
                driver = webdriver.Chrome(service=service, options=options)
                return driver
                
            elif browser == "firefox":
                from webdriver_manager.firefox import GeckoDriverManager
                
                driver_path = GeckoDriverManager().install()
                options = FirefoxOptions()
                options.add_argument("--width=1920")
                options.add_argument("--height=1080")
                
                service = FirefoxService(driver_path)
                driver = webdriver.Firefox(service=service, options=options)
                return driver
                
            elif browser == "edge":
                from webdriver_manager.microsoft import EdgeChromiumDriverManager
                
                driver_path = EdgeChromiumDriverManager().install()
                options = EdgeOptions()
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-gpu")
                options.add_argument("--window-size=1920,1080")
                
                service = EdgeService(driver_path)
                driver = webdriver.Edge(service=service, options=options)
                return driver
                
        except Exception as e:
            logging.warning(f"WebDriver manager approach failed: {e}")
            return None
    
    @staticmethod
    def _try_manual_driver(browser):
        """Try to create driver with manual configuration"""
        try:
            if browser == "chrome":
                # Try to find Chrome installation
                chrome_paths = [
                    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                    os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe")
                ]
                
                chrome_path = None
                for path in chrome_paths:
                    if Path(path).exists():
                        chrome_path = path
                        break
                
                if chrome_path:
                    options = ChromeOptions()
                    options.binary_location = chrome_path
                    options.add_argument("--no-sandbox")
                    options.add_argument("--disable-dev-shm-usage")
                    options.add_argument("--disable-gpu")
                    options.add_argument("--window-size=1920,1080")
                    
                    driver = webdriver.Chrome(options=options)
                    return driver
                    
        except Exception as e:
            logging.warning(f"Manual driver approach failed: {e}")
            return None
    
    @staticmethod
    def create_headless_driver(browser_name=None):
        """Create a headless WebDriver instance"""
        browser = browser_name or Config.BROWSER.lower()
        
        try:
            driver = RobustDriverFactory.create_driver(browser)
            
            # Set headless mode
            if browser == "chrome":
                driver.execute_script("window.open('about:blank', '_blank');")
                driver.switch_to.window(driver.window_handles[-1])
            elif browser == "firefox":
                driver.execute_script("window.open('about:blank', '_blank');")
                driver.switch_to.window(driver.window_handles[-1])
            elif browser == "edge":
                driver.execute_script("window.open('about:blank', '_blank');")
                driver.switch_to.window(driver.window_handles[-1])
            
            return driver
            
        except Exception as e:
            logging.error(f"Failed to create headless driver: {e}")
            raise
