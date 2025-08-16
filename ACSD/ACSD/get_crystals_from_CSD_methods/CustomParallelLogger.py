"""
CustomParallelLogger.py, Geoffrey Weal, 27/4/24

This is designed to write the log file for parallel processes.
"""
import os
from datetime import datetime

class CustomParallelLogger:
	"""
	This is designed to at as an in memory logger for multiprocessing proposes. 

	This have been created to allow ACSD to provide all its logging information for a crystal together. 
	"""
	def __init__(self, filename="ACSD_logfile.log", filemode='w', instant_write=False):
		self.filename         = filename
		self.filemode         = filemode
		self.instant_write    = instant_write
		self.temp_information = []
		if (filemode == 'w') and os.path.exists(filename):
			os.remove(filename)

	def info(self, message):
		"""
		This method will add information to the log, in this case to the temp_information list.

		Parameters
		----------
		message : str.
			This is the message you would like to add onto the temp_information stack.
		"""

		# First, obtain the current date and time.
		now = datetime.now()

		# Second, separate the message into its components, and append each line to the temp_information stack.
		for segment in message.split('\n'):
			self.temp_information.append(str(now)+' - '+str(segment))

		# Third, write the stack to file if desired to do it instantly.
		if self.instant_write:
			self.write()

	def warning(self, message):
		"""
		
		"""
		self.info('WARNING: '+str(message))

	def write(self):
		"""
		Write all the log information from the temp_information to the actual log file.
		"""

		# First, if there is nothing in the stack, end recording here
		if self.temp_information == []:
			return
		
		# Second, write all the data from temp_information to the log file on disk
		with open(self.filename, 'a') as LOGFILE:
			for segment in self.temp_information:
				LOGFILE.write(segment+'\n')

		# Third, reset the temp_information list.
		self.temp_information = []
