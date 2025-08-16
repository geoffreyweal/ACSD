"""
check_crystal_quality.py, Geoffrey Weal, 10/6/22

This script is designed to hold methods for checking the quality of the crystal and writing this information to disk.
"""
import os, csv, re
from collections import Counter
from ACSD.ACSD.check_crystal_quality_methods.compare_molecules_to_SMILES import is_crystal_same_as_SMILES

def check_crystal_quality(crystal, molecules, molecule_graphs, entry_object):
	"""
	This method will perform several tasks that indicate if the crystal should be flagged for checking due to something weird about it.

	Parameters
	----------
	crystal : ase.Atoms
		This is the crystal object.
	molecules : list of ase.Atoms
		This is a list of the molecules in the crystal.
	molecule_graphs ; list of networkx.graphs
		This is a list of all the graphs associated with each molecule in the crystal.
	entry_object : ccdc.entry.Entry
		This is the ccdc entry object for this crystal.

	Returns
	-------
	has_disorder : bool.
		True if the crystal contains disorder in it. False if not
	crystal_different_to_user
		Is the chemical formula the same as indicated by the user, with and without hydrogens attahced.
	is_charge_zero
		True if the overall charge is 0, False if not
	is_mult_one
		True if the overall multiplicity is 1, False if not.
	crystal_same_as_SMILES
		True if the crystal has the same make-up as the SMILES code given by the user, False if not.
	"""

	# First, indicate if the crystal contains disorder
	has_disorder = entry_object.has_disorder

	# Second, indicate if the crystal element numbers may different to what the user indicates.
	entry_element_counter = get_chemical_formula(entry_object.formula)
	crystal_element_counter = Counter(crystal.get_chemical_symbols())
	crystal_different_to_user = [(not (crystal_element_counter == entry_element_counter))]
	if 'H' in crystal_element_counter:
		del crystal_element_counter['H']
	if 'H' in entry_element_counter:
		del entry_element_counter['H']
	crystal_different_to_user.append(not (crystal_element_counter == entry_element_counter))

	# Third, is the charge 0
	is_charge_zero = (crystal.get_initial_charges().sum() == 0.0)

	# Fourth, is the multiplicity 1.
	is_mult_one    = ((crystal.get_initial_magnetic_moments().sum() + 1) == 1.0)

	# Fifth, determine if the make-up of the crystal is the same as indicated by the user through the SMILES code. 
	crystal_same_as_SMILES = is_crystal_same_as_SMILES(molecules, molecule_graphs, entry_object)

	# Sixth, return results.
	return [has_disorder, crystal_different_to_user, is_charge_zero, is_mult_one, crystal_same_as_SMILES]

# ---------------------------------------------------------------------------------------------------------------------------

def get_chemical_formula(formula):
	"""
	This method will return a Counter of the chemical formula from the formula string.

	Parameters
	----------
	formula : str.
		This is the chemical formula for the crystal.

	Returns
	-------
	has_disorder : bool.
		True if the crystal contains disorder in it. False if not
	"""

	# First, get formula without commas and dots
	formula = formula.replace(',',' ')
	formula = formula.split()

	# Second, sort out if their are charges in the formula
	for index in range(len(formula)):
		if ('+' in formula[index]) or ('-' in formula[index]):
			tostring = formula[index]
			new_tostring = ''
			for character in tostring:
				if not (character.isdigit() or (character in ['.', '+', '-'])):
					new_tostring += character
			formula[index] = new_tostring
	formula = ' '.join(formula)

	# Third, get the Counter object
	entry_elements = Counter()

	# Fourth, get the elements in brackets
	res = re.findall(r'\(.*?\)', formula)
	for bracket in res:
		no_multiplier = False
		# ------------------------------------
		front_index = formula.index(bracket)
		# get the multiplier for the bracket
		front_multiplier = ''
		for index in range(front_index-1,-1,-1):
			if (formula[index] in ['n', 'x', 'y', 'z']):
				no_multiplier = True
				front_multiplier = formula[index] + front_multiplier
			elif formula[index].isdigit() or (formula[index] == '.'):
				front_multiplier = formula[index] + front_multiplier
			else:
				break
		# ------------------------------------
		back_index = front_index + len(bracket)
		back_multiplier = ''
		for index in range(back_index,len(formula),+1):
			if (formula[index] in ['n', 'x', 'y', 'z']):
				no_multiplier = True
				back_multiplier = back_multiplier + formula[index]
			elif formula[index].isdigit() or (formula[index] == '.'):
				back_multiplier = back_multiplier + formula[index] 
			else:
				break
		# ------------------------------------
		bracket = bracket.replace('(','').replace(')','')
		# use multiplier
		if not no_multiplier:
			if front_multiplier == '':
				front_multiplier_no = 1.0
			else:
				front_multiplier_no = float(front_multiplier)
			if back_multiplier == '':
				back_multiplier_no = 1.0
			else:
				back_multiplier_no = float(back_multiplier)

			multiplier_no = front_multiplier_no * back_multiplier_no
			# get the elements inside the bracket
			for value in bracket.split():
				element, number_of = get_element_and_number_from_string(value)
				entry_elements[element] += multiplier_no*float(number_of)
		# remove this bracket from the formula, been accounted for
		full_bracket_string = str(front_multiplier)+'('+bracket+')'+str(back_multiplier)
		formula = formula.replace(full_bracket_string,'').rstrip().lstrip()

	# Fifth, get the elements in the main part of the formula
	for value in formula.split():
		element, number_of = get_element_and_number_from_string(value)
		entry_elements[element] += float(number_of)

	# Sixth, return element counter object
	return entry_elements

def get_element_and_number_from_string(value):
	"""
	This method will extract the elements and the number of those elements from the input string.

	Parameters
	----------
	value : str.
		This is the input string

	Returns
	-------
	element : str.
		This is the element.
	number_of : float
		This is the number of elements in the string.
	"""

	# First, process the value variable.
	tostring = re.split(r'(\d+)', value)
	while '' in tostring:
		tostring.remove('')

	# Second, obtain the element.
	element = tostring[0]
	if element == 'D':
		element = 'H'

	# Third, obtain the number of this element in value.
	number_of = float(''.join(tostring[1:]))

	# Fourth, return the element and the number of that element in the value variable.
	return element, number_of

# ---------------------------------------------------------------------------------------------------------------------------

flag_filename = 'crystal_quality_information.csv'
smiles_filenameGCD = 'different_to_smiles.gcd'
smiles_filenameTXT = 'different_to_smiles.txt'
headers = ['Identifier', 'Has Disorder', 'Crystal different to Crystallographer Drawing (including Hydrogens)', 'Crystal different to Crystallographer Drawing (excluding Hydrogens)', 'Is Total Charge 0', 'Is Total Multiplicity 1']
def save_flags_to_disk(identifier, flags, save_to_filepath, crystal_quality_information_lock):
	"""
	This method will save the flags about this crystal to disk

	Parameters
	----------
	identifier : str.
		This is the identifier for the crystal
	flags : list of bool.
		These are the booleans that indicate statements about the crystal.
	save_to_filepath : str.
		This is the path to save flags to.
	crystal_quality_information_lock : FileLock.lock
		This is the lock for recording crystal quality information
	"""

	# First, pop the end of the flags list that indicates if the crystal has the same configuration as the SMILES code. 
	smiles_comparison_data = flags.pop(-1)

	# Second, check if the flag_filename already exists
	flag_file_exists = os.path.exists(save_to_filepath+'/'+flag_filename)

	# Third, lock the disk writing at this point. 
	with crystal_quality_information_lock:

		# Fourth, save the flags to file.
		with open(save_to_filepath+'/'+flag_filename, 'a') as flagCSV:

			# 4.1: create the csv writer for the csv file.
			csvwriter = csv.writer(flagCSV)

			# 4.2: If the csv file does not exist, write a header for the csv file
			if not flag_file_exists:
				csvwriter.writerow(headers)

			# 4.3: Obtain the components that were examined from the flags list
			has_disorder, crystal_different_to_user, is_charge_zero, is_mult_one = flags

			# 4.4: Determine if the crystal have the same number of atoms, include and excluding Hydrogen atoms. 
			crystal_different_to_user_with_H, crystal_different_to_user_without_H = crystal_different_to_user

			# 4.5: Write the information about the crystal to the csv file
			csvwriter.writerow([str(identifier), has_disorder, crystal_different_to_user_with_H, crystal_different_to_user_without_H, is_charge_zero, is_mult_one])

		# Fifth, if the crystal is different to it's SMILES code, write this to a gcd file and a txt file that indicates the differences between the crystal make-up and the SMILES code. 
		if not smiles_comparison_data[0]:
			with open(save_to_filepath+'/'+smiles_filenameGCD, 'a') as flagTXT:
				flagTXT.write(str(identifier)+'\n')
			with open(save_to_filepath+'/'+smiles_filenameTXT, 'a') as flagTXT:
				flagTXT.write(str(identifier)+'\t'+str(smiles_comparison_data[1:])+'\n')

# ---------------------------------------------------------------------------------------------------------------------------

