import csv
import numpy as np

# list: 1次元配列
def write_csv(list: list[str]):
	with open('./csv/pages.csv', 'w') as f:
		writer = csv.writer(f)
		to_list = np.array(list).reshape(len(list),1).tolist()
		writer.writerows(to_list)
