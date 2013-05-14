### ---------------------------------------------------------------------------
###   VERSION 1.1 (for ArcGIS 10)
### SBDD_CheckSubmission.py
### Created on: Thurs Jan 13 2011 
### Created by: Michael Byrne
### Federal Communications Commission 
### ---------------------------------------------------------------------------
### Edited March 9, 2010 to work in ArcGIS 10.x
### Edited December 5, 2011 to conform to new business rules defined by NTIA
### Edited February 7 to do the following
###           - remove duplicate WireLessTranstech call
###           - allow for nulls in road segment fields (addmin, addmax, streetname
###             city and ZIP5
###           - add wirelss search flag  Flag_TT70_MAD11
###           
### ---------------------------------------------------------------------------
### Edited July 7, 2012 for NTIA/Awardee proposed changes
### includes the folowing changes
###Request	    |   Recommendation
###- Make Script work with an ArcEdit License, rather than an ArcInfo License   |
###         Replace the use of the Frequency Tool, with the use of the
###         Statistics Tool	
###- Change the scrip to not fail when a single provider offers service to a
###         block at different speeds for different end user categories	    |
###         Change the SpeedTier Business rule to include the EndUserCat as
###         a summary field to get unique values for this field as well.
###         The result will be that a different speed tier is allowed by the
###         same provider in a single block if it is a different end user category
###- Change script to fix exception w/ Middle Mile Elevation	|   Remove the 
###         ElevFeet check from the script
###- Change script to fix exception w/ Middle Mile Ownership	|   Remove the
###         ownership check from Middle Mile
###- Change the scrip to not fail when a single provider offers service to a
###         address at different speeds for different end user categories   |
###         Remove the SpeedTier check from the address table
###- Allow wireless technologies in CAI data	|   Add a query category for
###         CAI transtech to include All available options
###- Fix allowable nulls in road segment data	|   Ensure only NBM data fields
###         are checked for integrity issues
###- Change MaxAdUp and MaxAdDown in CAI data to include acceptance of Nulls
###         and default values (e.g. ZZ)	|   Remove the MaxAdDown and MaxAdUp
###         checks from CAI
###- Allow people to run on all or just a single layer to see what the check
###         status is   | added a new argument to let users choose the all
###         or an individual layer to run the code on
###
### ---------------------------------------------------------------------------

# Import system modules
import sys, string, os, arcpy
from arcpy import env
import time
from datetime import date
from os import remove, close
today = date.today()

#acquire arguments
theLocation = "C:/Users/michael.byrne/NBM/Spring2013/Data/"
theYear = "2013"
theMonth = "04"
theDay = "01"

States = ["AK","AL","AR","AS","AZ","CA","CO","CT"]          #1
States = States + ["DC","DE","FL","GA","GU","HI","IA","ID"] #2
States = States + ["IL","IN","KS","KY","LA","MA","MD","ME"] #3 
States = States + ["MI","MN","MO","MP","MS","MT","NC","ND"] #4 
States = States + ["NE","NH","NJ","NM","NV","NY","OH","OK"] #5
States = States + ["OR","PA","PR","RI","SC","SD","TN","TX"] #6
States = States + ["UT","VA","VI","VT","WA","WI","WV","WY"] #7
States = ["AS","VI"]

#set up variables
myFlag = 0

#write out functions
#Function sbdd_qry creates a layer from a query and determines if the 
#count is greater than 0; essentially this function looks for unexpected
#values in a source layer field
def sbdd_qry (theFL, myFL, myQry, mySeverity):
    if mySeverity == "Fail":
        myMsg = "    FAILED      " + myFL + " YOU MUST FIX THESE"
    if mySeverity == "Warn":
        myMsg = "    WARNING     " + myFL + " YOU MUST EXPLAIN THESE " 
    myFlag = 0
    myCnt = 0
    arcpy.AddMessage("     Checking for unexpected values: " + myFL)
    arcpy.MakeFeatureLayer_management(theFL, myFL, myQry)
    myCnt = int(arcpy.GetCount_management(myFL).getOutput(0))
    arcpy.Delete_management(myFL)
    if myCnt > 0: #exception occurred
        myFile.write("      Field Check: " + myMsg + " UNEXPECTED VALUES \n")
        myFlag = 1
    else:
        myFile.write("      Field Check:     passed      " + myFL + \
                     " values are good \n")
    del myCnt, theFL, myFL, myQry
    return (myFlag) 

#Function sbdd_checkGeometry checks the geometry,
#and if there is a problem fixes it.
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
        myMsg = "      Geometry FAILED and fixed:  Layer now has " + \
                     str(geoCnt) + " records. \n"
        myFile.write(myMsg)
    else:
        myMsg = "      Geometry PASSED:  Layer has " + str(geoCnt) + " records. \n"
        myFile.write(myMsg)
    del myMsg, myCnt, geoCnt, theFGDB
    return ()

# Process: Check for Speed Tiers
# a Speed tier is where a provider is listing more than 1 record for a
#technology in a given block; like 'Mikes Net providing DSL at MaxAd Down/Up
#of 5/3 and 3/1 in Block 001       
def sbdd_SpeedTier(myFL):
    theFGDB = theFD.rstrip("NATL_Broadband_Map")
    arcpy.AddMessage("     Checking for speed tiers: " + myFL)
    if arcpy.Exists(theFGDB + "/Speed_FRQ"):
        arcpy.Delete_management(theFGDB + "/Speed_FRQ")
    arcpy.Statistics_analysis(theFD + "/BB_Service_" + myFL, theFGDB + \
                              "/Speed_FRQ", [["FRN", "COUNT"]], ["FRN", "FULLFIPSID", "TRANSTECH","EndUserCat"]) 
    theTblView = "myView" + theST + myFL + "SpeedTier"
    arcpy.MakeTableView_management(theFGDB + "/Speed_FRQ", theTblView,
                                   "FREQUENCY > 1")
    if (int(arcpy.GetCount_management(theTblView).getOutput(0)) > 0):
        myMsg = "      Speed Tier:      FAILED      Go check data "
        myMsg = myMsg + "and keep only Maximum Advertised Speeds \n"
        myFile.write(myMsg)
        myFlag = 1
    else:
        myMsg = "      Speed Tier Record Check PASSED \n"
        myFile.write(myMsg)
        myFlag = 0
    arcpy.Delete_management(theTblView)
    if arcpy.Exists(theFGDB + "/Speed_FRQ"):
        arcpy.Delete_management(theFGDB + "/Speed_FRQ")
    del theFGDB, theTblView, myMsg
    return (myFlag)

#sbdd_qryDef writes out the definitions for the queries,
#since these are used multiple times
def sbdd_qryDef (myField):
    if myField == "CAITRANSTECH":
        theQry = "TRANSTECH IS NULL OR (TRANSTECH <> 10 AND TRANSTECH <> 20 AND "
        theQry = theQry + "TRANSTECH <> 30 AND TRANSTECH <> 40 AND TRANSTECH "
        theQry = theQry + "<> 41 AND TRANSTECH <> 50 AND TRANSTECH <> 90 AND "
        theQry = theQry + "TRANSTECH <> 70 AND TRANSTECH <> 71 AND "
        theQry = theQry + "TRANSTECH <> 80 AND TRANSTECH <> 60 AND TRANSTECH <> -9999)"        
    if myField == "WiredTRANSTECH":
        theQry = "TRANSTECH IS NULL OR (TRANSTECH <> 10 AND TRANSTECH <> 20 AND "
        theQry = theQry + "TRANSTECH <> 30 AND TRANSTECH <> 40 AND TRANSTECH "
        theQry = theQry + "<> 41 AND TRANSTECH <> 50 AND TRANSTECH <> 90)"
    if myField == "WireLessTRANSTECH":
        theQry = "TRANSTECH IS NULL OR (TRANSTECH <> 70 AND TRANSTECH <> 71 AND "
        theQry = theQry + "TRANSTECH <> 80 AND TRANSTECH <> 60)"
    if myField == "MaxAdDown":
        theQry = "MAXADDOWN IS NULL OR (MAXADDOWN <> '3' AND MAXADDOWN <> '4' AND "
        theQry = theQry + "MAXADDOWN <> '5' AND MAXADDOWN <> '6' AND MAXADDOWN <> "
        theQry = theQry + "'7' AND MAXADDOWN <> '8' AND MAXADDOWN <> '9' "
        theQry = theQry + "AND MAXADDOWN <> '10' AND MAXADDOWN <> '11' )"
    if myField == "MaxAdUp":
        theQry = "MAXADUP IS NULL OR (MAXADUP <> '2' AND MAXADUP <> '3' AND "
        theQry = theQry + "MAXADUP <> '4' AND MAXADUP <> '5' AND MAXADUP <> '6' "
        theQry = theQry + "AND MAXADUP <> '7' AND MAXADUP <> '8' AND MAXADUP "
        theQry = theQry + " <> '9' AND MAXADUP <> '10' AND MAXADUP <> '11' )"
    if myField == "Flag_TT10_MAD7":
        theQry = "TRANSTECH = 10 AND MAXADDOWN = '7'"
    if myField == "Flag_TT10_MAD8":
        theQry = "TRANSTECH = 10 AND MAXADDOWN = '8'"
    if myField == "Flag_TT10_MAD9":
        theQry = "TRANSTECH = 10 AND MAXADDOWN = '9'"
    if myField == "Flag_TT10_MAD10":
        theQry = "TRANSTECH = 10 AND MAXADDOWN = '10'"
    if myField == "Flag_TT10_MAD11":
        theQry = "TRANSTECH = 10 AND MAXADDOWN = '11'"
    if myField == "Flag_TT40_MAD3":
        theQry = "TRANSTECH = 40 AND MAXADDOWN = '3'"
    if myField == "Flag_TT40_MAD4":
        theQry = "TRANSTECH = 40 AND MAXADDOWN = '4'"
    if myField == "Flag_TT40_MAD5":
        theQry = "TRANSTECH = 40 AND MAXADDOWN = '5'"
    if myField == "Flag_TT40_MAD6":
        theQry = "TRANSTECH = 40 AND MAXADDOWN = '6'"
    if myField == "Flag_TT40_MAD7":
        theQry = "TRANSTECH = 40 AND MAXADDOWN = '7'"
    if myField == "Flag_TT40_MAD8":
        theQry = "TRANSTECH = 40 AND MAXADDOWN = '8'"
    if myField == "Flag_TT41_MAD8":
        theQry = "TRANSTECH = 41 AND MAXADDOWN = '8'"
    if myField == "Flag_TT41_MAD9":
        theQry = "TRANSTECH = 41 AND MAXADDOWN = '9'"
    if myField == "Flag_TT41_MAD10":
        theQry = "TRANSTECH = 41 AND MAXADDOWN = '10'"
    if myField == "Flag_TT70_MAD7":
        theQry = "TRANSTECH = 70 AND MAXADDOWN = '7'"
    if myField == "Flag_TT70_MAD8":
        theQry = "TRANSTECH = 70 AND MAXADDOWN = '8'"
    if myField == "Flag_TT70_MAD9":
        theQry = "TRANSTECH = 70 AND MAXADDOWN = '9'"
    if myField == "Flag_TT70_MAD10":
        theQry = "TRANSTECH = 70 AND MAXADDOWN = '10'"
    if myField == "Flag_TT70_MAD11":
        theQry = "TRANSTECH = 70 AND MAXADDOWN = '11'"
    if myField == "Flag_TT70_MAU7":
        theQry = "TRANSTECH = 70 AND MAXADUP = '7'"
    if myField == "Flag_TT70_MAU8":
        theQry = "TRANSTECH = 70 AND MAXADUP = '8'"
    if myField == "Flag_TT70_MAU9":
        theQry = "TRANSTECH = 70 AND MAXADUP = '9'"
    if myField == "Flag_TT70_MAU10":
        theQry = "TRANSTECH = 70 AND MAXADUP = '10'"
    if myField == "Flag_TT70_MAU11":
        theQry = "TRANSTECH = 70 AND MAXADUP = '11'"
    if myField == "Flag_TT71_MAD7":
        theQry = "TRANSTECH = 71 AND MAXADDOWN = '7'"
    if myField == "Flag_TT71_MAD8":
        theQry = "TRANSTECH = 71 AND MAXADDOWN = '8'"
    if myField == "Flag_TT71_MAD9":
        theQry = "TRANSTECH = 71 AND MAXADDOWN = '9'"
    if myField == "Flag_TT71_MAD10":
        theQry = "TRANSTECH = 71 AND MAXADDOWN = '10'"
    if myField == "Flag_TT71_MAD11":
        theQry = "TRANSTECH = 71 AND MAXADDOWN = '11'"
    if myField == "Flag_TT80_MAD7":
        theQry = "TRANSTECH = 80 AND MAXADDOWN = '7'"        
    if myField == "PROVNAME":
        theQry = "PROVNAME Is Null OR PROVNAME = '' OR PROVNAME = ' '"
    if myField == "DBANAME":
        theQry = "DBANAME Is Null OR DBANAME = '' OR DBANAME = ' '"
    if myField == "FRN":
        theQry = "FRN Is Null OR FRN = '' OR (CHAR_LENGTH(FRN) < 10 AND FRN <> '9999')"
    if myField == "OWNERSHIP":
        theQry ="OWNERSHIP Is Null OR (OWNERSHIP < 0 OR OWNERSHIP > 1)"
    if myField == "BHCAPACITY":
        theQry = "BHCAPACITY < 0 OR BHCAPACITY > 9"
    if myField == "BHTYPE":
        theQry = "BHTYPE < 0 OR BHTYPE > 4"
    if myField == "LATITUDE":
        theQry = "LATITUDE Is Null OR LATITUDE < 0"
    if myField == "LONGITUDE":
        theQry = "LONGITUDE Is Null OR (LONGITUDE > -170 OR LONGITUDE < -60"
    if myField == "ELEVFEET":
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
        theQry = "CAICAT IS NULL OR (CAICAT < 1 OR CAICAT > 7)"
    if myField == "ENDUSERCAT":
        theQry = "ENDUSERCAT IS NULL OR (ENDUSERCAT < 1 OR ENDUSERCAT > 5)"
    if myField == "BBSERVICE":
        theQry = "BBSERVICE IS NULL OR BBSERVICE = '' OR BBSERVICE = ' ' OR "
        theQry = theQry + " (BBSERVICE <> 'N' AND BBSERVICE <> 'Y' AND "
        theQry = theQry + " BBSERVICE <> 'U')"
    if myField == "FULLFIPSID":
        theQry = "FULLFIPSID IS NULL OR FULLFIPSID = '' OR FULLFIPSID = ' ' "
        theQry = theQry + " OR (CHAR_LENGTH(FULLFIPSID) <> 15)"
    if myField == "PROVIDER_TYPE":
        theQry = "PROVIDER_TYPE IS NULL OR (PROVIDER_TYPE <> 1 AND "
        theQry = theQry + "PROVIDER_TYPE <> 2 AND PROVIDER_TYPE <> 3 )"
    if myField == "STATEFIPS":
        theQry = "STATEFIPS IS NULL OR STATEFIPS = '' OR STATEFIPS = ' ' "
        theQry = theQry + "OR STATEFIPS <> '" + stFIPS + "'"
    if myField == "COUNTYFIPS":
        theQry = "COUNTYFIPS IS NULL OR COUNTYFIPS = '' OR COUNTYFIPS = ' ' "
        theQry = theQry + " OR (CHAR_LENGTH(COUNTYFIPS) <> 3)"
    if myField == "TRACT":
        theQry = "TRACT IS NULL OR TRACT = '' OR TRACT = ' ' OR "
        theQry = theQry + "(CHAR_LENGTH(TRACT) <> 6)"
    if myField == "BLOCKID":
        theQry = "BLOCKID IS NULL OR BLOCKID = '' OR BLOCKID = ' ' OR "
        theQry = theQry + " (CHAR_LENGTH(BLOCKID) <> 4)"
    if myField == "BLOCKSUBGROUP":
        theQry = "BLOCKSUBGROUP = '' OR BLOCKSUBGROUP = ' ' OR "
        theQry = theQry + " (CHAR_LENGTH(BLOCKSUBGROUP) <> 1)"
    if myField == "GEOUNITTYPE":
        theQry = "GEOUNITTYPE IS NULL OR (GEOUNITTYPE <> 'CO')"
    if myField == "STATECOUNTYFIPS":
        theQry = "STATECOUNTYFIPS IS NULL OR (STATECOUNTYFIPS NOT LIKE '" 
        theQry = theQry + stFIPS + "%') OR (CHAR_LENGTH(STATECOUNTYFIPS) <> 5)"
    if myField == "ADDMIN":
        theQry = "(ADDMIN = '' OR ADDMIN = ' ')"
    if myField == "ADDMAX":
        theQry = "(ADDMAX = '' OR ADDMAX = ' ')"
    if myField == "STATE":
        theQry = "STATE IS NULL OR (STATE <> '" + theST + "')"
    if myField == "SPECTRUM":
        theQry = "SPECTRUM IS NULL OR (SPECTRUM < 1 OR SPECTRUM > 10)"
    if myField == "OneSpeedAndNotTheOther":  #speed needs to be consistently populated
        theQry = "(MAXADDOWN IS NOT NULL  AND MAXADUP = '') OR "
        theQry = theQry + " (MAXADDOWN = ''  AND MAXADUP IS NOT NULL)"
    return(theQry)

#sbdd_qryDef writes out the definitions for the queries,
#since these are used multiple times
def sbdd_setFIPS (myST):
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
        theMsg = "You likely did not enter a valid two letter state abbreviation,"
        theMsg = theMsg + "please run again"
        arcpy.addmessage(theMsg)
        del theMsg
    return(stFIPS)

try: 
    for theST in States:
        arcpy.AddMessage("the state is: " + theST)
        ##check to see if field is added, if not add it
        ##populate field
        theFD =  theLocation + theST + "/" + theST + "_SBDD_" + theYear + "_"
        theFD = theFD + theMonth + "_" + theDay + ".gdb/NATL_Broadband_Map"
        thisYear = today.year
        thisMonth = today.month
        thisDay = today.day
        #set up output file
        outFile = theLocation + "/" + theST + "_" + str(thisYear) + "_" + str(thisMonth) + "_" + str(thisDay) + ".txt"
        myFile = open(outFile, 'w')
        myFile.write("" + "\n")
        myFile.write("* -----------------------------------------------------------------------------" + "\n")
        myFile.write("* Data Submission Reciept" + "\n")
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
        myFile.write("*****                     Submission Reciept File  v3v                    *****" + "\n")
        myFile.write("*****                     Check below for any FAILED Statements           *****" + "\n")
        myFile.write("*****  Check below for any WARNEING Statements and if so describe why     *****" + "\n")
        myFile.write("*****                                                                     *****" + "\n")
        myFile.write("*******************************************************************************" + "\n")
        myFile.close()
        del thisDay, thisMonth, thisYear

        #set the stateFIPS number
        stFIPS = sbdd_setFIPS (theST)
        #check for BB_Service_CensusBlock
        theLyr = "CensusBlock"
        arcpy.AddMessage("Begining checks on Feature Class: " + theLyr)
        myFile = open(outFile, 'a')
        myFile.write("" + "\n")
        myFile.write("*Check Layer: " + theLyr + "\n")             
        sbdd_checkGeometry("/BB_Service_", theLyr)
        myChecks = ["WiredTRANSTECH", "MaxAdDown", "MaxAdUp" ] #Fail queries
        for myCheck in myChecks:
                myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theST + theLyr + "_" +
                                            myCheck, sbdd_qryDef(myCheck), "Fail")	 
        myChecks = ["Flag_TT10_MAD7","Flag_TT10_MAD8","Flag_TT10_MAD9","Flag_TT10_MAD10",
                    "Flag_TT10_MAD11","Flag_TT40_MAD3","Flag_TT40_MAD4","Flag_TT40_MAD5",
                    "Flag_TT40_MAD6","Flag_TT40_MAD7","Flag_TT40_MAD8","Flag_TT41_MAD8",
                    "Flag_TT41_MAD9","Flag_TT41_MAD10"]
        for myCheck in myChecks:
                myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theST + theLyr + "_" +
                                            myCheck, sbdd_qryDef(myCheck), "Warn")
        myChecks = ["PROVNAME", "DBANAME", "PROVIDER_TYPE", "FRN", "STATEFIPS", "COUNTYFIPS",
                    "TRACT", "BLOCKID", "BLOCKSUBGROUP", "FULLFIPSID", "OneSpeedAndNotTheOther"]
        for myCheck in myChecks:
            myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theST + theLyr + "_" +
                                        myCheck, sbdd_qryDef(myCheck), "Fail")
        myFlag = myFlag + sbdd_SpeedTier(theLyr)
        myFile.close()

        #check for BB_Service_Address
        theLyr = "Address"
        arcpy.AddMessage("Begining checks on Feature Class: " + theLyr)
        myFile = open(outFile, 'a')
        myFile.write("" + "\n")
        myFile.write("*Check Layer: " + theLyr + "\n")            
        sbdd_checkGeometry("/BB_Service_", theLyr)
        myChecks = ["WiredTRANSTECH", "MaxAdDown", "MaxAdUp" ] #Fail queries
        for myCheck in myChecks:
                myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theST + theLyr + "_" +
                                            myCheck, sbdd_qryDef(myCheck), "Fail")	
        myChecks = ["Flag_TT10_MAD7","Flag_TT10_MAD8","Flag_TT10_MAD9","Flag_TT10_MAD10",
                    "Flag_TT10_MAD11","Flag_TT40_MAD3","Flag_TT40_MAD4","Flag_TT40_MAD5",
                    "Flag_TT40_MAD6","Flag_TT40_MAD7","Flag_TT40_MAD8","Flag_TT41_MAD8",
                    "Flag_TT41_MAD9","Flag_TT41_MAD10"]
        for myCheck in myChecks:
                myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theST + theLyr + "_" +
                                            myCheck, sbdd_qryDef(myCheck), "Warn")
        myChecks = ["PROVNAME", "DBANAME", "PROVIDER_TYPE", "FRN", "ADDRESS" , "BLDGNBR",
                    "STREETNAME", "CITY", "STATECODE", "ZIP5", "LATITUDE", "LONGITUDE",
                    "ENDUSERCAT", "FULLFIPSID", "OneSpeedAndNotTheOther"]
        for myCheck in myChecks:
            myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theST + theLyr + "_" +
                                        myCheck, sbdd_qryDef(myCheck), "Fail")
        myFile.close()

        #check for BB_Service_RoadSegement
        theLyr = "RoadSegment"
        arcpy.AddMessage("Begining checks on Feature Class: " + theLyr)
        myFile = open(outFile, 'a')
        myFile.write("" + "\n")
        myFile.write("*Check Layer: " + theLyr + "\n")            
        sbdd_checkGeometry("/BB_Service_", theLyr)
        myChecks = ["WiredTRANSTECH", "MaxAdDown", "MaxAdUp" ] #Fail queries
        for myCheck in myChecks:
                myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theST + theLyr + "_" +
                                            myCheck, sbdd_qryDef(myCheck), "Fail")	
        myChecks = ["Flag_TT10_MAD7","Flag_TT10_MAD8","Flag_TT10_MAD9","Flag_TT10_MAD10",
                    "Flag_TT10_MAD11","Flag_TT40_MAD3","Flag_TT40_MAD4","Flag_TT40_MAD5",
                    "Flag_TT40_MAD6","Flag_TT40_MAD7","Flag_TT40_MAD8","Flag_TT41_MAD8",
                    "Flag_TT41_MAD9","Flag_TT41_MAD10"]
        for myCheck in myChecks:
                myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theST + theLyr + "_" +
                                            myCheck, sbdd_qryDef(myCheck), "Warn")
        myChecks = ["PROVNAME", "DBANAME", "PROVIDER_TYPE", "FRN", "OneSpeedAndNotTheOther"]
        for myCheck in myChecks:
            myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theST + theLyr + "_" +
                                        myCheck, sbdd_qryDef(myCheck), "Fail")
        myFile.close()

        #check for BB_Service_Wireless
        theLyr = "Wireless"
        arcpy.AddMessage("Begining checks on Feature Class: " + theLyr)
        myFile = open(outFile, 'a')
        myFile.write("" + "\n")
        myFile.write("*Check Layer: " + theLyr + "\n")            
        sbdd_checkGeometry("/BB_Service_", theLyr)
        myChecks = ["WireLessTRANSTECH", "MaxAdDown", "MaxAdUp" ] #Fail queries
        for myCheck in myChecks:
                myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theST + theLyr + "_" +
                                            myCheck, sbdd_qryDef(myCheck), "Fail")	
        myChecks = ["Flag_TT70_MAD7","Flag_TT70_MAD8","Flag_TT70_MAD9","Flag_TT70_MAD10","Flag_TT70_MAD11",
                    "Flag_TT70_MAU7","Flag_TT70_MAU8","Flag_TT70_MAU9","Flag_TT70_MAU10",
                    "Flag_TT70_MAU11","Flag_TT71_MAD7","Flag_TT71_MAD8","Flag_TT71_MAD9",
                    "Flag_TT71_MAD10","Flag_TT71_MAD11","Flag_TT80_MAD7"]
        for myCheck in myChecks:
                myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theST + theLyr + "_" +
                                            myCheck, sbdd_qryDef(myCheck), "Warn")
        myChecks = ["PROVNAME", "DBANAME", "FRN", "STATEABBR", "SPECTRUM"]
        for myCheck in myChecks:
            myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theST + theLyr + "_" +
                                        myCheck, sbdd_qryDef(myCheck), "Fail")
        myFile.close()

        #check for BB_Service_CAInstitutions
        theLyr = "CAInstitutions"
        arcpy.AddMessage("Begining checks on Feature Class: " + theLyr)
        myFile = open(outFile, 'a')
        myFile.write("" + "\n")
        myFile.write("*Check Layer: " + theLyr + "\n")            
        sbdd_checkGeometry("/BB_Service_", theLyr)
        myChecks = ["CAITRANSTECH"]
        for myCheck in myChecks:
                myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theST + theLyr + "_" +
                                            myCheck, sbdd_qryDef(myCheck), "Warn")
        myChecks = ["ANCHORNAME", "ADDRESS", "BLDGNBR", "STREETNAME", "CITY" , "STATECODE",
                    "ZIP5", "CAICAT", "BBSERVICE", "DBANAME", "FULLFIPSID"]
        for myCheck in myChecks:
            myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theST + theLyr + "_" +
                                        myCheck, sbdd_qryDef(myCheck), "Fail")
        myFile.close()


        #check for BB_Service_Overview
        theLyr = "Overview"
        arcpy.AddMessage("Begining checks on Feature Class: " + theLyr)
        myFile = open(outFile, 'a')
        myFile.write("" + "\n")
        myFile.write("*Check Layer: " + theLyr + "\n")            
        sbdd_checkGeometry("/BB_Service_", theLyr)
        myChecks = ["WiredTRANSTECH", "MaxAdDown", "MaxAdUp" ]
        for myCheck in myChecks:
                myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theST + theLyr + "_" +
                                            myCheck, sbdd_qryDef(myCheck), "Fail")
        myChecks = ["PROVNAME", "DBANAME", "FRN", "GEOUNITTYPE" , "STATECOUNTYFIPS",
                    "STATEABBR", "CITY", "STATECODE", "ZIP5", "LATITUDE", "LONGITUDE",
                    "ENDUSERCAT", "FULLFIPSID", "OneSpeedAndNotTheOther"]
        for myCheck in myChecks:
            myFlag = myFlag + sbdd_qry (theFD + "/BB_Service_" + theLyr, theST + theLyr + "_" +
                                        myCheck, sbdd_qryDef(myCheck), "Fail")
        myFile.close()


        #check for BB_ConnectionPoint_LastMile
        theLyr = "LastMile"
        arcpy.AddMessage("Begining checks on Feature Class: " + theLyr)
        myFile = open(outFile, 'a')
        myFile.write("" + "\n")
        myFile.write("*Check Layer: " + theLyr + "\n")            
        sbdd_checkGeometry("/BB_ConnectionPoint_", theLyr)
        myChecks = ["PROVNAME", "DBANAME", "FRN", "OWNERSHIP" , "BHCAPACITY",
                    "BHTYPE", "LATITUDE", "LONGITUDE", "ELEVFEET", "STATEABBR", "FULLFIPSID"]
        for myCheck in myChecks:
            myFlag = myFlag + sbdd_qry (theFD + "/BB_ConnectionPoint_" + theLyr, theST + theLyr + "_" +
                                        myCheck, sbdd_qryDef(myCheck), "Fail")
        myFile.close()

        #check for BB_ConnectionPoint_MiddleMile
        theLyr = "MiddleMile"
        arcpy.AddMessage("Begining checks on Feature Class: " + theLyr)
        myFile = open(outFile, 'a')
        myFile.write("" + "\n")
        myFile.write("*Check Layer: " + theLyr + "\n")            
        sbdd_checkGeometry("/BB_ConnectionPoint_", theLyr)
        myChecks = ["PROVNAME", "DBANAME", "FRN", "BHCAPACITY",
                    "BHTYPE", "LATITUDE", "LONGITUDE", "STATEABBR", "FULLFIPSID"]
        for myCheck in myChecks:
            myFlag = myFlag + sbdd_qry (theFD + "/BB_ConnectionPoint_" + theLyr, theST + theLyr + "_" +
                                        myCheck, sbdd_qryDef(myCheck), "Fail")
        myFile.close()

except:
    arcpy.AddMessage("Something bad happened")
       
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

  
