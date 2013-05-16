# ---------------------------------------------------------------------------
# SBDD_Check_CAI.py
# Created on: May 14, 2013
# Created by: Michael Byrne
# Federal Communications Commission
# checks CAI for non-ascii stuff, and replaces them w ' ' 
# ---------------------------------------------------------------------------

# Import system modules
import arcpy
from arcpy import env
import sys, string, os, math

#global variables
theOF = "C:/Users/michael.byrne/"

States = ["AK","AL","AR","AS","AZ","CA","CO","CT"]          #1
States = States + ["DC","DE","FL","GA","GU","HI","IA","ID"] #2
States = States + ["IL","IN","KS","KY","LA","MA","MD","ME"] #3
States = States + ["MI","MN","MO","MS","MT","NC","ND","MP"] #4
States = States + ["NE","NH","NJ","NM","NV","NY","OH","OK"] #5
States = States + ["OR","PA","PR","RI","SC","SD","TN","TX"] #6
States = States + ["UT","VA","VI","VT","WA","WI","WV","WY"] #7 

theLocation = "C:/Users/michael.byrne/NBM/Spring2013/Data/"
theYear = "2013"
theMonth = "04"
theDay = "01"

#Function sbdd_ProviderReport writes out the unique Provider Values Detail
#has no argument; 
def sbdd_exportFile (myTbl, myOutFile):
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
                    #arcpy.AddMessage(c.encode('ascii','replace'))
                    myStr = myStr + c.encode('ascii','replace')
                myStr = myStr.replace('?',' ')
                arcpy.AddMessage("     old: " + myVal)
                arcpy.AddMessage("     new: " + myStr)
                row.setValue(myF, myStr)
                rows.updateRow(row)                
                myFile.write(theST + ": has errors on record: " + myID + "for field: " + myF + "\n") 
    myFile.close()
    del row, rows

#****************************************************************************
##################Main Code below
#****************************************************************************

outFile = theOF + "cai_errors.txt"
myFile = open(outFile, 'w')
myFile.write("errors for CAI w/ non-utf-8/ascii characters" + "\n")
for theST in States:
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
            sbdd_exportFile(theFD + "BB_Service_CAInstitutions", outFile)
#            del myFile, outFile, theMsg, myCnt
    else:
        theMsg = "     CAI table for " + theST
        theMsg = theMsg + " does not exist" 
        arcpy.AddMessage(theMsg)
        del theMsg
del theFD, theST, States #theHead, 
del theOF, theLocation, theYear, theMonth, theDay 



  
