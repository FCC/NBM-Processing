# ---------------------------------------------------------------------------
# SBDD_Append.py
# Created on: May 16, 2011 
# Created by: Michael Byrne
# Federal Communications Commission
# creates tables of unique combinations of fields by state
# ---------------------------------------------------------------------------

# Import system modules
import arcpy
from arcpy import env
import sys, string, os, math

#global variables
thePGDB = "C:/Users/michael.byrne/Processing.gdb"  #processing file geodatabase
arcpy.env.workspace = thePGDB

States = ["AK","AL","AR","AS","AZ","CA","CO","CT"]          #1
States = States + ["DC","DE","FL","GA","GU","HI","IA","ID"] #2
States = States + ["IL","IN","KS","KY","LA","MA","MD","ME"] #3 
States = States + ["MI","MN","MO","MP","MS","MT","NC","ND"] #4 
States = States + ["NE","NH","NJ","NM","NV","NY","OH","OK"] #5
States = States + ["OR","PA","PR","RI","SC","SD","TN","TX"] #6
States = States + ["UT","VA","VI","WA","WI","WV","WY"] #7"VT",


##write out functions
##Function sbdd_ExportToShape exports the created layers to shapefiles in appropriate directories
def sbdd_CleanUp (myTbl):
    if arcpy.Exists(myTbl):
        arcpy.AddMessage("     CleaningUp")
        arcpy.Delete_management(myTbl)
    del myTbl
    return ()

##Function to create the table which will contain all the overlay information
def sbdd_CreateTable (myTbl):
    arcpy.AddMessage("     Creating output table")
    if arcpy.Exists(myTbl):
        arcpy.Delete_management(myTbl)
    arcpy.CreateTable_management(thePGDB, myTbl)
    arcpy.AddField_management(myTbl, "FREQUENCY", "LONG", "", "", "15")
    arcpy.AddField_management(myTbl, "FRN", "TEXT", "", "", "10")
    arcpy.AddField_management(myTbl, "PROVNAME", "TEXT", "", "", "200")
    arcpy.AddField_management(myTbl, "DBANAME", "TEXT", "", "", "200")
    arcpy.AddField_management(myTbl, "TRANSTECH", "SHORT", "", "", "15")
    arcpy.AddField_management(myTbl, "MAXADDOWN", "TEXT", "", "", "2")
    arcpy.AddField_management(myTbl, "MAXADUP", "TEXT", "", "", "2")
    arcpy.AddField_management(myTbl, "TYPICDOWN", "TEXT", "", "", "2")
    arcpy.AddField_management(myTbl, "TYPICUP", "TEXT", "", "", "2")
    arcpy.AddField_management(myTbl, "STATE", "TEXT", "", "", "2")
#    arcpy.AddField_management(myTbl, "SPECTRUM", "SHORT", "", "", "2")
    del myTbl
    return ()

#*******************************************************************************************************
##################Main Code below
#*******************************************************************************************************
try:
    theFCs = ["BB_Service_Address","BB_Service_CensusBlock","BB_Service_RoadSegment","BB_Service_Wireless"] 
    for theFC in theFCs:
        sbdd_CleanUp(theFC)
        sbdd_CreateTable(theFC)
        for theST in States:
            if arcpy.Exists(theFC + "_" + theST + "_frq"):
                arcpy.AddMessage("     appending:" + theFC + "_" + theST + "_frq")
                arcpy.Append_management([theFC + "_" + theST + "_frq"], theFC, "NO_TEST")
    del theST, States, thePGDB, theFCs, theFC
except:
    arcpy.AddMessage("Something bad happened")

  
