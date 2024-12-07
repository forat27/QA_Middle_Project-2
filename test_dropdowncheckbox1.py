import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC

class TestCheckboxes():
  def setup_method(self, method):
    self.driver = webdriver.Chrome()
    #self.driver = webdriver.Edge()

    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def wait_for_window(self, timeout = 2):
    time.sleep(round(timeout / 1000))
    wh_now = self.driver.window_handles
    wh_then = self.vars["window_handles"]
    if len(wh_now) > len(wh_then):
      return set(wh_now).difference(set(wh_then)).pop()
  

#selecting checkboxes
  def test_checkboxes(self):
    self.driver.get("https://webdriveruniversity.com/Dropdown-Checkboxes-RadioButtons/")
    self.driver.set_window_size(1296, 688)
    checkboxes = [
        "label:nth-child(1) > input",
        "label:nth-child(3) > input",
        "label:nth-child(7) > input",
        "label:nth-child(5) > input"
    ]
    for selector in [checkboxes[0], checkboxes[1], checkboxes[2]]:
        checkbox = self.driver.find_element(By.CSS_SELECTOR, selector)
        checkbox.click()
        time.sleep(0.3)
    for selector in [checkboxes[2], checkboxes[3], checkboxes[1], checkboxes[0]]:
        checkbox = self.driver.find_element(By.CSS_SELECTOR, selector)
        checkbox.click()
        time.sleep(0.3)
    final_states = [
        self.driver.find_element(By.CSS_SELECTOR, selector).is_selected()
        for selector in checkboxes
    ]
    assert not any(final_states), f"Expected all checkboxes to be deselected, but got: {final_states}"

    

#testing selected elements state after refreshing page (do not get saved)   
  @pytest.mark.xfail(reason="Checkbox states do not persist after page refresh")
  def test_refreshcheckbox(self):
      self.driver.get("https://webdriveruniversity.com/Dropdown-Checkboxes-RadioButtons/")
      self.driver.set_window_size(1296, 688)
      checkbox1 = self.driver.find_element(By.CSS_SELECTOR, "label:nth-child(1) > input")
      checkbox1.click()
      time.sleep(0.5)
      checkbox2 = self.driver.find_element(By.NAME, "color")
      checkbox2.click()
      time.sleep(0.5)
      checkbox1_state = checkbox1.is_selected()
      checkbox2_state = checkbox2.is_selected()
      time.sleep(1)
      self.driver.refresh()
      assert (self.driver.find_element(By.CSS_SELECTOR, "label:nth-child(1) > input").is_selected() == checkbox1_state and
            self.driver.find_element(By.CSS_SELECTOR, "input:nth-child(7)").is_selected() == checkbox2_state), (
        f"Expected checkbox states to persist after refresh. "
        f"Checkbox 1: {checkbox1_state}, Checkbox 2: {checkbox2_state}. "
        f"Got: {self.driver.find_element(By.CSS_SELECTOR, 'label:nth-child(1) > input').is_selected()} "
        f"and {self.driver.find_element(By.CSS_SELECTOR, 'input:nth-child(7)').is_selected()}"
    )
    


#selecting dropdown using keyboard
  def test_dropdownkeyboard(self):
    self.driver.get("https://webdriveruniversity.com/Dropdown-Checkboxes-RadioButtons/")
    self.driver.set_window_size(1296, 688)
    self.driver.find_element(By.ID, "dropdowm-menu-1").click()
    dropdown1 = self.driver.find_element(By.ID, "dropdowm-menu-1")
    #first-Python-third choice
    select1=dropdown1.find_element(By.XPATH, "//option[. = 'Python']")
    time.sleep(0.3)
    select1.click()
    self.driver.find_element(By.ID, "dropdowm-menu-2").click()
    dropdown2 = self.driver.find_element(By.ID, "dropdowm-menu-2")
    #second-Mavens-second choice
    select2=dropdown2.find_element(By.XPATH, "//option[. = 'Maven']")
    time.sleep(0.3)
    select2.click()
    self.driver.find_element(By.ID, "dropdowm-menu-3").click()
    dropdown3 = self.driver.find_element(By.ID, "dropdowm-menu-3")
    #third-JavaScript-third choice
    select3=dropdown3.find_element(By.XPATH, "//option[. = 'JavaScript']")
    time.sleep(0.3)
    select3.click()
    select1_state=select1.is_selected()
    select2_state=select2.is_selected()
    select3_state=select3.is_selected()
    assert (dropdown1.find_element(By.XPATH, "//option[. = 'Python']").is_selected() == select1_state and
          dropdown2.find_element(By.XPATH, "//option[. = 'Maven']").is_selected() == select2_state and
          dropdown3.find_element(By.XPATH, "//option[. = 'JavaScript']").is_selected() == select3_state), (
      f"Expected selected states to be Python: {select1_state}, Maven: {select2_state}, JavaScript: {select3_state}. "
      f"Got: Python: {dropdown1.find_element(By.XPATH, '//option[. = \'Python\']').is_selected()}, "
      f"Maven: {dropdown2.find_element(By.XPATH, '//option[. = \'Maven\']').is_selected()}, "
      f"JavaScript: {dropdown3.find_element(By.XPATH, '//option[. = \'JavaScript\']').is_selected()}"
    )


#selecting checkboxes using keyboard
  def test_checkbox_keyboard(self):
    self.driver.get("https://webdriveruniversity.com/Dropdown-Checkboxes-RadioButtons/")
    self.driver.set_window_size(1296, 688)
    expected_states = {}
    checkbox_indices = [1, 3, 5, 7]
    for i in checkbox_indices:
        time.sleep(0.5)
        checkbox = self.driver.find_element(By.CSS_SELECTOR, f"label:nth-child({i}) > input")
        checkbox.send_keys(Keys.SPACE)
        print(f"Toggled checkbox {i} using SPACE.")
        expected_states[f"checkbox{i}"] = checkbox.is_selected()
    actual_states = {
        f"checkbox{i}": self.driver.find_element(By.CSS_SELECTOR, f"label:nth-child({i}) > input").is_selected()
        for i in checkbox_indices
    }
    assert actual_states == expected_states, (
        f"Checkbox states do not match. Expected: {expected_states}, Got: {actual_states}"
    )



#verify all dropdown options display correctly (3tests) - 
# u cant really see what the code is doing since its only verifying the options presence
  @pytest.mark.parametrize("dropdown_id, expected_options", 
      [
          ("dropdowm-menu-1", ["JAVA", "C#", "Python", "SQL"]),  # First dropdown
          ("dropdowm-menu-2", ["Eclipse", "Maven", "TestNG","JUnit"]),
            ("dropdowm-menu-3", ["HTML", "CSS", "JavaScript","JQuery"])
      ])
  def test_dropdown_options(self, dropdown_id, expected_options):
      self.driver.get("https://webdriveruniversity.com/Dropdown-Checkboxes-RadioButtons/")
      self.driver.set_window_size(1296, 688)
      dropdown = WebDriverWait(self.driver, 10).until(
          EC.presence_of_element_located((By.ID, dropdown_id))
      )
      select = Select(dropdown)
      options = select.options
      option_texts = [option.text for option in options]
      assert sorted(option_texts) == sorted(expected_options), f"Expected options {expected_options}, but got {option_texts}"