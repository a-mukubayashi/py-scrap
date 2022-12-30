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

# 要素が見つかるまで10秒待つ
driver.implicitly_wait(10)

# 詳細ページのリンクを取得
detail_links = detail_page.get_page_links(config.URL, driver)

# csvに書き込み
csv_defs.write_detail_links(detail_links)

driver.quit()
print("=== All done! ===")
