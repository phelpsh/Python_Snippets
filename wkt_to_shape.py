"""WKT test for OI. - reads WKT file and writes an ArcGIS featureclass """
import arcpy
import csv
import sys

wk = arcpy.env.workspace = arcpy.GetParameterAsText(2)
csv_location = arcpy.GetParameterAsText(0)
fcname = arcpy.GetParameterAsText(1)

# wk = arcpy.env.workspace = r"C:\Users\xx\Documents\ArcGIS\Projects\xx.gdb"  # noqa: E501
# fcname = "oi_locations_test"

sr = arcpy.SpatialReference(4326)


csv_location = r"C:\Users\xx\Documents\data\Companies\OI\sample_data\xx.csv"  # NOQA
# input data is proprietary, but looks like this:

#   id  class   class_geom  use             
# 0 11c23fdc-4d13-4862-9298-2ee170e8c8f1    mining  MULTIPOLYGON EMPTY  proprietary for internal testing and demo use only              
# 1 11c23fdc-4d13-4862-9298-2ee170e8c8f1    parking_lot MULTIPOLYGON EMPTY  proprietary for internal testing and demo use only              
# 2 11c23fdc-4d13-4862-9298-2ee170e8c8f1    golf_course MULTIPOLYGON EMPTY  proprietary for internal testing and demo use only              
# 3 11c23fdc-4d13-4862-9298-2ee170e8c8f1    water   MULTIPOLYGON(((-77.6006467933053 35.0540195517939,-77.6006252056598 35.0540313852814,-77.6004606778546 35.0540313852814,-77.6004277722935 35.053869047619,-77.6005974710934 35.0538167226746,-77.6006467933053 35.0540195517939)))  proprietary for internal testing and demo use only              

# MULTIPOLYGON(((-77.6006467933053 35.0540195517939,-77.6006252056598 35.0540313852814,-77.6004606778546 35.0540313852814,-77.6004277722935 35.053869047619,-77.6005974710934 35.0538167226746,-77.6006467933053 35.0540195517939)))

# --------------------------------------- increase to account for huge WKT fields --- # NOQA
maxInt = sys.maxsize
decrement = True

while decrement:
    # decrease the maxInt value by factor 10
    # as long as the OverflowError occurs.
    decrement = False
    try:
        csv.field_size_limit(maxInt)
    except OverflowError:
        maxInt = int(maxInt / 10)
        decrement = True
# --------------------------------------- end increase sys to account for huge WKT fields --- # NOQA

# # check to see if fc already exists (adds to existing fc)
if arcpy.Exists(fcname) is False:
    arcpy.CreateFeatureclass_management(wk, fcname, "POLYGON", spatial_reference=sr)  # NOQA

arcpy.management.AddFields(fcname, [["ID", 'TEXT', "ID", 255],
                                    ["CLASS", "TEXT", "CLASS", 255],  # NOQA
                                    ["USE", 'TEXT', "USE", 255],
                                   ])

entslist = ["ID", "CLASS", "USE", "SHAPE@WKT"]
iCur = arcpy.da.InsertCursor(fcname, entslist)

with open(csv_location) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        if row[3] != "MULTIPOLYGON EMPTY":
            if row[3] != "class_geom":
                #  add multipolygon to new_fc
                thedata = [row[1], row[2], row[4], row[3]]
                iCur.insertRow(thedata)

del iCur
