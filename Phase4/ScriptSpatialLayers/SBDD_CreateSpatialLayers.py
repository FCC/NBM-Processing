# ---------------------------------------------------------------------------
# SBDD_CreateSpatialLayers.py
# Created on: May 16, 2011
# Created by: Michael Byrne
# Federal Communications Commission
# creates the individual layers necessary for the
# National Broadband Map from the source file geodatabases
# requires one State submission at a time
#
# Updated to Add EndUserCat and Provider_Type on export 7/3/14 ES/CG.
# ---------------------------------------------------------------------------

# Import system modules
import arcpy
from arcpy import env
import sys, string, os, math

#Write out variables
thePGDB = "C:/SpatialDATA/Spring2014/Processing2.gdb"
theOF = "C:/SpatialDATA/Spring2014/export/Shape/"

States = ["AK","AL","AR","AS","AZ","CA","CO","CT"]          #1
States = States + ["DC","DE","FL","GA","GU","HI","IA","ID"] #2
States = States + ["IL","IN","KS","KY","LA","MA","MD","ME"] #3
States = States + ["MI","MN","MO","MS","MT","NC","ND","MP"] #4
States = States + ["NE","NH","NJ","NM","NV","NY","OH","OK"] #5
States = States + ["OR","PA","PR","RI","SC","SD","TN","TX"] #6
States = States + ["UT","VA","VI","VT","WA","WI","WV","WY"] #7
##States = ["DC"]


theLocation = "C:/SpatialDATA/Spring2014/"
theYear = "2014"
theMonth = "04"
theDay = "01"

doAddress = "No" #Yes
doBlock = "No" #Yes
doCAI = "No"  #Yes
doMM = "No" #Yes
doRoad = "No" #Yes
doWireless = "Yes" #Yes

##write out functions
##Function sbdd_ProcessCAI prepares the CAI export
def sbdd_ProcessCAI (myFD, myFL):
    arcpy.AddMessage("     Begining CAI Processing")
    if arcpy.Exists("CAI"):
        arcpy.Delete_management("CAI")
    if int(arcpy.GetCount_management(myFD + "/" + myFL).getOutput(0)) > 0:
        arcpy.Copy_management(myFD + "/" + myFL, "CAI")
        arcpy.AddMessage("          Repairing geometry ...")
        arcpy.RepairGeometry_management("CAI")
    else:
        arcpy.AddMessage("          Nothing to do ...")
    sbdd_ExportToShape("CAI")
    del myFD, myFL
    return ()

##Function sbdd_ProcessCAI prepares the MiddleMile export
def sbdd_ProcessMM (theFD, theFL):
    arcpy.AddMessage("     Begining MiddleMile Processing")
    if arcpy.Exists("MiddleMile"):
        arcpy.Delete_management("MiddleMile")
    if int(arcpy.GetCount_management(theFD + "/" + theFL).getOutput(0)) > 0:
        arcpy.Copy_management(theFD + "/" + theFL, "MiddleMile")
    sbdd_ExportToShape("MiddleMile")
    del theFD, theFL
    return ()

##Function sbdd_BlockDissolve creates a dissolve of the block layer
##works on the Block layer only
def sbdd_ProcessBlock (myFD, myFL):
    arcpy.AddMessage("     Begining Block Processing")
    theFields = ["FRN","PROVNAME","DBANAME","FULLFIPSID","TRANSTECH","MAXADDOWN","MAXADUP",
                 "TYPICDOWN","TYPICUP","Provider_Type","EndUserCat"]
    if arcpy.Exists("Block"):
        arcpy.Delete_management("Block")
    if arcpy.Exists(myFD + "/" + myFL): #its ok to process
        myFLName = myFL + theST
        theQ = "(MAXADDOWN = '3' OR MAXADDOWN = '4' OR MAXADDOWN = '5' OR MAXADDOWN = '6' OR " + \
               " MAXADDOWN = '7' OR MAXADDOWN = '8' OR MAXADDOWN = '9' OR MAXADDOWN = '10' OR MAXADDOWN = '11') AND " + \
               "(MAXADUP = '2' OR MAXADUP = '3' OR MAXADUP = '4' OR MAXADUP = '5' OR MAXADUP = '6' OR " + \
               " MAXADUP = '7' OR MAXADUP = '8' OR MAXADUP = '9' OR MAXADUP = '10' OR MAXADUP = '11' )"
        arcpy.MakeFeatureLayer_management(myFD + "/" + myFL, myFLName, theQ)
        arcpy.Dissolve_management(myFLName, "Block", theFields)
        arcpy.Delete_management(myFLName)
        arcpy.AddMessage("          Repairing geometry ...")
        arcpy.RepairGeometry_management("Block")
        sbdd_ExportToShape("Block")
        del theQ, myFLName
    del theFields, myFL, myFD
    return ()

##Function sbdd_ProcessRoad performs the buffer and multi to single
##part conversion for Roads or address point features
def sbdd_ProcessRoad (myFD, myFL):
    arcpy.AddMessage("     Begining Road Processing")
    theFields = ["FRN","PROVNAME","DBANAME","FULLFIPSID","TRANSTECH","MAXADDOWN","MAXADUP",
                 "TYPICDOWN","TYPICUP","Provider_Type","EndUserCat"]
    if arcpy.Exists("Road"):
        arcpy.Delete_management("Road")
    if int(arcpy.GetCount_management(myFD + "/" + myFL).getOutput(0)) > 0:
        myFLName = myFL + theST
        theQ = "(MAXADDOWN = '3' OR MAXADDOWN = '4' OR MAXADDOWN = '5' OR MAXADDOWN = '6' OR " + \
               " MAXADDOWN = '7' OR MAXADDOWN = '8' OR MAXADDOWN = '9' OR MAXADDOWN = '10' OR MAXADDOWN = '11') AND " + \
               "(MAXADUP = '2' OR MAXADUP = '3' OR MAXADUP = '4' OR MAXADUP = '5' OR MAXADUP = '6' OR " + \
               " MAXADUP = '7' OR MAXADUP = '8' OR MAXADUP = '9' OR MAXADUP = '10' OR MAXADUP = '11' )"
        arcpy.MakeFeatureLayer_management(myFD + "/" + myFL, myFLName, theQ)
        arcpy.Buffer_analysis(myFLName, "Road", "500 Feet", "FULL", "ROUND", "LIST", theFields)
        arcpy.Delete_management(myFLName)
        del theQ, myFLName
        arcpy.AddMessage("          Repairing geometry ...")
        #arcpy.RepairGeometry_management("Road")
        sbdd_ExportToShape("Road")
    del theFields, myFD, myFL
    return ()

##Function sbdd_ProcessWireless prepares the CAI export
def sbdd_ProcessWireless (myFD, myFL):
    arcpy.AddMessage("     Begining Wireless Processing")
    ##theFields = ["FRN","PROVNAME","DBANAME","TRANSTECH","MAXADDOWN","MAXADUP",
    ##             "TYPICDOWN","TYPICUP","EndUserCat","SPECTRUM"]
    if arcpy.Exists("Wireless"):
        arcpy.Delete_management("Wireless")

    if int(arcpy.GetCount_management(myFD + "/" + myFL).getOutput(0)) > 0:
        myFLName = myFL + theST
        theQ = "(MAXADDOWN = '3' OR MAXADDOWN = '4' OR MAXADDOWN = '5' OR MAXADDOWN = '6' OR " + \
               " MAXADDOWN = '7' OR MAXADDOWN = '8' OR MAXADDOWN = '9' OR MAXADDOWN = '10' OR MAXADDOWN = '11') AND " + \
               "(MAXADUP = '2' OR MAXADUP = '3' OR MAXADUP = '4' OR MAXADUP = '5' OR MAXADUP = '6' OR " + \
               " MAXADUP = '7' OR MAXADUP = '8' OR MAXADUP = '9' OR MAXADUP = '10' OR MAXADUP = '11' )"
        arcpy.MakeFeatureLayer_management(myFD + "/" + myFL, myFLName, theQ)
        arcpy.CopyFeatures_management(myFLName, "Wireless")
        arcpy.Delete_management(myFLName)
        arcpy.AddMessage("          Repairing geometry ...")
        arcpy.RepairGeometry_management("Wireless")
        sbdd_ExportToShape("Wireless")
        del myFLName, theQ
    del myFD, myFL
    return ()

##Function sbdd_ProcessAddress performs the address layer processing
##address point features
##this is a complicated process of creating individual multi-part polygons for
##unique cominations of FRN, DBANAME,PROVNAME, TRANSTECH, MAXADUP and MAXADDOWN
##for each combination, we point raster the data to develop a single 'buffered'
##layer to get around the complications arising from the ArcGIS buffer command
##and issues relating to too complicated geographies and dissolve
##the for each loop is then appended to a master set of features
def sbdd_ProcessAddress (myFD, myFL):
    arcpy.AddMessage("     Begining Address Processing")
    theFields = ["FRN","PROVNAME","DBANAME","FULLFIPSID","TRANSTECH","MAXADDOWN","MAXADUP",
                 "TYPICDOWN","TYPICUP","Provider_Type","EndUserCat"]
    chkFC = ["Address_frq","Address"]
    for cFC in chkFC:
        if arcpy.Exists(cFC):
            arcpy.Delete_management(cFC)
    if int(arcpy.GetCount_management(myFD + "/" + myFL).getOutput(0)) > 1:
        arcpy.Frequency_analysis(myFD + "/" + myFL, "Address" + "_frq", theFields, "")
        #open a cursor loop to get all the distinct values
        myCnt = 1
        theQ = "(MAXADDOWN = '3' OR MAXADDOWN = '4' OR MAXADDOWN = '5' OR MAXADDOWN = '6' OR " + \
               " MAXADDOWN = '7' OR MAXADDOWN = '8' OR MAXADDOWN = '9' OR MAXADDOWN = '10' OR MAXADDOWN = '11') AND " + \
               "(MAXADUP = '2' OR MAXADUP = '3' OR MAXADUP = '4' OR MAXADUP = '5' OR MAXADUP = '6' OR " + \
               " MAXADUP = '7' OR MAXADUP = '8' OR MAXADUP = '9' OR MAXADUP = '10' OR MAXADUP = '11' )"
        for row in arcpy.SearchCursor("Address" + "_frq", theQ):
            theProvName = row.getValue("PROVNAME").replace("'","")
            theDBA = row.getValue("DBANAME").replace("'","")
            theFRN = row.getValue("FRN")
            theTransTech = row.getValue("TRANSTECH")
            theAdUp = row.getValue("MAXADUP")
            theAdDown = row.getValue("MAXADDOWN")
            theTyUp = row.getValue("TYPICUP")
            theTyDown = row.getValue("TYPICDOWN")
            theTyUpQ = ""
            theTyDownQ = ""
            if theTyUp == "ZZ":
                theTyUp = "ZZ"  #used for naming / logic on calculating
                theTyUpQ = "TYPICUP = 'ZZ'"  #used as a selection set
            elif theTyUp == None:
                theTyUp = "IsNull"  #used for naming / logic on calculating
                theTyUpQ = "TYPICUP Is Null"  #used as a selection set
            elif theTyUp == " ":
                theTyUp = "IsNull"
                theTyUpQ = "TYPICUP = ' '"
            else:
                theTyUp = str(abs(int(theTyUp)))
                theTyUpQ = "TYPICUP = '" + theTyUp + "'"
            if theTyDown == "ZZ":
                theTyDown = "ZZ"  #used for naming / logic on calculating
                theTyDownQ = "TYPICDOWN = 'ZZ'"  #used as a selection set
            elif theTyDown == None:
                theTyDown = "IsNull"
                theTyDownQ = "TYPICDOWN Is Null"
            elif theTyDown == " ":
                theTyDown = "IsNull"
                theTyDownQ = "TYPICDOWN = ' '"
            else:
                theTyDown = str(abs(int(theTyDown)))
                theTyDownQ = "TYPICDOWN = '" + theTyDown + "'"
            theQry = "FRN = '" + theFRN + "'"
            theQry = theQry + " AND TRANSTECH = " + str(theTransTech)
            theQry = theQry + " AND MAXADDOWN = '" + theAdDown + "' AND MAXADUP = '"
            theQry = theQry + theAdUp + "' AND " + theTyUpQ + " AND " + theTyDownQ
            myFLName = theFRN + str(theTransTech) + theAdUp + theAdDown + theTyUp + theTyDown
            arcpy.MakeFeatureLayer_management(myFD + "/" + myFL, myFLName, theQry)
            if int(arcpy.GetCount_management(myFLName).getOutput(0)) > 0 :  #originally 1 for the raster case
                outPT = theST + theFRN + "_" + str(theTransTech) + "_" + theAdDown + "_" + \
                        theAdUp + "_" + theTyDown + "_" + theTyUp + "_x" #the selection of points
                outRT = theST + theFRN + "_" + str(theTransTech) + "_" + theAdDown + "_" + \
                        theAdUp + "_" + theTyDown + "_" + theTyUp + "_g" #the raster grid
                inPly = theST + theFRN + "_" + str(theTransTech) + "_" + theAdDown + "_" + \
                        theAdUp + "_" + theTyDown + "_" + theTyUp + "_p" #the output of grid poly
                bfPly = theST + theFRN + "_" + str(theTransTech) + "_" + theAdDown + "_" + \
                        theAdUp + "_" + theTyDown + "_" + theTyUp + "_pb" #the output of buffer
                chkFC = [outPT, outRT, inPly, bfPly]
                for cFC in chkFC:
                    if arcpy.Exists(cFC):
                        arcpy.Delete_management(cFC)
                del cFC, chkFC
                #first create a feature class of the selected points
                arcpy.FeatureClassToFeatureClass_conversion(myFLName, thePGDB, outPT)
                arcpy.RepairGeometry_management(outPT)
                arcpy.Delete_management(myFLName)
                if int(arcpy.GetCount_management(outPT).getOutput(0)) > 50:
                    arcpy.AddMessage("          processing by raster point: " + outPT)
                    #second covert the selection to a grid data set (e.g. raster)
                    arcpy.PointToRaster_conversion(outPT, "FRN", outRT, "", "", 0.0028)
                    theH = arcpy.Describe(outRT).Height
                    theW = arcpy.Describe(outRT).Width
                    if int(theH) > 2 and int(theW) > 2:
                        #third convert the rasters back to a polygon
                        arcpy.RasterToPolygon_conversion(outRT, inPly, "NO_SIMPLIFY", "")
                        arcpy.AddField_management (inPly, "FRN", "TEXT", "", "", 10)
                        arcpy.AddField_management (inPly, "PROVNAME", "TEXT", "", "", 200)
                        arcpy.AddField_management (inPly, "DBANAME", "TEXT", "", "", 200)
                        arcpy.AddField_management (inPly, "TRANSTECH", "SHORT", "", "", "")
                        arcpy.AddField_management (inPly, "MAXADDOWN", "TEXT", "", "", 2)
                        arcpy.AddField_management (inPly, "MAXADUP", "TEXT", "", "", 2)
                        arcpy.AddField_management (inPly, "TYPICDOWN", "TEXT", "", "", 2)
                        arcpy.AddField_management (inPly, "TYPICUP", "TEXT", "", "", 2)
                        arcpy.AddField_management (inPly, "State", "TEXT", "", "", 2)
                        arcpy.CalculateField_management(inPly, "FRN", "'" + theFRN + "'" ,"PYTHON")
                        arcpy.CalculateField_management(inPly, "PROVNAME", r"'" + theProvName + "'" ,"PYTHON")
                        arcpy.CalculateField_management(inPly, "DBANAME", r"'" + theDBA + "'" ,"PYTHON")
                        arcpy.CalculateField_management(inPly, "TRANSTECH", theTransTech, "PYTHON")
                        arcpy.CalculateField_management(inPly, "MAXADDOWN", "'" + theAdDown + "'" ,"PYTHON")
                        arcpy.CalculateField_management(inPly, "MAXADUP", "'" + theAdUp + "'" ,"PYTHON")
                        if theTyDown <> "IsNull":
                            arcpy.CalculateField_management(inPly, "TYPICDOWN", "'" + theTyDown + "'" ,"PYTHON")
                        if theTyUp <> "IsNull":
                            arcpy.CalculateField_management(inPly, "TYPICUP", "'" + theTyUp + "'" ,"PYTHON")
                        arcpy.CalculateField_management(inPly, "State", "'" + theST + "'" ,"PYTHON")
                        arcpy.Buffer_analysis(inPly, bfPly, "100 Feet", "FULL", "ROUND", "LIST", theFields)
                        if myCnt == 1:  #this is the first time through, rename the bfPly to Address
                            arcpy.Rename_management(bfPly,"Address")
                        else: #otherwise append it to the first one through
                            arcpy.Append_management([bfPly], "Address")
                    del theH, theW
                #then buffer them
                else:
                    arcpy.AddMessage("          processing by buffering: " + outPT)
                    arcpy.Buffer_analysis(outPT, bfPly, "500 Feet", "FULL", "ROUND", "LIST", theFields)
                    if myCnt == 1:  #this is the first time through, rename the bfPly to Address
                        arcpy.Rename_management(bfPly,"Address")
                    else: #otherwise append it to the first one through
                        arcpy.Append_management([bfPly], "Address")
                chkFC = [outPT, outRT, inPly, bfPly]
                for cFC in chkFC:
                    if arcpy.Exists(cFC):
                        arcpy.Delete_management(cFC)
                del outPT, outRT, inPly, bfPly, cFC, chkFC
                myCnt = myCnt + 1
            del theProvName, theDBA, theFRN, theTransTech, theAdUp, theAdDown, theTyUp, \
                theTyUpQ, theTyDown, theTyDownQ, theQry, myFLName
        sbdd_ExportToShape("Address")
        arcpy.Delete_management("Address_frq")
        del row, myCnt, theFields, theQ, myFL, myFD
    return ()

##Function sbdd_ExportToShape exports the created layers to shapefiles in
##appropriate directories
def sbdd_ExportToShape (myFC):
    if arcpy.Exists(theOF + myFC + "/" + myFC + ".shp"):
        arcpy.Delete_management(theOF + myFC + "/" + myFC + ".shp")
    if arcpy.Exists(theOF + myFC + "/" + theST + "_" + myFC + ".shp"):
        arcpy.Delete_management(theOF + myFC + "/" + theST + "_" +
                                myFC + ".shp")
    if arcpy.Exists(myFC):  #then export it
        arcpy.AddMessage("          Exporting " + myFC)
        if myFC == "Wireless":
            arcpy.DeleteField_management(myFC, "STATEABBR")
            arcpy.DeleteField_management(myFC, "SBDD_ID")
        arcpy.FeatureClassToShapefile_conversion(myFC, theOF + myFC)
        arcpy.Rename_management(theOF + myFC + "/" + myFC + ".shp", theOF +
                                myFC + "/" + theST + "_" + myFC + ".shp")
    del myFC
    return ()

##Function sbdd_ExportToShape exports the created layers to shapefiles in
##appropriate directories
def sbdd_CleanUp ():
    arcpy.AddMessage("     CleaningUp")
    theFCs = ["Address","Block","CAI","Road","Wireless"]
    for theFC in theFCs:
        if arcpy.Exists(theFC):
            arcpy.Delete_management(theFC)
    del theFC, theFCs
    return ()

#*******************************************************************************
##################Main Code below
#*******************************************************************************
try:
    for theST in States:
        if arcpy.Exists(thePGDB):
            arcpy.AddMessage("Begining process")
        else:
            arcpy.AddMessage("File Geodatabase " + thePGDB + " doesn't exist.  exiting..." )
        arcpy.AddMessage("the state is: " + theST)
        theFD = theLocation + theST + "/" + theST + "_SBDD_"
        theFD = theFD + theYear + "_" + theMonth + "_" + theDay
        theFD = theFD + ".gdb/NATL_Broadband_Map/"
        arcpy.env.workspace = thePGDB
        if arcpy.Exists(theFD):
            #prepare Address
            if doAddress == "Yes":
                sbdd_ProcessAddress(theFD, "BB_Service_Address")
            #prepare Blocks
            if doBlock == "Yes":
                sbdd_ProcessBlock(theFD, "BB_Service_CensusBlock")
            #prepapre CAI
            if doCAI == "Yes":
                sbdd_ProcessCAI(theFD, "BB_Service_CAInstitutions")
            #prepapre MiddleMile; this one is only done on request
            if doMM == "Yes":
                sbdd_ProcessMM(theFD, "BB_ConnectionPoint_MiddleMile")
            #prepare Roads
            if doRoad == "Yes":
                sbdd_ProcessRoad(theFD, "BB_Service_RoadSegment")
            #prepapre Wireless
            if doWireless == "Yes":
                sbdd_ProcessWireless(theFD, "BB_Service_Wireless")
            #CleanUp
            sbdd_CleanUp()
    del theFD, theST, States, theOF, thePGDB
    del doAddress, doBlock, doCAI, doRoad, doWireless, doMM
except:
    arcpy.AddMessage("Something bad happened")


