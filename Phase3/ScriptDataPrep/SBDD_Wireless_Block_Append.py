# ---------------------------------------------------------------------------
# SBDD_Wireless_Block_Append.py
# Created on: May 16, 2011
# Created by: Michael Byrne
# Federal Communications Commission
# Appends the results of the Wireless Block overlay into State Tables
#
# ADDED END_USER_CAT field. 7/2/14 ES
# ---------------------------------------------------------------------------

# Import system modules
import arcpy
from arcpy import env
import sys, string, os, math

##Global Variables
#thePGDB = "C:/SpatialDATA/Spring2014/Processing_wireless.gdb"  #the Output Location
thePGDB = "C:/work/nbbm/2014_2/chkResult/wlOverlay/Processing_wireless.gdb"
arcpy.env.workspace = thePGDB
#theInFGDB = "C:/SpatialData/Spring2014/Processing.gdb/" #input file geodatabase
theInFGDB = "C:/work/nbbm/2014_2/chkResult/wlOverlay/Processing.gdb/"
States = ["AK","AL","AR","AS","AZ","CA","CO","CT"]#1
States = States + ["DC","DE","FL","GA","GU","HI","IA","ID"]#2
States = States + ["IL","IN","KS","KY","LA","MA","MD","ME"] #3
States = States + ["MI","MN","MO","MS","MT","NC","ND","MP"] #4
States = States + ["NE","NH","NJ","NM","NV","NY","OH","OK"] #5
States = States + ["OR","PA","PR","RI","SC","SD","TN","TX"] #6
States = States + ["UT","VA","VI","VT","WA","WI","WV","WY"] #7

theLocation = "C:/work/nbbm/2014_2/gdb/"
theYear = "2014"
theMonth = "10"
theDay = "01"

##write out functions
##Function sbdd_CreateTable defines a new state table into which all state records will be appended
def sbdd_CreateTable(myTbl):
    arcpy.AddMessage("  Creating output table:" + myTbl)
    if arcpy.Exists(myTbl):
        arcpy.Delete_management(myTbl)
    arcpy.CreateTable_management(thePGDB, myTbl)
    arcpy.AddField_management(myTbl, "GEOID10", "TEXT", "", "", "15")
    arcpy.AddField_management(myTbl, "PCT" ,"DOUBLE", "5" , "2", "")
    arcpy.AddField_management(myTbl, "FRN", "TEXT", "", "", "10")
    arcpy.AddField_management(myTbl, "PROVNAME", "TEXT", "", "", "200")
    arcpy.AddField_management(myTbl, "DBANAME", "TEXT", "", "", "200")
    arcpy.AddField_management(myTbl, "SPECTRUM", "SHORT", "", "", "15")
    arcpy.AddField_management(myTbl, "TRANSTECH", "SHORT", "", "", "15")
    arcpy.AddField_management(myTbl, "MAXADDOWN", "TEXT", "", "", "2")
    arcpy.AddField_management(myTbl, "MAXADUP", "TEXT", "", "", "2")
    arcpy.AddField_management(myTbl, "TYPICDOWN", "TEXT", "", "", "2")
    arcpy.AddField_management(myTbl, "TYPICUP", "TEXT", "", "", "2")
    arcpy.AddField_management(myTbl, "SBDD_ID", "TEXT", "", "", "20")
    arcpy.AddField_management(myTbl, "END_USER_CAT", "TEXT", "", "", "1")
    del myTbl
    return ()


##Function sbdd_AppendRecords appends records of each set to the state created table
def sbdd_AppendRecords(myTbl):
    arcpy.AddMessage("     Begining Append Processing")
    if arcpy.Exists(theFD + "BB_Service_Wireless"):
        theCnt = int(arcpy.GetCount_management(theFD + "BB_Service_Wireless").getOutput(0))
    else:
        arcpy.AddMessage("     the State has not been processed yet ...")
        theCnt = 1
    myCnt = 1
    while myCnt <= theCnt:
        inTbl = theInFGDB + "wireless_block_" + theST + "_" + str(myCnt)
        if arcpy.Exists(inTbl):
            arcpy.AddMessage("     Appending " + str(myCnt) + " of " + str(theCnt))
            arcpy.Append_management([inTbl], myTbl, "NO_TEST")
        myCnt = myCnt + 1
    del myTbl, theCnt, myCnt, inTbl

#****************************************************************************
##################Main Code below
#****************************************************************************
try:
    for theST in States:
        theFD =  theLocation + theST + "/" + theST + "_SBDD_" + theYear + "_"
        theFD = theFD + theMonth + "_" + theDay + ".gdb/NATL_Broadband_Map/"
        arcpy.AddMessage("the state is: " + theST)
        sbdd_CreateTable("wireless_block_overlay_" + theST)
        sbdd_AppendRecords(thePGDB + "/wireless_block_overlay_" + theST)
    del theST, States, thePGDB, theInFGDB
except:
    arcpy.AddMessage("Something bad happened")



