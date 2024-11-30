import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

class TestWebDriverUniversity:
  
    @pytest.fixture(scope="class")
    def setup(self):
        """Setup WebDriver for each test class."""
        #self.driver = webdriver.Chrome()
        self.driver = webdriver.Edge()
        self.driver.set_window_size(1296, 688)
        yield self.driver  # This makes driver available in each test
        self.driver.quit()

    def wait_for_window(self, driver, timeout=2):
        """Wait for a new window to open."""
        time.sleep(round(timeout / 1000))
        wh_now = driver.window_handles
        wh_then = self.vars.get("window_handles", [])
        if len(wh_now) > len(wh_then):
            return set(wh_now).difference(set(wh_then)).pop()

    def test_draganddrop(self, setup):
        driver = setup
        driver.get("https://webdriveruniversity.com/")
        driver.find_element(By.CSS_SELECTOR, "#actions h1").click()
        driver.switch_to.window(driver.window_handles[1]) 
        draggable_element = driver.find_element(By.CSS_SELECTOR, "#draggable b")
        drop_target = driver.find_element(By.CSS_SELECTOR, "#droppable")
        actions = ActionChains(driver)
        actions.click_and_hold(draggable_element).move_to_element(drop_target).release().perform()
        WebDriverWait(driver, 5).until(
            lambda driver: drop_target.value_of_css_property("background-color") != "rgba(229, 229, 229, 1)"  # initial color before drop
        )
        new_color = drop_target.value_of_css_property("background-color")
        expected_color = 'rgba(97, 109, 179, 1)' 
        assert new_color == expected_color, f"Expected color to be {expected_color}, but it was {new_color}"

    @pytest.mark.xfail  
    def test_draganddrop_invalid_zone(self, setup):
        driver = setup
        driver.get("https://webdriveruniversity.com/")
        driver.find_element(By.CSS_SELECTOR, "#actions h1").click()
        driver.switch_to.window(driver.window_handles[1])
        draggable_element = driver.find_element(By.CSS_SELECTOR, "#draggable b")
        random_x = 500  
        random_y = 200
        actions = ActionChains(driver)
        actions.click_and_hold(draggable_element).move_by_offset(random_x, random_y).release().perform()
        time.sleep(1) 
        original_position = draggable_element.location
        new_position = draggable_element.location
        assert original_position == new_position, f"Expected element to remain in the original position, but it moved. Original position: {original_position}, New position: {new_position}"
        drop_zone = driver.find_element(By.CSS_SELECTOR, "#droppable")
        drop_zone_color = drop_zone.value_of_css_property('background-color')
        expected_color = 'rgba(255, 255, 255, 1)'  
        assert drop_zone_color == expected_color, f"Expected color to be {expected_color}, but it was {drop_zone_color}"

    def test_double_click_change_color(self, setup):
        driver = setup
        driver.get("https://webdriveruniversity.com/Actions/index.html")
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#double-click"))
        )
        driver.execute_script("arguments[0].scrollIntoView();", button)
        initial_color = button.value_of_css_property("background-color")
        actions = ActionChains(driver)
        actions.double_click(button).perform()
        new_color = button.value_of_css_property("background-color")
        assert initial_color != new_color, f"Expected color to change, but it didn't. Initial: {initial_color}, New: {new_color}"
        expected_green = 'rgba(147, 203, 90, 1)'  
        assert new_color == expected_green, f"Expected color to be {expected_green}, but it was {new_color}"

    def test_clicklink(self, setup):
        driver = setup
        driver.get("https://webdriveruniversity.com/")
        self.vars = {}
        self.vars["window_handles"] = driver.window_handles
        driver.find_element(By.CSS_SELECTOR, "#actions h1").click()
        self.vars["win2662"] = self.wait_for_window(driver, 2000)
        driver.switch_to.window(self.vars["win2662"])
        element = driver.find_element(By.CSS_SELECTOR, ".hover > .dropbtn")
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
        driver.find_element(By.LINK_TEXT, "Link 1").click()
        assert driver.switch_to.alert.text == "Well done you clicked on the link!"
