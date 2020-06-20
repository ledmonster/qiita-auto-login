import os
import time
from urllib.parse import urlparse

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

CLIENT_ID = os.environ["client_id"]
EMAIL = os.environ["email"]
PASSWORD = os.environ["password"]
CHROME_PATH = '/opt/chrome/headless-chromium'
CHROMEDRIVER_PATH = '/opt/chrome/chromedriver'

REDIRECT_URL="http://localhost:8081/"


def lambda_handler(event, context):
    options = Options()
    options.binary_location = CHROME_PATH
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--single-process')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(CHROMEDRIVER_PATH, chrome_options=options)
    driver.get(f"https://qiita.com/api/v2/oauth/authorize?client_id={CLIENT_ID}&scope=read_qiita+write_qiita_team")
    
    # qiita ログイン画面
    email_field = driver.find_element_by_id("identity")
    email_field.send_keys(EMAIL)
    password_field = driver.find_element_by_id("password")
    password_field.send_keys(PASSWORD)
    login_button = driver.find_element_by_name("commit")
    login_button.click()
    
    # 認可
    driver.implicitly_wait(10)
    driver.find_element_by_name("authenticity_token")
    permit_button = driver.find_element_by_name("commit")
    permit_button.click()
    
    # 現在のURL
    time.sleep(5)
    parsed = urlparse(driver.current_url)

    return {"code": parsed.query.split("=")[1]}
