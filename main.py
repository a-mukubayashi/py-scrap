import time
import os

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By

import csv_page

# ブラウザのオプション
options = Options()
options.add_argument("--blink-settings=imagesEnabled=false")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-browser-side-navigation")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
# options.add_argument("--headless")  # ブラウザを非表示で起動する
options.add_argument("--ignore-certificate-errors")
options.add_argument("--incognito")
options.add_argument("--no-sandbox")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_experimental_option("useAutomationExtension", False)

# ブラウザ起動
service = ChromeService(executable_path="./chromedriver_mac_arm64/chromedriver")
driver = webdriver.Chrome(service=service, options=options)

# # 要素が見つかるまで10秒待つ
driver.implicitly_wait(10)

URL = os.getenv('URL')
base_path = URL + "/result/?pageNum="

page_link_list = []
# page_max = 136
page_max = 3
page_min = 1
for x in range(page_max):
	page_num = x + 1
	# URLにアクセス
	driver.get(base_path + str(page_num))

	# ブラウザのHTMLを取得
	soup = BeautifulSoup(driver.page_source, features="html.parser")

	# リンク一覧を取得
	button_links = driver.find_elements(By.LINK_TEXT, '大会結果を見る')
	link_list = []
	for link in button_links:
		link_list.append(link.get_attribute('href'))
	page_link_list.extend(link_list)
	time.sleep(3)

# csvに書き込み
csv_page.write_csv(page_link_list)

driver.quit()
print("=== All done! ===")
