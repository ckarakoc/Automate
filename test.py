from selenium import webdriver
from chromedriver_py import binary_path  # this will get you the path variable
from selenium.webdriver.chrome.service import Service

svc = Service(executable_path=binary_path)
driver = webdriver.Chrome(service=svc)

# deprecated but works in older selenium versions
# driver = webdriver.Chrome(executable_path=binary_path)
driver.get("http://www.python.org")

driver.quit()
