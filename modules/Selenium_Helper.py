from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action.chains import ActionChains

class Selenium_Helper(object):
    def __init__(self, driverPath, url):
        self.driver = webdriver.Chrome(service=Service(driverPath))
        self.driver.get(url)
        self.driverMaxwait = 30

    def clear_fill_element(self, pathType, path, fill):
        element = self.waitOn_find_element(pathType, path)
        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(Keys.DELETE)
        element.send_keys(fill)

    def sendKeyTo_element(self, pathType, path, key, times):
        element = self.waitOn_find_element(pathType, path)
        actions = ActionChains(self.driver).move_to_element(element).click(element)
        for _ in range(times):
            actions.send_keys(key)
        actions.perform()

    def click_element(self, pathType, path):
        element= self.waitOn_find_element (pathType, path)
        ActionChains(self.driver).move_to_element(element).click(element).perform()

    def waitOn_find_element(self, pathType, path):
        WebDriverWait(self.driver, self.driverMaxwait).until(EC.presence_of_element_located((pathType, path)))
        return self.driver.find_element (pathType, path)

    def wait(self, seconds):
        self.driver.implicitly_wait(seconds)

    def end(self):
        self.driver.quit