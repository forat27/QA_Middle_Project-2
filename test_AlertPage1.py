import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
import time

# Initialize WebDriver
@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.get("https://webdriveruniversity.com/Popup-Alerts/index.html")
    yield driver
    driver.quit()

def test_page_title(driver):
    """Verify the page title."""
    expected_title = "WebDriver | Popups & Alerts"
    assert driver.title == expected_title, f"Page title mismatch! Expected: '{expected_title}', Found: '{driver.title}'"
    print("Page title is correct, page loaded successfully.")

def test_key_element_present(driver):
    """Verify a key element is present."""
    alert_button = driver.find_element(By.ID, "button1")
    assert alert_button.is_displayed(), "The alert button is not visible, page might not have loaded correctly."
    print("Key elements are present, page loaded correctly.")

def test_no_console_errors(driver):
    """Verify there are no JavaScript errors in the console."""
    for log in driver.get_log("browser"):
        assert "error" not in log["message"].lower(), f"JavaScript Error: {log['message']}"
    print("No JavaScript errors found.")

# Clicks OK & Cancel using ESC and Enter for fourth alert
def test_buttondismissbykey(driver):
    driver.get("https://webdriveruniversity.com/Popup-Alerts/index.html")
    driver.set_window_size(1296, 688)
    driver.execute_script("window.scrollTo(0, 1080)")
    # Click on Enter (OK)
    driver.find_element(By.CSS_SELECTOR, "#button4 > p").click()
    time.sleep(2)
    assert driver.switch_to.alert.text == "Press a button!"
    driver.switch_to.alert.accept()
    # Click on Esc (Cancel)
    driver.find_element(By.CSS_SELECTOR, "#button4 > p").click()
    time.sleep(2)
    assert driver.switch_to.alert.text == "Press a button!"
    driver.switch_to.alert.dismiss()
    time.sleep(2)

# Clicks OK for the first alert
def test_oKbuttondismiss(driver):
    driver.get("https://webdriveruniversity.com/Popup-Alerts/index.html")
    driver.set_window_size(1296, 688)
    driver.find_element(By.CSS_SELECTOR, "#button1 > p").click()
    assert driver.switch_to.alert.text == "I am an alert box!"
    time.sleep(1)
    driver.switch_to.alert.accept()

# JavaScript Alert Test - Checking text of alert
def test_javascript_alert(driver):
    alert_button = driver.find_element(By.ID, "button1")
    alert_button.click()
    alert = Alert(driver)
    alert_text = alert.text
    expected_text = "I am an alert box!"
    assert alert_text == expected_text, f"Alert text mismatch! Expected: '{expected_text}', Found: '{alert_text}'"
    alert.accept()

