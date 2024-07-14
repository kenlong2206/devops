# test_ui.py
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def test_ui():
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Remote(
        command_executor='http://127.0.0.1:4444/wd/hub',
        options=options
    )

    driver.get("http://127.0.0.1:9000")

    # Click Start button
    start_button = driver.find_element(By.ID, "startButton")
    start_button.click()
    time.sleep(2)

    # # Click Stop button
    # stop_button = driver.find_element(By.ID, "stopButton")
    # stop_button.click()
    # time.sleep(2)
    #
    # # Click Reset button
    # reset_button = driver.find_element(By.ID, "resetButton")
    # reset_button.click()
    # time.sleep(2)
    #
    # # Confirm a new sum appears
    # sum_element = driver.find_element(By.ID, "sum")
    # assert sum_element is not None

    driver.quit()

if __name__ == "__main__":
    test_ui()
