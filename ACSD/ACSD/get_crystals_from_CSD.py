"""
get_crystals_from_CSD.py, 16/4/24

This method will obtain the crystals associated with the given identifiers from the Cambridge Structral Database.
"""
import os, sys
from tqdm     import tqdm
from shutil   import rmtree
from filelock import FileLock

import multiprocessing as mp
from tqdm.contrib.concurrent import process_map

from ACSD.ACSD.get_crystals_from_CSD_methods.get_inputs                          import get_inputs
from ACSD.ACSD.get_crystals_from_CSD_methods.get_crystal_from_CSD_single_process import get_crystal_from_CSD_single_process
from ACSD.ACSD.get_crystals_from_CSD_methods.Integer                             import Integer
from ACSD.ACSD.get_crystals_from_CSD_methods.CustomParallelLogger                import CustomParallelLogger

def get_crystals_from_CSD(identifiers, save_crystals_to, overwrite_existing_crystal_files=True, no_of_cpus=1):
	"""
	This method will obtain the crystals associated with the given identifiers from the Cambridge Structral Database.
	
	Parameters
	----------
	identifiers : list of str.
		This is a list of the identifiers to obtain crystal files for. 
	save_crystals_to : str.
		This is the folder to save crystal files to.
	overwrite_existing_crystal_files : bool.
		This boolean indicate if you want to overwrite already existing crystal files in the crystal database folder. Default: True.
	no_cpus : int
		This is the number of cpus you would like to use to process the ACSD. 
		
	Return
	------
	no_of_crystals_recorded : int
		This is the number of crystals that have been written to disk
	flags : dit.
		This dictionary contains all the information about flags to consider if a user is using this data.
	"""

	# First, make a folder that contains the crystals that were found that contain segments from the segments list.
	if overwrite_existing_crystal_files:
		if os.path.exists(save_crystals_to):
			rmtree(save_crystals_to)
		os.makedirs(save_crystals_to)
	else:
		if not os.path.exists(save_crystals_to):
			os.makedirs(save_crystals_to)

	# Second, get the path to the crystals_not_written.txt to write identifiers to that the ACSD program attempted to 
	#         write the crystal file for, but did not for some reason
	path_to_crystals_not_written_TXT_file = save_crystals_to+'/'+'crystals_not_written.txt'

	# Third, create the logger for recording messages about about programs run to the logfile.
	'''
	import logging
	Log_Format = "%(levelname)s %(asctime)s - %(message)s"
	filemode = 'w' if overwrite_existing_crystal_files else 'a'
	logging.basicConfig(filename="ACSD_logfile.log",filemode=filemode,format=Log_Format,level=logging.NOTSET)
	logger = logging.getLogger()
	logger.info("==========================================================")
	logger.info('Running ACSD Program'.upper())
	'''
	filemode = 'w' if overwrite_existing_crystal_files else 'a'
	instant_write = True if (no_of_cpus == 1) else False
	logger = CustomParallelLogger(filename="ACSD_logfile.log", filemode=filemode, instant_write=instant_write)
	logger.info("==========================================================")
	logger.info('Running ACSD Program'.upper())
	logger.write()

	# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
	# Fourth, obtain the crystals of interest from the CCDC. 

	if no_of_cpus == 1: # If the user only wants to use 1 cpu, perform tasks without using multiprocessing

		# 4.1.1: Make a record of the number of crystals that have been recorded.
		no_of_crystals_recorded = Integer(0)

		# 4.1.2: Make a record of the number of crystals that have been excluded from being processed.
		no_of_excluded_crystals = Integer(0)

		# 4.1.3: Make a record of the number of crystals that have been skipped as they have already been recorded. 
		no_of_already_processed_crystals = Integer(0)

		# 4.1.4: Set this lock to None, we dont need to use it for single cpu processes. 
		crystals_not_written_lock = Empty_With()

		# 4.1.5: Set this lock to None, we dont need to use it for single cpu processes. 
		could_not_find_identifiers_lock = Empty_With()

		# 4.1.6: Set this lock to None, we dont need to use it for single cpu processes. 
		no_coordinates_given_lock = Empty_With()

		# 4.1.7: Set this lock to None, we dont need to use it for single cpu processes. 
		rejected_crystals_lock = Empty_With()

		# 4.1.8: Set this lock to None, we dont need to use it for single cpu processes. 
		crystal_quality_information_lock = Empty_With()

		# 4.1.9: Set this lock to None, we dont need to use it for single cpu processes. 
		logger_lock = Empty_With()

		# 4.1.10: Get the input generator.
		inputs = get_inputs(identifiers, overwrite_existing_crystal_files, no_of_crystals_recorded, no_of_excluded_crystals, no_of_already_processed_crystals, save_crystals_to, crystals_not_written_lock, could_not_find_identifiers_lock, no_coordinates_given_lock, rejected_crystals_lock, crystal_quality_information_lock, logger, logger_lock, False)

		# 4.1.11: Create a progress bar for running this task.
		with tqdm(inputs, total=len(identifiers), unit='identifier', desc='Obtaining Crystals from CCDC') as pbar:

			# 4.1.11.1: For each comparison of molecules.
			for input_data in pbar:

				# 4.1.11.2: Get the identifier from input_data.
				identifier = input_data[0]

				# 4.1.11.3: If identifier startswith #, make a note and remove the #.
				move_on_tag = identifier.startswith('#')
				if move_on_tag:
					identifier = identifier[1:]

				# 4.1.11.4: Update the progress bar.
				description = 'Processing: '+str(identifier)
				pbar.set_description(description)

				# 4.1.11.5: If move_on_tag is true, move on
				if move_on_tag:
					no_of_excluded_crystals.value += 1
					no_of_crystals_recorded.value += 1
					continue

				# 4.1.11.6: If you have chosen not to override the files in save_crystals_to, and you can find identifier.xyz in save_crystals_to, move on
				if (not overwrite_existing_crystal_files) and (identifier+'.xyz' in os.listdir(save_crystals_to)):
					pbar.set_description(f'Found {identifier}.xyz. Continuing on to the next identifier.')
					no_of_already_processed_crystals += 1
					no_of_crystals_recorded.value    += 1
					continue

				# 4.1.11.7: Obtain the crystal from the CCDC database. 
				get_crystal_from_CSD_single_process(input_data)

		# 4.1.12: Convert "no_of_crystals_recorded" from a mp.Value object to a int variable.
		no_of_crystals_recorded = int(no_of_crystals_recorded.value)

		# 4.1.13: Convert "no_of_excluded_crystals" from a mp.Value object to a int variable.
		no_of_excluded_crystals = int(no_of_excluded_crystals.value)

		# 4.1.14: Convert "no_of_already_processed_crystals" from a mp.Value object to a int variable.
		no_of_already_processed_crystals = int(no_of_already_processed_crystals.value)

	else:

		# 4.2.1: Create the manager to save lists to.
		with mp.Manager() as manager:

			# 4.2.2: Make a record of the number of crystals that have been recorded.
			no_of_crystals_recorded = manager.Value('i', 0)

			# 4.2.3: Make a record of the number of crystals that have been excluded from being processed.
			no_of_excluded_crystals = Integer(0)

			# 4.2.4: Make a record of the number of crystals that have been skipped as they have already been recorded. 
			no_of_already_processed_crystals = manager.Value('i', 0)

			# 4.2.5: Create a lock for writing information to "crystals_not_written.txt"
			crystals_not_written_lock = manager.Lock()

			# 4.2.6: Create a lock for writing information to "could_not_find_identifiers.txt"
			could_not_find_identifiers_lock = manager.Lock()

			# 4.2.7: Create a lock for writing information to "no_coordinates_given.txt"
			no_coordinates_given_lock = manager.Lock()

			# 4.2.8: Create a lock for writing information to "rejected_crystals.txt"
			rejected_crystals_lock = manager.Lock()

			# 4.2.9: Create a lock for writing information to crystal_quality_information files
			crystal_quality_information_lock = manager.Lock()

			# 4.2.10: Create a lock for when the lower runs.
			logger_lock = manager.Lock()

			# 4.2.11: Get the input generator.
			inputs = get_inputs(identifiers, overwrite_existing_crystal_files, no_of_crystals_recorded, no_of_excluded_crystals, no_of_already_processed_crystals, save_crystals_to, crystals_not_written_lock, could_not_find_identifiers_lock, no_coordinates_given_lock, rejected_crystals_lock, crystal_quality_information_lock, logger, logger_lock, True)

			# 4.2.12: Obtain the crystal from the CCDC database.
			print(f'Obtaining Crystal xyz files from the CCDC using {no_of_cpus} cpus', file=sys.stderr)
			process_map(get_crystal_from_CSD_single_process, inputs, total=len(identifiers), unit='identifier', desc='Obtaining Crystals from CCDC', max_workers=no_of_cpus)
			# = mp.Pool(processes=no_of_cpus)
			#pool.map_async(get_crystal_from_CSD_single_process, tqdm(inputs, total=len(identifiers), unit='identifier', desc='Obtaining Crystals from CCDC'))
			#pool.close()
			#pool.join()

			# 4.2.13: Convert "no_of_crystals_recorded" from a mp.Value object to a int variable.
			no_of_crystals_recorded = int(no_of_crystals_recorded.value)

			# 4.2.14: Convert "no_of_excluded_crystals" from a mp.Value object to a int variable.
			no_of_excluded_crystals = int(no_of_excluded_crystals.value)

			# 4.2.15: Convert "no_of_already_processed_crystals" from a mp.Value object to a int variable.
			no_of_already_processed_crystals = int(no_of_already_processed_crystals.value)

	# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

	# Fifth, write the ending message to the log file
	logger.info("==========================================================")
	logger.info('Ended ACSD Program'.upper())
	logger.info("==========================================================")
	logger.write()

	# Sixth, return the number of crystals that were recorded
	return int(no_of_crystals_recorded), int(no_of_excluded_crystals), int(no_of_already_processed_crystals) #, flags

# ---------------------------------------------------------------------------------------------------------------------------------------------------------

class Empty_With():
    def __init__(self):
    	pass
    def __enter__(self):
        return self
    def __exit__(self, exception_type, exception_value, exception_traceback):
    	pass
