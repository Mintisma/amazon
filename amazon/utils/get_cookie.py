import os
import pickle

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from amazon.settings import BASE_DIR, COOKIES_FILE

chrome_options = Options()
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--no-sandbox")


def get_browser_cookie(start_url='https://www.amazon.com/'):
    if not os.path.exists(COOKIES_FILE):
        browser = webdriver.Chrome(executable_path='/Users/ted/Desktop/chromedriver')
        wait = WebDriverWait(browser, 10)
        browser.get(start_url)

        # change address
        addr = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#glow-ingress-line2')))
        addr.click()

        input_zipCode = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[class="GLUX_Full_Width a-declarative"]')))
        input_zipCode.send_keys('94203')

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
        cookie_dict = pickle.load(open(COOKIES_FILE, 'rb'))
        print(cookie_dict)

    return cookie_dict