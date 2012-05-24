\NBM-Processing\DataPrep
May 24, 2011

This directory contains the scripts which create the output directly from the file geodatabases 
which drive the map (and download).  there are two of three processes automated
1) Block table - an export of the block table from the file geodatabse
2) Random Point Overlay (NOT COMPLETE) - an overlay of address points and street segments on the Random Points
3) Wireless Block overlay (NOT COMPLETE - an overlay of the wireless shape on blocks

SBDD_BlockTable
##Arguments
No arguments are necessary to run this script; it runs on a big loop of all states

##global variables
theOF = "C:/Users/Export/BlockTable/"

##expected directories / files
- all data is expected to live in "C:/Users/Spring2011/" and conform the the naming convention on line 65
- all states are expected to be in a file geodatabase conforming to the standard w/ a feature dataset named "NATL_Broadband_Map"
- data is exported to "C:/Users/Export/BlockTable/"
- these .dbf's are used for both the data to drive map (give to paul) and data for download

##expected run time
1 hour for whole county


SBDD_RndPtOverlay
##Arguments
No arguments are necessary to run this script; it runs on a big loop of all states

##global variables
theOF = "C:/Users/Export/RandomPTTables/"
thePGDB = "C:/Users/Processing.gdb"  #processing file geodatabase
theRndPT = "C:/Users/RandomPoint50States.gdb/point_all_50States" #point_all_50States"

##expected directories / files
- all data is expected to live in "C:/Users/Spring2011/" and conform the the naming convention on line 248
- all states are expected to be in a file geodatabase conforming to the standard w/ a feature dataset named "NATL_Broadband_Map"
- data is exported to "C:/Users/Export/RandomPTTables/"
  as .dbf's for the data download pages; one for both address and roadsement
- a master table of records appended is also created in "C:/Users/Processing.gdb" and is named "RndPtOverlay"

##expected run time
-unknown