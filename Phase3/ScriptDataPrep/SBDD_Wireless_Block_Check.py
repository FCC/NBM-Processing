# ---------------------------------------------------------------------------
# SBDD_Wireless_Block_Check.py
# Created on: May 16, 2011 
# Created by: Michael Byrne
# Federal Communications Commission
# checks to make sure that all SBDD_IDs are accounted for
# in the overlay output tables that are in the input data
# ---------------------------------------------------------------------------

# Import system modules
import arcpy
from arcpy import env
import sys, string, os, math

thePGDB = "C:/Users/michael.byrne/Processing.gdb"  #processing file geodatabase
theLocation = "C:/Users/michael.byrne/NBM/Spring2013/Data/"
theYear = "2013"
theMonth = "04"
theDay = "01"

arcpy.env.workspace = thePGDB
States = ["AK","AL","AR","AS","AZ","CA","CO","CT"]          #1
States = States + ["DC","DE","FL","GA","GU","HI","IA","ID"] #2
States = States + ["IL","IN","KS","KY","LA","MA","MD","ME"] #3 
States = States + ["MI","MN","MO","MS","MT","NC","ND","MP"] #4 
States = States + ["NE","NH","NJ","NM","NV","NY","OH","OK"] #5
States = States + ["OR","PA","PR","RI","SC","SD","TN","TX"] #6 
States = States + ["UT","VA","VI","VT","WA","WI","WV","WY"] #7
States = ["AK"]


##write out functions
##Function sbdd_ExportToShape exports the created layers to shapefiles in
##appropriate directories
def checkOverlyRecords():
    theCnt = int(arcpy.GetCount_management(theFD + "BB_Service_Wireless").getOutput(0))
    myCnt = 1
    if theCnt > 0:  #if there are records in the wireless shape class        
        rows = arcpy.SearchCursor(theFD + "BB_Service_Wireless")
        for row in rows: #for every row in the delivered wireless layer
            arcpy.AddMessage("     checking ID " + str(myCnt) + " of " + str(theCnt))
            myTech = str(row.getValue("TRANSTECH"))
            myID = row.getValue("SBDD_ID") 
            if arcpy.Exists("wireless_block_" + theST + "_" + str(myCnt) ):  #if the state table exists, get the record count on it
                if myTech <> "60":                   
                    myQry = "TRANSTECH <> 60 AND SBDD_ID = '" + str(myID) + "'"
                    myLyr = theST + "SBDD_ID_Check_" + str(myCnt)
                    arcpy.MakeTableView_management ("wireless_block_" + theST + "_" + str(myCnt) , myLyr, myQry)
                    if int(arcpy.GetCount_management(myLyr).getOutput(0)) < 1:
                        arcpy.AddMessage("        SBDD_ID " + str(myID) + " is missing from " + theST)
                        del myLyr, myQry
                del myTech, myID
            elif myTech == "60":
                arcpy.AddMessage("       this record is a satellite record: " + myID)
            else:
                arcpy.AddMessage("     the state hasn't been run yet")
            myCnt = myCnt + 1
        del rows, row
    del  theCnt, myCnt
    return ()

#****************************************************************************
##################Main Code below
#****************************************************************************
try:
    for theST in States:
        theFD = theLocation + theST + "/" + theST + "_SBDD_" + theYear
        theFD = theFD + "_" + theMonth + "_" + theDay
        theFD = theFD + ".gdb/NATL_Broadband_Map/"
        arcpy.AddMessage("the state is: " + theST)
        checkOverlyRecords()
    del theFD, theST, States, thePGDB
except:
    arcpy.AddMessage("Something bad happened")


  
