# ---------------------------------------------------------------------------
# SBDD_Export_WirelessOverlay.py
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
theOF = "C:/Users/michael.byrne/NBM/Export/Wirelessoverlay/"
theFGDB = "C:/Users/michael.byrne/Processing_wireless.gdb/"
thePrefix = "wireless_block_overlay_"

States = ["AK","AL","AR","AS","AZ","CA","CO","CT"]          #1
States = States + ["DC","DE","FL","GA","GU","HI","IA","ID"] #2
States = States + ["IL","IN","KS","KY","LA","MA","MD","ME"] #3
States = States + ["MI","MN","MO","MS","MT","NC","ND","MP"] #4
States = States + ["NE","NH","NJ","NM","NV","NY","OH","OK"] #5
States = States + ["OR","PA","PR","RI","SC","SD","TN","TX"] #6
States = States + ["UT","VA","VI","VT","WA","WI","WV","WY"] #7

States = ["AS"]

theLocation = "C:/Users/michael.byrne/NBM/Spring2013/data/"
theYear = "2013"
theMonth = "04"
theDay = "01"
theSuffix = "_NBM-WirelessOverlay-" + theYear + "-" + theMonth + ".csv"

#Function sbdd_ProviderReport writes out the unique Provider Values Detail
#has no argument; 
def sbdd_exportFile (myTbl, myOutFile):
    #go open up and read this table
    myFile = open(myOutFile, 'a')
    for row in arcpy.SearchCursor(myTbl):
        myOID = str(row.getValue("OBJECTID")).strip()
        myBlk = str(row.getValue("GEOID10")).strip()
        myPCT = str(row.getValue("PCT")).strip()
        myFRN = str(row.getValue("FRN")).strip()        
        myProv = str(row.getValue("PROVNAME").encode('utf-8')).strip()
        myDBA = str(row.getValue("DBANAME").encode('utf-8')).strip() 
        myTech = str(row.getValue("TRANSTECH"))
        myDown = str(row.getValue("MAXADDOWN")).strip()      
        myUp = str(row.getValue("MAXADUP")).strip()
        myTYDown = str(row.getValue("TYPICDOWN")).strip()         
        myTYUp = str(row.getValue("TYPICUP")).strip()
        myID = str(row.getValue("SBDD_ID")).strip()
        myStr = myOID + "|" + myBlk + "|" + myPCT + "|"
        myStr = myStr + myFRN + "|" + myProv + "|" + myDBA + "|"
        myStr = myStr + myTech + "|" + myDown + "|"
        myStr = myStr + myUp + "|" + myTYDown + "|" + myTYUp + "|"
        myStr = myStr + myID
        myFile.write(myStr +  "\n")
        del myOID, myBlk, myPCT
        del myFRN, myProv, myDBA
        del myTech, myDown
        del myUp, myTYDown, myTYUp
        del myID, myStr
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
        theHead = "SHAPEID|CENSUSBLOCK_FIPS|PCT_BLK_IN_SHAPE|FRN|"
        theHead = theHead + "PROVANME|DBANAME|TRANSTECH|"
        theHead = theHead + "MAXADDOWN|MAXADUP|TYPICDOWN|TYPICUP|SBDD_ID"
        #write output
        theTbl = theFGDB + thePrefix + theST
        if arcpy.Exists(theTbl):
            outFile = theOF + theST + theSuffix
            myFile = open(outFile, 'w')
            myFile.write(theHead + "\n")
            myFile.close()            
            myCnt = str(arcpy.GetCount_management(theTbl).getOutput(0))
            theMsg = "     going to write out this many records for "
            theMsg = theMsg + theST + ": " + myCnt
            arcpy.AddMessage(theMsg)
            sbdd_exportFile(theTbl, outFile)
            del myFile, outFile, theMsg, myCnt            
        else:
            theMsg = "     wireless overlay table for " + theST
            theMsg = theMsg + " does not exist" 
            arcpy.AddMessage(theMsg)
            del theMsg
    del theFD, theHead, theST, States, theTbl, thePrefix
    del theOF, theSuffix, theLocation, theYear, theMonth, theDay 
except:
    arcpy.AddMessage("Something bad happened")


  
