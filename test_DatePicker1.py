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
from datetime import datetime

class TestDatePickerOpen():
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
  
#clicking on the input field or icon to open calender (2 tests)
  @pytest.mark.parametrize("selector", [".glyphicon", ".form-control"])
  def test_datePickerOpen(self, selector):
      self.driver.get("https://webdriveruniversity.com/Datepicker/index.html")
      self.driver.set_window_size(1296, 688)
      self.driver.find_element(By.CSS_SELECTOR, selector).click()
      elements = self.driver.find_elements(By.CSS_SELECTOR, ".datepicker")
      assert len(elements) > 0
      time.sleep(2)
  

#current date is pre selected
  def test_currentdatepreselected(self):
    self.driver.get("https://webdriveruniversity.com/")
    self.driver.set_window_size(1050, 652)
    self.vars["window_handles"] = self.driver.window_handles
    self.driver.find_element(By.CSS_SELECTOR, "#datepicker h1").click()
    self.vars["win6257"] = self.wait_for_window(2000)
    self.driver.switch_to.window(self.vars["win6257"])
    today_date = datetime.now().strftime("%m-%d-%Y")
    assert self.driver.find_element(By.CSS_SELECTOR, "#datepicker input").get_attribute("value") == today_date


#date updates in every click
  def test_updatedate(self):
    self.driver.get("https://webdriveruniversity.com/Datepicker/index.html")
    self.driver.set_window_size(1296, 688)
    self.driver.find_element(By.CSS_SELECTOR, ".glyphicon").click()
    initial_date = datetime.now().strftime("%m-%d-%Y")
    new_date=self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(2) > .day:nth-child(7)").click()
    assert initial_date != new_date, f"Date did not change! Initial: {initial_date}, New: {new_date}"
    time.sleep(2)


#past date
  def test_pastdates(self):
    self.driver.get("https://webdriveruniversity.com/")
    self.driver.set_window_size(1296, 688)
    self.vars["window_handles"] = self.driver.window_handles
    self.driver.find_element(By.CSS_SELECTOR, "#datepicker h1").click()
    self.vars["win299"] = self.wait_for_window(2000)
    self.driver.switch_to.window(self.vars["win299"])
    self.driver.find_element(By.CSS_SELECTOR, ".input-group-addon").click()
    self.driver.find_element(By.CSS_SELECTOR, ".datepicker-days .datepicker-switch").click()
    self.driver.find_element(By.CSS_SELECTOR, ".datepicker-months .datepicker-switch").click()
    self.driver.find_element(By.CSS_SELECTOR, ".datepicker-years .prev").click()
    self.driver.find_element(By.CSS_SELECTOR, ".year:nth-child(1)").click()
    self.driver.find_element(By.CSS_SELECTOR, ".month:nth-child(2)").click()
    self.driver.find_element(By.CSS_SELECTOR, ".old:nth-child(4)").click()
    assert self.driver.find_element(By.CSS_SELECTOR, "#datepicker input").get_attribute("value") == "01-28-2009"
