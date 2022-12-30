import csv
import numpy as np

# 詳細ページのリンクをcsvファイルに書き込み
# list: 1次元配列
def write_detail_links(list: list[str]):
	with open('./csv/page_detail_links.csv', 'w') as f:
		writer = csv.writer(f)
		to_list = np.array(list).reshape(len(list),1).tolist()
		writer.writerows(to_list)

# 詳細ページのリンクをcsvファイルから読み込み
def read_detail_links():
	with open('./csv/page_detail_links.csv') as f:
		reader = csv.reader(f)
		rows: list[str] = []
		for row in reader:
			rows.extend(row)
		return rows
