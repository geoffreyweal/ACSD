# The information about the Access Cambridge Structural Database program

__name__    = 'ACSD (The Access Cambridge Structural Database Program)'
__version__ = '0.18'
__author__  = 'Dr. Geoffrey Weal, Dr. Josh Sutton, Dr. Chayanit Wechwithayakhlung, Dr. Daniel Packwood, Dr. Paul Hume, Prof. Justin Hodgkiss'

import sys
from importlib.util import find_spec

if sys.version_info[0] == 2:
	toString = ''
	toString += '\n'
	toString += '================================================'+'\n'
	toString += 'This is the Access Cambridge Structural Database Program'+'\n'
	toString += 'Version: '+str(__version__)+'\n'
	toString += '\n'
	toString += 'The Access Cambridge Structural Database requires Python3. You are attempting to execute this program in Python2.'+'\n'
	toString += 'Make sure you are running the Access Cambridge Structural Database program in Python3 and try again'+'\n'
	toString += 'This program will exit before beginning'+'\n'
	toString += '================================================'+'\n'
	raise ImportError(toString)
if not sys.version_info[1] >= 4:
	toString = ''
	toString += '\n'
	toString += '================================================'+'\n'
	toString += 'This is the Access Cambridge Structural Database Program'+'\n'
	toString += 'Version: '+str(__version__)+'\n'
	toString += '\n'
	#toString += 'The Access Cambridge Structural Database program requires Python 3.7.'+'\n'
	#toString += 'This is because the Cambridge Structural Database Python API required Python 3.7.'+'\n'
	toString += 'The Access Cambridge Structural Database program requires Python 3.4 or higher.'+'\n'
	toString += 'You are using Python '+str('.'.join([str(value) for value in sys.version_info]))
	toString += '\n'
	toString += 'Change the version of Python you are using to Python 3.7.\n'
	toString += 'This program will exit before beginning'+'\n'
	toString += '================================================'+'\n'
	raise ImportError(toString)

# ------------------------------------------------------------------------------------------------------------------------
# A check for ASE

ase_spec = find_spec("ase")
ase_found = (ase_spec is not None)
if not ase_found:
	toString = ''
	toString += '\n'
	toString += '================================================'+'\n'
	toString += 'This is the Access Cambridge Structural Database Program'+'\n'
	toString += 'Version: '+str(__version__)+'\n'
	toString += '\n'
	toString += 'The Access Cambridge Structural Database Prep program requires ASE.'+'\n'
	toString += '\n'
	toString += 'Install ASE through pip by following the instruction in https://github.com/GardenGroupUO/ACSD'+'\n'
	toString += 'These instructions will ask you to install ase by typing the following into your terminal\n'
	toString += 'pip install --user --upgrade ase\n'
	toString += '\n'
	toString += 'This program will exit before beginning'+'\n'
	toString += '================================================'+'\n'
	raise ImportError(toString)	

import ase
ase_version_minimum = '3.19.0'
from packaging import version
#from distutils.version import StrictVersion
#if StrictVersion(ase.__version__) < StrictVersion(ase_version_minimum):
if version.parse(ase.__version__) < version.parse(ase_version_minimum):
	toString = ''
	toString += '\n'
	toString += '================================================'+'\n'
	toString += 'This is the Access Cambridge Structural Database Program'+'\n'
	toString += 'Version: '+str(__version__)+'\n'
	toString += '\n'
	toString += 'The Access Cambridge Structural Database program requires ASE greater than or equal to '+str(ase_version_minimum)+'.'+'\n'
	toString += 'The current version of ASE you are using is '+str(ase.__version__)+'.'+'\n'
	toString += '\n'
	toString += 'Install ASE through pip by following the instruction in https://github.com/GardenGroupUO/ACSD'+'\n'
	toString += 'These instructions will ask you to install ase by typing the following into your terminal\n'
	toString += 'pip install --user --upgrade ase\n'
	toString += '\n'
	toString += 'This program will exit before beginning'+'\n'
	toString += '================================================'+'\n'
	raise ImportError(toString)

# ------------------------------------------------------------------------------------------------------------------------

numpy_spec = find_spec("numpy")
numpy_found = (numpy_spec is not None)
if not numpy_found:
	toString = ''
	toString += '\n'
	toString += '================================================'+'\n'
	toString += 'This is the Access Cambridge Structural Database Program'+'\n'
	toString += 'Version: '+str(__version__)+'\n'
	toString += '\n'
	toString += 'The Access Cambridge Structural Database program requires the "numpy" program.'+'\n'
	toString += '\n'
	toString += 'Install numpy by typing the following into your terminal\n'
	toString += '\n'
	toString += 'pip install --user --upgrade numpy\n'
	toString += '\n'
	toString += 'This program should have been installed when you installed ASE using pip\n'
	toString += '\n'
	toString += 'This program will exit before beginning'+'\n'
	toString += '================================================'+'\n'
	raise ImportError(toString)	

# ------------------------------------------------------------------------------------------------------------------------

ccdc_spec = find_spec("ccdc")
ccdc_found = (ccdc_spec is not None)
if not ccdc_found:
	toString = ''
	toString += '\n'
	toString += '================================================'+'\n'
	toString += 'This is the Access Cambridge Structural Database Program'+'\n'
	toString += 'Version: '+str(__version__)+'\n'
	toString += '\n'
	toString += 'The Access Cambridge Structural Database program requires the "ccdc" program.'+'\n'
	toString += '\n'
	toString += 'Install ccdc by following the instructions at https://downloads.ccdc.cam.ac.uk/documentation/API/installation_notes.html#installation.'+'\n'
	toString += '\n'
	toString += 'This program will exit before beginning'+'\n'
	toString += '================================================'+'\n'
	raise ImportError(toString)	

# ------------------------------------------------------------------------------------------------------------------------

pysmiles_spec = find_spec("pysmiles")
pysmiles_found = (pysmiles_spec is not None)
if not pysmiles_found:
	toString = ''
	toString += '\n'
	toString += '================================================'+'\n'
	toString += 'This is the Access Cambridge Structural Database Program'+'\n'
	toString += 'Version: '+str(__version__)+'\n'
	toString += '\n'
	toString += 'The Access Cambridge Structural Database program requires the "pysmiles" program.'+'\n'
	toString += '\n'
	toString += 'pip install --user --upgrade pysmiles\n'
	toString += '\n'
	toString += 'This program will exit before beginning'+'\n'
	toString += '================================================'+'\n'
	raise ImportError(toString)	

# ------------------------------------------------------------------------------------------------------------------------

packaging_spec = find_spec("packaging")
packaging_found = (packaging_spec is not None)
if not packaging_found:
	toString = ''
	toString += '\n'
	toString += '================================================'+'\n'
	toString += 'This is the Access Cambridge Structural Database Program'+'\n'
	toString += 'Version: '+str(__version__)+'\n'
	toString += '\n'
	toString += 'The Access Cambridge Structural Database program requires the "packaging" program.'+'\n'
	toString += '\n'
	toString += 'Install packaging through pip by following the instruction in https://github.com/GardenGroupUO/ACSD'+'\n'
	toString += 'These instructions will ask you to install packaging by typing the following into your terminal\n'
	toString += '\n'
	toString += 'pip install --user --upgrade packaging\n'
	toString += '\n'
	toString += 'This program will exit before beginning'+'\n'
	toString += '================================================'+'\n'
	raise ImportError(toString)	

# ------------------------------------------------------------------------------------------------------------------------

tqdm_spec = find_spec("tqdm")
tqdm_found = (tqdm_spec is not None)
if not tqdm_found:
	toString = ''
	toString += '\n'
	toString += '================================================'+'\n'
	toString += 'This is the Access Cambridge Structural Database Program'+'\n'
	toString += 'Version: '+str(__version__)+'\n'
	toString += '\n'
	toString += 'The Access Cambridge Structural Database program requires the "tqdm" program..'+'\n'
	toString += '\n'
	toString += 'Install tqdm through pip by following the instruction in https://github.com/GardenGroupUO/ACSD'+'\n'
	toString += 'These instructions will ask you to install tqdm by typing the following into your terminal\n'
	toString += '\n'
	toString += 'pip install --user --upgrade tqdm\n'
	toString += '\n'
	toString += 'This program will exit before beginning'+'\n'
	toString += '================================================'+'\n'
	raise ImportError(toString)	

# ------------------------------------------------------------------------------------------------------------------------

__author_email__ = 'geoffrey.weal@vuw.ac.nz'
__license__ = 'GNU AFFERO GENERAL PUBLIC LICENSE'
__url__ = 'https://github.com/geoffreyweal/ACSD'
__doc__ = 'See https://github.com/geoffreyweal/ACSD for the documentation on this program'
__all__ = ['']

# ------------------------------------------------------------------------------------------------------------------------
