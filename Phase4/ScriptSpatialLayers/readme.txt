\NBM-Processing\SpatialLayers
May 24, 2011

This directory contains the script which create the spatial layers.  it is run off of the delivered file geodatabases.
- SBDD_CreateSpatialLayers.py

##Arguments
the are no arguments for this script.  it runs on all states in one large loop

##global variables
    thePGDB = "C:/Users/Processing.gdb"  #processing file geodatabase
    theOF = "C:/Users/Export/"                   

##Comments
- shape files are named by state.  output is given directly to Computech for spatial data generation
- modify States to only run a portion or individual states
- comment out the functions to only run an individual set of feature classes (e.g. cai, block etc)

##expected directories / files
- all data is expected to live in "C:/Users/Spring2011/" and conform the the naming convention on line 259
- all states are expected to be in a file geodatabase conforming to the standard w/ a feature dataset named "NATL_Broadband_Map"
- this script outputs shape files in theOF directory w/ sub directories for Address, Block, CAI, Road and Wireless
- table names are - ["BB_Service_Address","BB_Service_CensusBlock","BB_Service_RoadSegment","BB_Service_Wireless"]

##expected run time
7 hours for whole county


