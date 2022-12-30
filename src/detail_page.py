import time

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver


def get_page_links(url: str, driver: WebDriver):
	base_path = url + "/result/?pageNum="
	page_link_list = []
	# page_max = 136
	page_max = 3
	for x in range(page_max):
		page_num = x + 1
		# URLにアクセス
		driver.get(base_path + str(page_num))

		# ブラウザのHTMLを取得
		BeautifulSoup(driver.page_source, features="html.parser")

		# リンク一覧を取得
		button_links = driver.find_elements(By.LINK_TEXT, '大会結果を見る')
		link_list = []
		for link in button_links:
			link_list.append(link.get_attribute('href'))
		page_link_list.extend(link_list)
		time.sleep(3)
	return page_link_list
