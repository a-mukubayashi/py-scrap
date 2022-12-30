import time
import os

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By

# ブラウザのオプション
options = Options()
options.add_argument("--blink-settings=imagesEnabled=false")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-browser-side-navigation")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--headless")  # ブラウザを非表示で起動する
options.add_argument("--ignore-certificate-errors")
options.add_argument("--incognito")
options.add_argument("--no-sandbox")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_experimental_option("useAutomationExtension", False)

# ブラウザ起動
service = ChromeService(executable_path="./chromedriver_mac_arm64/chromedriver")
driver = webdriver.Chrome(service=service, options=options)

# 要素が見つかるまで10秒待つ
driver.implicitly_wait(10)

# URLにアクセス
URL = os.getenv('URL')
base_path = URL + "/result/"
query = "?pageNum=136"
url = base_path + query
driver.get(url)
time.sleep(1)

# ブラウザのHTMLを取得
soup = BeautifulSoup(driver.page_source, features="html.parser")

# リンク一覧を取得
button_links = driver.find_elements(By.LINK_TEXT, '大会結果を見る')
for link in button_links:
	print(link.get_attribute('href'))
