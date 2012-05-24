# ---------------------------------------------------------------------------
#   VERSION 1.2 (for ArcGIS 10)
# SBDD_CheckSubmission.py
# Created on: Thurs Jan 13 2011 
# Created by: Michael Byrne
# Federal Communications Commission
# ---------------------------------------------------------------------------
# Edited March 9, 2010 to work in ArcGIS 10.x
# edit on 6/28/11 for overview table changes

# Import system modules
import sys, string, os, arcpy
from arcpy import env
import time
from datetime import date
from os import remove, close
today = date.today()

#acquire arguments
theFD = sys.argv[1]  #theFeatureDataSet e.g. C:\Users\transfer\SBDD_Fall\DE\BB_Map_FGB_DE.gdb\NATL_Broadband_Map
theST = sys.argv[2]  #theState e.g. DE
theOF = sys.argv[3]  #theOutputFolder e.g. C:\Users\transfer\SBDD_Fall\DE

#set up variables
myFlag = 0

#Create Reciept
try:
    theYear = today.year
    theMonth = today.month
    theDay = today.day

    #set up output file
    outFile = theOF + "/" + theST + "_" + str(theYear) + "_" + str(theMonth) + "_" + str(theDay) + ".txt"
    myFile = open(outFile, 'w')
    myFile.write("" + "\n")
    myFile.write("* -----------------------------------------------------------------------------" + "\n")
    myFile.write("* Data Submission Receipt" + "\n")
    myFile.write("* CheckSBDDSubmission.py" + "\n")
    myFile.write("* Created on: " + str(theMonth) + "/" + str(theDay) + "/" + str(theYear) + "\n") #   
    myFile.write("* Created by: " + theST + "\n")  ###investigate getting who out of the metadata
    myFile.write("* State Broadband Data Development Program" + "\n")
    myFile.write("* NTIA / FCC" + "\n")
    myFile.write("* -----------------------------------------------------------------------------" + "\n")
    myFile.write("" + "\n")
    myFile.write("*******************************************************************************" + "\n")
    myFile.write("*****                                                                     *****" + "\n")
    myFile.write("*****                                                                     *****" + "\n")
    myFile.write("*****                         Submission Receipt File - version 1.2       *****" + "\n")
    myFile.write("*****                     Check below for any FAILED Statements           *****" + "\n")
    myFile.write("*****                                                                     *****" + "\n")
    myFile.write("*****                                                                     *****" + "\n")
    myFile.write("*******************************************************************************" + "\n")
    myFile.close()
    del theDay, theMonth, theYear
except:
    arcpy.AddMessage(arcpy.GetMessage(0))
    arcpy.AddMessage(arcpy.GetMessage(1))
    arcpy.AddMessage(arcpy.GetMessage(2))
    arcpy.AddMessage( "Something bad happened during the writing of the reciept; please re-run" )

#write out functions
#Function sbdd_qry creates a layer from a query and determines if the count is greater than 0
#essentially this function looks for unexpected values in a source layer field
def sbdd_qry (theFL, myFL, myQry):
    myFlag = 0
    myCnt = 0
    arcpy.AddMessage("     Checking for unexpected values: " + myFL)
    arcpy.MakeFeatureLayer_management(theFL, myFL, myQry)
    myCnt = int(arcpy.GetCount_management(myFL).getOutput(0))
    if myCnt > 0: #exception occurred
        myFile.write("      Field Check:     FAILED      " + myFL + " has UNEXPECTED VALUES \n")
        myFlag = 1
    else:
        myFile.write("      Field Check:     passed      " + myFL + " values are good \n")
    del myCnt, theFL, myFL, myQry
    return (myFlag) 

#Function sbdd_checkGeometry checks the geometry, and if there is a problem fixes it.
def sbdd_checkGeometry (thePre, myFL):
    #check to see if check geometry has been run, if has not, run it
    arcpy.AddMessage("     Checking geometry: " + myFL)
    geoCnt = int(arcpy.GetCount_management(theFD + thePre + myFL).getOutput(0))
    theFGDB = theFD.rstrip("NATL_Broadband_Map")
    if arcpy.Exists(theFGDB + myFL):
        arcpy.Delete_management(theFGDB + myFL)
    if not arcpy.Exists(theFGDB + myFL):
        arcpy.CheckGeometry_management(theFD + thePre + myFL, theFGDB + myFL)
    myCnt = int(arcpy.GetCount_management(theFGDB + myFL).getOutput(0))
    if myCnt > 0: #there is a geometry problem, we need to correct it
        arcpy.AddMessage("     FIXING geometry: " + myFL)
        arcpy.RepairGeometry_management(theFD + thePre + myFL)
        geoCnt = int(arcpy.GetCount_management(theFD + thePre + myFL).getOutput(0))
        myFile.write("      Geometry FAILED and fixed:  Layer now has " + str(geoCnt) + " records. \n")
    else:
        myFile.write("      Geometry PASSED:  Layer has " + str(geoCnt) + " records. \n")
    del myCnt, geoCnt, theFGDB
    return ()

# Process: Check for Speed Tiers
# a Speed tier is where a provider is listing more than 1 record for a technology in a given block
# like 'Mikes Net providing DSL at MaxAd Down/Up of 5/3 and 3/1 in Block 001       
def sbdd_SpeedTier(myFL):
    myFlag = 0
    theFGDB = theFD.rstrip("NATL_Broadband_Map")
    arcpy.AddMessage("     Checking for speed tiers: " + myFL)
    if arcpy.Exists(theFGDB + "/Speed_FRQ"):
        arcpy.Delete_management(theFGDB + "/Speed_FRQ")
    arcpy.Frequency_analysis(theFD + "/BB_Service_" + myFL, theFGDB + "/Speed_FRQ", "FRN; FULLFIPSID; TRANSTECH", "")
    theTblView = "myView" + myFL + "SpeedTier"
    arcpy.MakeTableView_management(theFGDB + "/Speed_FRQ", theTblView, "FREQUENCY > 1")
    if (int(arcpy.GetCount_management(theTblView).getOutput(0)) > 0) :  #Exception occurred
        myFile.write("      Speed Tier:      FAILED      Go check data and keep only Maximum Advertised Speeds \n")
        myFlag = 1
    else:
        myFile.write("      Speed Tier Record Check PASSED \n")
    if arcpy.Exists(theFGDB + "/Speed_FRQ"):
        arcpy.Delete_management(theFGDB + "/Speed_FRQ")
    del theFGDB, theTblView
    return (myFlag)

#sbdd_qryDef writes out the definitions for the queries, since these are used multiple times
def sbdd_qryDef (myField):
    if myField == "PROVNAME":
        theQry = "PROVNAME Is Null OR PROVNAME = '' OR PROVNAME = ' '"
    if myField == "DBANAME":
        theQry = "DBANAME Is Null OR DBANAME = '' OR DBANAME = ' '"
    if myField == "FRN":
        theQry = "FRN Is Null OR FRN = '' OR (CHAR_LENGTH(FRN) < 10 AND FRN <> '9999')"
    if myField == "OWNERSHIP":
        theQry ="OWNERSHIP < 0 OR OWNERSHIP > 1"
    if myField == "BHCAPACITY":
        theQry = "BHCAPACITY < 0 OR BHCAPACITY > 9"
    if myField == "BHTYPE":
        theQry = "BHTYPE < 0 OR BHTYPE > 4"
    if myField == "LATITUDE":
        theQry = "LATITUDE Is Null OR LATITUDE <= 0"
    if myField == "LONGITUDE":
        theQry = "LONGITUDE Is Null OR (LONGITUDE < -170 OR LONGITUDE > -60)"
    if myField == "ELEVFEET":  #not being checked in version 1.1
        theQry = "ELEVFEET Is Null OR ELEVFEET < 0"
    if myField == "STATEABBR":
        theQry = "STATEABBR Is Null or STATEABBR <> '" + theST + "'"
    if myField == "ANCHORNAME":
        theQry = "ANCHORNAME IS NULL OR ANCHORNAME = '' OR ANCHORNAME = ' '"
    if myField == "ADDRESS":
        theQry = "ADDRESS IS NULL OR ADDRESS = '' OR ADDRESS = ' '"
    if myField == "BLDGNBR":
        theQry = "BLDGNBR IS NULL OR BLDGNBR = '' OR BLDGNBR = ' '"
    if myField == "STREETNAME":
        theQry = "STREETNAME IS NULL OR STREETNAME = '' OR STREETNAME = ' '"
    if myField == "CITY":
        theQry = "CITY IS NULL OR CITY = '' OR CITY = ' ' OR CITY = 'CITY'"
    if myField == "STATECODE":
        theQry = "STATECODE IS NULL OR STATECODE <> '" + theST + "'"
    if myField == "ZIP5":
        theQry = "ZIP5 IS NULL OR ZIP5 = '' OR ZIP5 = ' ' OR ZIP5 = '0'"
    if myField == "CAICAT":
        theQry = "CAICAT IS NULL OR (CAICAT < '1' OR CAICAT > '7')"
    if myField == "ENDUSERCAT":
        theQry = "ENDUSERCAT < '1' OR ENDUSERCAT > '5'"
    if myField == "BBSERVICE":
        theQry = "BBSERVICE IS NULL OR BBSERVICE = '' OR BBSERVICE = ' ' OR (BBSERVICE <> 'N' AND BBSERVICE <> 'Y' AND BBSERVICE <> 'U')"
    if myField == "TRANSTECH":
        theQry = "TRANSTECH <> 0 AND TRANSTECH <> 10 AND TRANSTECH <> 20 AND TRANSTECH <> 30 "
        theQry = theQry + "AND TRANSTECH <> 40 AND TRANSTECH <> 41 AND TRANSTECH <> 50 AND TRANSTECH <> 60 AND "
        theQry = theQry + "TRANSTECH <> 70 AND TRANSTECH <> 71 AND TRANSTECH <> 80 AND TRANSTECH <> 90 AND TRANSTECH <> 0"
    if myField == "WiredTRANSTECH":
        theQry = "TRANSTECH IS NULL OR (TRANSTECH <> 0 AND TRANSTECH <> 10 AND TRANSTECH <> 20 AND TRANSTECH <> 30 "
        theQry = theQry + "AND TRANSTECH <> 40 AND TRANSTECH <> 41 AND TRANSTECH <> 50 AND TRANSTECH <> 90)"
    if myField == "WirelessTRANSTECH":
        theQry = "TRANSTECH IS NULL OR (TRANSTECH <> 60 AND TRANSTECH <> 70 AND TRANSTECH <> 71 AND TRANSTECH <> 80) "
    if myField == "MAXADDOWN":
        theQry = "MAXADDOWN < '0' OR MAXADDOWN > '9'"
    if myField == "MAXADUP":
        theQry = "MAXADUP < '0' OR MAXADUP > '9'"
    if myField == "FULLFIPSID":
        theQry = "FULLFIPSID IS NULL OR FULLFIPSID = '' OR FULLFIPSID = ' ' OR (CHAR_LENGTH(FULLFIPSID) <> 15)"
    if myField == "PROVIDER_TYPE":
        theQry = "PROVIDER_TYPE IS NULL OR (PROVIDER_TYPE <> 1 AND PROVIDER_TYPE <> 2 AND PROVIDER_TYPE <> 3 )"
    if myField == "STATEFIPS":
        theQry = "STATEFIPS IS NULL OR STATEFIPS = '' OR STATEFIPS = ' ' OR STATEFIPS <> '" + stFIPS + "'"
    if myField == "COUNTYFIPS":
        theQry = "COUNTYFIPS IS NULL OR COUNTYFIPS = '' OR COUNTYFIPS = ' ' OR (CHAR_LENGTH(COUNTYFIPS) <> 3)"
    if myField == "TRACT":
        theQry = "TRACT IS NULL OR TRACT = '' OR TRACT = ' ' OR (CHAR_LENGTH(TRACT) <> 6)"
    if myField == "BLOCKID":
        theQry = "BLOCKID IS NULL OR BLOCKID = '' OR BLOCKID = ' ' OR (CHAR_LENGTH(BLOCKID) <> 4)"
    if myField == "BLOCKSUBGROUP": # Not being checked in version 1.1
        theQry = "BLOCKSUBGROUP = '' OR BLOCKSUBGROUP = ' ' OR (CHAR_LENGTH(BLOCKSUBGROUP) <> 1)"
    if myField == "TYPICDOWN":   # Not being checked in version 1.1
        theQry = "TYPICDOWN < 0 OR TYPICDOWN > 11"         
    if myField == "TYPICUP":     # Not being checked in version 1.1
        theQry = "TYPICUP < 0 OR TYPICUP > 11"
    if myField == "GEOUNITTYPE":
        theQry = "GEOUNITTYPE IS NULL OR (GEOUNITTYPE <> 'CO')"
    if myField == "STATECOUNTYFIPS":
        theQry = "STATECOUNTYFIPS IS NULL OR (STATECOUNTYFIPS NOT LIKE '" + stFIPS + "%') OR (CHAR_LENGTH(STATECOUNTYFIPS) <> 5)"
    if myField == "ADDMIN":  # Not being checked in version 1.1
        theQry = "(ADDMIN = '' OR ADDMIN = ' ')"
    if myField == "ADDMAX":  # Not being checked in version 1.1
        theQry = "(ADDMAX = '' OR ADDMAX = ' ')"
    if myField == "STATE":
        theQry = "STATE IS NULL OR (STATE <> '" + theST + "')"
    if myField == "SPECTRUM":
        theQry = "SPECTRUM IS NULL OR (SPECTRUM < 1 OR SPECTRUM > 10)"
    if myField == "SPEEDCHECK":  # Not being checked in version 1.1 
        theQry = "MaxAdDown <= TypicDown OR MaxAdUp <= TypicUp"
    if myField == "SpeedNotBB": #speed needs to meet the definition of broadband
        theQry = "MAXADDOWN = '1' OR MAXADDOWN = '2' OR MAXADUP = '1'"
    if myField == "OneSpeedAndNotTheOther":  #speed needs to be consistently populated
        theQry = "(MAXADDOWN IS NOT NULL  AND MAXADUP = '') OR (MAXADDOWN = ''  AND MAXADUP IS NOT NULL)"
    return(theQry)

#set the stFIPS
stFIPS = "0"
if theST == "AK":
    stFIPS = '02'
if theST == "AL":
    stFIPS = '01'
if theST == "AR":
    stFIPS = '05'
if theST == "AS":
    stFIPS = '60'
if theST == "AZ":
    stFIPS = '04'
if theST == "CA":
    stFIPS = '06'
if theST == "CO":
    stFIPS = '08'
if theST == "CT":
    stFIPS = '09'
if theST == "DC":
    stFIPS = '11'
if theST == "DE":
    stFIPS = '10'
if theST == "FL":
    stFIPS = '12'
if theST == "GA":
    stFIPS = '13'
if theST == "GU":
    stFIPS = '66'
if theST == "HI":
    stFIPS = '15'
if theST == "IA":
    stFIPS = '19'
if theST == "ID":
    stFIPS = '16'
if theST == "IL":
    stFIPS = '17'
if theST == "IN":
    stFIPS = '18'
if theST == "KS":
    stFIPS = '20'
if theST == "KY":
    stFIPS = '21'
if theST == "LA":
    stFIPS = '22'
if theST == "MA":
    stFIPS = '25'
if theST == "MD":
    stFIPS = '24'
if theST == "ME":
    stFIPS = '23'
if theST == "MP":
    stFIPS = '69'
if theST == "MI":
    stFIPS = '26'
if theST == "MN":
    stFIPS = '27'
if theST == "MO":
    stFIPS = '29'
if theST == "MS":
    stFIPS = '28'
if theST == "MT":
    stFIPS = '30'
if theST == "NC":
    stFIPS = '37'
if theST == "ND":
    stFIPS = '38'
if theST == "NE":
    stFIPS = '31'
if theST == "NH":
    stFIPS = '33'
if theST == "NJ":
    stFIPS = '34'
if theST == "NM":
    stFIPS = '35'
if theST == "NV":
    stFIPS = '32'
if theST == "NY":
    stFIPS = '36'
if theST == "OH":
    stFIPS = '39'
if theST == "OK":
    stFIPS = '40'
if theST == "OR":
    stFIPS = '41'
if theST == "PA":
    stFIPS = '42'
if theST == "PR":
    stFIPS = '72'
if theST == "RI":
    stFIPS = '44'
if theST == "SC":
    stFIPS = '45'
if theST == "SD":
    stFIPS = '46'
if theST == "TN":
    stFIPS = '47'
if theST == "TX":
    stFIPS = '48'
if theST == "UT":
    stFIPS = '49'
if theST == "VA":
    stFIPS = '51'
if theST == "VI":
    stFIPS = '78'
if theST == "VT":
    stFIPS = '50'
if theST == "WA":
    stFIPS = '53'
if theST == "WI":
    stFIPS = '55'
if theST == "WV":
    stFIPS = '54'
if theST == "WY":
    stFIPS = '56'
if stFIPS == "0":
    arcpy.addmessage("You likely did not enter a valid two letter state abbreviation, please run again")

#check for BB_ConnectionPoint_LastMile
theLyr = "LastMile"
arcpy.AddMessage("Begining checks on Feature Class: " + theLyr)
myFile = open(outFile, 'a')
myFile.write("" + "\n")
myFile.write("*Check Layer: " + theLyr + "\n")            
sbdd_checkGeometry("/BB_ConnectionPoint_", theLyr)
myFlag = myFlag + sbdd_qry (theFD + "/BB_ConnectionPoint_" + theLyr, theLyr + "_PROVNAME", sbdd_qryDef("PROVNAME")) 
myFlag = myFlag + sbdd_qry (theFD + "/BB_ConnectionPoint_" + theLyr, theLyr + "_DBANAME", sbdd_qryDef("DBANAME")) 
sbdd_qry (theFD + "/BB_ConnectionPoint_" + theLyr, theLyr + "_FRN", sbdd_qryDef("FRN"))
myFlag = myFlag + sbdd_qry (theFD + "/BB_ConnectionPoint_" + theLyr, theLyr + "_OWNERSHIP", sbdd_qryDef("OWNERSHIP")) 
myFlag = myFlag + sbdd_qry (theFD + "/BB_ConnectionPoint_" + theLyr, theLyr + "_BHCAPACITY", sbdd_qryDef("BHCAPACITY"))
myFlag = myFlag + sbdd_qry (theFD + "/BB_ConnectionPoint_" + theLyr, theLyr + "_BHTYPE", sbdd_qryDef("BHTYPE"))
myFlag = myFlag + sbdd_qry (theFD + "/BB_ConnectionPoint_" + theLyr, theLyr + "_LATITUDE", sbdd_qryDef("LATITUDE"))
myFlag = myFlag + sbdd_qry (theFD + "/BB_ConnectionPoint_" + theLyr, theLyr + "_LONGITUDE", sbdd_qryDef("LONGITUDE"))
myFlag = myFlag + sbdd_qry (theFD + "/BB_ConnectionPoint_" + theLyr, theLyr + "_STATEABBR", sbdd_qryDef("STATEABBR"))
myFlag = myFlag + sbdd_qry (theFD + "/BB_ConnectionPoint_" + theLyr, theLyr + "_FULLFIPSID", sbdd_qryDef("FULLFIPSID"))
myFile.close()
                 
#check on BB_ConnectionPoint_MiddleMile
theLyr = "MiddleMile"
arcpy.AddMessage("Begining checks on Feature Class: " + theLyr)
myFile = open(outFile, 'a')
myFile.write("" + "\n")
myFile.write("*Check Layer: " + theLyr + "\n")            
sbdd_checkGeometry("/BB_ConnectionPoint_", theLyr)
myFlag = myFlag + sbdd_qry (theFD + "/BB_ConnectionPoint_" + theLyr, theLyr + "_PROVNAME", sbdd_qryDef("PROVNAME")) 
myFlag = myFlag + sbdd_qry (theFD + "/BB_ConnectionPoint_" + theLyr, theLyr + "_DBANAME", sbdd_qryDef("DBANAME")) 
sbdd_qry (theFD + "/BB_ConnectionPoint_" + theLyr, theLyr + "_FRN", sbdd_qryDef("FRN"))
myFlag = myFlag + sbdd_qry (theFD + "/BB_ConnectionPoint_" + theLyr, theLyr + "_OWNERSHIP", sbdd_qryDef("OWNERSHIP")) 
myFlag = myFlag + sbdd_qry (theFD + "/BB_ConnectionPoint_" + theLyr, theLyr + "_BHCAPACITY", sbdd_qryDef("BHCAPACITY"))
myFlag = myFlag + sbdd_qry (theFD + "/BB_ConnectionPoint_" + theLyr, theLyr + "_BHTYPE", sbdd_qryDef("BHTYPE"))
myFlag = myFlag + sbdd_qry (theFD + "/BB_ConnectionPoint_" + theLyr, theLyr + "_LATITUDE", sbdd_qryDef("LATITUDE"))
myFlag = myFlag + sbdd_qry (theFD + "/BB_ConnectionPoint_" + theLyr, theLyr + "_LONGITUDE", sbdd_qryDef("LONGITUDE"))
myFlag = myFlag + sbdd_qry (theFD + "/BB_ConnectionPoint_" + theLyr, theLyr + "_STATEABBR", sbdd_qryDef("STATEABBR"))
myFlag = myFlag + sbdd_qry (theFD + "/BB_ConnectionPoint_" + theLyr, theLyr + "_FULLFIPSID", sbdd_qryDef("FULLFIPSID"))
myFile.close()

#check for BB_Service_Address
theLyr = "Address"
arcpy.AddMessage("Begining checks on Feature Class: " + theLyr)
myFile = open(outFile, 'a')
myFile.write("" + "\n")
myFile.write("*Check Layer: " + theLyr + "\n")            
sbdd_checkGeometry("/BB_Service_", theLyr)
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_PROVNAME", sbdd_qryDef("PROVNAME")) 
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_DBANAME", sbdd_qryDef("DBANAME"))
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_PROVIDER_TYPE", sbdd_qryDef("PROVIDER_TYPE"))
sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_FRN", sbdd_qryDef("FRN"))
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_ADDRESS", sbdd_qryDef("ADDRESS"))
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_BLDGNBR", sbdd_qryDef("BLDGNBR"))
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_STREETNAME", sbdd_qryDef("STREETNAME"))
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_CITY", sbdd_qryDef("CITY")) 
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_STATECODE", sbdd_qryDef("STATECODE"))
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_ZIP5", sbdd_qryDef("ZIP5"))
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_LATITUDE", sbdd_qryDef("LATITUDE"))
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_LONGITUDE", sbdd_qryDef("LONGITUDE"))
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_ENDUSERCAT", sbdd_qryDef("ENDUSERCAT"))
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_TRANSTECH", sbdd_qryDef("WiredTRANSTECH"))
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_MAXADDOWN", sbdd_qryDef("MAXADDOWN")) 
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_MAXADUP", sbdd_qryDef("MAXADUP"))
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_SpeedNotBB", sbdd_qryDef("SpeedNotBB")) 
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_OneSpeedAndNotTheOther", sbdd_qryDef("OneSpeedAndNotTheOther"))
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_FULLFIPSID", sbdd_qryDef("FULLFIPSID"))
myFile.close()

#check for BB_Service_CAInstitutions
theLyr = "CAInstitutions"
arcpy.AddMessage("Begining checks on Feature Class: " + theLyr)
myFile = open(outFile, 'a')
myFile.write("" + "\n")
myFile.write("*Check Layer: " + theLyr + "\n")            
sbdd_checkGeometry("/BB_Service_", theLyr)
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_ANCHORNAME", sbdd_qryDef("ANCHORNAME")) 
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_ADDRESS", sbdd_qryDef("ADDRESS"))
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_BLDGNBR", sbdd_qryDef("BLDGNBR")) 
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_STREETNAME", sbdd_qryDef("STREETNAME")) 
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_CITY", sbdd_qryDef("CITY")) 
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_STATECODE", sbdd_qryDef("STATECODE"))
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_ZIP5", sbdd_qryDef("ZIP5")) 
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_CAICAT", sbdd_qryDef("CAICAT")) 
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_BBSERVICE", sbdd_qryDef("BBSERVICE")) 
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_TRANSTECH", sbdd_qryDef("TRANSTECH")) 
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_MAXADDOWN", sbdd_qryDef("MAXADDOWN")) 
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_MAXADUP", sbdd_qryDef("MAXADUP"))
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_SpeedNotBB", sbdd_qryDef("SpeedNotBB")) 
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_OneSpeedAndNotTheOther", sbdd_qryDef("OneSpeedAndNotTheOther"))
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_FULLFIPSID", sbdd_qryDef("FULLFIPSID"))
myFile.close()

#check for BB_Service_CensusBlock
theLyr = "CensusBlock"
arcpy.AddMessage("Begining checks on Feature Class: " + theLyr)
myFile = open(outFile, 'a')
myFile.write("" + "\n")
myFile.write("*Check Layer: " + theLyr + "\n")            
sbdd_checkGeometry("/BB_Service_", theLyr)
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_PROVNAME", sbdd_qryDef("PROVNAME")) 
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_DBANAME", sbdd_qryDef("DBANAME")) 
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_PROVIDER_TYPE", sbdd_qryDef("PROVIDER_TYPE"))
sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_FRN", sbdd_qryDef("FRN"))
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_STATEFIPS", sbdd_qryDef("STATEFIPS")) 
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_COUNTYFIPS", sbdd_qryDef("COUNTYFIPS"))
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_TRACT", sbdd_qryDef("TRACT")) 
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_BLOCKID", sbdd_qryDef("BLOCKID")) 
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_FULLFIPSID", sbdd_qryDef("FULLFIPSID"))
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_TRANSTECH", sbdd_qryDef("WiredTRANSTECH"))
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_MAXADDOWN", sbdd_qryDef("MAXADDOWN")) 
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_MAXADUP", sbdd_qryDef("MAXADUP"))
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_SpeedNotBB", sbdd_qryDef("SpeedNotBB")) 
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_OneSpeedAndNotTheOther", sbdd_qryDef("OneSpeedAndNotTheOther"))
myFlag = sbdd_SpeedTier(theLyr)
myFile.close()

#check for BB_Service_Overview
theLyr = "Overview"
arcpy.AddMessage("Begining checks on Feature Class: " + theLyr)
myFile = open(outFile, 'a')
myFile.write("" + "\n")
myFile.write("*Check Layer: " + theLyr + "\n")            
sbdd_checkGeometry("/BB_Service_", theLyr)
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_PROVNAME", sbdd_qryDef("PROVNAME")) 
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_DBANAME", sbdd_qryDef("DBANAME")) 
sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_FRN", sbdd_qryDef("FRN"))
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_GEOUNITTYPE", sbdd_qryDef("GEOUNITTYPE")) 
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_STATECOUNTYFIPS", sbdd_qryDef("STATECOUNTYFIPS"))
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_TRANSTECH", sbdd_qryDef("WiredTRANSTECH")) 
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_STATEABBR", sbdd_qryDef("STATEABBR"))
myFile.close()
    
#check for BB_Service_RoadSegement
theLyr = "RoadSegment"
arcpy.AddMessage("Begining checks on Feature Class: " + theLyr)
myFile = open(outFile, 'a')
myFile.write("" + "\n")
myFile.write("*Check Layer: " + theLyr + "\n")            
sbdd_checkGeometry("/BB_Service_", theLyr)
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_PROVNAME", sbdd_qryDef("PROVNAME")) 
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_DBANAME", sbdd_qryDef("DBANAME")) 
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_PROVIDER_TYPE", sbdd_qryDef("PROVIDER_TYPE"))
sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_FRN", sbdd_qryDef("FRN"))  
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_STATE", sbdd_qryDef("STATE"))
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_TRANSTECH", sbdd_qryDef("WiredTRANSTECH")) 
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_MAXADDOWN", sbdd_qryDef("MAXADDOWN")) 
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_MAXADUP", sbdd_qryDef("MAXADUP"))
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_SpeedNotBB", sbdd_qryDef("SpeedNotBB")) 
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_OneSpeedAndNotTheOther", sbdd_qryDef("OneSpeedAndNotTheOther"))
myFile.close()

#check for BB_Service_Wireless
theLyr = "Wireless"
arcpy.AddMessage("Begining checks on Feature Class: " + theLyr)
myFile = open(outFile, 'a')
myFile.write("" + "\n")
myFile.write("*Check Layer: " + theLyr + "\n")            
sbdd_checkGeometry("/BB_Service_", theLyr)
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_PROVNAME", sbdd_qryDef("PROVNAME")) 
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_DBANAME", sbdd_qryDef("DBANAME")) 
sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_FRN", sbdd_qryDef("FRN"))
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_TRANSTECH", sbdd_qryDef("WirelessTRANSTECH")) 
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_MAXADDOWN", sbdd_qryDef("MAXADDOWN")) 
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_MAXADUP", sbdd_qryDef("MAXADUP"))
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_SpeedNotBB", sbdd_qryDef("SpeedNotBB")) 
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_OneSpeedAndNotTheOther", sbdd_qryDef("OneSpeedAndNotTheOther"))
myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theLyr + "_STATEABBR", sbdd_qryDef("STATEABBR"))
myFile.close()

# Process: Check for duplicate Records
#version 10 has an "Find Identical", which seems to work; i haven't employed the code
#because we are not on 10 yet, and am not sure who else isn't

# Process: Check for topology rules being followed
#have not implemented this part of the code yet

# Process: Check for wireless rasterization
#have not implemented this part of the code yet;
#the issues is if vectorization of raster datasets in the wireless
#shape has occurred, there are sometimes relics of single raster cells
#which cause significant issues in post processing the data

       
if myFlag > 0:
    arcpy.AddMessage("*********************************************")
    arcpy.AddMessage("*********************WARNING*****************")
    arcpy.AddMessage("It appears you have some data inegrity issues")
    arcpy.AddMessage("1) Check the reciept file for a complete list")
    arcpy.AddMessage("2) take appropriate corrective action")
    arcpy.AddMessage("3) and rerun the Check_Submission process")
    arcpy.AddMessage("*********************WARNING*****************")    
    arcpy.AddMessage("*********************************************")
if myFlag == 0:
    arcpy.AddMessage("*****************************************************")
    arcpy.AddMessage("*********************CONGRATULATIONS*****************")
    arcpy.AddMessage("      It appears you have NO data inegrity issues")
    arcpy.AddMessage("        this file is ready to submit to the FCC")
    arcpy.AddMessage("*********************CONGRATULATIONS*****************")    
    arcpy.AddMessage("*****************************************************")
del myFile, outFile, myFlag

  
