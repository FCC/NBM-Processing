# ---------------------------------------------------------------------------
# SBDD_Export_BlockTable.py
# Created on: May 24, 2011 
# Created by: Michael Byrne
# Federal Communications Commission
# exports the feature classes for the block table
# ---------------------------------------------------------------------------
# updated May 16 w/ enduser cat in the output
#
# ---------------------------------------------------------------------------
# Import system modules
import arcpy
from arcpy import env
import sys, string, os, math

#global variables
#theOF = "C:/Users/michael.byrne/nbm/Export/BlockTable/"
theOF = "C:/work/nbbm/2014_2/chkResult/export/BlockTable/"

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
theSuffix = "_NBM-Block-" + theYear + "-" + theMonth + ".csv"

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
        myStFIPS = str(row.getValue("STATEFIPS")).strip()
        myCtyFIPS = str(row.getValue("COUNTYFIPS")).strip()
        myTract = str(row.getValue("TRACT")).strip()
        myBlk = str(row.getValue("BLOCKID")).strip()
        myFIPS = str(row.getValue("FULLFIPSID")).strip()      
        myTech = str(row.getValue("TRANSTECH"))
        myDown = str(row.getValue("MAXADDOWN")).strip()      
        myUp = str(row.getValue("MAXADUP")).strip()
        myTYDown = str(row.getValue("TYPICDOWN")).strip()         
        myTYUp = str(row.getValue("TYPICUP")).strip()
        myCat = str(row.getValue("ENDUSERCAT")).strip()
        myID = str(row.getValue("SBDD_ID")).strip()
        myStr = myProv + "|" + myDBA + "|" + myProvType + "|"
        myStr = myStr + myFRN + "|" + myStFIPS + "|" + myCtyFIPS + "|"
        myStr = myStr + myTract + "|" + myBlk + "|" + myFIPS + "|"
        myStr = myStr + myTech + "|" + myDown + "|" + myUp + "|"
        myStr = myStr + myTYDown + "|" + myTYUp + "|" + myCat + "|" + myID
        myFile.write(myStr +  "\n")
        del myProv, myDBA, myProvType
        del myFRN, myStFIPS, myCtyFIPS
        del myTract, myBlk, myFIPS
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
        theHead = "PROVANME|DBANAME|Provider_Type|FRN|STATEFIPS|COUNTYFIPS|"
        theHead = theHead + "TRACT|BLOCKID|FULLFIPSID|TRANSTECH|MAXADDOWN|"
        theHead = theHead + "MAXADUP|TYPICDOWN|TYPICUP|ENDUSERCAT|SBDD_ID"

        #write output
        if arcpy.Exists(theFD + "BB_Service_CensusBlock"):
            outFile = theOF + theST + theSuffix
            myFile = open(outFile, 'w')
            myFile.write(theHead + "\n")
            myFile.close()            
            myCnt = str(arcpy.GetCount_management(
                theFD + "BB_Service_CensusBlock").getOutput(0))
            theMsg = "     going to write out this many records for "
            theMsg = theMsg + theST + ": " + myCnt
            arcpy.AddMessage(theMsg)
            sbdd_exportFile(theFD + "BB_Service_CensusBlock", outFile)
            del myFile, outFile, theMsg, myCnt
        else:
            theMsg = "     block table for " + theST
            theMsg = theMsg + " does not exist" 
            arcpy.AddMessage(theMsg)
            del theMsg
    del theFD, theHead, theST, States
    del theOF, theSuffix, theLocation, theYear, theMonth, theDay 
except:
    arcpy.AddMessage("Something bad happened")
    
