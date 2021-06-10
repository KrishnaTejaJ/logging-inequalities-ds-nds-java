from log_instances import LogInstances
from logvnlog import LogVsNlog
from log_level import LogLevel
from config import Config

#All the logging methods
class Logging_:

	def log_instances_():
		LogInstances.excel2json(Config.repo_file)
		LogInstances.json2semgrep(Config.excel2repo)
		LogInstances.semgrep2json()

	def logvnonlog_():
		LogVsNlog.gitchanges()
		total_lines = LogVsNlog.changesjson()

	def log_level_():
		LogLevel.semgrep2json()
		LogLevel.finallogeveljson()
