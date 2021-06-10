    from logging_ import Logging_
from folderoperations import FolderOperations
import os
from config import Config
import finalexport
import gini_index
import finalexport2

#Easing the process of required folder operations
FolderOperations.createFolder([Config.files, Config.datascience, Config.nondatascience, Config.log_instances, Config.log_instances_input, Config.log_level, Config.logvnlog])

#Counting the individual log statements in the repo
Logging_.log_instances_()

#To find number of Log based changes and Non Log based changes made to the repo in last 10 versions
Logging_.logvnonlog_()

#For extracting log level based information
Logging_.log_level_()

#For the final excel sheet with all the logging data
finalexport.finalcalc()
finalexport2.finalcalc()

#For extracting all the gini values of the repositories on method, class and file level for various logging types
gini_index.gini_input(Config.final)
