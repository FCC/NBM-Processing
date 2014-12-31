# ---------------------------------------------------------------------------
#   VERSION 0.1 (for ArcGIS 10)
# SBDD_Export_RndPoint.py
# Created on: Sat. March 26 2011 
# Created by: Michael Byrne
# Federal Communications Commission
# writes out a text file for download
# ---------------------------------------------------------------------------

# Import system modules
import sys, string, os, arcpy
from arcpy import env
import time
from datetime import date
from os import remove, close
today = date.today()

#global variables
#theOF = "C:/Users/michael.byrne/NBM/Export/RndPoint/"
theOF = "C:/work/nbbm/2014_2/chkResult/export/RndPoint/"

#theFGDB = "C:/Users/michael.byrne/Processing_rndpt.gdb/"
theFGDB = "C:/work/nbbm/2014_2/chkResult/RntPtOverlay/Processing_rndpt.gdb/"

thePrefix = "RandomPoint_"
#theSuffix = "_NBM-RNDPoint-CSV-Dec-2012.csv"
theSuffix = "_NBM-RNDPoint-CSV-Jun-2014.csv"

States = ["AK","AL","AR","AS","AZ","CA","CO","CT"] #1
States = States + ["DC","DE","FL","GA","GU","HI","IA","ID"] #2
States = States + ["IL","IN","KS","KY","LA","MA","MD","ME"] #3
States = States + ["MI","MN","MO","MS","MT","NC","ND","MP"] #4 
States = States + ["NE","NH","NJ","NM","NV","NY","OH","OK"] #5
States = States + ["OR","PA","PR","RI","SC","SD","TN","TX"] #6
States = States + ["UT","VA","VI","VT","WA","WI","WV","WY"] #7

#Function sbdd_ProviderReport writes out the unique Provider Values Detail
#has no argument; 
def sbdd_exportFile (myTbl, myOutFile):
    #go open up and read this table
    myFile = open(myOutFile, 'a')
    for row in arcpy.SearchCursor(myTbl):
        myPTID = str(row.getValue("POINTID")).strip()
        mySrc = str(row.getValue("DATASOURCE")).strip()
        myIntID = str(row.getValue("JOIN_FID")).strip()
        myFIPS = str(row.getValue("BLOCKID10")).strip()        
        myFRN = str(row.getValue("FRN")).strip()
        myProv = str(row.getValue("PROVNAME").encode('utf-8')).strip()
        myDBA = str(row.getValue("DBANAME").encode('utf-8')).strip() 
        myTech = str(row.getValue("TRANSTECH"))
        myType = str(row.getValue("PROVIDER_T")).strip()        
        myDown = str(row.getValue("MAXADDOWN")).strip()      
        myUp = str(row.getValue("MAXADUP")).strip()
        myTYDown = str(row.getValue("TYPICDOWN")).strip()         
        myTYUp = str(row.getValue("TYPICUP")).strip()
        myEndCat = str(row.getValue("ENDUSERCAT")).strip()
        myID = str(row.getValue("SBDD_ID")).strip()
        myStr = myPTID + "|" + mySrc + "|" + myIntID + "|" + myFIPS + "|"
        myStr = myStr + myFRN + "|" + myProv + "|" + myDBA + "|" + myTech + "|" 
        myStr = myStr + myType + "|" + myDown + "|" + myUp + "|" 
        myStr = myStr + myTYDown + "|" + myTYUp + "|" + myEndCat + "|" + myID
        myFile.write(myStr +  "\n")
        del myPTID, mySrc, myIntID, myFIPS,  
        del myFRN, myProv, myDBA, myTech
        del myType, myDown, myUp
        del myTYDown, myTYUp, myID, myStr
    myFile.close()
    #del row - commented out

##***********Primary Code flow begins below
try:
    for theST in States:
        #set up output file
        #write out the state file        
        theHead = "RANDOM_PT_OBJECTID|DATASOURCE|ROADSED_ADDR_OBJECTID|"
        theHead = theHead + "CENSUSBLOCK_FIPS|FRN|PROVNAME|DBANAME|"
        theHead = theHead + "TRANSTECH|PROVIDER_TYPE|MAXADDOWN|MAXADUP|"
        theHead = theHead + "TYPICDOWN|TYPICUP|ENDUSERCAT|SBDD_ID"
        theTbl = theFGDB + thePrefix + theST
        #write output
        arcpy.AddMessage("the state is: " + theST)
        if arcpy.Exists(theTbl):
            outFile = theOF + theST + theSuffix
            myFile = open(outFile, 'w')
            myFile.write(theHead + "\n")
            myFile.close()
            myCnt = str(arcpy.GetCount_management(theTbl).getOutput(0))
            theStr = "     going to write out this many records for "
            theStr = theStr + theST + ": " + myCnt
            #arcpy.AddMessage(theStr)
            sbdd_exportFile(theTbl, outFile)
            del outFile, myFile, myCnt
        else:
            arcpy.AddMessage("   table does not exist")
        del theHead, theTbl
    del theST, States, theStr
    del theOF, theFGDB, thePrefix, theSuffix    
except:
    arcpy.AddMessage("Something bad happened")

