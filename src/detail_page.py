import time

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver

import src.csv_defs as csv_defs

# 一覧ページから詳細ページのリンクを取得
# url: 読み込むサイトurl
def get_detail_links(url: str, driver: WebDriver):
	base_path = url + "/result/?pageNum="
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
		# csvに書き込み
		csv_defs.write_detail_links(link_list)
		time.sleep(2)

def analyze_detail_page(detail_page_url: str, driver: WebDriver):
	driver.get(detail_page_url)
	date = ''
	place = ''
	game_index = 0
	source = detail_page_url
	rows = []

	# ブラウザのHTMLを取得
	soup = BeautifulSoup(driver.page_source, features="html.parser")

	match_information = soup.select('.match.section > dl > dt')
	for info in match_information:
		if info.text == '日時':
			date_text = ''
			if info.next_sibling is not None and info.next_sibling.next_sibling is not None:
				date_text = info.next_sibling.next_sibling.text
			date = date_text.strip().replace('  ', '').replace('\n', '')
		if info.text == '会場':
			place_text = ''
			if info.next_sibling is not None and info.next_sibling.next_sibling is not None:
				place_text = info.next_sibling.next_sibling.text
			place = place_text.strip().replace('  ', '').replace('\n', '')

	match_list = soup.select('.matchList.section > dl > dd')
	for game in match_list:
		game_index = game_index + 1
		champions = []
		challengers = []
		game_time = ''
		finish = ''
		win_name = ''
		lose_name = ''
		victory = ''
		# n対nの場合があるのでforする
		match_rows = game.select('.matchWrapper > .row.cf')
		for match in match_rows:
			# champion_tagを抽出
			champ_tag = match.select_one('.left > .name')
			if champ_tag == None:
				champ_tag = match.select_one('.left > a > .name')

			# set champions
			champ_name = ''
			if champ_tag is not None:
				champ_name = champ_tag.text
			champions.extend([champ_name])

			# challengerを抽出
			challenger_tag = match.select_one('.right > .name')
			if challenger_tag == None:
				challenger_tag = match.select_one('.right > a > .name')

			# set challenger
			challenger_name = ''
			if challenger_tag is not None:
				challenger_name = challenger_tag.text
			challengers.extend([challenger_name])

			# game_time, finish
			finish_element = game.select_one('.finish > a')
			finish_section = ''
			if finish_element is not None:
				finish_section = finish_element.text
			finish_list = finish_section.split('　')
			# たまに勝敗やfinishがないデータがある
			if 0 < len(finish_list) and finish_list[0] != '':
				game_time = finish_list[0].strip()
			if 1 < len(finish_list) and finish_list[1] != '':
				finish = finish_list[1].strip()

			# チャンピオンチームの勝敗
			champ_game_image = match.select_one('.left > .resultImg > img')
			if champ_game_image is not None:
				src: str | None = champ_game_image.get('src') #type: ignore
				if src is not None:
					if 'win.png' in src:
						win_name = champ_name
						victory = 'champion'
					elif 'lose.png' in src:
						lose_name = champ_name

			# チャレンジャーチームの勝敗
			challenger_game_image = match.select_one('.right > .resultImg > img')
			if challenger_game_image is not None:
				src: str | None = challenger_game_image.get('src') #type: ignore
				if src is not None:
					if 'win.png' in src:
						win_name = challenger_name
						victory = 'challenger'
					elif 'lose.png' in src:
						lose_name = challenger_name

		# 1列に詰める情報をまとめる
		current_row = ['／'.join(champions), '／'.join(challengers), game_index, date, place, game_time, finish, win_name, lose_name, victory, source]
		rows.append(current_row)
	# 日時でcsvに書き込み
	csv_defs.write_detail_games(rows)
	time.sleep(2)
