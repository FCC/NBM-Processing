# ---------------------------------------------------------------------------
# SBDD_CreateIDs.py
# Created on: May 16, 2011 
# Created by: Michael Byrne
# Federal Communications Commission
# creates the unique ID for every table in the submission
# National Broadband Map from the source file geodatabases
# requires one State submission at a time
# ---------------------------------------------------------------------------

# Import system modules
import arcpy
from arcpy import env
import sys, string, os, math

##Global Variables
##these need changing every time
##theRound number increases by 1 every six months;
##1 = delivered April 2010 
##2 = delivered Oct 2010
##3 = delivered April 2011
##4 = delivered oct 2011
##5 = delivered April 2012
theRound = 5
##theSubmission is the first, second, third submission from the state
theSubmission = 1

theLocation = "C:/Users/NBMSource/Spring2012/"
theYear = "2012"
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
##Function sbdd_ReturnFIPS returns the FIPSID for the State
def sbdd_IDField ():
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
        stFIPS = "NOT"
    return (stFIPS)

##Function sbdd_CalcID populates the uniqueID
##performs the calculation of the unqique ID
def sbdd_CalcID (theFD, theFC):
    arcpy.AddMessage("     Calulating Field on " + theST + ": " + theFC)
    if theFC == "BB_Service_Address":
        theLCode = "1"
    if theFC == "BB_Service_CAInstitutions":
        theLCode = "2"
    if theFC == "BB_Service_CensusBlock":
        theLCode = "3"
    if theFC == "BB_Service_Overview":
        theLCode = "4"
    if theFC == "BB_Service_RoadSegment":
        theLCode = "5"
    if theFC == "BB_Service_Wireless":
        theLCode = "6"        
    if theFC == "BB_ConnectionPoint_LastMile":
        theLCode = "7"        
    if theFC == "BB_ConnectionPoint_MiddleMile":
        theLCode = "8"
    arcpy.DeleteField_management(theFD + theFC, ["SBDD_ID"])
    arcpy.AddField_management(theFD + theFC,"SBDD_ID", "TEXT", "","", "20")
    theExp = "'" + str(theRound) + "-" + str(theSubmission) + "-" + sbdd_IDField() + \
             "-" + theLCode + "-" + "!OBJECTID!" + "'"   
    arcpy.CalculateField_management(theFD + theFC, "SBDD_ID", theExp, "PYTHON")
    del theExp, theLCode
    return ()

#*******************************************************************************************************
##################Main Code below
#*******************************************************************************************************
try: 
    for theST in States:
        arcpy.AddMessage("the state is: " + theST)
        ##check to see if field is added, if not add it
        ##populate field
        theFD =  theLocation + theST + "/" + theST + "_SBDD_" + theYear + "_"
        theFD = theFD + theMonth + "_" + theDay + ".gdb/NATL_Broadband_Map/"        
        theFCs = ["BB_Service_Address", "BB_Service_CAInstitutions", "BB_Service_CensusBlock", \
                  "BB_Service_Overview", "BB_Service_RoadSegment", "BB_Service_Wireless", \
                  "BB_ConnectionPoint_LastMile", "BB_ConnectionPoint_MiddleMile"]
        for theFC in theFCs:
            sbdd_CalcID(theFD, theFC)
    del theFD, theST, States, theFC, theFCs, theSubmission, theRound, theMonth, theDay
except:
    arcpy.AddMessage("Something bad happened")

  
