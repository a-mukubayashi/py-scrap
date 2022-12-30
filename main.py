from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService

import src.csv_defs as csv_defs
import src.detail_page as detail_page
import config

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

# 詳細ページのリンクを取得
detail_page.get_detail_links(config.URL, driver)

# 詳細ページの解析, csvへ出力
links = csv_defs.read_detail_links()
headers = ['champion', 'challenger', 'game_index', 'date', 'place', 'game_time', 'finish', 'win_name', 'lose_name', 'victory', 'source']
csv_defs.write_detail_games([headers])
for link in links:
	detail_page.analyze_detail_page(link, driver)

driver.quit()
print("=== All done! ===")
