# ---------------------------------------------------------------------------
# SBDD_Check_CAI.py
# Created on: May 14, 2013
# Created by: Michael Byrne
# Federal Communications Commission
# checks CAI for carriage returns line feeds
# ---------------------------------------------------------------------------

# Import system modules
import arcpy
from arcpy import env
import sys, string, os, math

#global variables
#theOF = "C:/Users/michael.byrne/NBM/2013_1/"
theOF = "C:/work/nbbm/2014_2/chkResult/chkCAI/"

States = ["AK","AL","AR","AS","AZ","CA","CO","CT"]          #1
States = States + ["DC","DE","FL","GA","GU","HI","IA","ID"] #2
States = States + ["IL","IN","KS","KY","LA","MA","MD","ME"] #3
States = States + ["MI","MN","MO","MS","MT","NC","ND","MP"] #4
States = States + ["NE","NH","NJ","NM","NV","NY","OH","OK"] #5
States = States + ["OR","PA","PR","RI","SC","SD","TN","TX"] #6
States = States + ["UT","VA","VI","VT","WA","WI","WV","WY"] #7 


theLocation = "C:/work/nbbm/2014_2/gdb/"
theYear = "2014"
theMonth = "10"
theDay = "01"

#Function sbdd_ascii - checks and replaces non-ascii characters
def sbdd_ascii (myTbl, myOutFile):
    #go open up and read this table
    myFile = open(myOutFile, 'a')
    rows = arcpy.UpdateCursor(myTbl)
    for row in rows:
        for myF in ["Anchorname", "Address", "Url", "CAIID", "StreetType", "City"]:
            myID = row.getValue("SBDD_ID")
            myVal = row.getValue(myF)
            try:
                if myVal is not None:
                    myVal.decode('ascii')
            except:
                #
                arcpy.AddMessage("       fixing error in sbdd_id:" + myID)
                myStr = ''
                for c in myVal:
#                    arcpy.AddMessage(c.encode('ascii','replace'))
                    myStr = myStr + c.encode('ascii','replace').strip()
                myStr = myStr.replace('?','#')
#                arcpy.AddMessage("          old: " + myVal)
                arcpy.AddMessage("          new: " + myStr)
#                row.setValue(myF, myStr)
#                rows.updateRow(row)                
                myFile.write(theST + ": has errors on record: " + myID + " for field: " + myF + " new: " + myStr + "\n") 
    myFile.close()
    del row, rows

#Function for correctly inserting the Lat/Lon
#has argument of myTbl
def sbdd_LatLon(myTbl):
    rows = arcpy.UpdateCursor(myTbl)
    for row in rows:
        myX = row.getValue("Shape").getPart().X
        myY = row.getValue("Shape").getPart().Y
        arcpy.AddMessage("theValue of X is: " + str(myX) + " and the value is: " + str(row.getValue("Longitude")))
        arcpy.AddMessage("theValue of Y is: " + str(myY) + " and the value is: " + str(row.getValue("Latitude")))
        row.longitude = myX
        row.latitude = myY
        rows.updateRow(row)


#****************************************************************************
##################Main Code below
#****************************************************************************


for theST in States:
    outFile = theOF + theST + "_cai_errors.txt"
    myFile = open(outFile, 'w')
    myFile.write("errors for CAI w/ non-utf-8/ascii characters" + "\n")
    theFD = theLocation + theST + "/" + theST + "_SBDD_" + theYear
    theFD = theFD + "_" + theMonth + "_" + theDay
    theFD = theFD + ".gdb/NATL_Broadband_Map/"   
    if arcpy.Exists(theFD + "BB_Service_CAInstitutions"):
        myFile = open(outFile, 'a')
        myFile.write("errors for state: " + theST + "\n")
        myFile.close()            
        myCnt = str(arcpy.GetCount_management(
            theFD + "BB_Service_CAInstitutions").getOutput(0))
        theMsg = "     going to check out this many records for "
        theMsg = theMsg + theST + ": " + myCnt
        arcpy.AddMessage(theMsg)
        if myCnt <> '0':
#            sbdd_ascii(theFD + "BB_Service_CAInstitutions", outFile)
            sbdd_LatLon(theFD + "BB_Service_CAInstitutions")
            del myFile, outFile, theMsg, myCnt
    else:
        theMsg = "     CAI table for " + theST
        theMsg = theMsg + " does not exist" 
        arcpy.AddMessage(theMsg)
        del theMsg
del theFD, theST, States #theHead, 
del theOF, theLocation, theYear, theMonth, theDay 
  
