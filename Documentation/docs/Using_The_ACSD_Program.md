# How To Use The ACSD Program

## Running the ACSD Program

The Access Cambridge Structural Database (ACSD) program is run by typing the ``ACSD run`` command into the terminal. This command requires either a ``gcd`` file, or a folder of ``gcd`` files. 

```bash
# Example of running the ACSD program on a gcd file.
ACSD run crystals_like_ACUSEZ.gcd

# Example of running the ACSD program on a folder of gcd files.
ACSD run crystal_gcd_files
```
You can also give multiple ``gcd`` files and folders:

```bash
# Example of providing multiple gcd files and folder to ACSD
ACSD run crystals_like_ACUSEZ.gcd crystal_gcd_files
```
An example of a ``gcd`` file can be found in the [Example of a ``gcd`` file](Using_The_ACSD_Program.md#example-of-a-gcd-file) section. 

There are several optional commands you can also provide to the ``ACSD run`` command:

* ``--overwrite``: If you are re-running the ``ACSD run`` command, you can either:

	* ``--overwrite True``  -> Overwrite existing crystal files (this is the default).
	* ``--overwrite False`` -> Skip any crystals that have already been processed. 

* ``--crystals_to_exclude``: If you want to exclude any crystal identifiers, you can create a txt file that contains all the identifiers you want to exclude
	
	* This is generally used for problem-solving or debugging if one or more of the crystals in your ``gcd`` files and folders is having problems, but you dont want to remove those identifiers from these  ``gcd`` files and folders. 

* ``--no_cpus``: This indicates the number of cpu cores you would to the ACSD program to use. Default: 1

	!!! tip

		If you have a number of crystals to process, consider setting this value higher to utilise more of your CPU. Doing this will allow the ACSD to process multiple crystals simultaneously.

An example of using these optional commands is given below:

```bash
# Example of providing multiple gcd files and folder to ACSD
ACSD -T run crystal_gcd_files --overwrite False --crystals_to_exclude exclude_crystals.txt
```

!!! note

	Depending on the number of crystal you are wanting to inspect from the CSD, this program can take a few hours to collect all the crystals. 

!!! example

	You can find examples for running the ACSD program in [the ``Examples`` folder here](https://github.com/geoffreyweal/ACSD/tree/main/Examples).

## Outputs from the ACSD Program

The ACSD program will create a folder called ``crystal_database`` and will save xyz files of the crystals given in your ``gcd`` file(s) to this folder. See the [Crystal XYZ File Format](Crystal_File_Format.md) chapter to learn more about the format of these crystal files. The ``crystal_database`` will also possibly contain the following files

* ``crystal_quality_information.csv``: This file contain information about the quality of the crystals that were written as ``xyz`` file. 
* ``crystals_not_written.txt``: This file contains the crystals where ``xyz`` files were not written for them, and an explanation for why these crystals were not written as an ``xyz`` file. 
* ``different_to_smiles.gcd``: If there are any crystals where the molecules are different to the SMILES code, this may indicate there is a structural problems with the molecules. 

	* Note that the crystal may be fine, as it may be that the user has entered in the SMILE code for this crystal incorrectly. 
	* It pays to check these crystal, but it is possible that there is no problem with the crystal. 

* ``different_to_smiles.txt``: This is a complementary file to ``different_to_smiles.gcd`` that indicates possible reasons why there is a difference between the ``SMILES`` code and the crystal. 

As well as the  ``crystal_database`` folder, the ACSD program will also create a file called ``ACSD_logfile.log`` that will record any warning messages produced while the ``ACSD run`` command runs. 


### Information about crystal quality given in the ``crystal_quality_information.csv`` file

The information that is recorded in the ``crystal_quality_information.csv`` file are:

* `Identifier` (`str.`): This is the name of the crystal from the CCDC.
* `Has Disorder` (`bool.`): This indicates if the crystal was recorded with disorder in them or not
* `Crystal different to Crystallographer Drawing (including Hydrogens)` (`bool.`): This indicates if the crystal differs from its SMILES code (including hydrogens)
* `Crystal different to Crystallographer Drawing (excluding Hydrogens)` (`bool.`): This indicates if the crystal differs from its SMILES code (excluding hydrogens)
* `Is Total Charge 0` (`bool.`): This indicates if the crystal have a non-zero charge (as recorded from the CCDC).
* `Is Total Multiplicity 1` (`bool.`): This indicates if the multiplicity of the crystal is not 1 (as recorded from the CCDC).

An example of the ``crystal_quality_information.csv`` file:

| Identifier | Has Disorder | Crystal different to Crystallographer Drawing (including Hydrogens) | Crystal different to Crystallographer Drawing (excluding Hydrogens) | Is Total Charge 0 | Is Total Multiplicity 1 |
|------------|--------------|---------------------------------------------------------------------|---------------------------------------------------------------------|-------------------|-------------------------|
| ABALIZ     | True         | True                                                                | True                                                                | True              | True                    |
| ABEXOX     | False        | True                                                                | True                                                                | True              | True                    |
| ABIBEW     | False        | True                                                                | True                                                                | True              | True                    |
| ABIBIA     | False        | False                                                               | False                                                               | True              | True                    |
| ABIBOG     | True         | False                                                               | False                                                               | True              | True                    |
| ABICAT     | True         | True                                                                | True                                                                | True              | True                    |
| ABICEX     | False        | False                                                               | False                                                               | True              | True                    |
| ...        | ...          | ...                                                                 | ...                                                                 | ...               | ...                     |

!!! note 

	If you find that one or more crystals have ``Crystal different to Crystallographer Drawing`` as ``False`` (with and without hydrogens), this is probably ok as the is common that there is a discrepency between the crystal structure and the way that CCDC evaluates the crystallographer's drawing.


## Example of a ``gcd`` file

An example of a ``gcd`` file called ``crystals_like_ACUSEZ.gcd`` is shown below

```bash
ACUSEZ
ACUSID
AKUCIU
AQEDEH
AQEDIL
AQEDOR
AQIBOT
ATOMED
AWUQEQ
AYESOO
BOMMOI
CONKIC
CONKOI
CONKUO
DAYVEH
DAZZEK
DIRKOH
EBOZEE
EBOZII
ECENAD
EDUKUM
EDULIB
EGODUB
EGOFAJ
EGOFEN
EGOKIW
ELOLAV
EWEWAH
EXEVOT
FEYDIZ
FEYDOF
FIQSEG
FIQSIK
FIQSOQ
FOXDII
FUSFEH
GAGVUJ
GATXEH
HURJAI
HUWSUQ
INAZEE
IPALIX
IPAMOE
IRIJAX
IWERIN
JITLII
JOQZIA
KEPDIV
KEPDIV01
KEPDOB
KEPDOB01
KEPDUH
KEPDUH01
KOTWOI
KOTWUO
KOTXAV
KOTXEZ
KOTXID
KOTXOJ
KOTXUP
KOTYAW
MERQIM
MERQOS
MERQUY
MERRAF
MIGDAK
MIGLAS
MIGLIA
MIXXID
MOPGII
MUQNIX
NAYWIW
NAYWOC
NAYWUI
NESXOB
NIXVEW
OFUSEQ
OFUSIU
OFUSOA
OFUSUG
OHAZEF
OXECOM
PENCIW
PIJGOH
PIJGUN
PUKBOP
PUKBUV
QEPKIG
QEWRIU
QEWSAN
RAJLEX
RAQNAC
RAQNEG
RUGFEG
RUGFIK
RUGFOQ
SAZQIX
SAZQOD
SIZNIB
SIZNOH
SIZNUN
SIZPAV
SIZPEZ
SOYCOB
TUDJAF
UCIVIO
UCIVOU
UMUTIH
VAGTUV
VAHVEI
VARFOL
VIVDUC
VUCDOP
WATJAF
WAWSAR
WOTHAQ
XURLAZ
XURLED
XURLON
XURLUT
XURMAA
XURMEE
XURMII
XURMUU
XURNAB
YOCFAA
ZUSBAT
```