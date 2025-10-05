from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from config.config import Config
import logging
from pathlib import Path
from .robust_driver_factory import RobustDriverFactory

class DriverFactory:
    @staticmethod
    def create_driver(browser_name=None):
        """Create and return a WebDriver instance using robust approach"""
        try:
            # Try the robust driver factory first
            return RobustDriverFactory.create_driver(browser_name)
        except Exception as e:
            logging.warning(f"Robust driver factory failed: {e}")
            
            # Fallback to original approach
            browser = browser_name or Config.BROWSER.lower()
            
            # Try browsers in order of preference
            browsers_to_try = [browser]
            if browser != "chrome":
                browsers_to_try.append("chrome")
            if browser != "edge":
                browsers_to_try.append("edge")
            if browser != "firefox":
                browsers_to_try.append("firefox")
            
            last_error = None
            for browser_to_try in browsers_to_try:
                try:
                    logging.info(f"Attempting to create {browser_to_try} driver")
                    if browser_to_try == "chrome":
                        return DriverFactory._create_chrome_driver()
                    elif browser_to_try == "firefox":
                        return DriverFactory._create_firefox_driver()
                    elif browser_to_try == "edge":
                        return DriverFactory._create_edge_driver()
                except Exception as e:
                    logging.warning(f"Failed to create {browser_to_try} driver: {e}")
                    last_error = e
                    continue
            
            # If all browsers failed, raise the last error
            raise Exception(f"Failed to create any browser driver. Last error: {last_error}")
    
    @staticmethod
    def _create_chrome_driver():
        """Create Chrome driver with options"""
        try:
            chrome_options = Options()
            
            if Config.HEADLESS:
                chrome_options.add_argument("--headless")
            
            # Common Chrome options for better stability
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-plugins")
            # chrome_options.add_argument("--disable-images")  # Commented out as it may break product images
            # chrome_options.add_argument("--disable-javascript")  # Commented out as it may break the website
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
            
            # Disable notifications
            prefs = {
                "profile.default_content_setting_values.notifications": 2,
                "profile.default_content_settings.popups": 0
                # "profile.managed_default_content_settings.images": 2  # Commented out to allow images
            }
            chrome_options.add_experimental_option("prefs", prefs)
            
            # Try to get the correct driver path with better error handling
            try:
                # Clear any cached drivers that might be corrupted
                import shutil
                cache_dir = Path.home() / ".wdm"
                if cache_dir.exists():
                    logging.info("Clearing WebDriver cache to avoid corrupted drivers")
                    try:
                        shutil.rmtree(cache_dir)
                    except:
                        pass
                
                driver_path = ChromeDriverManager().install()
                logging.info(f"Chrome driver path: {driver_path}")
                
                # Verify the driver file exists and is executable
                if not Path(driver_path).exists():
                    raise Exception(f"Driver file not found: {driver_path}")
                
                service = Service(driver_path)
            except Exception as e:
                logging.error(f"Chrome driver setup failed: {e}")
                raise
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.implicitly_wait(Config.IMPLICIT_WAIT)
            driver.maximize_window()
            
            logging.info("Chrome driver created successfully")
            return driver
            
        except Exception as e:
            logging.error(f"Failed to create Chrome driver: {e}")
            raise
    
    @staticmethod
    def _create_firefox_driver():
        """Create Firefox driver with options"""
        try:
            firefox_options = FirefoxOptions()
            
            if Config.HEADLESS:
                firefox_options.add_argument("--headless")
            
            firefox_options.add_argument("--width=1920")
            firefox_options.add_argument("--height=1080")
            
            service = Service(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service, options=firefox_options)
            driver.implicitly_wait(Config.IMPLICIT_WAIT)
            driver.maximize_window()
            
            logging.info("Firefox driver created successfully")
            return driver
            
        except Exception as e:
            logging.error(f"Failed to create Firefox driver: {e}")
            raise
    
    @staticmethod
    def _create_edge_driver():
        """Create Edge driver with options"""
        try:
            edge_options = EdgeOptions()
            
            if Config.HEADLESS:
                edge_options.add_argument("--headless")
            
            # Common Edge options for better stability
            edge_options.add_argument("--no-sandbox")
            edge_options.add_argument("--disable-dev-shm-usage")
            edge_options.add_argument("--disable-gpu")
            edge_options.add_argument("--window-size=1920,1080")
            edge_options.add_argument("--disable-extensions")
            edge_options.add_argument("--disable-plugins")
            
            # Disable notifications
            prefs = {
                "profile.default_content_setting_values.notifications": 2,
                "profile.default_content_settings.popups": 0
            }
            edge_options.add_experimental_option("prefs", prefs)
            
            # Try to get Edge driver with better error handling
            try:
                # Clear any cached drivers that might be corrupted
                import shutil
                cache_dir = Path.home() / ".wdm"
                if cache_dir.exists():
                    logging.info("Clearing WebDriver cache to avoid corrupted drivers")
                    try:
                        shutil.rmtree(cache_dir)
                    except:
                        pass
                
                driver_path = EdgeChromiumDriverManager().install()
                logging.info(f"Edge driver path: {driver_path}")
                
                # Verify the driver file exists and is executable
                if not Path(driver_path).exists():
                    raise Exception(f"Driver file not found: {driver_path}")
                
                service = EdgeService(driver_path)
            except Exception as e:
                logging.error(f"Edge driver setup failed: {e}")
                raise
            driver = webdriver.Edge(service=service, options=edge_options)
            driver.implicitly_wait(Config.IMPLICIT_WAIT)
            driver.maximize_window()
            
            logging.info("Edge driver created successfully")
            return driver
            
        except Exception as e:
            logging.error(f"Failed to create Edge driver: {e}")
            raise
