
from selenium import webdriver

from selenium.webdriver.chrome.options import Options

options = Options()
options.chrome_executable_path = r"C:\Users\zxcvb\Desktop\python sql\python-sql-selenium\chromedriver.exe"

driver = webdriver.Chrome(options = options)
driver.get('https://www.google.com.tw/')
driver.maximize_window()
driver.save_screenshot("screenshot-google.png")
driver.close()