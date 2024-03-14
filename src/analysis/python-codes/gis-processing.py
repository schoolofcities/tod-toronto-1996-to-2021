import arcpy 
import csv
from arcpy import env
env.overwriteOutput = True

#change the main folder here, all the other 
folder = "D:/Softwares/OneDrive - Amdev Property/3 School of Cities/Transit Analysis"
env.workspace = f"{folder}/Transit Analysis 3.gdb"
#arrays to collect transit line names
transitLineNames = []
transitPointNames = []
#input layer
transit_line_orig = f"{folder}/data.gdb/Transit_Line"
transit_points = f"{folder}/data.gdb/Transit_Line_Points"
station = f"{folder}/data.gdb/Station"
#only need to run this the first time
arcpy.management.CalculateGeometryAttributes(station, [['PointX', 'POINT_X'], ['PointY', 'POINT_Y']], "","",arcpy.SpatialReference(26917))

census1996 = f"{folder}/data.gdb/OntarioCensus_1996"
census2021 = f"{folder}/data.gdb/OntarioCensus_2021"

canada1996 = f"{folder}/Data/DLI_1996_Census_CBF_Eng_Nat_ea_GeoPortal/Census1996_EnumerationArea.shp"
canada2021 = f"{folder}/Data/lda_000b21a_e/Census2021_DisseminationArea.shp"

#find unique transit line names i.e Yonge-University Line

with arcpy.da.SearchCursor(transit_line_orig, ["NAME"]) as cur:
    for row in cur:
        transitLineNames.append(row[0])

#find unique transit line point names

with arcpy.da.SearchCursor(station, ["NAME"]) as cur:
    for row in cur: 
        if row[0] not in transitPointNames:
            transitPointNames.append(row[0])

#arcpy.conversion.FeatureClassToFeatureClass(canada1996, env.workspace, census1996, f"PRUID = '35'")
#arcpy.conversion.FeatureClassToFeatureClass(canada2021, env.workspace, census2021, f"PRUID = '35'")

#calculate area for census da area
#arcpy.management.CalculateGeometryAttributes(census1996, [["DA_Area", "AREA_GEODESIC"]], "METERS", "SQUARE_METERS", arcpy.SpatialReference(26917))
#arcpy.management.CalculateGeometryAttributes(census2021, [["DA_Area", "AREA_GEODESIC"]], "METERS", "SQUARE_METERS", arcpy.SpatialReference(26917))

bufferList21 = []
bufferList96 = []
segments = []
transit_pointgdb = f"{folder}/transit_points.gdb"
transit_stationgdb = f"{folder}/transit_station.gdb"
thiessengdb = f"{folder}/thiessen.gdb"

for transit in transitLineNames:
    print("Exporting: ", transit)
    transitName = transit.replace(":", "").replace(" ", "").replace("-","")
    
    transit_line = f"{transitName}"
    arcpy.conversion.FeatureClassToFeatureClass(transit_line_orig, env.workspace, transit_line, f"NAME = '{transit}'" )
    arcpy.conversion.FeatureClassToFeatureClass(station, transit_stationgdb, f"{transitName}_station", f"NAME = '{transit}'" )
    arcpy.conversion.FeatureClassToFeatureClass(transit_points, transit_pointgdb, f"{transitName}_transitPoint", f"NAME = '{transit}'" ) 
    
    print("Thiessen Polygon")
    #transit_line_buffer = f"Buffer_{transitName}"#arcpy.analysis.Buffer(transit_line_segments, transit_line_buffer,"20 METERS", "", "FLAT")
    linestation = transit_stationgdb + "/" + f"{transitName}_station"
    thiessen = f"thiessen_{transitName}"
    #create thiessen polygon to extract identify which station the transit point is closer to, this also helps put info to 
    arcpy.analysis.CreateThiessenPolygons(linestation, thiessen, "ALL")
    
    """
    print("Transit Segments")
    transit_line_segments = f"Seg_{transitName}"
    arcpy.management.SplitLineAtPoint(transit_line, linestation, transit_line_segments, "20 METERS")
    arcpy.management.CalculateGeometryAttributes(transit_line_segments, [['LineLen', 'LENGTH_GEODESIC']], "","",arcpy.SpatialReference(26917))
    segments.append(transit_line_segments)
    """


    print("Intersecting Thiessen Polygon with Points")
    #intersect the transit points to get the station information. 
    transit_line_points = transit_pointgdb + "/" + f"{transitName}_transitPoint"
    transitPoints_withStation = f"StationIntersect_{transitName}"
    arcpy.analysis.Intersect([thiessen, transit_line_points], transitPoints_withStation)
    #calculate the xy coordinates of the points. 
    arcpy.management.CalculateGeometryAttributes(transitPoints_withStation, [['PointX', 'POINT_X'], ['PointY', 'POINT_Y']], "","",arcpy.SpatialReference(26917))
    
    
    #buffer the intersected transit points
    print("Point Buffer")
    transit_buffer = f"PointBuffer_{transitName}"
    arcpy.analysis.Buffer(transitPoints_withStation, transit_buffer,"800 METERS")

    print("Intersecting Census")
    #intersect with Census 2021 and Census 1996
    census_intersect_2021 = f"Census_2021_Buffer_{transitName}"
    arcpy.analysis.Intersect([transit_buffer, census2021], census_intersect_2021)
    bufferList21.append(env.workspace + f"/{census_intersect_2021}")
    census_intersect_1996 = f"Census_1996_Buffer_{transitName}"
    arcpy.analysis.Intersect([transit_buffer, census1996], census_intersect_1996)
    bufferList96.append(env.workspace + f"/{census_intersect_1996}")
    #calculate intersected area
    arcpy.management.CalculateGeometryAttributes(census_intersect_2021, [["Int_Area", "AREA_GEODESIC"]], "METERS", "SQUARE_METERS", arcpy.SpatialReference(26917))
    arcpy.management.CalculateGeometryAttributes(census_intersect_1996, [["Int_Area", "AREA_GEODESIC"]], "METERS", "SQUARE_METERS", arcpy.SpatialReference(26917))

mergedgdb = f"{folder}/merged.gdb"
print("Merging Layers")

"""merged_seg = f"{mergedgdb}/merged_segments"
arcpy.management.Merge(segments, merged_seg)"""



merge_2021 = f"{mergedgdb}/merge_21"
arcpy.management.Merge(bufferList21, merge_2021)
merge_1996 = f"{mergedgdb}/merge_96"
arcpy.management.Merge(bufferList96, merge_1996)

field_names21 = [f.name for f in arcpy.ListFields(merge_2021)]
field_names96 = [f.name for f in arcpy.ListFields(merge_1996)]


rowList = []

processedFolder = f"{folder}/ProcessedTables"
print("Exporting to CSV")


arcpy.conversion.TableToTable(station, f"{processedFolder}", "station.csv")


with arcpy.da.SearchCursor(merge_2021,field_names21) as cursor:
    for row in cursor:
        rowList.append(row)

with open(f"{processedFolder}/merge21.csv", 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',')
    spamwriter.writerow(field_names21)
    for row in rowList:
        spamwriter.writerow(row)

rowList = []

with arcpy.da.SearchCursor(merge_1996,field_names96) as cursor:
    for row in cursor:
        rowList.append(row)

with open(f"{processedFolder}/merge96.csv", 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',')
    spamwriter.writerow(field_names96)
    for row in rowList:
        spamwriter.writerow(row)
"""
rowList = []
with arcpy.da.SearchCursor(merged_seg,field_namesSeg) as cursor:
    for row in cursor:
        rowList.append(row)

with open(f"{processedFolder}/mergeSeg.csv", 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',')
    spamwriter.writerow(field_namesSeg)
    for row in rowList:
        spamwriter.writerow(row)
        """