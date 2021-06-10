import pandas as pd
from file_operations import FileOperations
from config import Config
import os
import glob

#To find the logs and categorise into info, warning, critical and error
class LogLevel:

	#json for storing the log level info of the repos
	def semgrep2json():
		paths = [f"{Config.datascience}*/", f"{Config.nondatascience}*/"]
		for path in paths:
			for folder in glob.glob(path, recursive = True):
				reponame = folder.split('/')[-2]
				os.system(f"semgrep -f {Config.semgrep_loglevel} {folder} --json -o {Config.log_level}{reponame}.json")

	#final json for scraping only the log based information
	def finallogeveljson():
		path = f"{Config.log_level}*.json"
		pattern_data = {}
		for filename_ in glob.glob(path, recursive=True):
			filename = filename_.split('/')[-1]
			data = FileOperations.json.read_json(filename_)
			filename = filename.split('.')[0]
			pattern_data[filename] = {}
			info_log = {}
			for i in range(len(data['results'])):
				f_name_list = data['results'][i]['path']
				f_name = f_name_list.split('/')[-1]
				pattern_data[filename].setdefault(f_name, {})
				log_type = data['results'][i]['check_id']
				pattern_data[filename][f_name].setdefault('end_line_', {'line': 0})
				pattern_data[filename][f_name].setdefault('logs', "")
				t_line = ""
				if log_type in ['info', 'error', 'warning', 'debug', 'trace']: 
					t_line = data['results'][i]['extra']['lines']
					pattern_data[filename][f_name]["logs"] += t_line + ','
				if log_type == 'end_line_':
					pattern_data[filename][f_name][log_type]['line'] = data['results'][i]['end']['line'] - 1
				else:
					pattern_data[filename][f_name].setdefault(log_type, {'lines': [], 'count': 0})
					pattern_data[filename][f_name][log_type]['count'] += 1
					#To remove the redundancy of count in info when it matches with other log
					info_log.setdefault(f_name, [])
					if log_type == 'info':
						info_log[f_name].append([data['results'][i]['extra']['lines'], data['results'][i]['start']['col']])
					#to elimate the matching confusion for a statement with two logs
					elif [data['results'][i]['extra']['lines'], data['results'][i]['start']['col']] in info_log[f_name]:
						pattern_data[filename][f_name]['info']['count'] -= 1
					start, end = data['results'][i]['start']['line'], data['results'][i]['end']['line']
					pattern_data[filename][f_name][log_type]['lines'].append([start, end])
		FileOperations.json.save_json(pattern_data, f"{Config.log_level}pattern_output.json")
