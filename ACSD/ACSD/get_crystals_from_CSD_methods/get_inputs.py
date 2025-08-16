"""
get_inputs.py. Geoffrey Weal, 16/4/24

This generator is designed to return all the input methods required for the get_crystal_from_CSD_single_process method.  
"""

def get_inputs(identifiers, overwrite_existing_crystal_files, no_of_crystals_recorded, no_of_excluded_crystals, no_of_already_processed_crystals, save_crystals_to, crystals_not_written_lock, could_not_find_identifiers_lock, no_coordinates_given_lock, rejected_crystals_lock, crystal_quality_information_lock, logger, logger_lock, is_parallel):
	"""
	This generator is designed to return all the input methods required for the get_crystal_from_CSD_single_process method. 

	Parameters
	----------
	identifiers : list
		This is the list of identifiers you want to obtain the crystals for from the CCDC. 

	overwrite_existing_crystal_files : bool.
		This boolean indicates if you want to overwrite already given crystals. If so, set this to True.

	no_of_crystals_recorded : int object
		This is a record of the number of crystals that have been reported.
	no_of_excluded_crystals : int object
		This is a record of the number of crystals that were excluded from being recorded. 
	no_of_already_processed_crystals : int object
		This is a record of the number of crystals that were skipped because they have already been recorded. 

	save_crystals_to : str.
		This is the path to the folder to save crystals to. 

	crystals_not_written_lock : multiprocessing.Manager.lock
		This is the lock for the file at crystals_not_written_TXT_file.

	could_not_find_identifiers_lock : multiprocessing.Manager.lock
		This is the lock for the file at could_not_find_identifiers_TXT_file.
	no_coordinates_given_lock : multiprocessing.Manager.lock
		This is the lock for the file at no_coordinates_given_TXT_file.
	rejected_crystals_lock : multiprocessing.Manager.lock
		This is the lock for the file at rejected_crystals_TXT_file.

	crystal_quality_information_lock : multiprocessing.Manager.lock
		This is the lock for recording crystal quality information.

	logger : logging
		This is the log for recording warning issues. 
	logger_lock : FileLock.FileLock
		This is the lock for recording logger information. 

	Returns
	-------
	identifier : str.
		This is the identifier you want to obtain the crystal of from the CCDC. 

	overwrite_existing_crystal_files : bool.
		This boolean indicates if you want to overwrite already given crystals. If so, set this to True.

	no_of_crystals_recorded : int object
		This is a record of the number of crystals that have been reported.
	no_of_excluded_crystals : int object
		This is a record of the number of crystals that were excluded from being recorded. 
	no_of_already_processed_crystals : int object
		This is a record of the number of crystals that were skipped because they have already been recorded. 

	save_crystals_to : str.
		This is the path to the folder to save crystals to. 

	crystals_not_written_lock : multiprocessing.Manager.lock
		This is the lock for the file at crystals_not_written_TXT_file.

	could_not_find_identifiers_lock : multiprocessing.Manager.lock
		This is the lock for the file at could_not_find_identifiers_TXT_file.
	no_coordinates_given_lock : multiprocessing.Manager.lock
		This is the lock for the file at no_coordinates_given_TXT_file.
	rejected_crystals_lock : multiprocessing.Manager.lock
		This is the lock for the file at rejected_crystals_TXT_file.

	crystal_quality_information_lock : multiprocessing.Manager.lock
		This is the lock for recording crystal quality information.

	logger : logging
		This is the log for recording warning issues. 
	logger_lock : FileLock.FileLock
		This is the lock for recording logger information. 

	is_parallel : bool.
		This indicates if you are running your process in parallel or not. 
	"""

	# First, for each identifier in identifiers
	for identifier in identifiers:

		# Second, yield the input variables
		yield identifier, overwrite_existing_crystal_files, no_of_crystals_recorded, no_of_excluded_crystals, no_of_already_processed_crystals, save_crystals_to, crystals_not_written_lock, could_not_find_identifiers_lock, no_coordinates_given_lock, rejected_crystals_lock, crystal_quality_information_lock, logger, logger_lock, is_parallel

