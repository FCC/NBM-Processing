\NBM-Processing\FRQFRN
May 24, 2011

This directory contains the scripts which create unique FRN combinations across all tables 
so matching to HOCONUM can happen; this script also helps in understanding initial variation
in the data (e.g. initial assessment).

- SBDD_FRQ_uniques.py
- SBDD_Append.py

##Arguments
No arguments are necessary to run this script; it runs on all states in a big loop

##global variables
thePGDB = "C:/Users/Processing.gdb"

##Comments
- make sure thePGDB is empty.  when there are relic tables, this script has some trouble
- change theFields to modify how the output is generated (line 25)
- fequency in large loops tends to crash arcgis due to memory; still trying to figure this out
  but perhaps converting the inputs all to arcgis version 10 file geodatabases might be a good idea
- change States to only run on particular states (lines 52 - 58)
- change theFCs to only run on certain tables (line 48)

##expected directories / files
- all data is expected to live in "C:/Users/Spring2011/" and conform the the naming convention on line 85
- all states are expected to be in a file geodatabase conforming to the standard w/ a feature dataset named "NATL_Broadband_Map"
- data is exported to tables named for each feature class in thePGDB
- table names are - ["BB_Service_Address","BB_Service_CensusBlock","BB_Service_RoadSegment","BB_Service_Wireless"]

##expected run time
unknown