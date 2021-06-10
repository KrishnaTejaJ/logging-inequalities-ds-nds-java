from config import Config
from openpyxl import Workbook
#from logging import Logging
from file_operations import FileOperations

def finalcalc():
	final_list = []
	cnt = 0

	final = FileOperations.json.read_json(Config.excel2repo)
	logcount = FileOperations.json.read_json(Config.log_count)
	logvsnlog = FileOperations.json.read_json(Config.logvsnonlog)
	pattern_data = FileOperations.json.read_json(Config.pattern_op)

	for repo, repodata in pattern_data.items():
		#To add the all the repo related data in the before hand
		try:
			final_list.append([final[repo]['Type'], repo, final[repo]['Repo Link']])
		except KeyError:
			continue
		total = {'class_' : 0, 'method_' : 0, 'end_line_' : 0, 'info' : 0, 'error' : 0, 'warning' : 0, 'debug' : 0, 'trace' : 0}
		files_count = 0
		log_level_lines = ""
		for file_, log_data in repodata.items():
			files_count += 1
			for log_name, log_level in log_data.items():
				if log_name == "end_line_":
					total["end_line_"] += log_data['end_line_']["line"]
				elif log_name in total.keys():
					total[log_name] += log_data[log_name]["count"]
				if log_name in ['info', 'error', 'warning', 'debug', 'trace']:
					log_level_lines += log_data['logs'] + ','

		total_log_lines = logvsnlog[repo]['log_lines']
		if total_log_lines == []:
			total_log_lines = 'No logs'
		else:
			total_log_lines = ""
			for log_line in logvsnlog[repo]['log_lines']:
				total_log_lines += log_line


		final_list[cnt].extend([total['end_line_'], logcount[repo]['logging'], logcount[repo]['log4j'], logcount[repo]['slf4j'], logcount[repo]['print'], logcount[repo]['tinylog'], f"{logvsnlog[repo]['logchanges']} / {logvsnlog[repo]['logchanges'] + logvsnlog[repo]['nonlogchanges']}", total_log_lines, files_count, total['class_'], total['method_'], total['debug'], total['info'], total['warning'], total['error'], total['trace'], log_level_lines])
		cnt += 1

	#For adding all the data to the final excel sheet
	book = Workbook()
	sheet = book.active

	for final_row in final_list:
		sheet.append(final_row)

	book.save(Config.final2)
