import os
import time
from locale import currency

import requests
from datetime import datetime

from chromedriver_py import binary_path
from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup


def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('disable-infobars')
    options.add_argument('start-maximized')
    options.add_argument('disable-dev-shm-usage')
    options.add_argument('disable-blink-features=AutomationControlled')
    options.add_argument('no-sandbox')
    options.add_argument('incognito')
    options.add_argument('disable-extensions')
    options.add_argument('headless')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])

    prefs = {"credentials_enable_service": False,
             "profile.password_manager_enabled": False}
    options.add_experimental_option("prefs", prefs)

    svc = Service(executable_path=binary_path)
    driver = webdriver.Chrome(options=options, service=svc)
    return driver


def first(driver, url, xpath):
    # 1. Get value by XPATH
    driver.get(url=url)
    element = driver.find_element(by=By.XPATH, value=xpath)
    print(f"1.\t{element.text.encode('ascii', 'ignore').decode('ascii')}")


def second(driver, url):
    # 2. Get Dynamic Value by XPATH
    xpath = '/html/body/div[1]/div/h1[2]'
    driver.get(url=url)
    time.sleep(2)  # wait so that the dynamic value can load
    element = driver.find_element(by=By.XPATH, value=xpath)
    print(f"2.\t{element.text.encode('ascii', 'ignore').decode('ascii')}")


def third(driver):
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


def fourth(driver):
    # 4. Exercise
    url = 'https://titan22.com/account/login?return_url=%2Faccount'
    temp_mail = 'vilip20339@aqqor.com'
    uname = 'automate'
    pwd = 'automateautomate'

    driver.get(url)
    driver.find_element(by=By.ID, value='CustomerEmail').send_keys(temp_mail)
    driver.find_element(by=By.ID, value='CustomerPassword').send_keys(pwd)
    actions = ActionChains(driver)
    actions.send_keys(Keys.RETURN).perform()
    time.sleep(2)
    # todo: We encounter a Captcha
    xpath = '//*[@id="shopify-section-footer"]/section/div/div[1]/div[1]/div[1]/nav/ul/li[1]/a'
    el = driver.find_element(by=By.XPATH, value=xpath)
    el.click()
    time.sleep(3)
    print(driver.current_url)


def run():
    url = 'https://automated.pythonanywhere.com/'
    xpath = '/html/body/div[1]/div/h1[1]'
    # driver = get_driver()

    # first(driver, url, xpath)
    # second(driver, url)
    # third(driver)
    # fourth(driver)
    # driver.quit()

    # Fifth
    in_currency, out_currency = 'EUR', 'TRY'
    url = f'https://www.x-rates.com/calculator/?from={in_currency}&to={out_currency}&amount=1'
    print(url)
    content = requests.get(url).text
    soup = BeautifulSoup(content, 'html.parser')
    currency = soup.find('span', class_='ccOutputRslt')
    date = soup.find('span', class_='calOutputTS')
    print(currency.text, date.text)


if __name__ == '__main__':
    run()
