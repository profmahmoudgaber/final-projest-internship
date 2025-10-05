import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BASE_URL = "https://cartlow.com/uae/en"
    BROWSER = os.getenv("BROWSER", "edge")
    HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
    IMPLICIT_WAIT = int(os.getenv("IMPLICIT_WAIT", "10"))
    EXPLICIT_WAIT = int(os.getenv("EXPLICIT_WAIT", "20"))
    
    # Test data
    EMAIL = os.getenv("EMAIL", "test@example.com")
    PASSWORD = os.getenv("PASSWORD", "testpassword")
    
    # Product details
    LAPTOP_NAME = "Dell Latitude 7490 Intel Core i7-8650U 14\" FHD Display, 16GB RAM, 512GB SSD, Windows 10 Pro"
    WATCH_NAME = "Apple Watch Series 6 (40mm, GPS + Cellular) Gold Aluminum Case with Pink Sand Sport Band"
    WATCH_CONNECTIVITY = "GPS and Cellular"
    WATCH_COLOR = "Silver"
    WATCH_SIZE = "44mm"
