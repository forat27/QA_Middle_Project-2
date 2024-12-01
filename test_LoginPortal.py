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

class TestLoginPortal():
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
  
  def test_ValidCredentials(self):
    self.driver.get("https://webdriveruniversity.com/")
    self.driver.set_window_size(1296, 688)
    self.vars["window_handles"] = self.driver.window_handles
    self.driver.find_element(By.CSS_SELECTOR, "#login-portal h1").click()
    self.vars["win9519"] = self.wait_for_window(2000)
    self.driver.switch_to.window(self.vars["win9519"])
    self.driver.find_element(By.ID, "text").click()
    self.driver.find_element(By.ID, "text").send_keys("webdriver")
    self.driver.find_element(By.ID, "password").click()
    self.driver.find_element(By.ID, "password").send_keys("webdriver123")
    self.driver.find_element(By.ID, "login-button").click()
    time.sleep(2)
    assert self.driver.switch_to.alert.text == "validation succeeded"


  @pytest.mark.parametrize("username, password, expected_alert", [
        ("webdriver2", "webdriver321", "validation succeeded"),
        ("webdriver", "wrongpass1", "validation failed"),
        ("wrongusername", "webdriver123", "validation failed"),
        ("webdriver", "", "validation failed"),
        ("", "webdriver123", "validation failed"),
        ("", "", "validation failed")])
  def test_LogInPortalInputs(self, username, password, expected_alert):
    self.driver.get("https://webdriveruniversity.com/")
    self.driver.set_window_size(1296, 688)
    self.vars["window_handles"] = self.driver.window_handles
    self.driver.find_element(By.CSS_SELECTOR, "#login-portal h1").click()
    self.vars["win9519"] = self.wait_for_window(2000)
    self.driver.switch_to.window(self.vars["win9519"])
    self.driver.find_element(By.ID, "text").click()
    self.driver.find_element(By.ID, "text").send_keys(username)
    self.driver.find_element(By.ID, "password").click()
    self.driver.find_element(By.ID, "password").send_keys(password)
    self.driver.find_element(By.ID, "login-button").click()
    time.sleep(2)
    assert self.driver.switch_to.alert.text == expected_alert
