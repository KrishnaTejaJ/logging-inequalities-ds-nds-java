from config import Config
from openpyxl import Workbook
#from logging import Logging
from file_operations import FileOperations


def finalcalc():
	final_list = []
	final_ = []
	cnt = 0

	final = FileOperations.json.read_json(Config.excel2repo)
	logcount = FileOperations.json.read_json(Config.log_count)
	logvsnlog = FileOperations.json.read_json(Config.logvsnonlog)
	pattern_data = FileOperations.json.read_json(Config.pattern_op)


	for repo, repodata in pattern_data.items():
		#To add the all the repo related data in the before hand
		try:
			final_list.append([final[repo]['Type'], repo, final[repo]['Repo Link'], logcount[repo]['logging'], logcount[repo]['log4j'], logcount[repo]['slf4j'], logcount[repo]['print'], logcount[repo]['tinylog']])
		except KeyError:
			continue
		flag_r = 0
		#Log Level
		for file_, log_data in repodata.items():
			class_counts = {}
			method_counts = {}
			total_classes, total_methods = 0, 0
			log_count = 0
			log_count_sep = {'info' : 0, 'error' : 0, 'warning' : 0, 'debug' : 0, 'trace' : 0}
			log_count_sep_class = {'info' : 0, 'error' : 0, 'warning' : 0, 'debug' : 0, 'trace' : 0}
			log_count_sep_method = {'info' : 0, 'error' : 0, 'warning' : 0, 'debug' : 0, 'trace' : 0}
			for log_name, log_level in log_data.items():
				if log_name in ['info', 'error', 'warning', 'debug', 'trace']:
					log_count += log_data[log_name]['count']
					log_count_sep[log_name] += log_data[log_name]['count']
					for k in log_data[log_name]['lines']:
						if 'class_' in log_data.keys():
							for c in log_data['class_']['lines']:
								if k[0] > c[0] and k[0] < c[1]:
									class_name = 'class_' + str(c[0]) + "-" + str(c[1])
									class_counts[class_name] = class_counts.get(class_name, 0) + 1
									log_count_sep_class[log_name] += 1
						if 'method_' in log_data.keys():
							for m in log_data['method_']['lines']:
								if k[0] > m[0] and k[0] < m[1]:
									method_name = 'method_' + str(m[0]) + "-" + str(m[1])
									method_counts[method_name] = method_counts.get(method_name, 0) + 1
									log_count_sep_method[log_name] += 1
				else:
					if log_name == 'class_':
						total_classes += log_data['class_']['count']
					elif log_name == 'method_':
						total_methods += log_data['method_']['count']

			#Log Density
			log_den_file, log_den_class, log_den_method = 0, 0, 0
			numof_lines = log_data['end_line_']['line']
			if numof_lines != 0:
				log_den_file = log_count/numof_lines
			if 'class_' in log_data.keys() and total_classes != 0:
				log_den_class = log_count/total_classes
			if 'method_' in log_data.keys() and total_methods !=0:
				log_den_method = log_count/total_methods
			if flag_r == 1:
				final_list.append([""] * 8)
				final_list[cnt].extend([file_, log_data['end_line_']['line'], log_den_file, log_den_class, log_den_method, log_count_sep['info'], log_count_sep['error'], log_count_sep['warning'], log_count_sep['debug'], log_count_sep['trace'], log_count_sep_class['info'], log_count_sep_class['error'], log_count_sep_class['warning'], log_count_sep_class['debug'], log_count_sep_class['trace'], log_count_sep_method['info'], log_count_sep_method['error'], log_count_sep_method['warning'], log_count_sep_method['debug'], log_count_sep_method['trace'], "", ""])
			if flag_r == 0:
				final_list[cnt].extend(["-"] * 20)
				final_list[cnt].extend([logvsnlog[repo]['logchanges'] , logvsnlog[repo]['nonlogchanges']])

			flag_r = 1
			cnt += 1

		if flag_r == 0:
			final_list[cnt].extend(["-"] * 20)

	#For adding all the data to the final excel sheet
	book = Workbook()
	sheet = book.active

	for final_row in final_list:
		sheet.append(final_row)

	book.save(Config.final)
