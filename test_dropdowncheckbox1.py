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
    # self.driver = webdriver.Chrome()
    self.driver = webdriver.Edge()
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
    self.driver.get("https://webdriveruniversity.com/")
    self.driver.set_window_size(1296, 688)
    self.vars["window_handles"] = self.driver.window_handles
    self.driver.find_element(By.CSS_SELECTOR, "#dropdown-checkboxes-radiobuttons h1").click()
    self.vars["win4182"] = self.wait_for_window(2000)
    self.driver.switch_to.window(self.vars["win4182"])
    #select checkbox
    self.driver.find_element(By.CSS_SELECTOR, "label:nth-child(1) > input").click()
    time.sleep(0.3)
    self.driver.find_element(By.CSS_SELECTOR, "label:nth-child(3) > input").click()
    time.sleep(0.3)
    self.driver.find_element(By.CSS_SELECTOR, "label:nth-child(7) > input").click()
    #deselect checkbox
    time.sleep(0.3)
    self.driver.find_element(By.CSS_SELECTOR, "label:nth-child(7) > input").click()
    time.sleep(0.3)
    self.driver.find_element(By.CSS_SELECTOR, "label:nth-child(5) > input").click()
    time.sleep(0.3)
    self.driver.find_element(By.CSS_SELECTOR, "label:nth-child(3) > input").click()
    time.sleep(0.3)
    self.driver.find_element(By.CSS_SELECTOR, "label:nth-child(1) > input").click()

    
#testing selected elements state after refreshing page (do not get saved)   
  @pytest.mark.xfail(reason="Checkbox states do not persist after page refresh")
  def test_refreshcheckbox(self):
      self.driver.get("https://webdriveruniversity.com/")
      self.driver.set_window_size(1296, 688)
      self.vars["window_handles"] = self.driver.window_handles
      self.driver.find_element(By.CSS_SELECTOR, "#dropdown-checkboxes-radiobuttons h1").click()
      self.vars["win5780"] = self.wait_for_window(2000)
      self.driver.switch_to.window(self.vars["win5780"])
      checkbox1 = self.driver.find_element(By.CSS_SELECTOR, "label:nth-child(1) > input")
      checkbox1.click()
      checkbox2 = self.driver.find_element(By.NAME, "color")
      checkbox2.click()
      checkbox1_state = checkbox1.is_selected()
      checkbox2_state = checkbox2.is_selected()
      self.driver.refresh()
      assert self.driver.find_element(By.CSS_SELECTOR, "label:nth-child(1) > input").is_selected() != checkbox1_state
      assert self.driver.find_element(By.CSS_SELECTOR, "input:nth-child(7)").is_selected() != checkbox2_state


#selecting dropdown using keyboard
  def test_dropdownkeyboard(self):
    self.driver.get("https://webdriveruniversity.com/")
    self.driver.set_window_size(1296, 688)
    self.vars["window_handles"] = self.driver.window_handles
    self.driver.find_element(By.CSS_SELECTOR, "#dropdown-checkboxes-radiobuttons h1").click()
    self.vars["win4527"] = self.wait_for_window(2000)
    self.driver.switch_to.window(self.vars["win4527"])
    self.driver.find_element(By.ID, "dropdowm-menu-1").click()
    dropdown = self.driver.find_element(By.ID, "dropdowm-menu-1")
    #first-Python-third choice
    select1=dropdown.find_element(By.XPATH, "//option[. = 'Python']")
    select1.click()
    self.driver.find_element(By.ID, "dropdowm-menu-2").click()
    dropdown = self.driver.find_element(By.ID, "dropdowm-menu-2")
    #second-Mavens-second choice
    select2=dropdown.find_element(By.XPATH, "//option[. = 'Maven']")
    select2.click()
    self.driver.find_element(By.ID, "dropdowm-menu-3").click()
    dropdown = self.driver.find_element(By.ID, "dropdowm-menu-3")
    #third-JavaScript-third choice
    select3=dropdown.find_element(By.XPATH, "//option[. = 'JavaScript']")
    select3.click()
    select1_state=select1.is_selected()
    select2_state=select2.is_selected()
    select3_state=select3.is_selected()
    assert dropdown.find_element(By.XPATH, "//option[. = 'JavaScript']").is_selected()==select3_state
    assert dropdown.find_element(By.XPATH, "//option[. = 'Maven']").is_selected()==select2_state
    assert dropdown.find_element(By.XPATH, "//option[. = 'Python']").is_selected()==select1_state


#selecting checkboxes using keyboard
  def test_checkbox_keyboard(self):
    self.driver.get("https://webdriveruniversity.com/")
    self.driver.set_window_size(1296, 688)
    self.vars["window_handles"] = self.driver.window_handles
    self.driver.find_element(By.CSS_SELECTOR, "#dropdown-checkboxes-radiobuttons .section-title").click()
    self.vars["win1916"] = self.wait_for_window(2000)
    self.driver.switch_to.window(self.vars["win1916"])
    # Focus on the first checkbox using Tab
    first_checkbox = self.driver.find_element(By.CSS_SELECTOR, "label:nth-child(1) > input")
    first_checkbox.send_keys(Keys.TAB) 
    print("Pressed Tab to focus on the first checkbox.")
    # Press Space to select/deselect
    first_checkbox.send_keys(Keys.SPACE)
    print("Pressed Space to toggle the first checkbox.")
    # Repeat for the other checkboxes
    for i in [3, 5, 7]:
        time.sleep(2)
        checkbox = self.driver.find_element(By.CSS_SELECTOR, f"label:nth-child({i}) > input")
        checkbox.send_keys(Keys.TAB)
        print(f"Pressed Tab to focus on checkbox {i}.")
        checkbox.send_keys(Keys.SPACE)
        print(f"Pressed Space to toggle checkbox {i}.")



#verify all dropdown options display correctly (3tests)
  @pytest.fixture(scope="class")
  def setup(self):
      self.driver = webdriver.Chrome()
      self.driver.get("https://webdriveruniversity.com/Dropdown-Checkboxes-RadioButtons/index.html")
      yield self.driver
      self.driver.quit()
  @pytest.mark.parametrize(
      "dropdown_id, expected_options", 
      [
          ("dropdowm-menu-1", ["JAVA", "C#", "Python", "SQL"]),  # First dropdown
          ("dropdowm-menu-2", ["Eclipse", "Maven", "TestNG","JUnit"]),
            ("dropdowm-menu-3", ["HTML", "CSS", "JavaScript","JQuery"])
      ])
  def test_dropdown_options(self, setup, dropdown_id, expected_options):
      driver = setup
      dropdown = WebDriverWait(driver, 10).until(
          EC.presence_of_element_located((By.ID, dropdown_id))
      )
      select = Select(dropdown)
      options = select.options
      option_texts = [option.text for option in options]
      assert sorted(option_texts) == sorted(expected_options), f"Expected options {expected_options}, but got {option_texts}"
