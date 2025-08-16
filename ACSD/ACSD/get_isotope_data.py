"""
get_isotope_data.py, Geoffrey Weal, 24/1/2024

This method will provide isotope data to the ACSD from ASE
"""
import os
from ase.data.isotopes import download_isotope_data

def get_isotope_data():
	"""
	This method will provide isotope data to the ACSD from ASE.

	Returns
	-------
	isotopes : dict.
		This dictionary contains all the isotope information from ASE

	"""

	# First, make a folder to place this isotope data into.
	path_to_isotope_data  = os.path.dirname(__file__)+'/'+'isotope_data'
	if not os.path.exists(path_to_isotope_data):
		os.makedirs(path_to_isotope_data)

	# Second, if the isotope_data.txt file down not exist, download the isotoe data.
	isotope_data_filename = 'isotope_data.txt'
	if not os.path.exists(path_to_isotope_data+'/'+isotope_data_filename):
		print('Getting isotope information from ASE')
		isotopes = download_isotope_data()
		with open(path_to_isotope_data+'/'+isotope_data_filename, 'w') as isotopedataTXT:
			isotopedataTXT.write(str(isotopes))

	# Third, obtain the isotope data from isotope_data.txt
	with open(path_to_isotope_data+'/'+isotope_data_filename, 'r') as isotopedataTXT:
		isotopes = eval(isotopedataTXT.readline().rstrip())

	# Fourth, return isotopes dictionary.
	return isotopes