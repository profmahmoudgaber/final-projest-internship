# Cartlow E2E Automation Test Suite

This project contains a comprehensive Selenium automation test suite for the Cartlow website (https://cartlow.com/uae/en) using the Page Object Model (POM) pattern.

## Test Scenario

The test suite implements the following E2E scenario:

1. **Login** with a created account
2. **Open** the homepage
3. **Click** on the Laptops tab
4. **Select** the Dell Latitude 7490 laptop
5. **Add** 1 item to the cart
6. **Navigate** to the Smartwatches tab
7. **Select** the Apple Watch Series 6 with specific configurations:
   - Connectivity: GPS and Cellular
   - Color: Silver
   - Size: 44mm
8. **Add** 2 items to the cart
9. **Open** the cart and view cart
10. **Remove** the laptop from cart
11. **Proceed** to checkout

## Project Structure

```
automation project/
├── config/
│   ├── __init__.py
│   └── config.py              # Configuration settings
├── pages/
│   ├── __init__.py
│   ├── base_page.py           # Base page class with common methods
│   ├── login_page.py          # Login page object
│   ├── homepage.py            # Homepage object
│   ├── product_page.py        # Product page object
│   └── cart_page.py           # Cart page object
├── utils/
│   ├── __init__.py
│   ├── driver_factory.py      # WebDriver factory
│   └── test_helpers.py        # Test utility functions
├── tests/
│   ├── __init__.py
│   └── test_cartlow_e2e.py    # Main E2E test
├── reports/                   # Test reports (generated)
├── conftest.py               # Pytest configuration
├── pytest.ini               # Pytest settings
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## Prerequisites

- Python 3.7 or higher
- Chrome or Firefox browser
- Internet connection

## Installation

1. **Clone or download** the project to your local machine

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure test credentials**:
   - Create a `.env` file in the `config/` directory
   - Add your Cartlow account credentials:
     ```
     EMAIL=your_email@example.com
     PASSWORD=your_password
     ```

## Configuration

The test configuration is managed through `config/config.py` and environment variables:

- **Browser**: Chrome (default) or Firefox
- **Headless mode**: Set `HEADLESS=true` in `.env` for headless execution
- **Wait times**: Configurable implicit and explicit wait times
- **Base URL**: https://cartlow.com/uae/en

## Running Tests

### Run All Tests
```bash
pytest
```

### Run Specific Test
```bash
pytest tests/test_cartlow_e2e.py::TestCartlowE2E::test_complete_shopping_flow -v
```

### Run with HTML Report
```bash
pytest --html=reports/report.html --self-contained-html
```

### Run in Headless Mode
```bash
HEADLESS=true pytest
```

### Run with Different Browser
```bash
BROWSER=firefox pytest
```

## Test Features

### Page Object Model (POM)
- **BasePage**: Common functionality for all pages
- **LoginPage**: Handles user authentication
- **HomePage**: Manages homepage navigation
- **ProductPage**: Handles product selection and cart operations
- **CartPage**: Manages cart operations and checkout

### Robust Element Handling
- Explicit waits for element visibility and clickability
- Multiple selector strategies for finding elements
- Retry mechanisms for flaky operations
- Screenshot capture on test failures

### Test Utilities
- **DriverFactory**: Creates and configures WebDriver instances
- **TestHelpers**: Utility functions for common test operations
- **Config**: Centralized configuration management

### Error Handling
- Comprehensive logging throughout test execution
- Screenshot capture on failures
- Graceful handling of timeouts and exceptions

## Test Reports

Test execution generates:
- **Console output**: Real-time test progress and results
- **HTML report**: Detailed test report in `reports/report.html`
- **Log file**: Detailed execution log in `test_execution.log`
- **Screenshots**: Failure screenshots with timestamps

## Troubleshooting

### Common Issues

1. **WebDriver Issues**:
   - Ensure Chrome/Firefox is installed
   - Check internet connection
   - Verify WebDriver Manager can download drivers

2. **Element Not Found**:
   - Website structure may have changed
   - Check locators in page objects
   - Increase wait times if needed

3. **Login Failures**:
   - Verify credentials in `.env` file
   - Check if account is active
   - Ensure website is accessible

4. **Product Not Found**:
   - Product may be out of stock
   - Product name may have changed
   - Check product availability on website

### Debug Mode

Run tests with debug logging:
```bash
pytest -s --log-cli-level=DEBUG
```

## Customization

### Adding New Tests
1. Create new test methods in `test_cartlow_e2e.py`
2. Use existing page objects or create new ones
3. Follow the established naming conventions

### Modifying Page Objects
1. Update locators in respective page classes
2. Add new methods as needed
3. Maintain the POM pattern structure

### Configuration Changes
1. Modify `config/config.py` for new settings
2. Update `.env` file for environment-specific values
3. Adjust wait times based on website performance

## Best Practices

1. **Maintain Page Objects**: Keep locators updated with website changes
2. **Use Explicit Waits**: Avoid hard-coded sleep statements
3. **Handle Popups**: Implement popup handling in base page
4. **Log Everything**: Use logging for debugging and monitoring
5. **Clean Up**: Ensure proper driver cleanup in fixtures

## Support

For issues or questions:
1. Check the log files for detailed error information
2. Verify website accessibility and product availability
3. Review and update locators if website structure changes
4. Ensure all dependencies are properly installed

## License

This project is for educational and testing purposes.
