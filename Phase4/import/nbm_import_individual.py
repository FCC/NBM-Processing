## ---------------------------------------------------------------------------
###   VERSION 0.1 (for postgis)
### nbm_import_individual.py
### Created on: June 4, 20123
### Created by: Michael Byrne
### Federal Communications Commission 
##
## ---------------------------------------------------------------------------
##this script runs the import of shape files from NBM data integration process
##the output is individual state layers 

##dependencies
##software
##runs in python
##postgres/gis (open geo suite)
##data
##loads data as individual shapes into individual tables by state
##then fixes geometry errors which might be associated w/ each table

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
	srcshp = srcdir + myST + "_" + myfc + ".shp " #space is padded here
	print srcshp
	if os.path.exists(srcshp.strip()):
		thepSQL = "psql -p 54321 -h " + myHost + " " + db + " -c "
		thepSQL = thepSQL + "'DROP TABLE if exists " + schema + "." + myST.lower() 
		thepSQL = thepSQL + "_" + myfc + "'"
		os.system(thepSQL)
		theSQL = "shp2pgsql -s " + theEPSG + " -W latin1 -g geom -I " + srcshp + schema + "."
		theSQL = theSQL + myST.lower() + "_" + myfc + " " + db + " | psql -p 54321 -h localhost " + db
		os.system(theSQL)
		thepSQL = "psql -p " + myPort + " -h " + myHost + " " + db + " -c "
		thepSQL = thepSQL + "'ALTER TABLE " + schema + "." + myST.lower() + "_" + myfc
		thepSQL = thepSQL + " DROP CONSTRAINT enforce_geotype_geom;'"
		os.system(thepSQL)
		thepSQL = "psql -p " + myPort + " -h " + myHost + " " + db + " -c "
		thepSQL = thepSQL + "'UPDATE " + schema + "." + myST.lower() + "_" + myfc
		thepSQL = thepSQL + " set geom = st_buffer(geom,0) where not st_isvalid(geom);'"
		os.system(thepSQL)
		thepSQL = "psql -p " + myPort + " -h " + myHost + " " + db + " -c "
		thepSQL = thepSQL + "'ALTER TABLE " + schema + "." + myST.lower() + "_" + myfc
		thepSQL = thepSQL + " add CONSTRAINT enforce_geotype_geom CHECK (geometrytype(geom) = "
		thepSQL = thepSQL + "'POLYGON'::text OR geometrytype(geom) = 'MULTIPOLYGON'::text OR geom IS NULL);'"
#		os.system(theSQL)
		thepSQL = "psql -p 54321 -h " + myHost + " " + db + " -c "
		thepSQL = thepSQL + "'VACUUM " + schema + ".shp_" + myfc + "'"
		os.system(thepSQL)

try:
	theLoop = ["block"]  #"address", "road", "cai", "middlemile", 
	for fc in theLoop:
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
      
