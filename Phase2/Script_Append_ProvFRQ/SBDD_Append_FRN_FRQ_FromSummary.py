# ---------------------------------------------------------------------------
# SBDD_Append_FRN_FRQ_FromSummary.py.py
# Created on: October 26, 2011 
# Created by: Michael Byrne
# Federal Communications Commission
# appends the Prov_FRQ tables from every State into one table
# the Prov_FRQ table is at the root of each submitted file geodatabase
# and is the result of the Page 10 function of the State Summary
# ---------------------------------------------------------------------------

# Import system modules
import arcpy
from arcpy import env
import sys, string, os, math

#write out global variables
#thePGDB = "C:/Users/michael.byrne/Processing.gdb"  #processing file geodatabase
thePGDB = "C:/work/nbbm/2014_2/chkResult/appendFRNFRQ/Processing.gdb"
theLocation = "C:/work/nbbm/2014_2/gdb/"
theYear = "2014"
theMonth = "10"
theDay = "01"

States = ["AK","AL","AR","AS","AZ","CA","CO","CT"]          #1
States = States + ["DC","DE","FL","GA","GU","HI","IA","ID"] #2
States = States + ["IL","IN","KS","KY","LA","MA","MD","ME"] #3 
States = States + ["MI","MN","MO","MP","MS","MT","NC","ND"] #4 
States = States + ["NE","NH","NJ","NM","NV","NY","OH","OK"] #5
States = States + ["OR","PA","PR","RI","SC","SD","TN","TX"] #6
States = States + ["UT","VA","VI","VT","WA","WI","WV","WY"] #7


##write out functions
##Function sbdd_ExportToShape exports the created layers to shapefiles in appropriate directories
def sbdd_AddStToFRQ (myTB, myST):
    arcpy.AddMessage("     Begining " + myTB + " Processing")
    theSTexp = "'" + myST + "'"
    if arcpy.Exists(myTB):
        arcpy.DeleteField_management (myTB, ["State"])
        arcpy.AddField_management(myTB, "State", "TEXT", "", "", 2)
        arcpy.CalculateField_management(myTB, "State", theSTexp, "PYTHON")
        arcpy.Append_management([myTB], outTB, "NO_TEST")
    else:
        arcpy.AddMessage("     Table: " + myTB + " does not exist for this State")
    del myTB, theSTexp
    return ()

##Function to create the table which will contain all the overlay information
def sbdd_CreateTable (myTbl):
    arcpy.AddMessage("     Creating output table")
    if arcpy.Exists(myTbl):
        arcpy.Delete_management(myTbl)
    arcpy.CreateTable_management(thePGDB, myTbl)
    arcpy.AddField_management(myTbl, "FREQUENCY", "LONG", "", "", "15")
    arcpy.AddField_management(myTbl, "FRN", "TEXT", "", "", "10")
    arcpy.AddField_management(myTbl, "PROVNAME", "TEXT", "", "", "200")
    arcpy.AddField_management(myTbl, "DBANAME", "TEXT", "", "", "200")
    arcpy.AddField_management(myTbl, "STATE", "TEXT", "", "", "2")
    del myTbl
    return ()


#*******************************************************************************************************
##################Main Code below
#*******************************************************************************************************
try:
    arcpy.env.workspace = thePGDB
    outTB = "SBDD_UniqueProviders"
    if arcpy.Exists(thePGDB):
        sbdd_CreateTable(outTB)
        for theST in States:
            arcpy.AddMessage("the state is: " + theST)
            theTB = theLocation + theST + "/" + theST + "_SBDD_" + theYear
            theTB = theTB + "_" + theMonth + "_" + theDay + ".gdb/Prov_FRQ"
            sbdd_AddStToFRQ(theTB, theST)
            arcpy.AddMessage("     appending: "  + theST + " Prov_FRQ")
        del theTB, theST, States, thePGDB, outTB
    else:
        arcpy.AddMessage("You need a file named: " + thePGDB)
except:
    arcpy.AddMessage("Something bad happened")

  
