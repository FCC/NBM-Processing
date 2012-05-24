\NMB-Processing\Summary
May 24, 2011

This directory contains the scripts which create the state submission summary file;  
this script is run client (e.g. awardee side).

See the word document in this directory for documentation.

##Arguments
theFD = sys.argv[1]  #theFeatureDataSet e.g. C:\Users\transfer\SBDD_Fall\DE\BB_Map_FGB_DE.gdb\NATL_Broadband_Map
theST = sys.argv[2]  #theState e.g. DE
theOF = sys.argv[3]  #theOutputFolder e.g. C:\Users\transfer\SBDD_Fall\DE

##global variables
theFGDB              #the fileGeodatabase theFD.rstrip("NATL_Broadband_Map")
theYear = today.year
theMonth = today.month
theDay = today.day

##Comments
- the output is a csv file, which the use will copy and paste into the template.xls data worksheet
- the template.xls calculates all the summaries with references from the data worksheet, after data is pasted

##expected directories / files
- all states are expected to be in a file geodatabase conforming to the standard 
  w/ a feature dataset named "NATL_Broadband_Map"


##expected run time
about 20 minutes