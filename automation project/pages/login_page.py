from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import logging
import time

class LoginPage(BasePage):
    # Locators - Based on Cartlow website inspection
    ACCOUNT_BUTTON = (By.XPATH, "//span[contains(text(), 'Account')]")
    LOGIN_BUTTON = (By.XPATH, "//button[contains(text(), 'Login') or contains(text(), 'Sign In') or contains(text(), 'Log In')]")
    LOGIN_LINK = (By.XPATH, "//a[contains(text(), 'Login') or contains(text(), 'Sign In') or contains(text(), 'Log In')]")
    EMAIL_INPUT = (By.XPATH, "//input[@type='email' or @name='email' or @id='email' or contains(@placeholder, 'email') or contains(@placeholder, 'Email')]")
    PASSWORD_INPUT = (By.XPATH, "//input[@type='password' or @name='password' or @id='password']")
    SUBMIT_BUTTON = (By.XPATH, "//button[@type='submit' or contains(text(), 'Login') or contains(text(), 'Sign In') or contains(text(), 'Log In')]")
    USER_MENU = (By.XPATH, "//div[contains(@class, 'user') or contains(@class, 'account') or contains(@class, 'profile')]")
    LOGOUT_BUTTON = (By.XPATH, "//a[contains(text(), 'Logout') or contains(text(), 'Sign Out') or contains(text(), 'Log Out')]")
    ERROR_MESSAGE = (By.XPATH, "//div[contains(@class, 'error') or contains(@class, 'alert') or contains(@class, 'message')]")
    LOGIN_FORM = (By.XPATH, "//form[contains(@class, 'login') or contains(@class, 'signin')]")
    
    def __init__(self, driver):
        super().__init__(driver)
        
    def click_login_button(self):
        """Click the login button to open login form"""
        try:
            # Try different login button strategies - prioritize Account button based on inspection
            strategies = [
                self.ACCOUNT_BUTTON,  # This was found to be visible in inspection
                self.LOGIN_BUTTON,
                self.LOGIN_LINK
            ]
            
            for strategy in strategies:
                try:
                    if self.click_element(strategy):
                        time.sleep(3)  # Wait for login form to appear
                        return True
                except:
                    continue
            
            logging.error("Failed to find any login button")
            return False
        except Exception as e:
            logging.error(f"Failed to click login button: {e}")
            return False
            
    def enter_email(self, email):
        """Enter email in the email field"""
        try:
            return self.send_keys(self.EMAIL_INPUT, email)
        except Exception as e:
            logging.error(f"Failed to enter email: {e}")
            return False
            
    def enter_password(self, password):
        """Enter password in the password field"""
        try:
            return self.send_keys(self.PASSWORD_INPUT, password)
        except Exception as e:
            logging.error(f"Failed to enter password: {e}")
            return False
            
    def click_submit(self):
        """Click submit button to login"""
        try:
            return self.click_element(self.SUBMIT_BUTTON)
        except Exception as e:
            logging.error(f"Failed to click submit button: {e}")
            return False
            
    def login(self, email, password):
        """Complete login process"""
        try:
            # Check if already logged in
            if self.is_logged_in():
                logging.info("User is already logged in")
                return True
            
            # Try to open login form
            if self.click_login_button():
                time.sleep(3)  # Wait for login form to appear
                
                # Try to find and fill login form
                if self.enter_email(email) and self.enter_password(password):
                    time.sleep(1)
                    return self.click_submit()
                else:
                    logging.error("Failed to enter login credentials")
                    return False
            else:
                logging.error("Failed to open login form")
                return False
        except Exception as e:
            logging.error(f"Login failed: {e}")
            return False
            
    def is_logged_in(self):
        """Check if user is logged in"""
        try:
            return self.is_element_present(self.USER_MENU)
        except Exception as e:
            logging.error(f"Failed to check login status: {e}")
            return False
            
    def logout(self):
        """Logout user"""
        try:
            if self.hover_element(self.USER_MENU):
                time.sleep(1)
                return self.click_element(self.LOGOUT_BUTTON)
            return False
        except Exception as e:
            logging.error(f"Logout failed: {e}")
            return False
            
    def get_error_message(self):
        """Get error message if login fails"""
        try:
            return self.get_text(self.ERROR_MESSAGE)
        except Exception as e:
            logging.error(f"Failed to get error message: {e}")
            return ""
