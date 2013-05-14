# ---------------------------------------------------------------------------
#   VERSION 0.1 (for ArcGIS 10)
# SBDD_CleanData.py
# Created on: Thurs Sept 29 2011 
# Created by: Michael Byrne
# Federal Communications Commission
# checks to make sure the export data going to computech is clean
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

def sbdd_qry (theFL, myFL, myQry, myField):
        arcpy.AddMessage("       Checking for unexpected values: " + myFL)
        #you will need to edits this to make the read in feature dbfs and make tableview
        #MakeTableView_management (in_table, out_view, {where_clause}, {workspace}, {field_info})
        arcpy.MakeFeatureLayer_management(theFL, myFL, myQry)
        myCnt = int(arcpy.GetCount_management(myFL).getOutput(0))
        if myCnt > 0: #exception occurred            
                myStr = str(myCnt) #"FAILED"
                if myField == "TYPICUP":
                        theExp = "'0'"
                	arcpy.CalculateField_management(myFL,"TYPICUP" ,theExp, "PYTHON")
                #if TYPICDOWN, then calc typicdown to 0
                if myField == "TYPICDOWN":
                	theExp = "'0'"
                	arcpy.CalculateField_management(myFL,"TYPICDOWN" ,theExp, "PYTHON")
                #if FRN_SPACE
                if myField == "FRN_SPACE":
                	theExp = "!FRN!.strip(' ')"
                	arcpy.CalculateField_management(myFL,"FRN" ,theExp, "PYTHON")
                #if FULLFIPSID_SPACE
                if myField == "FULLFIPSID_SPACE":
                	theExp = "!FULLFIPSID!.strip(' ')"
                	arcpy.CalculateField_management(myFL,"FULLFIPSID" ,theExp, "PYTHON")
                #if DBANANME_SPACE
                if myField == "DBANAME_SPACE":
                	theExp = "!DBANAME!.strip(' ')"
                	arcpy.CalculateField_management(myFL,"DBANAME" ,theExp, "PYTHON_9.3")
                #if PROVNAME_SPACE
                if myField == "PROVNAME_SPACE":
                	theExp = "!PROVNAME!.strip(' ')"
                	arcpy.CalculateField_management(myFL,"PROVNAME" ,theExp, "PYTHON")
                #if TRANSTECH_SPACE
                if myField == "TRANSTECH_SPACE":
                	theExp = "!TRANSTECH!.strip(' ')"
                	arcpy.CalculateField_management(myFL,"TRANSTECH" ,theExp, "PYTHON")            
                #if MAMAXADDOWN_SPACE
                if myField == "MAMAXADDOWN_SPACE":
                	theExp = "!MAMAXADDOWN!.strip(' ')"
                	arcpy.CalculateField_management(myFL,"MAMAXADDOWN" ,theExp, "PYTHON")                 
                #if MAXADUP_SPACE
                if myField == "MAMAXADUP_SPACE":
                	theExp = "!MAMAXADUP!.strip(' ')"
                	arcpy.CalculateField_management(myFL,"MAMAXADUP" ,theExp, "PYTHON")  
                #if TYPICDOWN_SPACE
                if myField == "TYPICDOWN_SPACE":
                	theExp = "!TYPICDOWN!.strip(' ')"
                	arcpy.CalculateField_management(myFL,"TYPICDOWN" ,theExp, "PYTHON")
                #if TYPICUP_SPACE
                if myField == "TYPICUP_SPACE":
                	theExp = "!TYPICUP!.strip(' ')"
                	arcpy.CalculateField_management(myFL,"TYPICUP" ,theExp, "PYTHON")                
                #if SPECTRUM_SPACE
                if myField == "SPECTRUM_SPACE":
                	theExp = "!SPECTRUM!.strip(' ')"
                	arcpy.CalculateField_management(myFL,"SPECTRUM" ,theExp, "PYTHON") 
                #if STATECODE_SPACE                
                if myField == "STATECODE_SPACE":
                	theExp = "!STATECODE!.strip(' ')"
                	arcpy.CalculateField_management(myFL,"STATECODE" ,theExp, "PYTHON") 
        else:
                myStr = "passed"
        arcpy.Delete_management(myFL)
        del myCnt, theFL, myFL, myQry
        return ("," + myStr) 


#sbdd_qryDef writes out the definitions for the queries, since these are used
##multiple times
def sbdd_qryDef (myField):

     if myField == "FULLFIPSID":
          theQry = "FULLFIPSID Is Null OR (CHAR_LENGTH(FULLFIPSID) <> 15)"
     if myField == "FRN":
          theQry = "FRN Is Null OR (CHAR_LENGTH(FRN) <> 10 AND FRN <> '9999')"
     if myField == "PROVNAME":
          theQry = "PROVNAME Is Null"
     if myField == "DBANAME":
          theQry = "DBANAME Is Null"
     if myField == "TRANSTECH":
          theQry = "TRANSTECH IS NULL OR (TRANSTECH <> 10 AND TRANSTECH <> 20 AND "
          theQry = theQry + "TRANSTECH <> 30 AND TRANSTECH <> 40 AND TRANSTECH "
          theQry = theQry + "<> 41 AND TRANSTECH <> 50 AND TRANSTECH <> 60 AND "
          theQry = theQry + "TRANSTECH <> 70 AND TRANSTECH <> 71 AND TRANSTECH <> "
          theQry = theQry + "80 AND TRANSTECH <> 90 )"
     if myField == "MAXADDOWN":
          theQry = "MAXADDOWN IS NULL OR (MAXADDOWN <> '3' AND MAXADDOWN <> '4' AND "
          theQry = theQry + "MAXADDOWN <> '5' AND MAXADDOWN <> '6' AND MAXADDOWN <> "
          theQry = theQry + "'7' AND MAXADDOWN <> '8' AND MAXADDOWN <> '9' "
          theQry = theQry + "AND MAXADDOWN <> '10' AND MAXADDOWN <> '11' )"
     if myField == "MAXADUP":
          theQry = "MAXADUP IS NULL OR (MAXADUP <> '2' AND MAXADUP <> '3' AND "
          theQry = theQry + "MAXADUP <> '4' AND MAXADUP <> '5' AND MAXADUP <> '6' "
          theQry = theQry + "AND MAXADUP <> '7' AND MAXADUP <> '8' AND MAXADUP "
          theQry = theQry + " <> '9' AND MAXADUP <> '10' AND MAXADUP <> '11' )"
     if myField == "TYPICDOWN":
          theQry = "TYPICDOWN IS NULL OR (TYPICDOWN <> '0' AND TYPICDOWN <> '1'AND TYPICDOWN <> "
          theQry = theQry + "'2' AND TYPICDOWN <> '3' AND TYPICDOWN <> '4' AND TYPICDOWN <> "
          theQry = theQry + "'5' AND TYPICDOWN <> '6' AND TYPICDOWN <> '7' AND TYPICDOWN <> "
          theQry = theQry + "'8' AND TYPICDOWN <> '9' AND TYPICDOWN <> '10' AND TYPICDOWN <> "
          theQry = theQry + "'11')"
     if myField == "TYPICUP":
          theQry = "TYPICUP IS NULL OR (TYPICUP <> '0' AND TYPICUP <> '1'AND TYPICUP <> "
          theQry = theQry + "'2' AND TYPICUP <> '3' AND TYPICUP <> '4' AND TYPICUP <> "
          theQry = theQry + "'5' AND TYPICUP <> '6' AND TYPICUP <> '7' AND TYPICUP <> "
          theQry = theQry + "'8' AND TYPICUP <> '9' AND TYPICUP <> '10' AND TYPICUP <> '11')"
     if myField == "STATEFIPS":
          theQry = "STATEFIPS Is Null OR (CHAR_LENGTH(STATEFIPS) <> 2 )"
     #write query for space before or after fields
     if myField == "FRN_SPACE":
          theQry = "FRN like '% ' OR FRN LIKE ' %'"
     if myField == "FULLFIPSID_SPACE":
          theQry = "FULLFIPSID like '% ' OR FULLFIPSID LIKE ' %'"
     if myField == "DBAName_SPACE":
          theQry = "DBAName like '% ' OR DBANAME LIKE ' %'"
     if myField == "PROVNAME_SPACE":
          theQry = "PROVNAME like '% ' OR PROVNAME LIKE ' %'"
     if myField == "TRANSTECH_SPACE":
          theQry = "TRANSTECH like '% ' OR TRANSTECH LIKE ' %'"
     if myField == "MAMAXADDOWN_SPACE":
          theQry = "MAMAXADDOWN like '% ' OR MAXADDOWN LIKE ' %'"
     if myField == "MAXADUP_SPACE":
          theQry = "MAXADUP like '% ' OR MAXADUP LIKE ' %'"
     if myField == "TYPICDOWN_SPACE":
          theQry = "TYPICDOWN like '% ' OR TYPICDOWN LIKE ' %'"
     if myField == "TYPICUP_SPACE":
          theQry = "TYPICUP like '% ' OR TYPICUP LIKE ' %'"
     if myField == "SPECTRUM":
          theQry = "SPECTRUM IS NULL OR (SPECTRUM <> 1 AND SPECTRUM <> 2 "
          theQry = theQry + "SPECTRUM <> 3 AND SPECTRUM <> 4 AND SPECTRUM "
          theQry = theQry + "<> 5 AND SPECTRUM <> 6 AND SPRCTRUM <> 7 "
          theQry = theQry + "SPECTRUM <> 8 AND SPECTRUM <> 9 AND "
          theQry = theQry + "SPECTRUM <> 10)"
     if myField == "SPECTRUM_SPACE":
          theQry = "SPECTRUM like '% ' OR SPECTRUM LIKE ' %'"
     if myField == "STATEABBR":
          theQry = "STATEABBR Is Null OR (CHAR_LENGTH(STATEABBR) <> 2)"
     if myField == "STATECODE":
          theQry = "STATECODE Is Null OR (CHAR_LENGTH(STATECODE) <> 2)"
     if myField == "STATECODE_SPACE":
          theQry = "STATECODE LIKE '% ' OR STATECODE LIKE ' %'"
     return(theQry)

##
##******************************************************************************
##  MAIN CODE ENGINE


try:
     #think about putting a loop in for type
     ##insert code for each state loop
     for theST in States:
          #Create Reciept/file variables
          theOFCB = theLocation + "CensusBlock_CleanData_" + theST + "_" + theYear + theMonth + ".csv"
          theOFAd = theLocation + "Address_CleanData_" + theST + "_" + theYear + theMonth + ".csv"
          theOFRd = theLocation + "RoadSegment_CleanData_" + theST + "_" + theYear + theMonth + ".csv"
          theOFWS = theLocation + "Wireless_CleanData_" + theST + "_" + theYear + theMonth + ".csv"
          theOFCAI = theLocation + "CAI_CleanData_" + theST + "_" + theYear + theMonth + ".csv"
          #set up output file
          ##you are going to write out 4 files; one for each feature class
          myFile = open(theOFCB, 'w')  #CensusBlock
          myFile.write("State,FullFIPSID,FRN,PROVNAME,DBANAME,TRANSTECH," +
                       "MAXADDOWN,MAXADUP,TYPICDOWN,TYPICUP,STATEFIPS," +
                       "FRN_SPACE,FULLFIPSID_SPACE,DBAName_SPACE,PROVNAME_SPACE," +
                       "TRANSTECH_SPACE,MAXADDOWN_SPACE,MAXADUP_SPACE," +
                       "TYPICDOWN_SPACE,TYPICUP_SPACE," + "\n")

          myFile = open(theOFAd, 'w')  #Address
          myFile.write("State,FullFIPSID,FRN,PROVNAME,DBANAME,TRANSTECH," +
                       "MAXADDOWN,MAXADUP,TYPICDOWN,TYPICUP,STATEFIPS," +
                       "FRN_SPACE,FULLFIPSID_SPACE,DBAName_SPACE,PROVNAME_SPACE," +
                       "TRANSTECH_SPACE,MAXADDOWN_SPACE,MAXADUP_SPACE," +
                       "TYPICDOWN_SPACE,TYPICUP_SPACE,STATECODE,STATECODE_SPACE" + "\n")

          myFile = open(theOFRd, 'w')  #RoadSegment
          myFile.write("State,FullFIPSID,FRN,PROVNAME,DBANAME,TRANSTECH," +
                       "MAXADDOWN,MAXADUP,TYPICDOWN,TYPICUP,STATEFIPS," +
                       "FRN_SPACE,FULLFIPSID_SPACE,DBAName_SPACE,PROVNAME_SPACE," +
                       "TRANSTECH_SPACE,MAXADDOWN_SPACE,MAXADUP_SPACE," +
                       "TYPICDOWN_SPACE,TYPICUP_SPACE,STATECODE,STATECODE_SPACE" + "\n")

          myFile = open(theOFWS, 'w')  #Wireless
          myFile.write("State,FullFIPSID,FRN,PROVNAME,DBANAME,TRANSTECH," +
                       "MAXADDOWN,MAXADUP,TYPICDOWN,TYPICUP,STATEFIPS," +
                       "FRN_SPACE,FULLFIPSID_SPACE,DBAName_SPACE,PROVNAME_SPACE," +
                       "TRANSTECH_SPACE,MAXADDOWN_SPACE,MAXADUP_SPACE," +
                       "TYPICDOWN_SPACE,TYPICUP_SPACE,SPECTRUM," +
                       "SPECTRUM_SPACE,STATEABBR" + "\n")

          myFile = open(theOFCAI, 'w')  #CAI
          myFile.write("State,FullFIPSID,FRN,PROVNAME,DBANAME,TRANSTECH," +
                       "MAXADDOWN,MAXADUP,TYPICDOWN,TYPICUP,STATEFIPS," +
                       "FRN_SPACE,FULLFIPSID_SPACE,DBAName_SPACE,PROVNAME_SPACE," +
                       "TRANSTECH_SPACE,MAXADDOWN_SPACE,MAXADUP_SPACE," +
                       "TYPICDOWN_SPACE,TYPICUP_SPACE,STATECODE,STATECODE_SPACE" + "\n")


          arcpy.AddMessage("Begining checks on: " + theST)
          for theLyr in ["CensusBlock","Wireless", "RoadSegment", "Address", "CAInstitutions"]:
               if theLyr == "CensusBlock":
                    theFile = theOFCB
               if theLyr == "Wireless":
                    theFile = theOFWS
               if theLyr == "RoadSegment":
                    theFile = theOFRd
               if theLyr == "Address":
                    theFile = theOFAd
               if theLyr == "CAInstitutions":
                    theFile = theOFCAI
               theFD = theLocation + theST + "/" + theST + "_SBDD_" + theYear + "_"
               theFD = theFD + theMonth + "_" + theDay + ".gdb/NATL_Broadband_Map/"
               #theLyr = "CensusBlock"
               theCBStr = theST
               if arcpy.Exists(theFD + "/BB_Service_" + theLyr):
                    arcpy.AddMessage("     Begining checks on Feature Class: " + theLyr)
                    theCBStr = theCBStr + sbdd_qry (theFD + "/BB_Service_" + theLyr,
                                                    theLyr + "_FULLFIPSID",
                                                    sbdd_qryDef("FULLFIPSID"), "FULLFIPSID")
                    theCBStr = theCBStr + sbdd_qry (theFD + "/BB_Service_" + theLyr,
                                                    theLyr + "_FRN",
                                                    sbdd_qryDef("FRN"), "FRN")
                    theCBStr = theCBStr + sbdd_qry (theFD + "/BB_Service_" + theLyr,
                                                    theLyr + "_PROVNAME",
                                                    sbdd_qryDef("PROVNAME"), "PROVNAME")
                    theCBStr = theCBStr + sbdd_qry (theFD + "/BB_Service_" + theLyr,
                                                    theLyr + "_DBANAME",
                                                    sbdd_qryDef("DBANAME"), "DBANAME")
                    theCBStr = theCBStr + sbdd_qry (theFD + "/BB_Service_" + theLyr,
                                                    theLyr + "_TRANSTECH",
                                                    sbdd_qryDef("TRANSTECH"), "TRANSTECH")
                    theCBStr = theCBStr + sbdd_qry (theFD + "/BB_Service_" + theLyr,
                                                    theLyr + "_MAXADDOWN",
                                                    sbdd_qryDef("MAXADDOWN"), "MAXADDOWN")
                    theCBStr = theCBStr + sbdd_qry (theFD + "/BB_Service_" + theLyr,
                                                    theLyr + "_MAXADUP",
                                                    sbdd_qryDef("MAXADUP"), "MAXADUP")
                    theCBStr = theCBStr + sbdd_qry (theFD + "/BB_Service_" + theLyr,
                                                    theLyr + "_TYPICDOWN",
                                                    sbdd_qryDef("TYPICDOWN"), "TYPICDOWN")
                    theCBStr = theCBStr + sbdd_qry (theFD + "/BB_Service_" + theLyr,
                                                    theLyr + "_TYPICUP",
                                                    sbdd_qryDef("TYPICUP"), "TYPICUP")
                    theCBStr = theCBStr + sbdd_qry (theFD + "/BB_Service_" + theLyr,
                                                    theLyr + "_STATEFIPS",
                                                    sbdd_qryDef("STATEFIPS"), "STATEFIPS")
                    theCBStr = theCBStr + sbdd_qry (theFD + "/BB_Service_" + theLyr,
                                                    theLyr + "_FRN_SPACE",
                                                    sbdd_qryDef("FRN_SPACE"), "FRN_SPACE")
                    theCBStr = theCBStr + sbdd_qry (theFD + "/BB_Service_" + theLyr,
                                                    theLyr + "_FULLFIPSID_SPACE",
                                                    sbdd_qryDef("FULLFIPSID_SPACE"), "FULLFIPSID_SPACE")
                    theCBStr = theCBStr + sbdd_qry (theFD + "/BB_Service_" + theLyr,
                                                    theLyr + "_DBAName_SPACE",
                                                    sbdd_qryDef("DBAName_SPACE"), "DBANAME_SPACE")
                    theCBStr = theCBStr + sbdd_qry (theFD + "/BB_Service_" + theLyr,
                                                    theLyr + "_PROVNAME_SPACE",
                                                    sbdd_qryDef("PROVNAME_SPACE"), "PROVNAME_SPACE")
                    theCBStr = theCBStr + sbdd_qry (theFD + "/BB_Service_" + theLyr,
                                                    theLyr + "_TRANSTECH_SPACE",
                                                    sbdd_qryDef("TRANSTECH_SPACE"), "TRANSTECH_SPACE")
                    theCBStr = theCBStr + sbdd_qry (theFD + "/BB_Service_" + theLyr,
                                                    theLyr + "_MAMAXADDOWN_SPACE",
                                                    sbdd_qryDef("MAMAXADDOWN_SPACE"), "MAMAXADDOWN_SPACE")              
                    theCBStr = theCBStr + sbdd_qry (theFD + "/BB_Service_" + theLyr,
                                                    theLyr + "_MAXADUP_SPACE",
                                                    sbdd_qryDef("MAXADUP_SPACE"), "MAXADUP_SPACE")  
                    theCBStr = theCBStr + sbdd_qry (theFD + "/BB_Service_" + theLyr,
                                                    theLyr + "_TYPICDOWN_SPACE",
                                                    sbdd_qryDef("TYPICDOWN_SPACE"), "TYPICDOWN_SPACE")
                    theCBStr = theCBStr + sbdd_qry (theFD + "/BB_Service_" + theLyr,
                                                    theLyr + "_TYPICUP_SPACE",
                                                    sbdd_qryDef("TYPICUP_SPACE"), "TYPICUP_SPACE")
                    if theLyr == "Wireless":
                         theCBStr = theCBStr + sbdd_qry (theFD + "/BB_Service_" + theLyr,
                                                         theLyr + "_SPECTRUM",
                                                         sbdd_qryDef("SPECTRUM"), "SPECTRUM")                         
                         theCBStr = theCBStr + sbdd_qry (theFD + "/BB_Service_" + theLyr,
                                                         theLyr + "_SPECTRUM_SPACE",
                                                         sbdd_qryDef("SPECTRUM_SPACE"), "SPECTRUM_SPACE")
                         theCBStr = theCBStr + sbdd_qry (theFD + "/BB_Service_" + theLyr,
                                                         theLyr + "_STATEABBR",
                                                         sbdd_qryDef("STATEABBR"), "STATEABBR")
                    if theLyr == "RoadSegment":
                         theCBStr = theCBStr + sbdd_qry (theFD + "/BB_Service_" + theLyr,
                                                         theLyr + "_STATECODE",
                                                         sbdd_qryDef("STATECODE"), "STATECODE")                         
                         theCBStr = theCBStr + sbdd_qry (theFD + "/BB_Service_" + theLyr,
                                                         theLyr + "_STATECODE_SPACE",
                                                         sbdd_qryDef("STATECODE_SPACE"), "STATECODE_SPACE")
                    if theLyr == "Address":
                         theCBStr = theCBStr + sbdd_qry (theFD + "/BB_Service_" + theLyr,
                                                         theLyr + "_STATECODE",
                                                         sbdd_qryDef("STATECODE"), "STATECODE")                         
                         theCBStr = theCBStr + sbdd_qry (theFD + "/BB_Service_" + theLyr,
                                                         theLyr + "_STATECODE_SPACE",
                                                         sbdd_qryDef("STATECODE_SPACE"), "STATECODE_SPACE")                      
                    if theLyr == "CAInstitutions":
                         theCBStr = theCBStr + sbdd_qry (theFD + "/BB_Service_" + theLyr,
                                                         theLyr + "_STATECODE",
                                                         sbdd_qryDef("STATECODE"), "STATECODE")                         
                         theCBStr = theCBStr + sbdd_qry (theFD + "/BB_Service_" + theLyr,
                                                         theLyr + "_STATECODE_SPACE",
                                                         sbdd_qryDef("STATECODE_SPACE"), "STATECODE_SPACE")                      

               else:
                    theCBStr = theST + ",File Not Submitted Yet"
               myFile = open(theFile, 'a')
               myFile.write(theCBStr + "\n")
               myFile.close()
     del theLyr, theCBStr, theFile, theST, States, theLocation, theYear, theMonth
except:
     arcpy.AddMessage( "Something bad happened during the writing of the reciept; please re-run" )


  
