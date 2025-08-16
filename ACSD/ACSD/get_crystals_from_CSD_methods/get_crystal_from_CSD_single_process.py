"""
get_crystal_from_CSD_single_process.py. Geoffrey Weal, 16/4/24

This method will obtain a crystal associated with the given identifier from the Cambridge Structral Database.
"""
import os
from ase.io                                                    import write
from SUMELF                                                    import is_solvent, get_symmetry_operations
from ACSD.ACSD.create_ASE_molecule_and_graph_from_CSD_molecule import create_ASE_molecule_and_graph_from_CSD_molecule
from SUMELF                                                    import make_crystal, add_hydrogens_to_molecules, remove_node_properties_from_graph, add_graph_to_ASE_Atoms_object
from ACSD.ACSD.check_crystal_quality                           import check_crystal_quality, save_flags_to_disk

def get_crystal_from_CSD_single_process(input_data):
	"""
	This method will obtain a crystal associated with the given identifier from the Cambridge Structral Database.

	Parameters
	----------
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
	"""

	# First, extract the input variables from input_data.
	identifier, overwrite_existing_crystal_files, no_of_crystals_recorded, no_of_excluded_crystals, no_of_already_processed_crystals, save_crystals_to, crystals_not_written_lock, could_not_find_identifiers_lock, no_coordinates_given_lock, rejected_crystals_lock, crystal_quality_information_lock, logger, logger_lock, is_parallel = input_data

	# Second, if identifier startswith #, make a note and remove the #.
	move_on_tag = identifier.startswith('#')
	if move_on_tag:
		no_of_excluded_crystals.value += 1
		no_of_crystals_recorded.value += 1
		return False

	# Fourth, if you have chosen not to override the files in save_crystals_to, and you can find identifier.xyz in save_crystals_to, move on
	if (not overwrite_existing_crystal_files) and (identifier+'.xyz' in os.listdir(save_crystals_to)):
		no_of_already_processed_crystals.value += 1
		no_of_crystals_recorded.value          += 1
		return False

	# Fifth, give the names of the files to write information to.
	crystals_not_written_TXT_file       = save_crystals_to+'/'+'crystals_not_written.txt'
	could_not_find_identifiers_TXT_file = save_crystals_to+'/'+'could_not_find_identifiers.txt'
	no_coordinates_given_TXT_file       = save_crystals_to+'/'+'no_coordinates_given.txt'
	rejected_crystals_TXT_file          = save_crystals_to+'/'+'rejected_crystals.txt'

	# Sixth, record the strings to print to files and the end of this process.
	logger_string = ''

	# Seventh, make a note in the logger for this crystal.
	logger_string += "==========================================================\n"
	description = 'Processing: '+str(identifier)
	logger_string += str(description)
	if (logger is not None):
		logger.info(logger_string)

	# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

	# Eighth, get the crystal file.
	if identifier.isdigit():

		# 8.1: If the identifier is a digit, find the crystal in the CCDC database
		raise Exception('Check this segment is working')

		# 8.1.1: Import the numerical search setting
		from ccdc.search import TextNumericSearch

		# 8.1.2: Find identifier in the CCDC database
		searcher = TextNumericSearch()
		searcher.add_ccdc_number(int(identifier))
		hits = searcher.search()

		# 8.1.3: Made sure that there is at least 1 hit from identifier. 
		#        * If there is more than 2 hits, take the first hit but give the user a warning. 
		if len(hits) == 0:
			append_to_file(could_not_find_identifiers_TXT_file, str(identifier), could_not_find_identifiers_lock)
			to_string = 'Error: Could not find an entry in the CCDC database for: '+str(identifier)
			write_to_logger(to_string, logger, is_parallel, logger_lock, write=True)
			append_to_file(crystals_not_written_TXT_file, str(identifier)+': '+str(to_string), crystals_not_written_lock)
			return False
		elif len(hits) >= 2:
			warnings_string = 'Warning: found '+str(len(hits))+' hits for '+str(identifier)
			warnings.warn(warnings_string)
			write_to_logger(warnings_string, logger, is_parallel, logger_lock, write=True)
		
		# 8.1.4: Obtain the CCDC object for this crystal
		entry_object = hits[0].entry

		# 8.1.5: Convert the CCDC id into its identifier name.
		identifier   = entry_object.identifier

	else:

		# 8.2: Obtain the crystal from the CCDC database based on its identifier. 

		# 8.2.1: Import the entry reader class
		from ccdc.io import EntryReader

		# 8.2.2: Import the CCDC database
		csd_reader = EntryReader('CSD')

		# 8.2.3: Obtain the entryobject for the identifier of interest from the database.
		try:
			entry_object = csd_reader.entry(identifier)
		except Exception as exception:
			# 8.2.4: There is a problem, so return a message indicating this and move on.
			append_to_file(could_not_find_identifiers_TXT_file, str(identifier), could_not_find_identifiers_lock)
			to_string = 'Error: Could not extract '+str(identifier)+' from CCDC Database --> Error Message: '+str(exception)
			write_to_logger(to_string, logger, is_parallel, logger_lock, write=True)
			append_to_file(crystals_not_written_TXT_file, str(identifier)+': '+str(to_string), crystals_not_written_lock)
			return False

	# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

	# Ninth, get the good version of the crystal without disorder issues.
	crystal_object = entry_object.crystal
	CSD_molecules = crystal_object.molecule

	# Tenth, if the crystal does not contain any coordinates, do not record it.
	if len(CSD_molecules.atoms) == 0:
		append_to_file(no_coordinates_given_TXT_file, str(identifier), no_coordinates_given_lock)
		to_string = 'Error: '+str(identifier)+' Contains no coordinates.'
		write_to_logger(to_string, logger, is_parallel, logger_lock, write=True)
		append_to_file(crystals_not_written_TXT_file, to_string, crystals_not_written_lock)
		return False

	# Seventh, if the CSD_molecules is a polymer, move on as we do not want these crystals.
	if CSD_molecules.is_polymeric or CSD_molecules.is_organometallic or any(a.is_metal for a in CSD_molecules.atoms) or (not CSD_molecules.is_organic):
		append_to_file(rejected_crystals_TXT_file, str(identifier), rejected_crystals_lock)
		to_string = 'Error: '+str(identifier)+' is either polymeric, organometallic (or otherwise contains a metal), or else is not purely organic.'
		write_to_logger(to_string, logger, is_parallel, logger_lock, write=True)
		append_to_file(crystals_not_written_TXT_file, to_string, crystals_not_written_lock)
		return False

	# ---------------------------------------------------------------
	# Eighth, obtain the molecules and graph information from the CCDC/CSD molecules object.
	#         * Note that the CSD_molecules object contains all the molecules in the crystal, contained in CSD_molecules.components 
	molecules, molecule_graphs, hydrogens_with_no_coordinates_in_mols = create_ASE_molecule_and_graph_from_CSD_molecule(CSD_molecules, logger)

	# ---------------------------------------------------------------
	# Ninth, Identify solvents. Refer to:
	#        * https://pubs.rsc.org/en/content/articlelanding/2020/ce/d0ce00299b#cit7
	#        * https://pubs.acs.org/doi/10.1021/acs.chemmater.7b00441

	'''
	# 9.1: Ensure labels are unique
	CSD_molecules.normalise_labels()

	# 9.2: Use a copy
	clone = CSD_molecules.copy()

	# 9.3: Remove all bonds containing a metal atom
	clone.remove_bonds(b for b in clone.bonds if any(a.is_metal for a in b.atoms))

	# 9.4: Work out which components to are solvents. If a solvent component is empty for some reason, remove it from the crystal.
	solvent_components = [index for index in range(len(clone.components)) if is_solvent(clone.components[index])]

	# 9.5: Figure out if all that is left is solvent molecules
	if len(CSD_molecules.components) == len(solvent_components):
		to_string = 'Error: After removing solvents from '+str(identifier)+' there was no more molecules in the crystal.'
		write_to_logger(to_string, logger, is_parallel, logger_lock, write=False)
		return False
	'''

	# 9.1: Obtain the names of the solvents in the crystal. 
	solvent_components = [name for name in molecule_graphs.keys() if is_solvent(molecule_graphs[name])]

	# ---------------------------------------------------------------

	# Tenth, obtain the cellpar from the crystal
	cell_lengths = crystal_object.cell_lengths[:]
	cell_angles  = crystal_object.cell_angles[:]
	cellpar = cell_lengths + cell_angles

	# Eleventh, obtain the symmetry_operators for the crystal.
	symmetry_operations = get_symmetry_operations(crystal_object.symmetry_operators)

	# Twelfth, create the ase crystal file.
	crystal, crystal_graph = make_crystal(molecules, symmetry_operations=symmetry_operations, cell=cellpar, wrap=False, solvent_components=solvent_components, remove_solvent=False, molecule_graphs=molecule_graphs)

	# Thirteenth, attempt to add missing hydrogens to molecules in crystal using CCDC algorithms
	if len(hydrogens_with_no_coordinates_in_mols) > 0:
		add_no_coord_hydrogens_message = description + ' - Adding non-coordinated hydrogens to crystal structure'
		#pbar.set_description(add_no_coord_hydrogens_message)
		molecules, molecule_graphs, were_hydrogens_added = add_hydrogens_to_molecules(hydrogens_with_no_coordinates_in_mols, molecules, molecule_graphs, crystal, crystal_graph, symmetry_operations=symmetry_operations, cell=cellpar, logger=logger, identifier=identifier)
		#pbar.set_description(description)
	else:
		were_hydrogens_added = False

	# Fourteenth, create the crystals object again with added hydrogens if these were added by the "add_hydrogens_to_molecules" method previously.
	#            * If no hydrogen were added to the crystal, the original crystal_graph will contain the 'no_of_neighbouring_non_cord_H' property which 
	#              should be removed. 
	if were_hydrogens_added:
		to_string = 'Missing hydrogens being added to crystal file for '+str(identifier)
		write_to_logger(to_string, logger, is_parallel, logger_lock, write=False)
		crystal, crystal_graph = make_crystal(molecules, symmetry_operations=symmetry_operations, cell=cellpar, wrap=False, solvent_components=solvent_components, remove_solvent=False, molecule_graphs=molecule_graphs)

	# Fifteenth, figure out if any crystals should be check or rejected cause they are a bit funny.
	flags = check_crystal_quality(crystal, molecules, molecule_graphs, entry_object)
	save_flags_to_disk(identifier, flags, save_crystals_to, crystal_quality_information_lock) # Save this information to disk

	# Sixteenth, add the node and edge properties of the crystal from the crystal_graph into the crystal ASE object itself. 
	add_graph_to_ASE_Atoms_object(crystal, crystal_graph)

	# Seventeenth, save the xyz file for the crystal
	crystal_filepath = save_crystals_to+'/'+identifier
	write(crystal_filepath+'.xyz', crystal)

	# Eighteenth, write the output from logger to the global logger.
	write_to_logger(None, logger, is_parallel, logger_lock, write=True)

	# Nineteenth. increment no_of_crystals_recorded as we have recorded a crystal
	no_of_crystals_recorded.value += 1

	# Twenty, we have recorded the crystal, so return True
	return True

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

def append_to_file(path_to_file, line, lock):
	"""
	This method is designed to allow the user to append a line to a file.

	Parameters
	----------
	path_to_file : str.
		This is the path to the file to add the line to
	line : str.
		This is the line to add to the file
	lock : filelock.lock
		This is the lock to prevent other processes from printing data to this file. 
	"""
	with lock:
		with open(path_to_file, 'a+') as FILE:
			FILE.write(str(line).rstrip()+'\n')

def write_to_logger(message_to_write, logger, is_parallel, logger_lock, write=False):
	"""
	This method will write information to the logger. 

	Parameters
	----------
	message_to_write : str. or None
		This is the message you want to write to the logger
	logger : logger
		This is the logger file.
	is_parallel : bool.
		This indicates if ACSD is running in parallel or not. 
	logger_lock : lock
		THis is the lock object for the logger
	write : bool.
		This indicates if you want to write the information to the logger file if in parallel. 
	"""

	# First, is there is no logger, do not perform this step.
	if (logger is None):
		return

	# Second, write the information to the logger (if there if a message to write).
	if message_to_write is not None:
		logger.info(message_to_write)

	# Third, if ACSD is in parallel and you want to write the data to the logger file, do this.
	if write and is_parallel:

		# 3.1: Run the lock so that the logger is only being written to by one process at a time.
		with logger_lock:

			# 3.2: Perform the writing task.
			logger.write()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

