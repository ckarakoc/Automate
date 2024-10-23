import os
import time
from datetime import datetime

from chromedriver_py import binary_path
from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By


def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('disable-infobars')
    options.add_argument('start-maximized')
    options.add_argument('disable-dev-shm-usage')
    options.add_argument('disable-blink-features=AutomationControlled')
    options.add_argument('no-sandbox')
    options.add_argument('--headless')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])

    svc = webdriver.ChromeService(executable_path=binary_path)
    driver = webdriver.Chrome(options=options, service=svc)
    return driver


def run():
    url = 'https://automated.pythonanywhere.com/'
    xpath = '/html/body/div[1]/div/h1[1]'
    driver = get_driver()

    # 1. Get value by XPATH
    # driver.get(url=url)
    # element = driver.find_element(by=By.XPATH, value=xpath)
    # print(f"1.\t{element.text.encode('ascii', 'ignore').decode('ascii')}")

    # 2. Get Dynamic Value by XPATH
    # xpath = '/html/body/div[1]/div/h1[2]'
    # driver.get(url=url)
    # time.sleep(2)  # wait so that the dynamic value can load
    # element = driver.find_element(by=By.XPATH, value=xpath)
    # print(f"2.\t{element.text.encode('ascii', 'ignore').decode('ascii')}")

    # 3. Login
    url = 'https://automated.pythonanywhere.com/login/'
    xpath = '/html/body/nav/div/a'
    uname = 'automated'
    pwd = 'automatedautomated'

    driver.get(url=url)
    driver.find_element(by=By.ID, value='id_username').send_keys(uname)
    driver.find_element(by=By.ID, value='id_password').send_keys(pwd)

    actions = ActionChains(driver)
    actions.send_keys(Keys.RETURN).perform()
    print(f"3.\t{driver.current_url}")

    driver.find_element(by=By.XPATH, value=xpath).click()
    print(f"\t{driver.current_url}")

    xpath = '/html/body/div[1]/div/h1[2]'
    el = driver.find_element(by=By.XPATH, value=xpath)
    time.sleep(2)
    print(f"\t{float(el.text.split(':')[1])}")

    count = 5
    arr = []
    while count != 0:
        el = driver.find_element(by=By.XPATH, value=xpath)
        arr.append(f"Writing to file: {datetime.now().strftime("%Y-%m-%d-%H-%M-%S")} {float(el.text.split(':')[1])}")
        time.sleep(2)
        count -= 1

    current_dir = os.path.dirname(__file__)
    path = os.path.join(current_dir, 'trash', 'output.txt')
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, 'w') as f:
        f.write(str.join('\n', arr))

    driver.quit()


if __name__ == '__main__':
    run()
