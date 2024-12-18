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

class TestToDoList():
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
    
   
#add tasks to todolist
  @pytest.mark.parametrize("task_input",[("write a poem"), ("In today's fast-paced, technology-driven world, the influence of digital innovation continues to grow exponentially. From smartphones and wearable devices to artificial intelligence and the Internet of Things (IoT), technology is deeply woven into the fabric of our daily lives. It reshapes how we communicate, work, and even think, offering endless opportunities for efficiency and connectivity. However, along with the benefits, this digital transformation brings challenges that require critical attention, such as privacy concerns, cybersecurity threats, and the ethical implications of automation."),
  (" "),("@_^$#$@")])
  def test_addtasks(self,task_input):
    self.driver.get("https://webdriveruniversity.com/To-Do-List/index.html")
    self.driver.set_window_size(1296, 688)
    self.driver.find_element(By.CSS_SELECTOR, "input").click()
    self.driver.find_element(By.CSS_SELECTOR, "input").send_keys(task_input)
    time.sleep(1)
    self.driver.find_element(By.CSS_SELECTOR, "input").send_keys(Keys.ENTER)
    time.sleep(2)
    assert task_input.strip() in [task.text for task in self.driver.find_elements(By.CSS_SELECTOR, "ul > li")]



  def test_deletetaskfromlist(self):
    self.driver.get("https://webdriveruniversity.com/To-Do-List/index.html")
    self.driver.set_window_size(1296, 688)
    self.driver.find_element(By.CSS_SELECTOR, "li:nth-child(1) .fa").click()
    elements = self.driver.find_elements(By.CSS_SELECTOR, "li:nth-child(1)")
    time.sleep(2)
    assert len(elements) == 1


  def test_selecttaskdone(self):
    self.driver.get("https://webdriveruniversity.com/To-Do-List/index.html")
    self.driver.set_window_size(1296, 688)
    element =self.driver.find_element(By.CSS_SELECTOR, "li:nth-child(1)")
    element.click()
    time.sleep(2)
    classes: str = element.get_attribute('class')
    assert classes.find('completed') != -1
