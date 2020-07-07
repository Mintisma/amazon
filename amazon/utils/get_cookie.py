import os
import pickle

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from amazon.settings import BASE_DIR, COOKIES_FILE_DICT

chrome_options = Options()
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--no-sandbox")


def get_browser_cookie(country, start_url='https://www.amazon.com/'):
    if not os.path.exists(COOKIES_FILE_DICT[country]):
        browser = webdriver.Chrome(executable_path='/Users/ted/Desktop/chromedriver')
        wait = WebDriverWait(browser, 30)
        browser.get(start_url)

        # change address
        addr = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#glow-ingress-line2')))
        addr.click()

        input_zipCode = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[class="GLUX_Full_Width a-declarative"]')))
        zip_code = get_zipcode(country)
        input_zipCode.send_keys(zip_code)

        apply = wait.until(EC.presence_of_element_located((By.XPATH, '//span[@id="GLUXZipUpdate"]')))
        apply.click()

        # confirm
        browser.refresh()

        # get & save cookie
        cookie_dict = dict()
        for cookie in browser.get_cookies():
            cookie_dict[cookie['name']] = cookie['value']
        print(cookie_dict)
        pickle.dump(cookie_dict, open(os.path.join(BASE_DIR, 'cookies/amazon.cookie'), 'wb'))
    else:
        cookie_dict = pickle.load(open(COOKIES_FILE_DICT[country], 'rb'))
        print(cookie_dict)

    return cookie_dict


def get_zipcode(country):
    if country == 'us':
        return '94203'
    if country == 'de':
        return '20095'
    if country == 'fr':
        return '75000'
    if country == 'uk':
        return 'E17AA'
