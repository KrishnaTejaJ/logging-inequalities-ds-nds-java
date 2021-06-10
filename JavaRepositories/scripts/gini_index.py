from config import Config
from typing import List
from itertools import combinations
from openpyxl import Workbook
import numpy as np
import pandas as pd

def gini(x: List[float]) -> float:
	x = np.array(x, dtype=np.float32)
	n = len(x)
	diffs = sum(abs(i - j) for i, j in combinations(x, r=2))
	return diffs / (n**2 * x.mean())

#To fetch various gini index input
def gini_input(log_metrics_file):
	log_metrics_data = pd.read_excel(log_metrics_file, header = None)
	final_list = []
	repo_list = ['Type of Repo', 'Repo Name', 'Repo GiniIndex', 'File GiniIndex', 'Class GiniIndex', 'Method GiniIndex', 'File GiniIndex Info', 'File GiniIndex Error', 'File GiniIndex Warning', 'File GiniIndex Debug', 'File GiniIndex Trace', 'Class GiniIndex Info', 'Class GiniIndex Error', 'Class GiniIndex Warning', 'Class GiniIndex Debug', 'Class GiniIndex Trace', 'Method GiniIndex Info', 'Method GiniIndex Error', 'Method GiniIndex Warning', 'Method GiniIndex Debug', 'Method GiniIndex Trace']

	for row in range(0, log_metrics_data.shape[0]):
		if log_metrics_data.iloc[row, 0] in ['DataScience', 'NonDataScience']:
			#print(repo_list)
			final_list.append(repo_list)
			gini_list = []
			for _ in range(18):
				gini_list.append([])
			repo_list = [log_metrics_data.iloc[row, 0], log_metrics_data.iloc[row, 1]]
			gini_repo = gini([log_metrics_data.iloc[row, index] for index in range(3, 8)])
			repo_list.append(gini_repo)
		else:
			if row != log_metrics_data.shape[0]-1:
				if log_metrics_data.iloc[row + 1, 0] not in ['DataScience', 'NonDataScience']:
					for col in range(10, 28):
						gini_list[col-10].append(log_metrics_data.iloc[row, col])
				else:
					gini_sep_ = []
					for col in range(0, 18):
						gini_sep_.append(gini(gini_list[col]))
					repo_list.extend(gini_sep_)
			else:
				for col in range(10, 28):
					gini_list[col-10].append(log_metrics_data.iloc[row, col])
				gini_sep_ = []
				for col in range(0, 18):
					gini_sep_.append(gini(gini_list[col]))
				repo_list.extend(gini_sep_)
				final_list.append(repo_list)

	book = Workbook()
	sheet = book.active
	for final_row in final_list:
		sheet.append(final_row)
	book.save(Config.gini_index)
