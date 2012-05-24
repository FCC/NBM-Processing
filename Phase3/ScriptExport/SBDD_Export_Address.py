# ---------------------------------------------------------------------------
# SBDD_Export_Address.py
# Created on: May 24, 2011 
# Created by: Michael Byrne
# Federal Communications Commission
# exports the feature classes for the block table
# ---------------------------------------------------------------------------

# Import system modules
import arcpy
from arcpy import env
import sys, string, os, math

#global variables
theOF = "C:/Users/michael.byrne/Export/Table/Address/"
theOF = "C:/Users/Export/Table/Address/"
theSuffix = "_NBM-Address-June-2011.csv"

States = ["AK","AL","AR","AS","AZ","CA","CO","CT"]          #1
States = States + ["DC","DE","FL","GA","GU","HI","IA","ID"] #2
States = States + ["IL","IN","KS","KY","LA","MA","MD","ME"] #3
States = States + ["MI","MN","MO","MS","MT","NC","ND","MP"] #4
States = States + ["NE","NH","NJ","NM","NV","NY","OH","OK"] #5
States = States + ["OR","PA","PR","RI","SC","SD","TN","TX"] #6
States = States + ["UT","VA","VI","VT","WA","WI","WV","WY"] #7

theLocation = "C:/Users/michael.byrne/NBMSource/Fall2011/"
theLocation = "C:/Users/NBMSource/Fall2011/"
theYear = "2011"
theMonth = "10"
theDay = "01"

#Function sbdd_ProviderReport writes out the unique Provider Values Detail
#has no argument; 
def sbdd_exportFile (myTbl, myOutFile):
    #go open up and read this table
    myFile = open(myOutFile, 'a')
    for row in arcpy.SearchCursor(myTbl):
        myProv = str(row.getValue("PROVNAME").encode('utf-8')).strip()
        myDBA = str(row.getValue("DBANAME").encode('utf-8')).strip() 
        myProvType = str(row.getValue("Provider_Type")).strip()
        myFRN = str(row.getValue("FRN")).strip()
        myFIPS = str(row.getValue("FULLFIPSID")).strip()
        myLat = str(row.getValue("LATITUDE"))
        myLon = str(row.getValue("LONGITUDE"))
        myEUC = str(row.getValue("ENDUSERCAT")).strip()
        myTech = str(row.getValue("TRANSTECH"))
        myDown = str(row.getValue("MAXADDOWN")).strip()      
        myUp = str(row.getValue("MAXADUP")).strip()
        myTYDown = str(row.getValue("TYPICDOWN")).strip()         
        myTYUp = str(row.getValue("TYPICUP")).strip()
        myID = str(row.getValue("SBDD_ID")).strip()
        myStr = myProv + "|" + myDBA + "|" + myProvType + "|"
        myStr = myStr + myFRN + "|" + myFIPS + "|" + myLat + "|"
        myStr = myStr + myLon + "|" + myEUC + "|"
        myStr = myStr + myTech + "|" + myDown + "|" + myUp + "|"
        myStr = myStr + myTYDown + "|" + myTYUp + "|" + myID
        myFile.write(myStr +  "\n")
        del myProv, myDBA, myProvType
        del myFRN, myFIPS, myLat, myLon, myEUC
        del myTech, myDown, myUp
        del myTYDown, myTYUp, myID, myStr
    myFile.close()
    del row

#****************************************************************************
##################Main Code below
#****************************************************************************
try:
    for theST in States:
        theFD = theLocation + theST + "/" + theST + "_SBDD_" + theYear
        theFD = theFD + "_" + theMonth + "_" + theDay
        theFD = theFD + ".gdb/NATL_Broadband_Map/"
        theHead = "PROVANME|DBANAME|Provider_Type|FRN|FULLFIPSID|LATITUDE|"
        theHead = theHead + "LONGITUDE|ENDUSERCATEGORY|TRANSTECH|MAXADDOWN|"
        theHead = theHead + "MAXADUP|TYPICDOWN|TYPICUP|SBDD_ID"

        #write output
        if arcpy.Exists(theFD + "BB_Service_Address"):
            outFile = theOF + theST + theSuffix
            myFile = open(outFile, 'w')
            myFile.write(theHead + "\n")
            myFile.close()            
            myCnt = str(arcpy.GetCount_management(
                theFD + "BB_Service_Address").getOutput(0))
            theMsg = "     going to write out this many records for "
            theMsg = theMsg + theST + ": " + myCnt
            arcpy.AddMessage(theMsg)
            if myCnt <> '0':
                sbdd_exportFile(theFD + "BB_Service_Address", outFile)
            del myFile, outFile, theMsg, myCnt
        else:
            theMsg = "     Address table for " + theST
            theMsg = theMsg + " does not exist" 
            arcpy.AddMessage(theMsg)
            del theMsg
    del theFD, theHead, theST, States
    del theOF, theSuffix, theLocation, theYear, theMonth, theDay 
except:
    arcpy.AddMessage("Something bad happened")


  
