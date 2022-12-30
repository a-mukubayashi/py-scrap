import time

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver

# 一覧ページから詳細ページのリンクを取得
# url: 読み込むサイトurl
def get_detail_links(url: str, driver: WebDriver):
	base_path = url + "/result/?pageNum="
	page_link_list = []
	# page_max = 136
	page_max = 3
	for x in range(page_max):
		page_num = x + 1
		# URLにアクセス
		driver.get(base_path + str(page_num))

		# リンク一覧を取得
		button_links = driver.find_elements(By.LINK_TEXT, '大会結果を見る')
		link_list = []
		for link in button_links:
			link_list.append(link.get_attribute('href'))
		page_link_list.extend(link_list)
		time.sleep(3)
	return page_link_list

def analyze_detail_page(detail_page_url: str, driver: WebDriver):
	driver.get(detail_page_url)
	headers = ['champion', 'challenger', 'game index', 'date', 'place', 'source']
	rows = [headers]
	date = ''
	place = ''
	source = detail_page_url

	# ブラウザのHTMLを取得
	soup = BeautifulSoup(driver.page_source, features="html.parser")

	match_information = soup.select('.match.section > dl > dt')
	for info in match_information:
		if info.text == '日時':
			dd_tag_text = info.next_sibling.next_sibling.text # type: ignore
			date = dd_tag_text.strip().replace('  ', '').replace('\n', '')
		if info.text == '会場':
			dd_tag_text = info.next_sibling.next_sibling.text # type: ignore
			place = dd_tag_text.strip().replace('  ', '').replace('\n', '')

	match_list = soup.select('.matchList.section > dl > dd')
	game_index = 0
	for game in match_list:
		game_index = game_index + 1
		champions = []
		challengers = []
		# n対nの場合があるのでforする
		match_rows = game.select('.matchWrapper > .row.cf')
		for match in match_rows:
			# championを抽出
			champ_tag = match.select_one('.left > .name')
			if champ_tag == None:
				champ_tag = match.select_one('.left > a > .name')
			# set champions
			if champ_tag is not None:
				champions.extend([champ_tag.text])
			elif champ_tag == None:
				champions.extend([''])
			# challengerを抽出
			challenger_tag = match.select_one('.right > .name')
			if challenger_tag == None:
				challenger_tag = match.select_one('.right > a > .name')
			# set challenger
			if challenger_tag is not None:
				challengers.extend([challenger_tag.text])
			elif challenger_tag == None:
				challengers.extend([''])
		# 1列に詰める情報をまとめる
		current_row = ['／'.join(champions), '／'.join(challengers), game_index, date, place, source]
		rows.append(current_row) # type: ignore

	return rows
