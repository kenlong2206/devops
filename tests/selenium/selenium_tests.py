import os
import time
import unittest
import HtmlTestRunner
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class ClientAppTests(unittest.TestCase):

    def setUp(self):
        # Setup WebDriver and options
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--headless")  # Optional: run in headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # Adjust the URL based on environment variable or default to localhost
        self.app_url = os.getenv('APP_URL', 'http://localhost:9000')
        self.driver = webdriver.Remote(
            command_executor=os.getenv('SELENIUM_HUB_URL', 'http://localhost:4444/wd/hub'),
            options=chrome_options
        )

    def tearDown(self):
        # Cleanup after each test
        self.driver.quit()

    def test_start_sending_and_stop(self):
        self.driver.get(self.app_url)

        # Click Start button
        start_button = self.driver.find_element(By.ID, "startButton")
        start_button.click()

        # Allow time for some results to be generated
        time.sleep(3)

        # Click Stop button
        stop_button = self.driver.find_element(By.ID, "stopButton")
        stop_button.click()

        # Verify that results have been generated
        result_rows = self.driver.find_elements(By.XPATH, "//tbody[@id='result-body']/tr")
        self.assertGreater(len(result_rows), 0)

    def test_reset_results(self):
        self.driver.get(self.app_url)

        # Click Start button
        start_button = self.driver.find_element(By.ID, "startButton")
        start_button.click()

        # Allow time for some results to be generated
        time.sleep(3)

        # Click Reset button
        reset_button = self.driver.find_element(By.ID, "resetButton")
        reset_button.click()

        # Verify that results are cleared
        result_rows = self.driver.find_elements(By.XPATH, "//tbody[@id='result-body']/tr")
        self.assertEqual(len(result_rows), 0)

    def test_delay_input(self):
        self.driver.get(self.app_url)

        # Set a different delay value
        delay_input = self.driver.find_element(By.ID, "delay")
        delay_input.clear()
        delay_input.send_keys("2")

        # Click Start button
        start_button = self.driver.find_element(By.ID, "startButton")
        start_button.click()

        # Allow time for results to be generated with the new delay
        time.sleep(4)  # Allow some buffer for results to be generated

        # Verify that results have been generated with the new delay
        result_rows = self.driver.find_elements(By.XPATH, "//tbody[@id='result-body']/tr")
        self.assertGreater(len(result_rows), 0)


if __name__ == "__main__":
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='/app/tests/test_reports'))
