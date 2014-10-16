### ---------------------------------------------------------------------------
###   VERSION 1.1 (for ArcGIS 10.2)
### SBDD_CheckBlock.py
### Created on: Thurs June 20 13 2014
### Created by: Chris Gao
### Federal Communications Commission 
### ---------------------------------------------------------------------------
### check the census block id and write out the invalid ids to a file by state
### ---------------------------------------------------------------------------

# Import system modules
import sys, string, os, arcpy
from arcpy import env
import time
from datetime import date
from os import remove, close
today = date.today()

#acquire arguments
theLocation = "C:\\work\\nbbm\\2014_2\\gdb\\"
theYear = "2014"
theMonth = "10"
theDay = "01"
theBlockDb = "K:\\Projects\\Broadband Data\\NBM\\SpatialData\\Library\\TabBlock_2010.gdb"

States = ["AK","AL","AR","AS","AZ","CA","CO","CT"]          #1
States = States + ["DC","DE","FL","GA","GU","HI","IA","ID"] #2
States = States + ["IL","IN","KS","KY","LA","MA","MD","ME"] #3 
States = States + ["MI","MN","MO","MP","MS","MT","NC","ND"] #4 
States = States + ["NE","NH","NJ","NM","NV","NY","OH","OK"] #5
States = States + ["NE","NH","NJ","NM","NV","NY","OH","OK"] #5
States = States + ["OR","PA","PR","RI","SC","SD","TN","TX"] #6
States = States + ["UT","VA","VI","VT","WA","WI","WV","WY"] #7
#States = ["WV","IN"]

#set up variables
myFlag = 0

#write out functions

#Function sbdd_checkBlock checks the census block id provided
def sbdd_checkBlock (thePre, myFL, nameST):
    #check to see if check geometry has been run, if has not, run it
    
    arcpy.AddMessage("     Checking blcok id: " + myFL)
    #geoCnt = int(arcpy.GetCount_management(theFD + thePre + myFL).getOutput(0))
    #theFGDB = theFD.rstrip("NATL_Broadband_Map")
    #make a feature layer of the census block of that state
    arcpy.AddMessage("     thePre: " + thePre)
    arcpy.AddMessage("     theBlockDb: " + theBlockDb)
    arcpy.AddMessage(theBlockDb + "\\Block_" + nameST)
    arcpy.AddMessage("     nameST: " + nameST)
    arcpy.AddMessage(theFD + "\\" + thePre + myFL)
    
    
    env.overwriteOutput = True
    arcpy.MakeFeatureLayer_management ( theBlockDb + "\\Block_" + nameST, "block_layer")
    #make a layer of the SBI data:
    arcpy.MakeFeatureLayer_management ( theFD + "\\" + thePre + myFL, "feature_layer")
    #inFeatures = theFD + thePre + myFL
    inField = "FULLFIPSID"
    #joinTable = theBlockDb + "\\Block_" + nameST
    joinField = "GEOID10"
    #arcpy.AddMessage("      inFeatures: " + inFeatures)
    arcpy.AddMessage("      joinField: " + joinField)
    #arcpy.JoinField_management (inFeatures, inField, joinTable,joinField, joinField)
    arcpy.AddJoin_management("feature_layer",inField,"block_layer",joinField)
    geoidField = 'Block_'+nameST+'.GEOID10'
    fullfipsidField = thePre + myFL +'.FULLFIPSID'
    whereClause = geoidField + " IS NULL"
    arcpy.AddMessage("whereClause: " + whereClause)
    #arcpy.MakeFeatureLayer_management("feature_layer","ivBlockNo_layer", whereClause,"",fieldsInfo)
    #myCnt = int(arcpy.GetCount_management("ivBlockNo_layer").getOutput(0))
    #arcpy.AddMessage(" myCnt: " + myCnt.toString())
    #if myCnt > 0:
    #desc = arcpy.Describe("feature_layer")
    #field_info = desc.fieldInfo
    #arcpy.AddMessage(" find field: " + str(field_info.getFieldName(10)))
    
    fileName = theLocation + nameST + myFL + "IvBlockNo.txt"
    if os.path.exists(fileName):
         arcpy.AddMessage("check file")
         os.remove(fileName)
    fo = open(fileName,"w")
   
    #check nulls (using a search cursor to check null GEOID10, then insert the invalid FULLFIPSID into a text file
    
    
    fields = [geoidField,fullfipsidField]
    #with arcpy.da.SearchCursor("feature_layer",fields) as cursor:
    #cursor = arcpy.da.SearchCursor("feature_layer","","",fields)
    cursor = arcpy.SearchCursor("feature_layer",whereClause)
    #cursor = arcpy.SearchCursor("invalide_block_id_layer")
    row = cursor.next()
    while row:
    #for row in cursor:
        invalidFipsStr = row.getValue(fullfipsidField)
        arcpy.AddMessage("invalid fips: " + invalidFipsStr)
        fo.write(invalidFipsStr + "\n")
        row=cursor.next()
    fo.close()
    fileSize = str(os.path.getsize(fileName))
    arcpy.AddMessage("file size of " + fileName + " is: " + fileSize)    
    if os.path.getsize(fileName) == 0:
        os.remove(fileName)
    return ()


try: 
    for theST in States:
        arcpy.AddMessage("the state is: " + theST)
        ##check to see if field is added, if not add it
        ##populate field
        theFD =  theLocation + theST + "\\" + theST + "_SBDD_" + theYear + "_"
        theFD = theFD + theMonth + "_" + theDay + ".gdb\\NATL_Broadband_Map"
       
        #set the stateFIPS number
        #stFIPS = sbdd_setFIPS (theST)
        #check for BB_Service_CensusBlock
        theLyr = "CensusBlock"
        arcpy.AddMessage("Begining checks on Feature Class: " + theLyr)
        arcpy.AddMessage("theFD: " + theFD)
        #myFile = open(outFile, 'a')
        #myFile.write("" + "\n")
        #myFile.write("*Check Layer: " + theLyr + "\n")             
        #added by Chris
        sbdd_checkBlock("BB_Service_", theLyr,theST)
        
        #check for BB_Service_Address
        theLyr = "Address"
        arcpy.AddMessage("Begining checks on Feature Class: " + theLyr)
        
        sbdd_checkBlock("BB_Service_", theLyr,theST)

        #check for BB_Service_CAInstitutions
        theLyr = "CAInstitutions"
        arcpy.AddMessage("Begining checks on Feature Class: " + theLyr)
        
        sbdd_checkBlock("BB_Service_", theLyr,theST)

        #check for BB_ConnectionPoint_MiddleMile
        #theLyr = "MiddleMile"
        #arcpy.AddMessage("Begining checks on Feature Class: " + theLyr)
        
        #sbdd_checkBlock("BB_ConnectionPoint_", theLyr,theST)

       
except:
    arcpy.AddMessage("Something bad happened")
       
#if myFlag > 0:
    #arcpy.AddMessage("*********************************************")
    #arcpy.AddMessage("*********************WARNING*****************")
    #arcpy.AddMessage("It appears you have some data inegrity issues")
    #arcpy.AddMessage("1) Check the reciept file for a complete list")
    #arcpy.AddMessage("2) take appropriate corrective action")
    #arcpy.AddMessage("3) and rerun the Check_Submission process")
    #arcpy.AddMessage("*********************WARNING*****************")    
    #arcpy.AddMessage("*********************************************")
#if myFlag == 0:
    #arcpy.AddMessage("*****************************************************")
    #arcpy.AddMessage("*********************CONGRATULATIONS*****************")
    #arcpy.AddMessage("      It appears you have NO data inegrity issues")
    #arcpy.AddMessage("        this file is ready to submit to the FCC")
    #arcpy.AddMessage("*********************CONGRATULATIONS*****************")    
    #arcpy.AddMessage("*****************************************************")
#del myFlag

  
