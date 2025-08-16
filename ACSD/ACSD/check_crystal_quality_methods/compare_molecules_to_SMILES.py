"""
compare_molecules_to_SMILES.py, Geoffrey Weal, 16/7/22

This script is designed to check the SMILES code to the moelcules in the crystal and check if they are the same or not.
"""
import re
from collections import Counter
from pysmiles import read_smiles

def is_crystal_same_as_SMILES(molecules, molecule_graphs, entry_object):
	"""
	This method is designed to check the SMILES code to the moelcules in the crystal and check if they are the same or not.

	Will report back either True or False if the SMILES code is the same or notto the molecules in the crystal.

	Parameters
	----------
	molecules : list of ase.Atoms
		This is a list of the molecules in the crystal.
	molecule_graphs ; list of networkx.graphs
		This is a list of all the graphs associated with each molecule in the crystal.
	entry_object : ccdc.entry
		This is the ccdc entry object for this crystal.

	Returns
	-------
	has_disorder : bool.
		True if the crystal contains disorder in it. False if not
	"""

	# Preliminary Step 1: Check to make sure that the molecules in the molecules dictionary are named consecutively from 1 to len(molecules)
	if not (sorted(molecules.keys()) == list(range(1,len(molecules)+1))):
		to_string  = f'Error: The molecules in the molecules dictionary are not consecutively ordered from 1 to len(molecules) (which is {len(molecules)}).\n'
		to_string += f'Molecule names in the molecules dictionary: {sorted(molecules.keys())}\n'
		to_string += f'Expected molecule names: {list(range(1,len(molecules)+1))}\n'
		to_string += 'Check this.'
		raise Exception(to_string)

	# Preliminary Step 2: Check to make sure that the graphs in molecule_graphs are named consecutively from 1 to len(molecule_graphs)
	if not (sorted(molecule_graphs.keys()) == list(range(1,len(molecule_graphs)+1))):
		to_string  = f'Error: The molecule graphs in molecule_graphs are not consecutively ordered from 1 to len(molecule_graphs) (which is {len(molecule_graphs)}).\n'
		to_string += f'Molecule names in molecule_graphs: {sorted(molecule_graphs.keys())}\n'
		to_string += f'Expected molecule names: {list(range(1,len(molecule_graphs)+1))}\n'
		to_string += 'Check this.'
		raise Exception(to_string)

	# Preliminary Step 3: Check to make sure all the molecules have an associated graph.
	if not (sorted(molecules.keys()) == sorted(molecule_graphs.keys())):
		to_string  = f'Error: Some of the molecules and/or their associated graphs are missing\n'
		to_string += f'Molecule names in molecules: {sorted(molecules.keys())}\n'
		to_string += f'Molecule names in molecule_graphs: {sorted(molecule_graphs.keys())}\n'
		to_string += 'Check this.'
		raise Exception(to_string)

	# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

	# First, obtain the SMILES graph from the entry_object
	smiles_graphs = []
	for molecule in entry_object.molecule.components:
		smiles_code = molecule.smiles
		if smiles_code is None:
			return (False, None, None)
		smiles_graphs.append(read_smiles(smiles_code))

	# Second, extract the information about the atoms from the SMILES graph of the molecules in the crystal.
	smiles_collections = []
	for smiles_graph in smiles_graphs:
		counter = []
		for node_index in smiles_graph.nodes:
			element = smiles_graph.nodes[node_index]['element']
			if element in ['H', 'D']:
				continue
			number_of_non_hydrogens = 0
			number_of_hydrogens = smiles_graph.nodes[node_index]['hcount']
			for neighbour_index in smiles_graph[node_index]:
				neighbour_element = smiles_graph.nodes[neighbour_index]['element']
				if neighbour_element in ['H', 'D']:
					number_of_hydrogens += 1
				else:
					number_of_non_hydrogens += 1
			charge = float(smiles_graph.nodes[node_index]['charge'])
			atom_details = (element, number_of_non_hydrogens, charge, number_of_hydrogens)
			counter.append(atom_details)
		counter = Counter(counter)
		smiles_collections.append(counter)

	# Third, extract the information about the atom from the molecules and molecule_graphs
	molecules_collections = []
	for molecule_name in sorted(molecules.keys()):
		molecule       = molecules[molecule_name]
		molecule_graph = molecule_graphs[molecule_name]
		counter = []
		for node_index in molecule_graph.nodes:
			element = molecule[node_index].symbol
			if element in ['H', 'D']:
				continue
			number_of_non_hydrogens = 0
			number_of_hydrogens = 0
			for neighbour_index in molecule_graph[node_index]:
				neighbour_element = molecule[neighbour_index].symbol
				if neighbour_element in ['H', 'D']:
					number_of_hydrogens += 1
				else:
					number_of_non_hydrogens += 1
			charge = float(molecule[node_index].charge)
			atom_details = (element, number_of_non_hydrogens, charge, number_of_hydrogens)
			counter.append(atom_details)
		counter = Counter(counter)
		molecules_collections.append(counter)

	# Fourth, determine the differences between the atom information between the SMILES codes and the molecules+molecule_graphs objects. 
	smiles_collections_diff = []
	for smiles_collection in smiles_collections:
		for index in range(len(molecules_collections)):
			molecules_collection = molecules_collections[index]
			compare_counters = Counter({key: (molecules_collection.get(key, 0) - value) for key, value in smiles_collection.items()})
			if all([(value == 0) for value in compare_counters.values()]):
				del molecules_collections[index]
				break
		else:
			smiles_collections_diff.append(smiles_collection)

	# Return:
	#    1. Is the crystal the same as the SMILES code (True = Yes, False = No)
	#    2. The SMILES components that differ to the molecules code.
	#    3. The molecule components that differ to the SMILES code.
	return (len(molecules_collections) == 0, smiles_collections_diff, molecules_collections)



	