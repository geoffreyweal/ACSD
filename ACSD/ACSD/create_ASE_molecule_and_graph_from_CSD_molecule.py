"""
create_ASE_molecule_and_graph_from_CSD_molecule.py, Geoffrey Weal, 22/6/2022

This script will convert the molecules in the crystal from CSD objects into ASE objects, and also creates molecule graphs of these molecules. 
"""

from copy                       import deepcopy
from ase                        import Atom, Atoms
from itertools                  import permutations
from networkx                   import Graph, relabel_nodes
from SUMELF                     import get_hybridisation_from_CSD, get_bond_type_from_CSD
from ACSD.ACSD.get_isotope_data import get_isotope_data
isotopes = get_isotope_data()

def create_ASE_molecule_and_graph_from_CSD_molecule(CSD_molecule, logger=None):
	"""
	This method will create the molecule graph from the CSD object.

	Parameters
	----------
	CSD_molecule : ccdc.molecule
		These are the molecules in the crystal.

	Return
	------
	ASE_molecules : dict of ase.Atoms
		These are all the molecules in the crystal.
	molecule_graphs : dict of networkx.Graph
		These are the graphs of all the molecules in the crystal. 
	hydrogens_with_no_coordinates_in_mols : dict. of dict. of {int:int}
		This dictionary contains all the atoms in the molecules that are attached to hydrogens that have not been coordinates.
	"""

	# First, this is the list of molecules and graphs for each molecule in CSD_molecule
	ASE_molecules   = {}
	molecule_graphs = {}

	# Second, initialise lists for recording hydrogen atoms with no coordinates
	all_non_coord_information = []

	# Third, initialise a list to record which atoms in the molecules in the crystal are bound to hydrogen atoms with no coordinates. 
	hydrogens_with_no_coordinates_in_mols = {}

	# Fourth, obtain all the separate unique molecules in the crystal (that are unique with respect to the symmetry of the crystal).
	if isinstance(CSD_molecule,(list, tuple)):
		components = CSD_molecule
	else:
		components = CSD_molecule.components

	# Fifth, these are all the components that make up the CSD_molecule
	for index, component in enumerate(components):

		# 5.1: Get the numerical name of the molecule:
		name = index + 1

		# 5.2: Get the atoms and bonds involved in the component
		CSD_atoms = component.atoms
		CSD_bonds = component.bonds

		# 5.3: Setup the ASE object for the molecule
		ASE_molecule = Atoms()

		# 5.4: Initalise the graph for this molecule.
		molecule_graph = Graph()

		# 5.5: Initialise a list that indicates what H atoms in the molecules have not been given positions
		non_coordinated_hydrogens = []

		# -----------------------------------------------------------------------------

		# 5.6: Add the atoms to the molecule graph.
		#      NOTE: all atom indices are related the index of the atom in the CSD object
		atom_indices_for_graph = []
		for atom in CSD_atoms:

			# 3.6.1: Make sure the atom has not been double recorded in the atom_indices_for_graph list.
			if atom.index in [index for (index, attr) in atom_indices_for_graph]:
				raise Exception('huh?')

			# 3.6.2: Check if this atom has coordinates. If it does not, move on.
			#        * Record if a atom with no position is a hydrogen atom
			element                 = atom.atomic_symbol
			has_coord               = (atom.coordinates is not None)
			if (not has_coord):
				if element in ['H', 'D', 'T']:
					non_coordinated_hydrogens.append(atom.index)
				continue

			# 3.6.3: Collect all the information about this atom
			position                = atom.coordinates
			charge                  = atom.formal_charge
			is_H_donor              = atom.is_donor
			is_H_acceptor           = atom.is_acceptor
			is_spiro_atom           = atom.is_spiro
			involved_in_no_of_rings = len(atom.rings)
			hybridisation           = get_hybridisation_from_CSD(atom)
			atom_information        = {'E': str(element), 'is_H_donor': is_H_donor, 'is_H_acceptor': is_H_acceptor, 'is_spiro_atom': is_spiro_atom, 'involved_in_no_of_rings': involved_in_no_of_rings, 'hybridisation': hybridisation, 'added_or_modified': False}

			# 3.6.4: Create the ASE atom object for this atom
			ase_atom = get_atom(element, position, charge, logger=logger)

			# 3.6.5: Add the ASE atom object for this atom.
			ASE_molecule.append(ase_atom)

			# 3.6.6: Record the atom into the atom_indices_for_graph
			atom_indices_for_graph.append((atom.index, atom_information))

		# 3.7: Add the atoms from the molecule as nodes in the graph.
		molecule_graph.add_nodes_from(atom_indices_for_graph)

		# -----------------------------------------------------------------------------

		# 3.8: Add the bonds to the molecule graph.
		#      NOTE: all atom indices are related the index of the atom in the CSD object
		bond_indices = []; bond_indices_for_graph = []
		for bond in CSD_bonds:

			# 3.8.1: Obtain the atoms involved in this bond. 
			atom1 = bond.atoms[0]
			atom2 = bond.atoms[1]

			# 3.8.2: Check that bond is not between the same atom (self bonding, which doesnt make sense)
			if atom1.index == atom2.index:
				raise Exception('huh?')

			# 3.8.3: Record the bond between two atoms. 
			#        * Here, the bond is recorded as (lower_index_number, higher_index_number)
			atoms_in_bond = (atom1.index, atom2.index) if (atom1.index < atom2.index) else (atom2.index, atom1.index)

			# 3.8.4: Check that this bond has not already been recorded.
			if atoms_in_bond in bond_indices:
				raise Exception('huh?')
			bond_indices.append(atoms_in_bond)

			# 3.8.5: Check that both atoms in the bond contain coordinates.
			if all([(atom_index in non_coordinated_hydrogens) for atom_index in atoms_in_bond]):
				raise Exception('Error: Both atoms in bond do not have coordinates')

			# 3.8.6: If the bond contains a hydrogen with no position, just record this in 'no_of_neighbouring_non_cord_H' and move on.
			bond_contains_hydrogen_with_no_coordinates = False
			for i1, i2 in permutations((0,1)):
				if atoms_in_bond[i1] in non_coordinated_hydrogens:
					hydrogens_with_no_coordinates_in_mols.setdefault(name,{}).setdefault(atoms_in_bond[i2],0)
					hydrogens_with_no_coordinates_in_mols[name][atoms_in_bond[i2]] += 1
					bond_contains_hydrogen_with_no_coordinates = True
					continue
			if bond_contains_hydrogen_with_no_coordinates:
				continue

			# 3.8.7: Collect all the information about this bond
			bond_type                 = str(bond.bond_type)
			is_conjugated             = bond.is_conjugated
			is_cyclic                 = bond.is_cyclic
			involved_in_no_of_rings   = len(bond.rings)
			bond_type_from_sybyl_type = get_bond_type_from_CSD(bond)
			bond_information          = {'bond_type': bond_type, 'is_conjugated': is_conjugated, 'is_cyclic': is_cyclic, 'involved_in_no_of_rings': involved_in_no_of_rings, 'bond_type_from_sybyl_type': bond_type_from_sybyl_type}

			# 3.8.6: Record information about the bond to bond_indices_for_graph.
			bond_indices_for_graph.append((atoms_in_bond[0], atoms_in_bond[1], bond_information))

		# 3.9: Add the bonds from the molecule as edges in the graph.
		molecule_graph.add_edges_from(bond_indices_for_graph)

		# -----------------------------------------------------------------------------

		# 3.10: Convert the indices from their value in the CSD.molecules object to their values specifically in the molecule itself.
		#      * These two indices are probably the same, but this makes sure that any issues about indexing are sorted, for example 
		#        any issues that may arise due to hydrogens or other atoms without non-coordinates. 
		mapping        = {atom.index: index for index, atom in enumerate(CSD_atoms)}
		molecule_graph = relabel_nodes(molecule_graph, mapping)

		# -----------------------------------------------------------------------------

		# 3.11: Check that name is not already in ASE_molecules
		if name in ASE_molecules.keys():
			raise Exception('Error: Found molecule '+str(name)+' in ASE_molecules. There is a programming error here. Check this.')

		# 3.12: Save the ASE atoms object describing the core information for the molecule into the ASE_molecules list.
		ASE_molecules[name] = ASE_molecule

		# 3.13: Check that name is not already in molecule_graphs
		if name in molecule_graphs.keys():
			raise Exception('Error: Found molecule '+str(name)+' in molecule_graphs. There is a programming error here. Check this.')

		# 3.14: Add the molecule_graph to the molecule_graphs list.
		molecule_graphs[name] = molecule_graph

	# Fourth, check to make sure that the molecules in ASE_molecules are named consecutively from 1 to len(components)
	if not (sorted(ASE_molecules.keys()) == list(range(1,len(components)+1))):
		to_string  = f'Error: The molecules in ASE_molecules are not consecutively ordered from 1 to len(components) (which is {len(components)}).\n'
		to_string += f'Molecule names in ASE_molecules: {sorted(ASE_molecules.keys())}\n'
		to_string += f'Expected molecule names: {list(range(1,len(components)+1))}\n'
		to_string += 'Check this.'
		raise Exception(to_string)

	# Fifth, check to make sure that the graphs in molecule_graphs are named consecutively from 1 to len(components)
	if not (sorted(molecule_graphs.keys()) == list(range(1,len(components)+1))):
		to_string  = f'Error: The molecule graphs in molecule_graphs are not consecutively ordered from 1 to len(components) (which is {len(components)}).\n'
		to_string += f'Molecule names in molecule_graphs: {sorted(molecule_graphs.keys())}\n'
		to_string += f'Expected molecule names: {list(range(1,len(components)+1))}\n'
		to_string += 'Check this.'
		raise Exception(to_string)

	# Sixth, make sure that all molecule names can be found in ASE_molecules and molecule_graphs
	if not (sorted(ASE_molecules.keys()) == sorted(molecule_graphs.keys())):
		to_string  = f'Error: There are missing names in ASE_molecules and/or molecule_graphs\n'
		to_string += f'Molecule names in ASE_molecules: {sorted(ASE_molecules.keys())}\n'
		to_string += f'Molecule names in molecule_graphs: {sorted(molecule_graphs.keys())}\n'
		to_string += 'Check this.'
		raise Exception(to_string)

	# Seventh, return all the molecule graphs for each component in the CSD_molecule
	return ASE_molecules, molecule_graphs, hydrogens_with_no_coordinates_in_mols

# =====================================================================================================================

def get_atom(symbol, position, charge, logger=None):
	"""
	This method is designed to convert the input variable into an ASE atom object

	Parameters
	----------
	symbol : str.
		This is the element of the atom
	position: tuple of floats
		This is the position of the atom
	charge : float
		This is the formal charge of the atom
	logger : 
		This is the log for recording what has been happening.

	Returns
	-------
	ASE_molecules : ase.Atoms
		This is the convert ASE object of the molecules of interest

	"""

	# First, make a note of what hydrogen isotopes have been recorded in the long.
	does_contain_deuterium = False
	does_contain_tritium = False

	# Second, if the atom is a Deuterium or Tritium atom, change the symbol to H (for hydrogen).
	if   symbol == 'D':

		# 2.1: This is a deuterium atom, set this as a hydrogen atom.
		if (logger is not None) and (not does_contain_deuterium):
			does_contain_deuterium = True
			logger.info('This molecule contains Deuterium')
		symbol = 'H'
		mass = isotopes[1][2]['mass']

	elif symbol == 'T':

		# 2.2: This is a tritium atom, set this as a hydrogen atom.
		if (logger is not None) and (not does_contain_tritium):
			does_contain_tritium = True
			logger.info('This molecule contains Tritium')
		symbol = 'H'
		mass = isotopes[1][3]['mass']

	# Third, create the ASE atom object
	if symbol in ['D', 'T']:
		ase_atom = Atom(symbol=symbol, position=position, charge=charge, mass=mass)
	else:
		ase_atom = Atom(symbol=symbol, position=position, charge=charge)

	# Fourth, return ase_atom
	return ase_atom

# =====================================================================================================================

