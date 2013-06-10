## ---------------------------------------------------------------------------
###   VERSION 0.1 (for postgis)
### nbm_import_shp.py
### Created on: June 4, 20123
### Created by: Michael Byrne
### Federal Communications Commission 
##
## ---------------------------------------------------------------------------
##this script runs the import of shape files from NBM data integration process

##dependencies
##software
##runs in python
##postgres/gis (open geo suite)
##data
##import shape files for each state in the State list
##outputs one table as an append of every shape input
##uses a template shape (from the state of RI) which is truncated
##appends all others to this blank table

# Import system modules
import sys, string, os
import time
now = time.localtime(time.time())
print "local time:", time.asctime(now)

#variables
myHost = "localhost"
myPort = "54321"
myUser = "postgres"
db = "feomike"
schema = "sbi2012dec"
srcdir = "/users/feomike/documents/data/sbi/2013_1/export/shapes/"
theEPSG = "4326"

#define ddl for block
def create_tbl_ddl(myTbl):
	myST = "ri"  #change to ri
	thepSQL = "psql -p 54321 -h " + myHost + " " + db + " -c "
	thepSQL = thepSQL + "'DROP TABLE if exists " + schema + ".shp_" + myTbl + "'"
	os.system(thepSQL)
	srcshp = srcdir + myST + "_" + myTbl + ".shp "
	thepSQL = "shp2pgsql -s " + theEPSG + " -I -W latin1 -g geom " + srcshp + schema + "."
	thepSQL = thepSQL + "shp_" + myTbl + " " +  db + " | psql -p 54321 -h localhost " + db
	os.system(thepSQL)
	thepSQL = "psql -p 54321 -h " + myHost + " " + db + " -c " 
	thepSQL = thepSQL + "'TRUNCATE " + schema + ".shp_" + myTbl + "'"
	os.system(thepSQL)

#define ddl for fc
def load_tbl(myST, myfc):
	srcshp = srcdir + myST + "_" + myfc + ".shp "
	if os.path.exists(srcshp.strip()):
		theSQL = "shp2pgsql -s " + theEPSG + " -W latin1 -g geom -a " + srcshp + schema + "."
		theSQL = theSQL + "shp_" + myfc + " " + db + " | psql -p 54321 -h localhost " + db
		os.system(theSQL)
		thepSQL = "psql -p 54321 -h " + myHost + " " + db + " -c "
		thepSQL = thepSQL + "'VACUUM " + schema + ".shp_" + myfc + "'"
		os.system(thepSQL)

try:
	theLoop = ["address", "road", "cai", "middlemile", "block"]  
	for fc in theLoop:
		create_tbl_ddl(fc)
		#load data
		States = ["AK","AL","AR","AS","AZ","CA","CO","CT"]          #1
		States = States + ["DC","DE","FL","GA","GU","HI","IA","ID"] #2
		States = States + ["IL","IN","KS","KY","LA","MA","MD","ME"] #3 
		States = States + ["MI","MN","MO","MP","MS","MT","NC","ND"] #4 
		States = States + ["NE","NH","NJ","NM","NV","NY","OH","OK"] #5
		States = States + ["OR","PA","PR","RI","SC","SD","TN","TX"] #6
		States = States + ["UT","VA","VI","VT","WA","WI","WV","WY"] #7
		for theST in States:
			load_tbl(theST, fc)
except:
	print "something bad bad happened"     
      
