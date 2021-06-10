import pandas as pd
from file_operations import FileOperations
from config import Config
import os
import glob

#To find the instances of each log in a repository
class LogInstances:

	#To create a json for easy repo data fetching
	def excel2json(repo_file):
		excel = pd.ExcelFile(repo_file)
		repo2json = {}
		for sheet in excel.sheet_names:
			data = pd.read_excel(excel, sheet_name = sheet)
			for link in data['Repo_Link']:
				repo_name = link.split('/')[-1]
				repo2json[repo_name] = {}
				repo2json[repo_name]['Type'] = sheet
				repo2json[repo_name]['Repo Link'] = link
		FileOperations.json.save_json(repo2json, f"{Config.log_instances}/input/excel2repo.json")

	#Applying semgrep rule on all the repos for specific log statement count
	def json2semgrep(jsonfile):
		json_data = FileOperations.json.read_json(jsonfile)
		semgrep_rule = Config.semgrep_logcount
		for repo_name, type_link in json_data.items():
			try:
				os.chdir(f"{Config.research}{type_link['Type']}/")
			except:
				os.mkdir(f"{Config.research}{type_link['Type']}/")
				os.chdir(f"{Config.research}{type_link['Type']}/")
			os.system(f"git clone {type_link['Repo Link']}")
			os.system(f"semgrep -f {semgrep_rule} {repo_name} --json -o {Config.log_instances}{repo_name}.json")

	#For creating a file logcount json
	def semgrep2json():
		os.chdir(f'{Config.log_instances}')
		path = '*.json'
		repo_log_count = {}
		for reponame in glob.glob(path, recursive = True):
			repo_log_count[reponame.split('.')[0]] = {'print' : 0, 'logging' : 0, 'log4j' : 0, 'tinylog' : 0,  'slf4j' : 0}
			file_logcount = FileOperations.json.read_json(reponame)
			for file_in_repo in file_logcount['results']:
				#for stoping the redundancy of sys.stderr in io and stdrr, """ is to avoid conflict when formatting is used
				'''if file_in_repo['check_id'] == 'stderr':
					repo_log_count[reponame.split('.')[0]]['io-file.write'] -= 1'''
				repo_log_count[reponame.split('.')[0]][file_in_repo['check_id']] += 1
		FileOperations.json.save_json(repo_log_count, f"{Config.log_instances}log_count.json")
