import os

#This class is to ease the process of folder operations
class FolderOperations:
	def createFolder(folderlist):
		for folder in folderlist:
			os.mkdir(folder)
		

