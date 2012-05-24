# ---------------------------------------------------------------------------
# SBDD_FRQ_uniques.py
# Created on: May 16, 2011 
# Created by: Michael Byrne
# Federal Communications Commission
# creates the individual layers necessary for the
# National Broadband Map from the source file geodatabases
# requires one State submission at a time
# ---------------------------------------------------------------------------

# Import system modules
import arcpy
from arcpy import env
import sys, string, os, math

#write out global variables
thePGDB = "C:/Users/michael.byrne/Processing.gdb"  #processing file geodatabase
arcpy.env.workspace = thePGDB

theLocation = "C:/Users/NBMSource/Fall2011/"
theLocation = "C:/Users/michael.byrne/NBMSource/Fall2011/"
theYear = "2011"
theMonth = "10"
theDay = "01"

States = ["AK","AL","AR","AS","AZ","CA","CO","CT"]          #1
States = States + ["DC","DE","FL","GA","GU","HI","IA","ID"] #2
States = States + ["IL","IN","KS","KY","LA","MA","MD","ME"] #3 
States = States + ["MI","MN","MO","MP","MS","MT","NC","ND"] #4 
States = States + ["NE","NH","NJ","NM","NV","NY","OH","OK"] #5
States = States + ["OR","PA","PR","RI","SC","SD","TN","TX"] #6
States = States + ["UT","VA","VI","WA","WI","WV","WY"] #7"VT",

##write out functions
##Function sbdd_ExportToShape exports the created layers to shapefiles in appropriate directories
def sbdd_FRQ (theFD, theFC):
    arcpy.AddMessage("     Begining " + theFC + " Processing")
    myTbls = [theFC + "_frq", theFC + "_" + theST + "_frq"]
    for myTbl in myTbls:
        if arcpy.Exists(myTbl):
            arcpy.Delete_management(myTbl)
    del myTbl, myTbls
    theFields = ["FRN","PROVNAME","DBANAME","TRANSTECH","MAXADDOWN","MAXADUP","TYPICDOWN","TYPICUP"] #,"SPECTRUM"]
    theSTexp = "'" + theST + "'"
    if int(arcpy.GetCount_management(theFD + "/" + theFC).getOutput(0)) > 1:
        arcpy.Frequency_analysis(theFD + "/" + theFC, theFC + "_frq", theFields, "")
        arcpy.AddField_management(theFC + "_frq", "State", "TEXT", "", "", 2)
        arcpy.CalculateField_management(theFC + "_frq", "State", theSTexp, "PYTHON")
        arcpy.Rename_management(theFC + "_frq", theFC + "_" + theST + "_frq")
    del theSTexp, theFields
    return ()

#*******************************************************************************************************
##################Main Code below
#*******************************************************************************************************
try:
    for theST in States:
        arcpy.AddMessage("the state is: " + theST)
        theFCs = ["BB_Service_Address","BB_Service_CensusBlock","BB_Service_RoadSegment","BB_Service_Wireless"]
        for theFC in theFCs:
            theFD = theLocation + theST + "/" + theST + "_SBDD_" + theYear + "_"
            theFD = theFD + theMonth + "_" + theDay + ".gdb/NATL_Broadband_Map/"          
            sbdd_FRQ(theFD, theFC)
    del theFD, theST, States, thePGDB, theFCs, theFC
except:
    arcpy.AddMessage("Something bad happened")

  
