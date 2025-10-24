from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import unittest

class LoginTest(unittest.TestCase):
    
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://your-login-page.com")
        self.wait = WebDriverWait(self.driver, 10)
    
    def test_valid_login(self):
        # AI-powered element location
        username_field = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
        password_field = self.driver.find_element(By.NAME, "password")
        login_button = self.driver.find_element(By.XPATH, "//button[contains(text(),'Login')]")
        
        username_field.send_keys("valid_user")
        password_field.send_keys("correct_password")
        login_button.click()
        
        # AI-enhanced validation - dynamic success element detection
        success_indicator = self.wait.until(
            EC.any_of(
                EC.presence_of_element_located((By.ID, "dashboard")),
                EC.presence_of_element_located((By.CLASS_NAME, "welcome-message")),
                EC.url_contains("dashboard")
            )
        )
        self.assertTrue(success_indicator, "Valid login failed")
    
    def test_invalid_login(self):
        username_field = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
        password_field = self.driver.find_element(By.NAME, "password")
        login_button = self.driver.find_element(By.XPATH, "//button[contains(text(),'Login')]")
        
        username_field.send_keys("invalid_user")
        password_field.send_keys("wrong_password")
        login_button.click()
        
        # AI-powered error message detection
        error_message = self.wait.until(
            EC.any_of(
                EC.presence_of_element_located((By.CLASS_NAME, "error")),
                EC.presence_of_element_located((By.ID, "error-message")),
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Invalid')]"))
            )
        )
        self.assertTrue(error_message.is_displayed(), "Error message not displayed")
    
    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    # Run tests and capture results
    suite = unittest.TestLoader().loadTestsFromTestCase(LoginTest)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Calculate success rates
    total_tests = result.testsRun
    failed_tests = len(result.failures) + len(result.errors)
    success_rate = ((total_tests - failed_tests) / total_tests) * 100
    
    print(f"\n=== TEST RESULTS ===")
    print(f"Total Tests: {total_tests}")
    print(f"Failed Tests: {failed_tests}")
    print(f"Success Rate: {success_rate:.2f}%")
