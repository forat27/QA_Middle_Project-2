import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
import time

class TestWebDriverPopups:
    
    @pytest.fixture(scope="module")
    def driver(self):
        """Initialize WebDriver."""
        self.driver = webdriver.Chrome()
        self.driver.get("https://webdriveruniversity.com/Popup-Alerts/index.html")
        yield self.driver
        self.driver.quit()

#Verify page title.
    def test_page_title(self, driver):
        expected_title = "WebDriver | Popups & Alerts"
        assert driver.title == expected_title, f"Page title mismatch! Expected: '{expected_title}', Found: '{driver.title}'"
        print("Page title is correct, page loaded successfully.")

#alert button with ID "button1" is present and visible on the page.
    def test_key_element_present(self, driver):
        alert_button = driver.find_element(By.ID, "button1")
        assert alert_button.is_displayed(), "The alert button is not visible, page might not have loaded correctly."
        print("Key elements are present, page loaded correctly.")


#Clicks OK & Cancel using ESC and Enter for fourth alert.
    def test_buttondismissbykey(self, driver):
        driver.set_window_size(1296, 688)
        driver.execute_script("window.scrollTo(0, 1080)")

        # Click on Enter (OK)
        driver.find_element(By.CSS_SELECTOR, "#button4 > p").click()
        time.sleep(2)
        alert_text_1 = driver.switch_to.alert.text
        driver.switch_to.alert.accept()

        # Click on Esc (Cancel)
        driver.find_element(By.CSS_SELECTOR, "#button4 > p").click()
        time.sleep(2)
        alert_text_2 = driver.switch_to.alert.text
        driver.switch_to.alert.dismiss()

        # Combined assertion
        assert alert_text_1 == "Press a button!" and alert_text_2 == "Press a button!", (
            f"Expected alert text to be 'Press a button!' for both alerts, but got '{alert_text_1}' and '{alert_text_2}'."
        )




#Clicks OK for the first alert.
    def test_oKbuttondismiss(self, driver):
        driver.set_window_size(1296, 688)
        driver.find_element(By.CSS_SELECTOR, "#button1 > p").click()
        assert driver.switch_to.alert.text == "I am an alert box!"
        time.sleep(1)
        driver.switch_to.alert.accept()

#JavaScript Alert Test - Checking text of alert.
    def test_javascript_alert(self, driver):
        alert_button = driver.find_element(By.ID, "button1")
        alert_button.click()
        alert = Alert(driver)
        alert_text = alert.text
        expected_text = "I am an alert box!"
        assert alert_text == expected_text, f"Alert text mismatch! Expected: '{expected_text}', Found: '{alert_text}'"
        alert.accept()
