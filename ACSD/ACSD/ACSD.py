"""
ACSD.py, Geoffrey Weal, 20/5/2022

This program, the Access Cambridge Structural Database program, will look through the Cambridge Structural Database for crystals that contain segments/fragments of molecules you are wanting to look through the database for.

"""
import os, sys
import warnings
warnings.filterwarnings('ignore')
from ACSD.ACSD.get_crystals_from_CSD import get_crystals_from_CSD
from ACSD.ACSD.get_isotope_data      import get_isotope_data
from ACSD.ACSD.utilities             import get_paths_to_identifiers, get_list_of_identifiers, get_list_of_crystals_to_exclude, get_identifiers_from_txt_file
isotopes = get_isotope_data()

class CLICommand:
	"""Collect crystal structures from the Cambridge Structural Database.
	"""

	@staticmethod
	def add_arguments(parser):
		parser.add_argument('paths_to_identifiers',  nargs='+', help='Add all the paths to the identifier list you want to examine, or just the name of the folder that contains all the gcd files you want to process.')
		parser.add_argument('--overwrite',           nargs=1,   help='Indicates if you want to overwrite crystal files that have already been included in the crystal database folder.', default=['True'])
		parser.add_argument('--crystals_to_exclude', nargs=1,   help='Exclude the crystal if given in these files.', default=[None])
		parser.add_argument('--no_cpus',             nargs=1,   help='This is the number of cpus to use to process the ACSD.', default=['1'])

	@staticmethod
	def run(arguments):

		# First, obtain the path to the file that contains all the idenitifiers, or the folder to all the gcd files that you want to read in.
		paths_to_identifiers = arguments.paths_to_identifiers
		
		# Second, give an error if no input was given
		if (paths_to_identifiers is None) or (len(paths_to_identifiers) == 0):
			raise Exception('Error: Paths to Identifiers must be given as arguments to this program')

		# Fourth, determine if you want to overwrite existing crystal files in the crystal database folder.
		overwrite_existing_crystal_files = arguments.overwrite
		if len(overwrite_existing_crystal_files) != 1:
			raise Exception('Error: overwrite has more than one input')
		overwrite_existing_crystal_files = overwrite_existing_crystal_files[0]
		if   overwrite_existing_crystal_files.lower() in ['t', 'true']:
			overwrite_existing_crystal_files = True
		elif overwrite_existing_crystal_files.lower() in ['f', 'false']:
			overwrite_existing_crystal_files = False
		else:
			to_string  = 'Error: your "overwrite" input must be either True or False.\n'
			to_string += f'Your "overwrite" input: {overwrite_existing_crystal_files}\n'
			to_string += 'Check this.'
			raise Exception(to_string)

		# Third, indicate the file you want to read in to indicate which idenitifiers you dont want to include. This is usually used for debugging
		crystals_to_exclude_filename = arguments.crystals_to_exclude
		if len(crystals_to_exclude_filename) != 1:
			raise Exception('Error: crystals_to_exclude has more than one input')
		crystals_to_exclude_filename = crystals_to_exclude_filename[0]

		# Fifth, determine the number of cpus to use for processing the crystals in the ACSD.
		no_cpus = arguments.no_cpus
		if len(no_cpus) != 1:
			raise Exception('Error: overwrite has more than one input')
		no_cpus = no_cpus[0]
		if not no_cpus.isdigit():
			raise Exception('Error: no_cpus is not a digit. no_cpus = '+str(no_cpus))
		no_cpus = int(no_cpus)

		# Fifth, run the ACSD program
		run_ACSD(paths_to_identifiers, overwrite_existing_crystal_files=overwrite_existing_crystal_files, crystals_to_exclude_filename=crystals_to_exclude_filename, no_cpus=no_cpus) 

# ------------------------------------------------------------------------------------------------------------

def run_ACSD(paths_to_identifiers, overwrite_existing_crystal_files=True, crystals_to_exclude_filename=None, no_cpus=1):
	"""
	This method will look through the Cambridge Structural Database for the crystal files you would like to obtain.

	Parameters
	----------
	paths_to_identifiers : list of strings
		These are the paths to the lists of identifiers to process.
	overwrite_existing_crystal_files : bool.
		This boolean indicate if you want to overwrite already existing crystal files in the crystal database folder. Default: True.
	crystals_to_exclude_filename : str. or None
		The is the path to the file that contain CCDC identifiers you do not want to include in this run. If None, don't exclude any CCDC IDs. Default: None
	no_cpus : int
		This is the number of cpus you would like to use to process the ACSD. 
	"""

	# First, get the list of identifers from the arguments
	no_of_lines = 40
	print('#'*no_of_lines)
	print('Getting Segments from arguments')
	print('-'*no_of_lines)
	print('Obtaining crystals from the CSD for identifiers in: '+str(paths_to_identifiers))

	# Second, get the name of the folder to save crystal files to
	crystals_database_folder_name = 'crystal_database'

	# Third, if the input for paths_to_identifiers given is a path to a folder that contains all the gcd files to read from, obtain the paths to all the gcd files in this folder.
	paths_to_identifiers = get_paths_to_identifiers(paths_to_identifiers)

	# Fourth, get the identifiers from the gcd files that contain the identifiers to obtain.
	identifiers = get_list_of_identifiers(paths_to_identifiers)

	# Fifth, obtain a list of the identifiers to exclude if they are in identifiers
	identifiers_to_exclude = get_list_of_crystals_to_exclude(crystals_to_exclude_filename)

	# Fifth, add identifers to exclude from the crystals_not_written.txt file. 
	#        * The ACSD did try to create these crystal files, but did not for some reason.
	path_to_crystals_not_written_TXT_file = crystals_database_folder_name+'/'+'crystals_not_written.txt'
	if os.path.exists(path_to_crystals_not_written_TXT_file):
		identifiers_to_exclude += get_list_of_crystals_to_exclude(path_to_crystals_not_written_TXT_file)

	# Fifth, remove excluded crystal from the crystals_to_exclude from all_identifiers
	#        * Removed idenifiers are replaced with None.
	identifiers = sorted(set(identifiers))
	identifiers_to_exclude = sorted(set(identifiers_to_exclude))
	for index in range(len(identifiers)):
		identifier = identifiers[index]
		if identifier in identifiers_to_exclude:
			identifiers[index] = '#'+identifiers[index]
			identifiers_to_exclude.remove(identifier)

	# Sixth, get the crystals for the identifers from the CSD database.
	print('Saving Data to: '+str(crystals_database_folder_name))
	no_of_crystals_recorded, no_of_excluded_crystals, no_of_already_processed_crystals = get_crystals_from_CSD(identifiers, crystals_database_folder_name, overwrite_existing_crystal_files, no_cpus)

	# Seventh, obtain the list of crystals that do not contain any coordinates
	no_coordinates_given_filepath = crystals_database_folder_name+'/'+'no_coordinates_given.txt'
	if os.path.exists(no_coordinates_given_filepath):
		list_of_crystals_with_no_coordinates_given = get_identifiers_from_txt_file(no_coordinates_given_filepath)
	else:
		list_of_crystals_with_no_coordinates_given = []

	# Eighth, obtain the list of crystals that were rejected for some reason (for example, contained a metal, was not organic, was a polymer, etc).
	rejected_crystals_filepath = crystals_database_folder_name+'/'+'rejected_crystals.txt'
	if os.path.exists(rejected_crystals_filepath):
		list_of_rejected_crystals = get_identifiers_from_txt_file(rejected_crystals_filepath)
	else:
		list_of_rejected_crystals = []

	# Ninth, obtain the list of identifiers that could not be found in the CCDC database. 
	could_not_find_identifiers_filepath = crystals_database_folder_name+'/'+'could_not_find_identifiers.txt'
	if os.path.exists(could_not_find_identifiers_filepath):
		list_of_identifiers_that_could_not_be_found = get_identifiers_from_txt_file(could_not_find_identifiers_filepath)
	else:
		list_of_identifiers_that_could_not_be_found = []

	# Tenth, print results from reading and recording crystals from the CSD database.
	print('Obtained crystals from the CSD for identifiers in: '+str(crystals_database_folder_name))
	print('Number of crystals obtained from the database: '+str(no_of_crystals_recorded))
	print('  -> Number of crystals already recorded in previous ACSD runs: '+str(no_of_already_processed_crystals))
	print('  -> Number of crystals excluded from the ACSD run for some reason (for example, contained a metal, was not organic, was a polymer, etc): '+str(no_of_excluded_crystals))
	print('-'*no_of_lines)
	print('Number of crystals with no coordinates given: '+str(len(list_of_crystals_with_no_coordinates_given)))
	print('Number of crystals rejected: '+str(len(list_of_rejected_crystals)))
	print('-'*no_of_lines)
	if len(list_of_identifiers_that_could_not_be_found) > 0:
		print('No of crystals not found in the database: '+str(len(list_of_identifiers_that_could_not_be_found)))
		print()
		print('These are:')
		print()
		for identifier in list_of_identifiers_that_could_not_be_found:
			print(identifier)
		print()
		print('-'*no_of_lines)
	print('-'*no_of_lines)

# ------------------------------------------------------------------------------------------------------------


