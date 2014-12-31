# -*- coding: cp1252 -*-
# ---------------------------------------------------------------------------
#   VERSION 0.1 (for ArcGIS 10)
# SBDD_Summary.py
# Created on: Sat. March 26 2011 
# Created by: Michael Byrne
# Federal Communications Commission 
# ---------------------------------------------------------------------------

# Import system modules
import sys, string, os, arcpy
from arcpy import env
import time
from datetime import date
from os import remove, close
today = date.today()

#global variables
theOF = "C:/work/nbbm/2014_2/chkResult/summary_all_files/"
theLocation = "C:/work/nbbm/2014_2/gdb/"
theYear = "2014"
theMonth = "10"
theDay = "01"

States = ["AK","AL","AR","AS","AZ","CA","CO","CT"] #1
States = States + ["DC","DE","FL","GA","GU","HI","IA","ID"] #2
States = States + ["IL","IN","KS","KY","LA","MA","MD","ME"] #3
States = States + ["MI","MN","MO","MS","MT","NC","ND","MP"] #4 
States = States + ["NE","NH","NJ","NM","NV","NY","OH","OK"] #5
States = States + ["OR","PA","PR","RI","SC","SD","TN","TX"] #6
States = States + ["UT","VA","VI","VT","WA","WI","WV","WY"] #7

#write out functions
#Function sbdd_CountFC returns the record count of a FeatureClass
#has an argument of the input table
def sbdd_CountFC (theFC):
    myCnt = int(arcpy.GetCount_management(theFC).getOutput(0))
    return (myCnt)

#Function sbdd_WriteLine writes a line to the output file 
#has an argument for writing a certain number of lines
def sbdd_WriteLine(theCnt):
    myCnt = 0
    while int(theCnt) > myCnt: #then write a line
        myFile.write("\n")
        myCnt = myCnt + 1
    del myCnt, theCnt
    return ()

#Function sbdd_UniqueISP writes out the unique number of ISPs per submission 
#no arguemtns
def sbdd_UniqueISP():
    theFCs = ["CensusBlock","Address","RoadSegment","Wireless","Overview"]
    for theFC in theFCs:
        if arcpy.Exists(theFGDB + "/" + theFC + "_FRQ"):
            arcpy.Delete_management(theFGDB + "/" + theFC + "_FRQ")
        arcpy.Frequency_analysis("BB_Service_" + theFC, theFGDB + "/" + theFC + "_FRQ", ["FRN","DBANAME","PROVNAME"])
    arcpy.Append_management([theFGDB + "/Address_FRQ", theFGDB + "/RoadSegment_FRQ", theFGDB + "/Wireless_FRQ", theFGDB + "/Overview_FRQ"], theFGDB + "/CensusBlock_FRQ" ,"TEST" ,"" ,"")
    if arcpy.Exists(theFGDB + "/ISP_FRQ"):
        arcpy.Delete_management(theFGDB + "/ISP_FRQ")
    arcpy.Frequency_analysis(theFGDB + "/CensusBlock_FRQ" ,theFGDB + "/ISP_FRQ", ["FRN","DBANAME","PROVNAME"])
    myCnt = int(arcpy.GetCount_management(theFGDB + "/ISP_FRQ").getOutput(0))
    myFile.write(",,Number of ISPs Provided in Submission " + "," + str(myCnt) + "\n")
    theFCs = ["CensusBlock","Address","RoadSegment","Wireless","Overview","ISP"]
    for theFC in theFCs:
        if arcpy.Exists(theFGDB + "/" + theFC + "_FRQ"):
            arcpy.Delete_management(theFGDB + "/" + theFC + "_FRQ")    
    del myCnt, theFC, theFCs
    return ()

#Function sbdd_RecordDetail writes out the record detail
#has an argument for the table to operate on
def sbdd_RecordDetail (theFC, theField):
    myCnt = int(arcpy.GetCount_management(theFC).getOutput(0))
    myFile.write(",Records Detail,Total Records," + str(myCnt) + "\n")
    sbdd_WriteLine("1")
    if theField <> "NOFIELD":
        if arcpy.Exists(theFGDB + "/sbdd_FRQ"):
            arcpy.Delete_management(theFGDB + "/sbdd_FRQ")
        arcpy.Frequency_analysis(theFC, theFGDB + "/sbdd_FRQ", theField)
        myCnt = int(arcpy.GetCount_management(theFGDB + "/sbdd_FRQ").getOutput(0))
        myFile.write(",,Total Count of " + theField + "," + str(myCnt) + "\n")
        if arcpy.Exists(theFD + "/sbdd_FRQ"):
            arcpy.Delete_management(theFD + "/sbdd_FRQ")
        del myCnt, theFC, theField    
    return ()

#Fucntion sbdd_ProviderDetail writes out the Service Provider detail
#has an argument for the table to operate on
def sbdd_ProviderDetail (theFC):
    myFile.write(",Service Provider Details \n")
    theFields = ["PROVNAME", "DBANAME", "FRN"]
    for f in theFields:
        myCnt = 0
        if arcpy.Exists(theFGDB + "/sbdd_FRQ"):
            arcpy.Delete_management(theFGDB + "/sbdd_FRQ")        
        arcpy.Frequency_analysis(theFC, theFGDB + "/sbdd_FRQ", f)
        myCnt = int(arcpy.GetCount_management(theFGDB + "/sbdd_FRQ").getOutput(0))
        myFile.write(",,Total Count of distinct " + f + "," + str(myCnt) + "\n")
        if arcpy.Exists(theFGDB + "/sbdd_FRQ"):
            arcpy.Delete_management(theFGDB + "/sbdd_FRQ")
    del theFC, myCnt
    return ()

#Function sbdd_TechnologyDetail writes out the Technology Detail
#has an argument for theFC to operate on; theTot is the Total number of records to get percents
def sbdd_TechnologyDetail (theFC):
    myFile.write(",Technology Details \n")
    Vals = ["10","20","30","40","41","50","60","70","71","80","90","0"]
    theTot = int(arcpy.GetCount_management(theFC).getOutput(0))
    myTot = 0
    for Val in Vals:
        myFL = "TransTech" + str(Val)
        myQry = "TRANSTECH = " + str(Val) 
        arcpy.MakeFeatureLayer_management(theFC, myFL, myQry)
        myCnt = int(arcpy.GetCount_management(myFL).getOutput(0))
        myTot = myTot + myCnt
        myFile.write("," + str(Val) + "," + sbdd_ReturnTech(Val) + "," + str(myCnt) + "," + "=" + str(myCnt) + "/" + str(theTot) + "\n")
        arcpy.Delete_management(myFL)
    #now do the N/A
    myFile.write(",,N/A," + str(theTot - myTot) + "," + "=" + str(theTot - myTot) + "/" + str(theTot) + "\n")
    del theFC, myCnt, myFL, myQry, Val, Vals, theTot, myTot
    return ()

#Function sbdd_SpeedDetail writes out the Speed Detail
#has an argument for theFC to operate on; and the type of speed
def sbdd_SpeedDetail (theFC, mySpeed):
    myFile.write("," + mySpeed + " Details \n")
    Vals = ["1","2","3","4","5","6","7","8","9","10","11"]
    theTot = int(arcpy.GetCount_management(theFC).getOutput(0))
    myTot = 0
    for Val in Vals:
        myFL = "Speed" + mySpeed + str(Val)
        myQry = mySpeed + " = '" + str(Val) + "'"
        arcpy.MakeFeatureLayer_management(theFC, myFL, myQry)
        myCnt = int(arcpy.GetCount_management(myFL).getOutput(0))
        myTot = myTot + myCnt
        myFile.write("," + str(Val) + "," + sbdd_ReturnSpeed(Val) + "," + str(myCnt) + "," + "=" + str(myCnt) + "/" + str(theTot) + "\n")
        arcpy.Delete_management(myFL)
    #now do the N/A
    myFile.write(",,N/A," + str(theTot - myTot) + "," + "=" + str(theTot - myTot) + "/" + str(theTot) + "\n")
    del theFC, myCnt, myFL, myQry, Val, Vals, theTot, myTot
    return ()

#Function sbdd_EndUserDetail writes out the End User Detail
#has an argument for theFC to operate on; 
def sbdd_EndUserDetail (theFC):
    myFile.write(",End User Category Details \n")
    Vals = ["1","2","3","4","5"]
    theTot = int(arcpy.GetCount_management(theFC).getOutput(0))
    myTot = 0
    for Val in Vals:
        myFL = "EndUserCat" + str(Val)
        myQry = "ENDUSERCAT = '" + str(Val) + "'"
        arcpy.MakeFeatureLayer_management(theFC, myFL, myQry)
        myCnt = int(arcpy.GetCount_management(myFL).getOutput(0))
        myTot = myTot + myCnt
        myFile.write("," + str(Val) + "," + sbdd_ReturnEndUCat(Val) + "," + str(myCnt) + "," + "=" + str(myCnt) + "/" + str(theTot) + "\n")
        arcpy.Delete_management(myFL)
    #now do the N/A
    myFile.write(",,N/A," + str(theTot - myTot) + "," + "=" + str(theTot - myTot) + "/" + str(theTot) + "\n")
    del theFC, myCnt, myFL, myQry, Val, Vals, theTot, myTot
    return ()

#Function sbdd_SpectrumDetail writes out the Spectrum Detail
#has an argument for theFC to operate on; theTot is the Total number of records to get percents; and the type of speed
def sbdd_SpectrumDetail (theFC):
    myFile.write(",Spectrum Details \n")
    Vals = ["1","2","3","4","5","6","7","8","9","10"]
    theTot = int(arcpy.GetCount_management(theFC).getOutput(0))
    myTot = 0
    for Val in Vals:
        myFL = "Spectrum" + str(Val)
        myQry = "Spectrum = " + str(Val)
        arcpy.MakeFeatureLayer_management(theFC, myFL, myQry)
        myCnt = int(arcpy.GetCount_management(myFL).getOutput(0))
        myTot = myTot + myCnt
        myFile.write("," + str(Val) + "," + sbdd_ReturnSpectrum (Val) + "," + str(myCnt) + "," + "=" + str(myCnt) + "/" + str(theTot) + "\n")
        arcpy.Delete_management(myFL)
    #now do the N/A
    myFile.write(",,N/A," + str(theTot - myTot) + "," + "=" + str(theTot - myTot) + "/" + str(theTot) + "\n")
    del theFC, myCnt, myFL, myQry, Val, Vals, theTot, myTot
    return ()

#Function sbdd_OverviewDetail writes out the ARPU/SNWS Detail
#has an argument for theFC to operate on; 
def sbdd_OverviewDetail (theFC):
    myFile.write(",Overview Details \n")
    theTot = int(arcpy.GetCount_management(theFC).getOutput(0))
    Vals = ["ARPU","SWNOMSPEED"]    
    for Val in Vals:
        myFL = Val + str(theTot)
        myQry = Val + " > 0"
        arcpy.MakeFeatureLayer_management(theFC, myFL, myQry)
        myCnt = int(arcpy.GetCount_management(myFL).getOutput(0))
        myFile.write("," + str(Val) + "," + str(myCnt) + "," + "=" + str(myCnt) + "/" + str(theTot) + "\n")
        arcpy.Delete_management(myFL)
    del theFC, myCnt, myFL, myQry, Val, Vals, theTot
    return ()

#Function sbdd_AnchorCatDetail writes out the Anchor Category Detail
#has an argument for theFC to operate on; 
def sbdd_AnchorCatDetail (theFC):
    myFile.write(",Anchor Category Details \n")
    Vals = ["1","2","3","4","5","6","7"]
    theTot = int(arcpy.GetCount_management(theFC).getOutput(0))
    myTot = 0
    for Val in Vals:
        myFL = "CAICAT" + str(Val)
        myQry = "CAICAT = '" + str(Val) + "'"
        arcpy.MakeFeatureLayer_management(theFC, myFL, myQry)
        myCnt = int(arcpy.GetCount_management(myFL).getOutput(0))
        myTot = myTot + myCnt
        myFile.write("," + str(Val) + "," + sbdd_ReturnCAICat(Val) + "," + str(myCnt) + "," + "=" + str(myCnt) + "/" + str(theTot) + "\n")
        arcpy.Delete_management(myFL)
    #now do the N/A
    myFile.write(",,N/A," + str(theTot - myTot) + "," + "=" + str(theTot - myTot) + "/" + str(theTot) + "\n")
    del theFC, myCnt, myFL, myQry, Val, Vals, theTot, myTot
    return ()

#Function sbdd_BBServiceDetail writes out the Broadband Service Detail
#has an argument for theFC to operate on; 
def sbdd_BBServiceDetail (theFC):
    myFile.write(",Broadband Service Details \n")
    Vals = ["Y","N","U"]
    theTot = int(arcpy.GetCount_management(theFC).getOutput(0))
    myTot = 0
    for Val in Vals:
        myFL = "BBService" + Val
        myQry = "BBSERVICE = '" + str(Val) + "'"
        arcpy.MakeFeatureLayer_management(theFC, myFL, myQry)
        myCnt = int(arcpy.GetCount_management(myFL).getOutput(0))
        myTot = myCnt + myTot
        myFile.write("," + str(Val) + "," + sbdd_ReturnBBService(Val) + "," + str(myCnt) + "," + "=" + str(myCnt) + "/" + str(theTot) + "\n")
        arcpy.Delete_management(myFL)
    #now do the N/A
    myFile.write(",,N/A," + str(theTot - myTot) + "," + "=" + str(theTot - myTot) + "/" + str(theTot) + "\n")
    del theFC, myCnt, myFL, myQry, Val, Vals, theTot, myTot
    return ()

#Function sbdd_PWifiDetail writes out the Public Wifi Detail
#has an argument for theFC to operate on; 
def sbdd_PWifiDetail (theFC):
    myFile.write(",Public Wifi Details \n")
    Vals = ["Y","N","U"]
    theTot = int(arcpy.GetCount_management(theFC).getOutput(0))
    myTot = 0
    for Val in Vals:
        myFL = "PublicWifi" + Val
        myQry = "PublicWifi = '" + str(Val) + "'"
        arcpy.MakeFeatureLayer_management(theFC, myFL, myQry)
        myCnt = int(arcpy.GetCount_management(myFL).getOutput(0))
        myTot = myTot + myCnt
        myFile.write("," + str(Val) + "," + sbdd_ReturnBBService(Val) + "," + str(myCnt) + "," + "=" + str(myCnt) + "/" + str(theTot) + "\n")
        arcpy.Delete_management(myFL)
    #now do the N/A
    myFile.write(",,N/A," + str(theTot - myTot) + "," + "=" + str(theTot - myTot) + "/" + str(theTot) + "\n")
    del theFC, myCnt, myFL, myQry, Val, Vals, theTot, myTot
    return ()

#Function sbdd_Ownership writes out the Ownership Detail
#has an argument for theFC to operate on; 
def sbdd_OwnerDetail (theFC):
    myFile.write(",Ownership Details \n")
    Vals = ["0","1"]
    theTot = int(arcpy.GetCount_management(theFC).getOutput(0))
    myTot = 0
    for Val in Vals:
        myFL = "Ownership" + Val
        myQry = "Ownership = " + str(Val)
        arcpy.MakeFeatureLayer_management(theFC, myFL, myQry)
        myCnt = int(arcpy.GetCount_management(myFL).getOutput(0))
        myTot = myTot + myCnt
        myFile.write("," + str(Val) + "," + sbdd_ReturnOwn(Val) + "," + str(myCnt) + "," + "=" + str(myCnt) + "/" + str(theTot) + "\n")
        arcpy.Delete_management(myFL)
    #now do the N/A
    myFile.write(",,N/A," + str(theTot - myTot) + "," + "=" + str(theTot - myTot) + "/" + str(theTot) + "\n")
    del theFC, myCnt, myFL, myQry, Val, Vals, theTot, myTot
    return ()

#Function sbdd_BHType writes out the Facility Detail
#has an argument for theFC to operate on; 
def sbdd_BHTypeDetail (theFC):
    myFile.write(",Facility Type Details \n")
    Vals = ["1","2","3","4"]
    theTot = int(arcpy.GetCount_management(theFC).getOutput(0))
    myTot = 0
    for Val in Vals:
        myFL = "BHTYPE"  + Val
        myQry = "BHTYPE = " + str(Val)
        arcpy.MakeFeatureLayer_management(theFC, myFL, myQry)
        myCnt = int(arcpy.GetCount_management(myFL).getOutput(0))
        myTot = myTot + myCnt
        myFile.write("," + str(Val) + "," + sbdd_ReturnBHType(Val) + "," + str(myCnt) + "," + "=" + str(myCnt) + "/" + str(theTot) + "\n")
        arcpy.Delete_management(myFL)
    #now do the N/A
    myFile.write(",,N/A," + str(theTot - myTot) + "," + "=" + str(theTot - myTot) + "/" + str(theTot) + "\n")
    del theFC, myCnt, myFL, myQry, Val, Vals, theTot, myTot
    return ()

#Function sbdd_BHCap writes out the Back Haul Capacity Detail
#has an argument for theFC to operate on; 
def sbdd_BHCapDetail (theFC):
    myFile.write(",Facility Type Details \n")
    Vals = ["1","2","3","4","5","6"]
    theTot = int(arcpy.GetCount_management(theFC).getOutput(0))
    myTot = 0
    for Val in Vals:
        myFL = "BHCAPACITY"  + Val
        myQry = "BHCAPACITY = " + str(Val)
        arcpy.MakeFeatureLayer_management(theFC, myFL, myQry)
        myCnt = int(arcpy.GetCount_management(myFL).getOutput(0))
        myTot = myTot + myCnt
        myFile.write("," + str(Val) + "," + sbdd_ReturnBHCap(Val) + "," + str(myCnt) + "," + "=" + str(myCnt) + "/" + str(theTot) + "\n")
        arcpy.Delete_management(myFL)
    #now do the N/A
    myFile.write(",,N/A," + str(theTot - myTot) + "," + "=" + str(theTot - myTot) + "/" + str(theTot) + "\n")
    del theFC, myCnt, myFL, myQry, Val, Vals, theTot
    return ()

#Function sbdd_SpeedReport writes out the unique TransTech Speed Values Detail
#has no argument; 
def sbdd_SpeedReport ():
    myFile.write(",Distinct Speed Tiers Provided \n")
    theFCs = ["TechSpeed_MA_FRQ","TechSpeed_TY_FRQ"]
    for theFC in theFCs:
        if arcpy.Exists(theFGDB + "/" + theFC):
            arcpy.Delete_management(theFGDB + "/" + theFC)
    theFCs = ["CensusBlock","Address","RoadSegment","Wireless"]
    for theFC in theFCs:
        if arcpy.Exists(theFGDB + "/" + theFC + "_FRQ"):
            arcpy.Delete_management(theFGDB + "/" + theFC + "_FRQ")
        arcpy.Frequency_analysis("BB_Service_" + theFC, theFGDB + "/" + theFC + "_FRQ", \
                                 ["TRANSTECH","MAXADDOWN","MAXADUP","TYPICDOWN","TYPICUP"])
    arcpy.Append_management([theFGDB + "/Address_FRQ", theFGDB + "/RoadSegment_FRQ", theFGDB + \
                             "/Wireless_FRQ"], theFGDB + "/CensusBlock_FRQ" ,"TEST" ,"" ,"")
    arcpy.Frequency_analysis(theFGDB + "/CensusBlock_FRQ" ,theFGDB + "/TechSpeed_MA_FRQ", \
                             ["TRANSTECH","MAXADDOWN","MAXADUP"], ["FREQUENCY"])
    arcpy.Frequency_analysis(theFGDB + "/CensusBlock_FRQ" ,theFGDB + "/TechSpeed_TY_FRQ", \
                             ["TRANSTECH","TYPICDOWN","TYPICUP"], ["FREQUENCY"])
    arcpy.JoinField_management(theFGDB + "/TechSpeed_MA_FRQ", "OBJECTID", \
                               theFGDB + "/TechSpeed_TY_FRQ", "OBJECTID")
    #go open up and read this table
    myFile.write("," + "Maximum Advertised Speed,,,,,Typical Speed" + "\n")
    myFile.write("," + "Technology,Download,Upload, Num. Records,,Technology,Download,Upload, Num. Records" + "\n")
    myCnt = 658 #658 is the row in the spreadsheet where this section begins
    for row in arcpy.SearchCursor(theFGDB + "/TechSpeed_MA_FRQ"):
        theMATech = str(row.getValue("TRANSTECH"))
        theMADown = str(row.getValue("MAXADDOWN"))
        theMAUp = str(row.getValue("MAXADUP"))
        theMAFRQ = str(row.getValue("FREQUENCY"))
        theTYTech = str(row.getValue("TRANSTECH_1"))
        theTYDown = str(row.getValue("TYPICDOWN"))
        theTYUp = str(row.getValue("TYPICUP"))
        theTYFRQ = str(row.getValue("FREQUENCY_1"))
        myFile.write("," + theMATech + "," + theMADown + "," + theMAUp + "," + theMAFRQ + \
                     ",," + theTYTech + "," + theTYDown + "," + theTYUp + "," + theTYFRQ + "\n")
        myCnt = myCnt + 1
    del theMATech, theMAUp, theMADown, theMAFRQ, row, theTYTech, theTYUp, theTYDown, theTYFRQ
    theFCs = ["CensusBlock","Address","RoadSegment","Wireless","TechSpeed_MA", "TechSpeed_TY"] 
    for theFC in theFCs:
        if arcpy.Exists(theFGDB + "/" + theFC + "_FRQ"):
            arcpy.Delete_management(theFGDB + "/" + theFC + "_FRQ")
    sbdd_WriteLine(1000 - myCnt)  #we want the records for the next section on the same row dispite the difference in row count
    del theFC, theFCs

#Function sbdd_ProviderReport writes out the unique Provider Values Detail
#has no argument; 
def sbdd_ProviderReport ():
    myFile.write(",Distinct Provided \n")
    theFCs = ["CensusBlock","Address","RoadSegment","Wireless","Prov"]
    for theFC in theFCs:
        if arcpy.Exists(theFGDB + "/" + theFC + "_FRQ"):
            arcpy.Delete_management(theFGDB + "/" + theFC + "_FRQ")
    theFCs = ["CensusBlock","Address","RoadSegment","Wireless"]
    for theFC in theFCs:
        arcpy.Frequency_analysis("BB_Service_" + theFC, theFGDB + "/" + theFC + "_FRQ", \
                                 ["FRN","DBANAME","PROVNAME"])
    arcpy.Append_management([theFGDB + "/Address_FRQ", theFGDB + "/RoadSegment_FRQ", theFGDB + \
                             "/Wireless_FRQ"], theFGDB + "/CensusBlock_FRQ" ,"TEST" ,"" ,"")
    arcpy.Frequency_analysis(theFGDB + "/CensusBlock_FRQ" ,theFGDB + "/Prov_FRQ", \
                             ["FRN","DBANAME","PROVNAME"])
    #go open up and read this table
    myFile.write("," + "FRN,DBANAME, PROVNAME" + "\n")
    for row in arcpy.SearchCursor(theFGDB + "/Prov_FRQ"):
        theFRN = str(row.getValue("FRN"))
        theDBA = row.getValue("DBANAME").encode('utf-8').strip() 
        theDBA = theDBA.replace(","," ")
        theDBA = theDBA.replace("'"," ")
        theProv = row.getValue("PROVNAME").encode('utf-8').strip()
        theProv = theProv.replace(","," ")
        theProv = theProv.replace("'"," ")
        myFile.write("," + theFRN + "," + theDBA + "," + theProv + "\n")
    del theFRN, theDBA, theProv, row
    theFCs = ["CensusBlock","Address","RoadSegment","Wireless"]  #"Prov"
    for theFC in theFCs:
        if arcpy.Exists(theFGDB + "/" + theFC + "_FRQ"):
            arcpy.Delete_management(theFGDB + "/" + theFC + "_FRQ")
    del theFC, theFCs


##**************************************************************
##***********************LookUp Functions***********************
##**************************************************************

#Function sbdd_ReturnTech returns the Technology English Value
#has an argument for the Coded DomainValue
def sbdd_ReturnTech (theCode):
  if theCode == "10":
    engValue = "Asymmetric xDSL"
  if theCode == "20":
    engValue = "Symmetric xDSL"
  if theCode == "30":
    engValue = "Other Copper Wireline"
  if theCode == "40":
    engValue = "Cable Modem - DOCSIS 3.0"
  if theCode == "41":
    engValue = "Cable Modem - Other"
  if theCode == "50":
    engValue = "Optical Carrier/ Fiber to End User"
  if theCode == "60":
    engValue = "Satellite"
  if theCode == "70":
    engValue = "Terrestrial Fixed Wireless - Unlicensed"
  if theCode == "71":
    engValue = "Terrestrial Fixed Wireless - Licensed"
  if theCode == "80":
    engValue = "Terrestrial Mobile Wireless"
  if theCode == "90":
    engValue = "Electric Power Line"
  if theCode == "0":
    engValue = "Other"
  return(engValue)

#Function sbdd_ReturnSpeed returns the Speed Tier English Value
#has an argument for the Coded DomainValue
def sbdd_ReturnSpeed (theCode):
  if theCode == "1":
    engValue = "< 200 kps."
  if theCode == "2":
    engValue = "> 200 kps to < 768 kps."
  if theCode == "3":
    engValue = "> 768 kps to < 1.5 mbps."
  if theCode == "4":
    engValue = "> 1.5 mbps to < 3 mbps."
  if theCode == "5":
    engValue = "> 3 mbps to < 6 mbps."
  if theCode == "6":
    engValue = "> 6 mbps to < 10 mbps."
  if theCode == "7":
    engValue = "> 10 mbps to < 25 mbps."
  if theCode == "8":
    engValue = "> 25 mbps to < 50 mbps."
  if theCode == "9":
    engValue = "> 50 mbps to < 100 mbps."
  if theCode == "10":
    engValue = "> 100 mbps to < 1 gbps."
  if theCode == "11":
    engValue = "> 1 gbps."
  return(engValue)

#Function sbdd_ReturnEndUCat returns the End User English Value
#has an argument for the Coded DomainValue
def sbdd_ReturnEndUCat (theCode):
  if theCode == "1":
    engValue = "Residential"
  if theCode == "2":
    engValue = "Government"
  if theCode == "3":
    engValue = "Small Business"
  if theCode == "4":
    engValue = "Medium or Large Enterprise"
  if theCode == "5":
    engValue = "Other"
  return(engValue)

#Function sbdd_ReturnSpectrum returns the Spectrum English Value
#has an argument for the Coded DomainValue
def sbdd_ReturnSpectrum (theCode):
  if theCode == "1":
    engValue = "800 Mhz Spectrum Used"
  if theCode == "2":
    engValue = "700 Mhz Spectrum Used"
  if theCode == "3":
    engValue = "1900 Mhz Spectrum Used"
  if theCode == "4":
    engValue = "1700 Mhz Spectrum Used"
  if theCode == "5":
    engValue = "2500 Mhz Spectrum Used"
  if theCode == "6":
    engValue = "Unlicensed Spectrum Used"
  if theCode == "7":
    engValue = "Other Spectrum Used"
  if theCode == "8":
    engValue = "Other Spectrum Used"
  if theCode == "9":
    engValue = "Other Spectrum Used"
  if theCode == "10":
    engValue = "Other"
  return(engValue)

#Function sbdd_ReturnCAICat returns the CAI Category English Value
#has an argument for the Coded DomainValue
def sbdd_ReturnCAICat (theCode):
  if theCode == "1":
    engValue = "School-K through 12"
  if theCode == "2":
    engValue = "Library"
  if theCode == "3":
    engValue = "Medical/healthcare"
  if theCode == "4":
    engValue = "Public safety"
  if theCode == "5":
    engValue = "University; college; other post-secondary"
  if theCode == "6":
    engValue = "Other community support-/gov't"
  if theCode == "7":
    engValue = "Other community support-non-/govt"
  return(engValue)

#Function sbdd_ReturnBBService returns the CAI Broadband Service English Value
#has an argument for the Coded DomainValue
def sbdd_ReturnBBService (theCode):
  if theCode == "Y":
    engValue = "Yes-Subscribes to Service"
  if theCode == "N":
    engValue = "No-Doesn't Subscribe to Service"
  if theCode == "U":
    engValue = "Unknown"
  return(engValue)

#Function sbdd_ReturnOwn returns the Ownership English Value
#has an argument for the Coded DomainValue
def sbdd_ReturnOwn (theCode):
  if theCode == "0":
    engValue = "Owned"
  if theCode == "1":
    engValue = "Leased"
  return(engValue)

#Function sbdd_ReturnBHType returns the Back Haul Capacity Type English Value
#has an argument for the Coded DomainValue
def sbdd_ReturnBHType (theCode):
  if theCode == "1":
    engValue = "Fiber"
  if theCode == "2":
    engValue = "Copper"
  if theCode == "3":
    engValue = "Hybrid Fiber Coax (HFC)"
  if theCode == "4":
    engValue = "Wireless"
  return(engValue)

#Function sbdd_ReturnBHCap returns the Back Haul Capacity English Value
#has an argument for the Coded DomainValue
def sbdd_ReturnBHCap (theCode):
  if theCode == "1":
    engValue = "Multiple T1s and less than 40 mpbs"
  if theCode == "2":
    engValue = "> 40 mbps to <150 mbps"
  if theCode == "3":
    engValue = ">150 mbps to < 600 mbps"
  if theCode == "4":
    engValue = "> 600 mbps to < 2.4 gbps"
  if theCode == "5":
    engValue = "> 2.4 gbps to  < 10 gbps"
  if theCode == "6":
    engValue = "> 10 gbps"
  return(engValue)

##***********Primary Code flow begins below
try:
    for theST in States:
        #theST = "CA"
        theFD = theLocation + theST + "/" + theST + "_SBDD_" + theYear + "_"
        theFD = theFD + theMonth + "_" + theDay + ".gdb/NATL_Broadband_Map"
        #arcpy.AddMessage("the FD is: " + theFD)

        arcpy.AddMessage("the state is: " + theST)
        theFGDB = theFD.rstrip("NATL_Broadband_Map")
        arcpy.env.workspace = theFD

        #Create Reciept
        myYear = today.year
        myMonth = today.month
        myDay = today.day

        #set up output file
        outFile = theOF + theST + "_" + str(myYear) + "_" + str(myMonth) + "_" + str(myDay) + ".csv"
        myFile = open(outFile, 'w')
        myFile.write("\n")
        myFile.write(theST + "\n")
        myFile.write("\n")
        myFile.write("Submission Summary" + "\n")
        myFile.write("\n")
        myFile.write(",,Date:,," + str(myMonth) + "/" + str(myDay) + "/" + str(myYear) + "\n")   
        myFile.write("\n")
        myFile.close()
        del myDay, myMonth, myYear

        #write Page #1
        arcpy.AddMessage("Writing page #1")
        myFile = open(outFile, 'a')
        myFile.write("FILES RECEIVED" + "\n")
        myFile.write(",,File Type,,Number of Records" + "\n")
        myFile.write(",,Total Records in all Files,,=sum(E11:E17)" + "\n")
        for FC in ["CensusBlock","Address","RoadSegment","Wireless","Overview","CAInstitutions",]:
            myFile.write(",," + FC + ",," + str(sbdd_CountFC(theFD + "/BB_Service_" + FC)) + "\n")
        myFile.write(",,MiddleMile,," + str(sbdd_CountFC(theFD + "/BB_ConnectionPoint_MiddleMile"))+ "\n")
        sbdd_UniqueISP()
        sbdd_WriteLine("15")
        myFile.close()

        #write Page #2 - Census Block Detail
        arcpy.AddMessage("Writing Page #2")
        myFile = open(outFile, 'a')
        sbdd_WriteLine("1")
        myFile.write("Census Blocks < 2 sq. Miles" + "\n")
        sbdd_WriteLine("1")
        myFile.write(",Code,Data Element,Count,%" + "\n")
        sbdd_RecordDetail(theFD + "/BB_Service_CensusBlock", "FULLFIPSID")
        sbdd_WriteLine("1")
        sbdd_ProviderDetail (theFD + "/BB_Service_CensusBlock")
        sbdd_WriteLine("1")
        sbdd_TechnologyDetail (theFD + "/BB_Service_CensusBlock")
        sbdd_WriteLine("1")
        sbdd_SpeedDetail(theFD + "/BB_Service_CensusBlock", "MAXADDOWN")
        sbdd_WriteLine("1")
        sbdd_SpeedDetail(theFD + "/BB_Service_CensusBlock", "TYPICDOWN")
        sbdd_WriteLine("1")
        sbdd_SpeedDetail(theFD + "/BB_Service_CensusBlock", "MAXADUP")
        sbdd_WriteLine("1")
        sbdd_SpeedDetail(theFD + "/BB_Service_CensusBlock", "TYPICUP")
        sbdd_WriteLine("15")
        myFile.close()

        #write Page #3 - Address Detail
        arcpy.AddMessage("Writing Page #3")
        myFile = open(outFile, 'a')
        sbdd_WriteLine("1")
        myFile.write("Address Level" + "\n")
        sbdd_WriteLine("1")
        myFile.write(",Code,Data Element,Count,%" + "\n")
        sbdd_RecordDetail(theFD + "/BB_Service_Address", "FULLFIPSID")
        sbdd_WriteLine("1")
        sbdd_ProviderDetail (theFD + "/BB_Service_Address")
        sbdd_WriteLine("1")
        sbdd_EndUserDetail (theFD + "/BB_Service_Address")
        sbdd_WriteLine("1")
        sbdd_TechnologyDetail (theFD + "/BB_Service_Address")
        sbdd_WriteLine("1")
        sbdd_SpeedDetail(theFD + "/BB_Service_Address", "MAXADDOWN")
        sbdd_WriteLine("1")
        sbdd_SpeedDetail(theFD + "/BB_Service_Address", "TYPICDOWN")
        sbdd_WriteLine("1")
        sbdd_SpeedDetail(theFD + "/BB_Service_Address", "MAXADUP")
        sbdd_WriteLine("1")
        sbdd_SpeedDetail(theFD + "/BB_Service_Address", "TYPICUP")
        sbdd_WriteLine("15")
        myFile.close()

        #write Page #4 - Street Segment Detail
        arcpy.AddMessage("Writing Page #4")
        myFile = open(outFile, 'a')
        sbdd_WriteLine("1")
        myFile.write("Street Segment Level" + "\n")
        sbdd_WriteLine("1")
        myFile.write(",Code,Data Element,Count,%" + "\n")
        sbdd_RecordDetail(theFD + "/BB_Service_RoadSegment", "NOFIELD")
        sbdd_WriteLine("1")
        sbdd_ProviderDetail (theFD + "/BB_Service_RoadSegment")
        sbdd_WriteLine("1")
        sbdd_TechnologyDetail (theFD + "/BB_Service_RoadSegment")
        sbdd_WriteLine("1")
        sbdd_SpeedDetail(theFD + "/BB_Service_RoadSegment", "MAXADDOWN")
        sbdd_WriteLine("1")
        sbdd_SpeedDetail(theFD + "/BB_Service_RoadSegment", "TYPICDOWN")
        sbdd_WriteLine("1")
        sbdd_SpeedDetail(theFD + "/BB_Service_RoadSegment", "MAXADUP")
        sbdd_WriteLine("1")
        sbdd_SpeedDetail(theFD + "/BB_Service_RoadSegment", "TYPICUP")
        sbdd_WriteLine("15")
        myFile.close()

        #write Page #5 - Wireless Segment Detail
        arcpy.AddMessage("Writing Page #5")
        myFile = open(outFile, 'a')
        sbdd_WriteLine("1")
        myFile.write("Wireless Shape File" + "\n")
        sbdd_WriteLine("1")
        myFile.write(",Code,Data Element,Count,%" + "\n")
        sbdd_RecordDetail(theFD + "/BB_Service_Wireless", "NOFIELD")
        sbdd_WriteLine("1")
        sbdd_ProviderDetail (theFD + "/BB_Service_Wireless")
        sbdd_WriteLine("1")
        sbdd_TechnologyDetail (theFD + "/BB_Service_Wireless")
        sbdd_WriteLine("1")
        sbdd_SpeedDetail(theFD + "/BB_Service_Wireless", "MAXADDOWN")
        sbdd_WriteLine("1")
        sbdd_SpeedDetail(theFD + "/BB_Service_Wireless", "TYPICDOWN")    
        sbdd_WriteLine("1")
        sbdd_SpeedDetail(theFD + "/BB_Service_Wireless", "MAXADUP")
        sbdd_WriteLine("1")
        sbdd_SpeedDetail(theFD + "/BB_Service_Wireless", "TYPICUP")
        sbdd_WriteLine("1")
        sbdd_SpectrumDetail (theFD + "/BB_Service_Wireless")
        sbdd_WriteLine("15")
        myFile.close()

        #write Page #6 - BB Service Overview
        arcpy.AddMessage("Writing Page #6")
        myFile = open(outFile, 'a')
        sbdd_WriteLine("1")
        myFile.write("BB Service Overview" + "\n")
        sbdd_WriteLine("1")
        myFile.write(",Code,Data Element,Count,%" + "\n")
        sbdd_RecordDetail(theFD + "/BB_Service_Overview", "STATECOUNTYFIPS")
        sbdd_WriteLine("1")
        sbdd_ProviderDetail (theFD + "/BB_Service_Overview")
        sbdd_WriteLine("1")
        sbdd_OverviewDetail (theFD + "/BB_Service_Overview")
        sbdd_WriteLine("1")
        sbdd_TechnologyDetail (theFD + "/BB_Service_Overview")
        sbdd_WriteLine("1")
        sbdd_SpeedDetail(theFD + "/BB_Service_Overview", "MAXADDOWN")
        sbdd_WriteLine("1")
        sbdd_SpeedDetail(theFD + "/BB_Service_Overview", "MAXADUP")
        sbdd_WriteLine("15")
        myFile.close()

        #write Page #7 - Community Anchor Institutions
        arcpy.AddMessage("Writing Page #7")
        myFile = open(outFile, 'a')
        sbdd_WriteLine("1")
        myFile.write("Community Anchor Institution" + "\n")
        sbdd_WriteLine("1")
        myFile.write(",Code,Data Element,Count,%" + "\n")
        sbdd_RecordDetail(theFD + "/BB_Service_CAInstitutions", "ADDRESS")
        sbdd_WriteLine("1")
        sbdd_AnchorCatDetail (theFD + "/BB_Service_CAInstitutions")
        sbdd_WriteLine("1")
        sbdd_BBServiceDetail (theFD + "/BB_Service_CAInstitutions")
        sbdd_WriteLine("1")
        sbdd_PWifiDetail (theFD + "/BB_Service_CAInstitutions")
        sbdd_WriteLine("1")
        sbdd_TechnologyDetail (theFD + "/BB_Service_CAInstitutions")
        sbdd_WriteLine("1")
        sbdd_SpeedDetail(theFD + "/BB_Service_CAInstitutions", "SubScrbDown")
        sbdd_WriteLine("1")
        sbdd_SpeedDetail(theFD + "/BB_Service_CAInstitutions", "SubSrbUp")
        sbdd_WriteLine("15")
        myFile.close()

        #write Page #8 - Middle Mile
        arcpy.AddMessage("Writing Page #8")
        myFile = open(outFile, 'a')
        sbdd_WriteLine("1")
        myFile.write("Middle Mile" + "\n")
        sbdd_WriteLine("1")
        myFile.write(",Code,Data Element,Count,%" + "\n")
        sbdd_RecordDetail(theFD + "/BB_ConnectionPoint_MiddleMile", "NOFIELD")
        sbdd_WriteLine("1")
        sbdd_ProviderDetail (theFD + "/BB_ConnectionPoint_MiddleMile")
        sbdd_WriteLine("1")
        sbdd_OwnerDetail (theFD + "/BB_ConnectionPoint_MiddleMile")
        sbdd_WriteLine("1")
        sbdd_BHTypeDetail (theFD + "/BB_ConnectionPoint_MiddleMile")
        sbdd_WriteLine("1")
        sbdd_BHCapDetail (theFD + "/BB_ConnectionPoint_MiddleMile")
        sbdd_WriteLine("16")
        myFile.close()

        #write Page #9 - Speed Report
        arcpy.AddMessage("Writing Page #9")
        myFile = open(outFile, 'a')
        sbdd_WriteLine("1")
        sbdd_SpeedReport ()
        sbdd_WriteLine("0")
        myFile.close()

        #write Page #10 - Unique Provider Report
        arcpy.AddMessage("Writing Page #10")
        myFile = open(outFile, 'a')
        sbdd_WriteLine("1")
        sbdd_ProviderReport ()
        myFile.close()

        del myFile, outFile

except:
    arcpy.AddMessage("Something bad happened")
  
