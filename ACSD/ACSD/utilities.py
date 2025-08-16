"""
utilities.py, Geoffrey Weal, 17/4/24

This scripts contains methods for using in the ACSD program. 
"""
import os

def get_paths_to_identifiers(paths_to_identifiers=None):
	"""
	This method will check all the identifiers files to make sure they are all exist. 

	Parameters
	----------
	paths_to_identifiers : list of str.
		These are the names of the files that contain identifier names. If None, read all .gcd files in the current folder. Default: None

	Return
	------
	full_paths_to_identifiers : list of str.
		These are the paths of all the files to obtain identifiers from. 
	"""

	if paths_to_identifiers is None:
		# First, if no identifiers filenames have been given, the program will find all .gcd files
		paths_to_identifiers = [file for file in os.listdir(os.getcwd()) if (os.path.isfile(os.getcwd()+'/'+file) and file.endswith('.gcd'))]

	elif len(paths_to_identifiers) == 1 and os.path.isdir(paths_to_identifiers[0]):
		folder_to_identifiers_filenames = paths_to_identifiers[0]
		paths_to_identifiers = [str(folder_to_identifiers_filenames+'/'+file) for file in os.listdir(folder_to_identifiers_filenames) if (os.path.isfile(folder_to_identifiers_filenames+'/'+file) and file.endswith('.gcd'))]

	return paths_to_identifiers

# ------------------------------------------------------------------------------------------------

def get_list_of_identifiers(identifiers_filenames=None):
	"""
	This method will extract all identifers from the file

	Parameters
	----------
	identifiers_filenames : list of str.
		These are the names of the files that contain identifier names. If None, read all .gcd files in the current folder. Default: None

	Return
	------
	identifiers : list
		This is a list of the identifiers to obtain crystal files for from the CSD.
	"""

	identifiers = []
	for identifiers_filename in identifiers_filenames:
		with open(identifiers_filename,'r') as identifiers_FILE:
			for line in identifiers_FILE:

				# First, if line starts with #, do not read the line
				if line.startswith('#'):
					continue

				# Second, get the identifier from the line
				identifier = line.rstrip()

				# Third, record the identifier if it has not already been recorded
				if identifier not in identifiers:
					identifiers.append(identifier)

	return sorted(set(identifiers))

# ------------------------------------------------------------------------------------------------

def get_list_of_crystals_to_exclude(crystals_to_exclude_filename=None):
	"""
	This method will extract all identifers from crystals_to_exclude_filename.

	Parameters
	----------
	crystals_to_exclude_filename : str. or None
		The is the path to the file that contain CCDC identifiers you do not want to include in this run. If None, don't exclude any CCDC IDs. Default: None

	Return
	------
	identifiers_to_exclude : list
		This is a list of the identifiers that we do not want to obtain crystal files for. 
	"""

	if crystals_to_exclude_filename is None:
		return []

	identifiers_to_exclude = []
	with open(crystals_to_exclude_filename,'r') as crystals_to_exclude_FILE:
		for line in crystals_to_exclude_FILE:

			# First, if line starts with #, do not read the line
			if line.startswith('#'):
				continue

			# Second, get the identifier from the line
			crystal_to_exclude = line.rstrip().split(':')[0]

			# Third, record the identifier if it has not already been recorded
			if crystal_to_exclude not in identifiers_to_exclude:
				identifiers_to_exclude.append(crystal_to_exclude)

	return sorted(set(identifiers_to_exclude))

# ------------------------------------------------------------------------------------------------

def get_identifiers_from_txt_file(filepath):
	"""
	This method is designed to extract the idenifiers from the txt file

	Parameters
	----------
	filepath : str.
		This is the path to the file to read identifiers from 

	Return
	------
	identifiers : list
		This is a list of the identifiers given in the file.
	"""

	# First, initialise a list to add identifiers from the file to.
	identifiers = []

	# Second, open the file.
	with open(filepath, 'r') as fileTXT:

		# Third, for each line in the file.
		for line in fileTXT:

			# Fourth, extract the name of the identifier from the file. 
			identifier = line.rstrip()

			# Fifth, add identifier to identifiers.
			identifiers.append(identifier)

	# Sixth, return identifiers
	return identifiers

# ------------------------------------------------------------------------------------------------
