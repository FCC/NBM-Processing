# ---------------------------------------------------------------------------
#   VERSION 0.1 (for ArcGIS 10)
# SBDD_BusRules.py
# Created on: Thurs Sept 29 2011 
# Created by: Michael Byrne
# Federal Communications Commission
# ---------------------------------------------------------------------------

# Import system modules
import sys, string, os, arcpy
from arcpy import env

#basic variabls
theLocation = "C:/Users/michael.byrne/NBM/Spring2013/Data/"
theYear = "2013"
theMonth = "04"
theDay = "01"

States = ["AK","AL","AR","AS","AZ","CA","CO","CT"] #1
States = States + ["DC","DE","FL","GA","GU","HI","IA","ID"] #2 
States = States + ["IL","IN","KS","KY","LA","MA","MD","ME"] #3
States = States + ["MI","MN","MO","MP","MS","MT","NC","ND"] #4 
States = States + ["NE","NH","NJ","NM","NV","NY","OH","OK"] #5
States = States + ["OR","PA","PR","RI","SC","SD","TN","TX"] #6
States = States + ["UT","VA","VI","VT","WA","WI","WV","WY"] #7

States = ["AS"]

##
##******************************************************************************
##*********************************FileWidth************************************
##******************************************************************************
##
##write out functions
##Function sbdd_qry creates a layer from a query (which is an argument passed to
##the function and determines if the count is greater than 0
##if the count is greater than 0, there is a failed value in the submitted data

def sbdd_qry (theFL, myFL, myQry):
    arcpy.AddMessage("       Checking for unexpected values: " + myFL)
    arcpy.MakeFeatureLayer_management(theFL, myFL, myQry)
    myCnt = int(arcpy.GetCount_management(myFL).getOutput(0))
    arcpy.Delete_management(myFL)
    if myCnt > 0: #exception occurred
        myStr = str(myCnt) #"FAILED"
    else:
        myStr = "passed"
    del myCnt, theFL, myFL, myQry
    return ("," + myStr) 

def sbdd_cnt (theFL, myFL, myQry):  
    arcpy.AddMessage("       Checking for complete record counts values: " + myFL)
    arcpy.MakeFeatureLayer_management(theFL, myFL, myQry)
    myCnt = int(arcpy.GetCount_management(myFL).getOutput(0))
    arcpy.Delete_management(myFL)
    if myCnt > 0: #there are records, 
        myStr = str(myCnt) #this is a count of records in the feature class
    else:
        myStr = "0"        #there were no records submitted in the FC
    del myCnt, theFL, myFL, myQry
    return ("," + myStr) 

#sbdd_qryDef writes out the definitions for the queries, since these are used
##multiple times
def sbdd_qryDef (myField):
    if myField == "RecCnt":
        theQry = "OBJECTID > 0" #gets a complete record count
    if myField == "WiredTRANSTECH":
        theQry = "TRANSTECH IS NULL OR (TRANSTECH <> 10 AND TRANSTECH <> 20 AND "
        theQry = theQry + "TRANSTECH <> 30 AND TRANSTECH <> 40 AND TRANSTECH "
        theQry = theQry + "<> 41 AND TRANSTECH <> 50 AND TRANSTECH <> 90)"
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
    if myField == "WireLessTRANSTECH":
        theQry = "TRANSTECH IS NULL OR (TRANSTECH <> 70 AND TRANSTECH <> 71 "
        theQry = theQry + "AND TRANSTECH <> 80 AND TRANSTECH <> 60)"
    if myField == "SPECTRUM":
        theQry = "SPECTRUM IS NULL OR (SPECTRUM < 1 AND SPECTRUM > 10)"
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
    return(theQry)

##
##******************************************************************************
##
try:
    ##insert code for each state loop
    for theST in States:
        #Create Reciept/file variables
        theOFCB = theLocation + "CensusBlock_BusRules_" + theST + "_" + theYear + theMonth + ".csv"
        theOFAd = theLocation + "Address_BusRules_" + theST + "_" + theYear + theMonth + ".csv"
        theOFRd = theLocation + "RoadSegment_BusRules_" + theST + "_" + theYear + theMonth + ".csv"
        theOFWS = theLocation + "Wireless_BusRules_" + theST + "_" + theYear + theMonth + ".csv"
        #set up output file
        ##you are going to write out 4 files; one for each feature class
        cbFile = open(theOFCB, 'w')
        cbFile.write("State,RecCnt,Rule_TransTech,Rule_MaxAdDown,Rule_MaxAdUp," +
                     "Flag_TT10_MAD7,Flag_TT10_MAD8,Flag_TT10_MAD9," +
                     "Flag_TT10_MAD10,Flag_TT10_MAD11,Flag_TT40_MAD3," +
                     "Flag_TT40_MAD4,Flag_TT40_MAD5,Flag_TT40_MAD6," +
                     "Flag_TT40_MAD7,Flag_TT40_MAD8,Flag_TT41_MAD8," +
                     "Flag_TT41_MAD9,Flag_TT41_MAD10" + "\n")

        cbFile.close()
        adFile = open(theOFAd, 'w')
        adFile.write("State,RecCnt,Rule_TransTech,Rule_MaxAdDown,Rule_MaxAdUp," +
                     "Flag_TT10_MAD7,Flag_TT10_MAD8,Flag_TT10_MAD9," +
                     "Flag_TT10_MAD10,Flag_TT10_MAD11,Flag_TT40_MAD3," +
                     "Flag_TT40_MAD4,Flag_TT40_MAD5,Flag_TT40_MAD6," +
                     "Flag_TT40_MAD7,Flag_TT40_MAD8,Flag_TT41_MAD8," +
                     "Flag_TT41_MAD9,Flag_TT41_MAD10" + "\n")
        adFile.close()
        rdFile = open(theOFRd, 'w')
        rdFile.write("State,RecCnt,Rule_TransTech,Rule_MaxAdDown,Rule_MaxAdUp," +
                     "Flag_TT10_MAD7,Flag_TT10_MAD8,Flag_TT10_MAD9," +
                     "Flag_TT10_MAD10,Flag_TT10_MAD11,Flag_TT40_MAD3," +
                     "Flag_TT40_MAD4,Flag_TT40_MAD5,Flag_TT40_MAD6," +
                     "Flag_TT40_MAD7,Flag_TT40_MAD8,Flag_TT41_MAD8," +
                     "Flag_TT41_MAD9,Flag_TT41_MAD10" + "\n")
        rdFile.close()
        wsFile = open(theOFWS, 'w')
        wsFile.write("State,RecCnt,Rule_TransTech,Rule_MaxAdDown,Rule_MaxAdUp," +
                     "Flag_TT70_MAD7,Flag_TT70_MAD8,Flag_TT70_MAD9," +
                     "Flag_TT70_MAD10,Flag_TT70_MAD11," +
                     "Flag_TT70_MAU7,Flag_TT70_MAU8,Flag_TT70_MAU9," +
                     "Flag_TT70_MAU10,Flag_TT70_MAU11," +
                     "Flag_TT71_MAD7,Flag_TT71_MAD8,Flag_TT71_MAD9," +
                     "Flag_TT71_MAD10,Flag_TT71_MAD11," +
                     "Flag_TT80_MAD7" + "\n")
        wsFile.close()
        arcpy.AddMessage("Begining checks on: " + theST)
        #******************************** 
        #check for BB_Service_CensusBlock
        #********************************        
        theFD = theLocation + theST + "/" + theST + "_SBDD_" + theYear + "_"
        theFD = theFD + theMonth + "_" + theDay + ".gdb/NATL_Broadband_Map/"
        theLyr = "CensusBlock"
        theCBStr = theST        
        if arcpy.Exists(theFD + "/BB_Service_" + theLyr):
            arcpy.AddMessage("     Begining checks on Feature Class: " + theLyr)      
            theCBStr = theCBStr + sbdd_cnt (theFD + "/BB_Service_" + theLyr,
                                            theLyr + "_RecCnt",
                                            sbdd_qryDef("RecCnt")) 
            theCBStr = theCBStr + sbdd_qry (theFD + "/BB_Service_" + theLyr,
                                            theLyr + "_TRANSTECH",
                                            sbdd_qryDef("WiredTRANSTECH"))      
            theCBStr = theCBStr + sbdd_qry (theFD + "/BB_Service_" + theLyr,
                                            theLyr + "_MaxAdDown",
                                            sbdd_qryDef("MaxAdDown"))
            theCBStr = theCBStr + sbdd_qry (theFD + "/BB_Service_" +
                                            theLyr, theLyr + "_MaxAdUp",
                                            sbdd_qryDef("MaxAdUp"))
            theCBStr = theCBStr + sbdd_qry (theFD + "/BB_Service_" +
                                            theLyr, theLyr + "_Flag_TT10_MAD7",
                                            sbdd_qryDef("Flag_TT10_MAD7"))
            theCBStr = theCBStr + sbdd_qry (theFD + "/BB_Service_" +
                                            theLyr, theLyr + "_Flag_TT10_MAD8",
                                            sbdd_qryDef("Flag_TT10_MAD8"))
            theCBStr = theCBStr + sbdd_qry (theFD + "/BB_Service_" +
                                            theLyr, theLyr + "_Flag_TT10_MAD9",
                                            sbdd_qryDef("Flag_TT10_MAD9"))
            theCBStr = theCBStr + sbdd_qry (theFD + "/BB_Service_" +
                                            theLyr, theLyr + "_Flag_TT10_MAD10",
                                            sbdd_qryDef("Flag_TT10_MAD10"))
            theCBStr = theCBStr + sbdd_qry (theFD + "/BB_Service_" +
                                            theLyr, theLyr + "_Flag_TT10_MAD11",
                                            sbdd_qryDef("Flag_TT10_MAD11"))            
            theCBStr = theCBStr + sbdd_qry (theFD + "/BB_Service_" +
                                            theLyr, theLyr + "_Flag_TT40_MAD3",
                                            sbdd_qryDef("Flag_TT40_MAD3"))            
            theCBStr = theCBStr + sbdd_qry (theFD + "/BB_Service_" +
                                            theLyr, theLyr + "_Flag_TT40_MAD4",
                                            sbdd_qryDef("Flag_TT40_MAD4"))
            theCBStr = theCBStr + sbdd_qry (theFD + "/BB_Service_" +
                                            theLyr, theLyr + "_Flag_TT40_MAD5",
                                            sbdd_qryDef("Flag_TT40_MAD5"))
            theCBStr = theCBStr + sbdd_qry (theFD + "/BB_Service_" +
                                            theLyr, theLyr + "_Flag_TT40_MAD6",
                                            sbdd_qryDef("Flag_TT40_MAD6"))
            theCBStr = theCBStr + sbdd_qry (theFD + "/BB_Service_" +
                                            theLyr, theLyr + "_Flag_TT40_MAD7",
                                            sbdd_qryDef("Flag_TT40_MAD7"))
            theCBStr = theCBStr + sbdd_qry (theFD + "/BB_Service_" +
                                            theLyr, theLyr + "_Flag_TT40_MAD8",
                                            sbdd_qryDef("Flag_TT40_MAD8"))              
            theCBStr = theCBStr + sbdd_qry (theFD + "/BB_Service_" +
                                            theLyr, theLyr + "_Flag_TT41_MAD8",
                                            sbdd_qryDef("Flag_TT41_MAD8")) 
            theCBStr = theCBStr + sbdd_qry (theFD + "/BB_Service_" +
                                            theLyr, theLyr + "_Flag_TT41_MAD9",
                                            sbdd_qryDef("Flag_TT41_MAD9"))
            theCBStr = theCBStr + sbdd_qry (theFD + "/BB_Service_" +
                                            theLyr, theLyr + "_Flag_TT41_MAD10",
                                            sbdd_qryDef("Flag_TT41_MAD10"))
        else:
            theCBStr = theST + ",File Not Submitted Yet"
        cbFile = open(theOFCB, 'a')
        cbFile.write(theCBStr + "\n")
        cbFile.close()
        
##
##******************************************************************************
##      #******************************** 
        #check for BB_Service_Address
##      #******************************** 
##******************************************************************************
##             
        theFD = theLocation + theST + "/" + theST + "_SBDD_" + theYear + "_"
        theFD = theFD + theMonth + "_01.gdb/NATL_Broadband_Map/"
        theLyr = "Address"
        theAdStr = theST        
        if arcpy.Exists(theFD + "/BB_Service_" + theLyr):
            arcpy.AddMessage("     Begining checks on Feature Class: " + theLyr)      
            theAdStr = theAdStr + sbdd_cnt (theFD + "/BB_Service_" + theLyr,
                                            theLyr + "_RecCnt",
                                            sbdd_qryDef("RecCnt"))
            theAdStr = theAdStr + sbdd_qry (theFD + "/BB_Service_" + theLyr,
                                            theLyr + "_TRANSTECH",
                                            sbdd_qryDef("WiredTRANSTECH"))      
            theAdStr = theAdStr + sbdd_qry (theFD + "/BB_Service_" + theLyr,
                                            theLyr + "_MaxAdDown",
                                            sbdd_qryDef("MaxAdDown"))
            theAdStr = theAdStr + sbdd_qry (theFD + "/BB_Service_" +
                                            theLyr, theLyr + "_MaxAdUp",
                                            sbdd_qryDef("MaxAdUp"))
            theAdStr = theAdStr + sbdd_qry (theFD + "/BB_Service_" +
                                            theLyr, theLyr + "_Flag_TT10_MAD7",
                                            sbdd_qryDef("Flag_TT10_MAD7"))
            theAdStr = theAdStr + sbdd_qry (theFD + "/BB_Service_" +
                                            theLyr, theLyr + "_Flag_TT10_MAD8",
                                            sbdd_qryDef("Flag_TT10_MAD8"))
            theAdStr = theAdStr + sbdd_qry (theFD + "/BB_Service_" +
                                            theLyr, theLyr + "_Flag_TT10_MAD9",
                                            sbdd_qryDef("Flag_TT10_MAD9"))
            theAdStr = theAdStr + sbdd_qry (theFD + "/BB_Service_" +
                                            theLyr, theLyr + "_Flag_TT10_MAD10",
                                            sbdd_qryDef("Flag_TT10_MAD10"))
            theAdStr = theAdStr + sbdd_qry (theFD + "/BB_Service_" +
                                            theLyr, theLyr + "_Flag_TT10_MAD11",
                                            sbdd_qryDef("Flag_TT10_MAD11"))            
            theAdStr = theAdStr + sbdd_qry (theFD + "/BB_Service_" +
                                            theLyr, theLyr + "_Flag_TT40_MAD3",
                                            sbdd_qryDef("Flag_TT40_MAD3"))            
            theAdStr = theAdStr + sbdd_qry (theFD + "/BB_Service_" +
                                            theLyr, theLyr + "_Flag_TT40_MAD4",
                                            sbdd_qryDef("Flag_TT40_MAD4"))
            theAdStr = theAdStr + sbdd_qry (theFD + "/BB_Service_" +
                                            theLyr, theLyr + "_Flag_TT40_MAD5",
                                            sbdd_qryDef("Flag_TT40_MAD5"))
            theAdStr = theAdStr + sbdd_qry (theFD + "/BB_Service_" +
                                            theLyr, theLyr + "_Flag_TT40_MAD6",
                                            sbdd_qryDef("Flag_TT40_MAD6"))
            theAdStr = theAdStr + sbdd_qry (theFD + "/BB_Service_" +
                                            theLyr, theLyr + "_Flag_TT40_MAD7",
                                            sbdd_qryDef("Flag_TT40_MAD7"))
            theAdStr = theAdStr + sbdd_qry (theFD + "/BB_Service_" +
                                            theLyr, theLyr + "_Flag_TT40_MAD8",
                                            sbdd_qryDef("Flag_TT40_MAD8"))              
            theAdStr = theAdStr + sbdd_qry (theFD + "/BB_Service_" +
                                            theLyr, theLyr + "_Flag_TT41_MAD8",
                                            sbdd_qryDef("Flag_TT41_MAD8")) 
            theAdStr = theAdStr + sbdd_qry (theFD + "/BB_Service_" +
                                            theLyr, theLyr + "_Flag_TT41_MAD9",
                                            sbdd_qryDef("Flag_TT41_MAD9"))
            theAdStr = theAdStr + sbdd_qry (theFD + "/BB_Service_" +
                                            theLyr, theLyr + "_Flag_TT41_MAD10",
                                            sbdd_qryDef("Flag_TT41_MAD10"))
        else:
            theAdStr = theST + ",File Not Submitted Yet"
        adFile = open(theOFAd, 'a')
        adFile.write(theAdStr + "\n")
        adFile.close()

##
##******************************************************************************
##      #******************************** 
        #check for BB_Service_RoadSegment
##      #******************************** 
##******************************************************************************
             
        theFD = theLocation + theST + "/" + theST + "_SBDD_" + theYear + "_"
        theFD = theFD + theMonth + "_01.gdb/NATL_Broadband_Map/"
        theLyr = "RoadSegment"
        theRdStr = theST        
        if arcpy.Exists(theFD + "/BB_Service_" + theLyr):
            arcpy.AddMessage("     Begining checks on Feature Class: " + theLyr)      
            theRdStr = theRdStr + sbdd_cnt (theFD + "/BB_Service_" + theLyr,
                                            theLyr + "_RecCnt",
                                            sbdd_qryDef("RecCnt"))
            theRdStr = theRdStr + sbdd_qry (theFD + "/BB_Service_" + theLyr,
                                            theLyr + "_TRANSTECH",
                                            sbdd_qryDef("WiredTRANSTECH"))      
            theRdStr = theRdStr + sbdd_qry (theFD + "/BB_Service_" + theLyr,
                                            theLyr + "_MaxAdDown",
                                            sbdd_qryDef("MaxAdDown"))
            theRdStr = theRdStr + sbdd_qry (theFD + "/BB_Service_" +
                                            theLyr, theLyr + "_MaxAdUp",
                                            sbdd_qryDef("MaxAdUp"))
            theRdStr = theRdStr + sbdd_qry (theFD + "/BB_Service_" +
                                            theLyr, theLyr + "_Flag_TT10_MAD7",
                                            sbdd_qryDef("Flag_TT10_MAD7"))
            theRdStr = theRdStr + sbdd_qry (theFD + "/BB_Service_" +
                                            theLyr, theLyr + "_Flag_TT10_MAD8",
                                            sbdd_qryDef("Flag_TT10_MAD8"))
            theRdStr = theRdStr + sbdd_qry (theFD + "/BB_Service_" +
                                            theLyr, theLyr + "_Flag_TT10_MAD9",
                                            sbdd_qryDef("Flag_TT10_MAD9"))
            theRdStr = theRdStr + sbdd_qry (theFD + "/BB_Service_" +
                                            theLyr, theLyr + "_Flag_TT10_MAD10",
                                            sbdd_qryDef("Flag_TT10_MAD10"))
            theRdStr = theRdStr + sbdd_qry (theFD + "/BB_Service_" +
                                            theLyr, theLyr + "_Flag_TT10_MAD11",
                                            sbdd_qryDef("Flag_TT10_MAD11"))            
            theRdStr = theRdStr + sbdd_qry (theFD + "/BB_Service_" +
                                            theLyr, theLyr + "_Flag_TT40_MAD3",
                                            sbdd_qryDef("Flag_TT40_MAD3"))            
            theRdStr = theRdStr + sbdd_qry (theFD + "/BB_Service_" +
                                            theLyr, theLyr + "_Flag_TT40_MAD4",
                                            sbdd_qryDef("Flag_TT40_MAD4"))
            theRdStr = theRdStr + sbdd_qry (theFD + "/BB_Service_" +
                                            theLyr, theLyr + "_Flag_TT40_MAD5",
                                            sbdd_qryDef("Flag_TT40_MAD5"))
            theRdStr = theRdStr + sbdd_qry (theFD + "/BB_Service_" +
                                            theLyr, theLyr + "_Flag_TT40_MAD6",
                                            sbdd_qryDef("Flag_TT40_MAD6"))
            theRdStr = theRdStr + sbdd_qry (theFD + "/BB_Service_" +
                                            theLyr, theLyr + "_Flag_TT40_MAD7",
                                            sbdd_qryDef("Flag_TT40_MAD7"))
            theRdStr = theRdStr + sbdd_qry (theFD + "/BB_Service_" +
                                            theLyr, theLyr + "_Flag_TT40_MAD8",
                                            sbdd_qryDef("Flag_TT40_MAD8"))              
            theRdStr = theRdStr + sbdd_qry (theFD + "/BB_Service_" +
                                            theLyr, theLyr + "_Flag_TT41_MAD8",
                                            sbdd_qryDef("Flag_TT41_MAD8")) 
            theRdStr = theRdStr + sbdd_qry (theFD + "/BB_Service_" +
                                            theLyr, theLyr + "_Flag_TT41_MAD9",
                                            sbdd_qryDef("Flag_TT41_MAD9"))
            theRdStr = theRdStr + sbdd_qry (theFD + "/BB_Service_" +
                                            theLyr, theLyr + "_Flag_TT41_MAD10",
                                            sbdd_qryDef("Flag_TT41_MAD10"))
        else:
            theRdStr = theST + ",File Not Submitted Yet"
        rdFile = open(theOFRd, 'a')
        rdFile.write(theRdStr + "\n")
        rdFile.close()

##
##******************************************************************************
##      #******************************** 
        #check for BB_Service_Wireless
##      #******************************** 
##******************************************************************************
##             
        theFD = theLocation + theST + "/" + theST + "_SBDD_" + theYear + "_"
        theFD = theFD + theMonth + "_01.gdb/NATL_Broadband_Map/"
        theLyr = "Wireless"
        theWsStr = theST        
        if arcpy.Exists(theFD + "/BB_Service_" + theLyr):
            arcpy.AddMessage("     Begining checks on Feature Class: " + theLyr)      
            theWsStr = theWsStr + sbdd_cnt (theFD + "/BB_Service_" + theLyr,
                                            theLyr + "_RecCnt",
                                            sbdd_qryDef("RecCnt"))
            theWsStr = theWsStr + sbdd_qry (theFD + "/BB_Service_" + theLyr,
                                            theLyr + "_TRANSTECH",
                                            sbdd_qryDef("WireLessTRANSTECH"))      
            theWsStr = theWsStr + sbdd_qry (theFD + "/BB_Service_" + theLyr,
                                            theLyr + "_MaxAdDown",
                                            sbdd_qryDef("MaxAdDown"))
            theWsStr = theWsStr + sbdd_qry (theFD + "/BB_Service_" +
                                            theLyr, theLyr + "_MaxAdUp",
                                            sbdd_qryDef("MaxAdUp"))
            theWsStr = theWsStr + sbdd_qry (theFD + "/BB_Service_" +
                                            theLyr, theLyr + "_Flag_TT70_MAD7",
                                            sbdd_qryDef("Flag_TT70_MAD7"))
            theWsStr = theWsStr + sbdd_qry (theFD + "/BB_Service_" +
                                            theLyr, theLyr + "_Flag_TT70_MAD8",
                                            sbdd_qryDef("Flag_TT70_MAD8"))
            theWsStr = theWsStr + sbdd_qry (theFD + "/BB_Service_" +
                                            theLyr, theLyr + "_Flag_TT70_MAD9",
                                            sbdd_qryDef("Flag_TT70_MAD9"))
            theWsStr = theWsStr + sbdd_qry (theFD + "/BB_Service_" +
                                            theLyr, theLyr + "_Flag_TT70_MAD10",
                                            sbdd_qryDef("Flag_TT70_MAD10"))
            theWsStr = theWsStr + sbdd_qry (theFD + "/BB_Service_" +
                                            theLyr, theLyr + "_Flag_TT70_MAD11",
                                            sbdd_qryDef("Flag_TT70_MAD11"))            

            theWsStr = theWsStr + sbdd_qry (theFD + "/BB_Service_" +
                                            theLyr, theLyr + "_Flag_TT70_MAU7",
                                            sbdd_qryDef("Flag_TT70_MAU7"))
            theWsStr = theWsStr + sbdd_qry (theFD + "/BB_Service_" +
                                            theLyr, theLyr + "_Flag_TT70_MAU8",
                                            sbdd_qryDef("Flag_TT70_MAU8"))
            theWsStr = theWsStr + sbdd_qry (theFD + "/BB_Service_" +
                                            theLyr, theLyr + "_Flag_TT70_MAU9",
                                            sbdd_qryDef("Flag_TT70_MAU9"))
            theWsStr = theWsStr + sbdd_qry (theFD + "/BB_Service_" +
                                            theLyr, theLyr + "_Flag_TT70_MAU10",
                                            sbdd_qryDef("Flag_TT70_MAU10"))
            theWsStr = theWsStr + sbdd_qry (theFD + "/BB_Service_" +
                                            theLyr, theLyr + "_Flag_TT70_MAU11",
                                            sbdd_qryDef("Flag_TT70_MAU11"))  


            theWsStr = theWsStr + sbdd_qry (theFD + "/BB_Service_" +
                                            theLyr, theLyr + "_Flag_TT71_MAD7",
                                            sbdd_qryDef("Flag_TT71_MAD7"))
            theWsStr = theWsStr + sbdd_qry (theFD + "/BB_Service_" +
                                            theLyr, theLyr + "_Flag_TT71_MAD8",
                                            sbdd_qryDef("Flag_TT71_MAD8"))
            theWsStr = theWsStr + sbdd_qry (theFD + "/BB_Service_" +
                                            theLyr, theLyr + "_Flag_TT71_MAD9",
                                            sbdd_qryDef("Flag_TT71_MAD9"))
            theWsStr = theWsStr + sbdd_qry (theFD + "/BB_Service_" +
                                            theLyr, theLyr + "_Flag_TT71_MAD10",
                                            sbdd_qryDef("Flag_TT71_MAD10"))
            theWsStr = theWsStr + sbdd_qry (theFD + "/BB_Service_" +
                                            theLyr, theLyr + "_Flag_TT71_MAD11",
                                            sbdd_qryDef("Flag_TT71_MAD11")) 


            theWsStr = theWsStr + sbdd_qry (theFD + "/BB_Service_" +
                                            theLyr, theLyr + "_Flag_TT80_MAD7",
                                            sbdd_qryDef("Flag_TT80_MAD7")) 

        else:
            theWsStr = theST + ",File Not Submitted Yet"
        wsFile = open(theOFWS, 'a')
        wsFile.write(theWsStr + "\n")
        wsFile.close()
    del theLyr, theFD, theST, States, theLocation, theYear, theMonth
    del theOFCB, theOFAd, theOFRd, theOFWS
    del theWsStr, theRdStr, theAdStr, theCBStr
except:
    arcpy.AddMessage( "Something bad happened during the writing of the reciept; please re-run" )


  
