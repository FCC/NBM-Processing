# ---------------------------------------------------------------------------
# SBDD_RndPtOverlay.py
# Created on: May 24, 2011 
# Created by: Michael Byrne
# Federal Communications Commission
# creates the output on the overlay of Points and Roads
# on the random point file
# National Broadband Map from the source file geodatabases
# requires one State submission at a time
# ---------------------------------------------------------------------------

# Import system modules
import arcpy
from arcpy import env
import sys, string, os, math

#global variables
theOF = "C:/Users/michael.byrne/"
#processing file geodatabase
thePGDB = "C:/Users/michael.byrne/Processing_rndpt.gdb"  
theRndPT = "C:/Users/michael.byrne/Library/RandomPtFall2012.gdb/RandomPt_GT2sqm"
env.workspace = thePGDB

States = ["AK","AL","AR","AS","AZ","CA","CO","CT"]          #1
States = States + ["DC","DE","FL","GA","GU","HI","IA","ID"] #2
States = States + ["IL","IN","KS","KY","LA","MA","MD","ME"] #3 
States = States + ["MI","MN","MO","MS","MT","NC","ND","MP"] #4 
States = States + ["NE","NH","NJ","NM","NV","NY","OH","OK"] #5
States = States + ["OR","PA","PR","RI","SC","SD","TN","TX"] #6
States = States + ["UT","VA","VI","VT","WA","WI","WV","WY"] #7

theFCs = ["BB_Service_Address", "BB_Service_RoadSegment"]
theLocation = "C:/Users/michael.byrne/NBM/Spring2013/data/"
theYear = "2013"
theMonth = "04"
theDay = "01"

##Function sbdd_CreateTable defines a new state table
##into which all state records will be appended
def sbdd_CreateTable():
    myTbl = "RandomPoint_" + theST
    arcpy.AddMessage("  Creating output table for: " + theST)
    if arcpy.Exists(myTbl):
        arcpy.Delete_management(myTbl)
    arcpy.CreateTable_management(thePGDB, myTbl)        
    arcpy.AddField_management(myTbl, "POINTID", "TEXT", "", "", "20")
    arcpy.AddField_management(myTbl, "DATASOURCE", "TEXT", "", "", "15")    
    arcpy.AddField_management(myTbl, "JOIN_FID", "LONG", "", "", "10")
    arcpy.AddField_management(myTbl, "BLOCKID10", "TEXT", "", "", "15")
    arcpy.AddField_management(myTbl, "FRN", "TEXT", "", "", "10")    
    arcpy.AddField_management(myTbl, "PROVNAME", "TEXT", "", "", "200")
    arcpy.AddField_management(myTbl, "DBANAME", "TEXT", "", "", "200")
    arcpy.AddField_management(myTbl, "Provider_T", "SHORT", "", "", "1")
    arcpy.AddField_management(myTbl, "TRANSTECH", "SHORT", "", "", "15")
    arcpy.AddField_management(myTbl, "MAXADDOWN", "TEXT", "", "", "2")
    arcpy.AddField_management(myTbl, "MAXADUP", "TEXT", "", "", "2")
    arcpy.AddField_management(myTbl, "TYPICDOWN", "TEXT", "", "", "2")
    arcpy.AddField_management(myTbl, "TYPICUP", "TEXT", "", "", "2")
    arcpy.AddField_management(myTbl, "STATE_CODE", "TEXT", "", "", "2")    
    arcpy.AddField_management(myTbl, "ENDUSERCAT", "TEXT", "", "", "4") 
    arcpy.AddField_management(myTbl, "SBDD_ID", "TEXT", "", "", "20")
    del myTbl
    return ()

##Function sbdd_ExportTodbf exports the overlay feature class, 
##just to a dbf, so it canbe appended to the result table; 
##these tables also serve as the data download tables
def sbdd_Append ():
    arcpy.AddMessage("     Appending...")
    if arcpy.Exists(theOF + theST + "_" + theFC + ".shp"):
        arcpy.Delete_management(theOF + theST + "_" + theFC + ".shp")
    arcpy.CopyFeatures_management("myOverlay", theOF + theST + "_" + theFC)
    arcpy.AddField_management(theOF + theST + "_" + theFC + ".shp",
                              "dataSource", "TEXT", "", "", "15")
    theStr = string.replace(theFC, "BB_Service_", "")
    arcpy.CalculateField_management(theOF + theST + "_" + theFC + ".shp",
                                    "dataSource", "'" + theStr + "'", "PYTHON")
    arcpy.AddField_management(theOF + theST + "_" + theFC + ".shp",
                              "state_code", "TEXT", "", "", "2")
    arcpy.CalculateField_management(theOF + theST + "_" + theFC + ".shp",
                                    "state_code", "'" + theST + "'", "PYTHON")
    Files = ["prj", "sbn", "sbx", "shp", "shp.xml", "shx"]
    for theFile in Files:  #leave the .dbf around so it can be appended
        if os.path.exists(theOF + theST + "_" + theFC + "." + theFile):
            os.remove(theOF + theST + "_" + theFC + "." + theFile)
    #append to the master table
    arcpy.Append_management([theOF + theST + "_" + theFC + ".dbf"],
                            "RandomPoint_" + theST, "NO_TEST")
    os.remove(theOF + theST + "_" + theFC + ".dbf")    
    del theStr, Files, theFile
    return ()

##Function sbdd_Overlay creates the overlay of the randpom 
##point and feature class
def sbdd_Overlay():
    arcpy.AddMessage("     Performing overlay")
    myFCs = ["myBuffer","myOverlay"]
    for FC in myFCs:
        if arcpy.Exists(FC):
            arcpy.Delete_management(FC)
    #buffer first
    #buffer the addres/road feature class 500'
    #create the random pt feature layer            
    arcpy.Buffer_analysis(theFD + theFC, "myBuffer", "500 FEET")      
    myLyr = theST + theFC
    theFIPS = sbdd_ReturnFIPS()
    #myQry = "state2 = '" + theFIPS + "'"
    myQry = "BLOCKID10 LIKE '" + theFIPS + "%'"
    arcpy.MakeFeatureLayer_management(theRndPT, myLyr, myQry)
    #create the overlay
    arcpy.AddMessage("      about to perform spatial join")
    #join the random points in that state to the buffer 
    arcpy.SpatialJoin_analysis(myLyr, "myBuffer", "myOverlay", \
                               "JOIN_ONE_TO_MANY", "KEEP_COMMON")
    if arcpy.Exists(myLyr):
        arcpy.Delete_management(myLyr)
    del myFCs, FC, myLyr, myQry, theFIPS
    return()

##Function sbdd_ExportToShape exports the created layers to 
##shapefiles in appropriate directories
def sbdd_CleanUp ():
    arcpy.AddMessage("     CleaningUp")
    theFCs = ["myBuffer","myOverlay"]
    for theFC in theFCs:
        if arcpy.Exists(theFC):
            arcpy.Delete_management(theFC)
    del theFC, theFCs
    return ()

##Function to the FIPS code based on the State abbreviation  
def sbdd_ReturnFIPS ():
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
        if theST == "WI":
            stFIPS = '55'
        if theST == "WY":
            stFIPS = '56'
        return(stFIPS)


#******************************************************************************
##################Main Code below
#******************************************************************************
try: 
    for theST in States:
        arcpy.AddMessage("the state is: " + theST)
        for theFC in theFCs:
            arcpy.AddMessage("  working on: " + theFC)
            theFD = theLocation + theST + "/" + theST + "_SBDD_" + theYear + "_"
            theFD = theFD + theMonth + "_" + theDay + ".gdb/NATL_Broadband_Map/"
            if arcpy.Exists(theFD + theFC) and int(arcpy.GetCount_management(theFD + theFC).getOutput(0)) > 0:
                if arcpy.Exists("RandomPoint_" + theST):
                    arcpy.AddMessage("    State table already created")
                else:
                    sbdd_CreateTable()
                sbdd_Overlay()
                #output the overlay just to a table, so it can be appended 
                sbdd_Append()
                #final cleanup
                sbdd_CleanUp()
            else:
                arcpy.AddMessage("     no features in: " + theFC)
    del theFD, theST, States, thePGDB, theFCs, theFC, theRndPT, theOF
    del theLocation, theYear, theMonth, theDay
except:
    arcpy.AddMessage("Something bad happened")

  
