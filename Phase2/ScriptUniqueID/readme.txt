\NBM-Processing\UniqueID
May 24, 2011

This directory contains the scripts which create unique ID for each record in the submission across
all tables in the file geodatabase.

- SBDD_CreateIDs.py

##Arguments
No arguments are necessary to run this script; it runs on all states in a big loop 

##global variables
##theRound number increases by 1 every six months; 
##theRound = 3

Spring 2010 = 1
Fall 2010 = 2
Spring 2011 = 3
Fall 2011 = 4
Spring 2012 = 5
Fall 2012 = 6
Spring 2013 = 7
Fall 2014 = 8
Spring 2015 = 9
Fall 2015 = 10

##theSubmission is the first, second, third submission from the state
theSubmission = 1

##Comments
- change theFCs to modify which tables the script runs on (line 188)
- change STATES to modify which states the script runs on (lines 176-182)
- change theRound to increase the round number (line 19)
- change theSubmission if the state has resubmitted (line 21)
- change theFD to ensure the path of the file geodatabases (line 185)

##expected directories / files
- all data is expected to live in "C:/Users/Spring2011/" and conform the the naming convention on line 66
- all states are expected to be in a file geodatabase conforming to the standard w/ a feature dataset named "NATL_Broadband_Map"
- a new field called SBDD_ID is added onto the end of each table; and populated with a unique ID
- table names are - ["BB_Service_Address","BB_Service_CensusBlock","BB_Service_RoadSegment","BB_Service_Wireless"]

##expected run time
about 1 hour
