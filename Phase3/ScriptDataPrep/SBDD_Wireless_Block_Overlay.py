# ---------------------------------------------------------------------------
# SBDD_Wireless_Block_Overlay.py
# Created on: May 16, 2011 
# Created by: Michael Byrne
# Federal Communications Commission
# performs the wireless polygon overlay
# ---------------------------------------------------------------------------

# Import system modules
import arcpy
from arcpy import env
import sys, string, os, math


#write out global variables
thePGDB = "C:/Users/Processing.gdb"
#thePGDB = "C:/Users/michael.byrne/Processing.gdb"  #processing file geodatabase
arcpy.env.workspace = thePGDB
theLocation = "C:/Users/NBMSource/Spring2012/"
#theLocation = "C:/Users/michael.byrne/NBMSource/Fall2011/"
theYear = "2012"
theMonth = "04"
theDay = "01"

States = ["AK","AL","AR","AS","AZ","CA","CO","CT"]          #1
States = States + ["DC","DE","FL","GA","GU","HI","IA","ID"] #2
States = States + ["IL","IN","KS","KY","LA","MA","MD","ME"] #3 
States = States + ["MI","MN","MO","MP","MS","MT","NC","ND"] #4 
States = States + ["NE","NH","NJ","NM","NV","NY","OH","OK"] #5
States = States + ["OR","PA","PR","RI","SC","SD","TN","TX"] #6
States = States + ["UT","VA","VI","VT","WA","WI","WV","WY"] #7

theBlockGDB = "C:/Users/SpatialData/Library/TabBlock_2010.gdb/"
#theBlockGDB = "C:/Users/michael.byrne/SpatialData/Library/TabBlock_2010.gdb/"

##write out functions
##Function sbdd_ExportToShape exports the created layers to shapefiles in
##appropriate directories
def blockIntersect():
    arcpy.AddMessage("     Begining overlay Processing")
    if arcpy.Exists("wireless_block_" + theST):
        arcpy.Delete_management("wireless_block_" + theST)
    theCnt = int(arcpy.GetCount_management(theFD + "BB_Service_Wireless").getOutput(0))
    theBlock = theBlockGDB + "Block_" + theST
    myCnt = 1
    if theCnt > 0:  #if there are records in the wireless shape class
        rows = arcpy.SearchCursor(theFD + "BB_Service_Wireless")
        for row in rows: #while  < theCnt:
            myID = row.getValue("OBJECTID")
            arcpy.AddMessage("     Performing overlay " + str(myCnt) + " of " + str(theCnt) + " and O-ID: " + str(myID))            
            myQry = "TRANSTECH <> 60 AND OBJECTID = " + str(myID)
            myLyr = theST + "NotSatellite" + str(myCnt)
            arcpy.MakeFeatureLayer_management (theFD + "BB_Service_Wireless", myLyr, myQry)
            if int(arcpy.GetCount_management(myLyr).getOutput(0)) > 0:  #there are no records in myLyr, it is a satellite record
                theOFC = "wireless_block_" + theST + "_" + str(myCnt)
                theOFCP = "wireless_block_" + theST + "_" + str(myCnt) + "_prj"
                myFCs = [theOFC, theOFCP]
                for myFC in myFCs:
                    if arcpy.Exists(myFC):
                        arcpy.Delete_management(myFC)
                arcpy.Intersect_analysis([myLyr, theBlock], theOFC)
                arcpy.Project_management(theOFC, theOFCP, "PROJCS['North_America_Albers_Equal_Area_Conic',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Albers'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-96.0],PARAMETER['Standard_Parallel_1',20.0],PARAMETER['Standard_Parallel_2',60.0],PARAMETER['Latitude_Of_Origin',40.0],UNIT['Meter',1.0]]", "NAD_1983_To_WGS_1984_1", "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]")
                arcpy.AddField_management(theOFCP, "PCT" ,"DOUBLE", "5" , "2", "")
                theExp = "([SHAPE_Area]) /( [ALAND10] + [AWATER10] )*100"
                arcpy.CalculateField_management(theOFCP, "PCT", theExp, "VB", "")
                arcpy.Delete_management(myLyr)
                if arcpy.Exists(theOFC):
                    arcpy.Delete_management(theOFC)
                myQry = "PCT > 100"
                myLyr = theST + "gtOne" + str(myCnt)
                arcpy.MakeFeatureLayer_management (theOFCP, myLyr, myQry)
                if int(arcpy.GetCount_management(myLyr).getOutput(0)) > 0:
                    arcpy.CalculateField_management(myLyr, "PCT", "100", "PYTHON", "")
                arcpy.Delete_management(myLyr)
                arcpy.CopyRows_management(theOFCP, theOFC)
                if arcpy.Exists(theOFCP):
                    arcpy.Delete_management(theOFCP)            
                del theExp, theOFCP, theOFC, myFC, myFCs
            myCnt = myCnt + 1
    del myLyr, myQry, theBlock, theCnt, myCnt, row, rows, myID
    return ()

#****************************************************************************
##################Main Code below
#****************************************************************************
try:
    for theST in States:
        theFD = theLocation + theST + "/" + theST + "_SBDD_" + theYear + "_"
        theFD = theFD + theMonth + "_" + theDay + ".gdb/NATL_Broadband_Map/"
        arcpy.AddMessage("the state is: " + theST)
        blockIntersect()
        #open a file to write when it finished
        outFile = "K:/Co-Share/Byrne/wireless_overlay_" + theST + ".txt"
        myFile = open(outFile, 'w')
        myFile.write(theST + ": finished\n")
        myFile.close()
    del theFD, theST, States
except:
    arcpy.AddMessage("Something bad happened")


  
